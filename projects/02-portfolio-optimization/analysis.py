import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Project 02 — Portfolio Optimization & Efficient Frontier
# Start simple: build the inputs first, understand them, then optimize.

tickers = ["SPY", "QQQ", "IWM", "TLT", "GLD"]

# We are keeping the same historical window as Project 01 for consistency.
data = yf.download(
    tickers,
    start="2021-01-01",
    end="2026-10-21",
    auto_adjust=True
)

close_prices = data["Close"]
daily_returns = close_prices.pct_change().dropna()

# Expected annual returns: average daily return x ~252 trading days.
annualized_returns = daily_returns.mean() * 252

# Covariance tells us how pairs of assets move together.
# Annualizing daily covariance also uses ~252 trading days.
annualized_covariance = daily_returns.cov() * 252

print("Annualized Expected Returns")
print(annualized_returns)
print()

print("Annualized Covariance Matrix")
print(annualized_covariance)
print()

# First portfolio: equal weight across all five assets.
# 1 / 5 = 20% in each asset.
weights = np.array([1 / len(tickers)] * len(tickers))

print("Equal-Weight Portfolio")
print(weights)
print("Weight Sum:", weights.sum())

# Next step:
# 1. Calculate this portfolio's expected return.
# 2. Calculate this portfolio's volatility using the covariance matrix.
# 3. Make sure you understand both formulas before random simulation/optimization.
