from risk_metrics import calculate_risk_report
from visualizations import generate_all_plots

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# ---------------------------------------
# 1. CONFIGURATION
# ---------------------------------------

TICKERS = ["SPY", "QQQ", "IWM", "TLT", "GLD"]

START_DATE = "2021-01-01"
END_DATE = "2026-10-22"

INITIAL_PORTFOLIO = 10_000
NUM_SIMULATIONS = 10_000
HORIZON_DAYS = 252

WEIGHTS = np.array([0.20] * len(TICKERS))

RNG = np.random.default_rng(42)

# ---------------------------------------
# 2. DOWNLOAD HISTORICAL DATA
# ---------------------------------------

prices = yf.download(
    TICKERS,
    start=START_DATE,
    end=END_DATE,
    auto_adjust=True,
    progress=False
)["Close"]

prices = prices[TICKERS].dropna()

returns = prices.pct_change().dropna()

# Estimate daily expected returns and covariance
mean_returns = returns.mean().to_numpy()
cov_matrix = returns.cov().to_numpy()

print("\nDaily Expected Returns:")
print(returns.mean())

print("\nDaily Covariance Matrix:")
print(returns.cov())

# ---------------------------------------
# 3. CHOLESKY DECOMPOSITION
# ---------------------------------------

L = np.linalg.cholesky(cov_matrix)

# ---------------------------------------
# 4. MULTI-ASSET MONTE CARLO
# ---------------------------------------

# Each row represents one simulation.
portfolio_paths = np.zeros(
    (NUM_SIMULATIONS, HORIZON_DAYS + 1)
)

portfolio_paths[:, 0] = INITIAL_PORTFOLIO

# Track the value of each individual asset allocation.
asset_values = np.tile(
    INITIAL_PORTFOLIO * WEIGHTS,
    (NUM_SIMULATIONS, 1)
)

for day in range(1, HORIZON_DAYS + 1):

    # Independent random shocks
    Z = RNG.standard_normal(
        (NUM_SIMULATIONS, len(TICKERS))
    )

    # Correlate shocks using Cholesky decomposition
    shocks = Z @ L.T

    # Simulate daily arithmetic returns
    simulated_returns = mean_returns + shocks

    # Update each asset's value (buy-and-hold)
    asset_values *= (1 + simulated_returns)

    # Calculate total portfolio value
    portfolio_paths[:, day] = asset_values.sum(axis=1)


# ---------------------------------------
# 5. RISK ANALYSIS
# ---------------------------------------

risk_results = calculate_risk_report(
    portfolio_paths=portfolio_paths,
    initial_value=INITIAL_PORTFOLIO,
    confidence_levels=(0.95, 0.99)
)

# ---------------------------------------
# 6. VISUALIZATION
# ---------------------------------------

generate_all_plots(
    portfolio_paths=portfolio_paths,
    initial_value=INITIAL_PORTFOLIO,
    risk_results=risk_results
)
