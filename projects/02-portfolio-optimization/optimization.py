import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# -----------------------------------
# DOWNLOAD DATA
# -----------------------------------

tickers = ["SPY", "QQQ", "IWM", "TLT", "GLD"]

data = yf.download(
    tickers,
    start="2021-01-01",
    end="2026-10-21",
    auto_adjust=True
)

close_prices = data["Close"][tickers]
daily_returns = close_prices.pct_change().dropna()
annualized_returns = daily_returns.mean() * 252
annualized_covariance = daily_returns.cov() * 252

# -----------------------------------
# EQUAL-WEIGHT PORTFOLIO
# -----------------------------------

weights = np.array([0.20, 0.20, 0.20, 0.20, 0.20])
portfolio_return = np.dot(weights, annualized_returns)
portfolio_variance = np.dot(weights.T, np.dot(annualized_covariance, weights))
portfolio_volatility = np.sqrt(portfolio_variance)
sharpe_ratio = portfolio_return / portfolio_volatility

print("Annualized Returns:")
print(annualized_returns)
print("\nAnnualized Covariance Matrix:")
print(annualized_covariance)
print("\nWeights:")
print(weights)
print("\nWeight Sum:")
print(weights.sum())
print("\nExpected Portfolio Return:")
print(portfolio_return)
print("\nPortfolio Variance:")
print(portfolio_variance)
print("\nPortfolio Volatility:")
print(portfolio_volatility)
print("\nPortfolio Sharpe Ratio:")
print(sharpe_ratio)

# -----------------------------------
# MONTE CARLO SIMULATION
# -----------------------------------

num_portfolios = 5000
portfolio_returns = []
portfolio_volatilities = []
portfolio_sharpes = []
portfolio_weights = []

for i in range(num_portfolios):
    random_weights = np.random.random(len(tickers))
    random_weights = random_weights / np.sum(random_weights)
    random_return = np.dot(random_weights, annualized_returns)
    random_variance = np.dot(random_weights.T, np.dot(annualized_covariance, random_weights))
    random_volatility = np.sqrt(random_variance)
    random_sharpe = random_return / random_volatility

    portfolio_returns.append(random_return)
    portfolio_volatilities.append(random_volatility)
    portfolio_sharpes.append(random_sharpe)
    portfolio_weights.append(random_weights)

portfolio_returns = np.array(portfolio_returns)
portfolio_volatilities = np.array(portfolio_volatilities)
portfolio_sharpes = np.array(portfolio_sharpes)
portfolio_weights = np.array(portfolio_weights)

# -----------------------------------
# MONTE CARLO MAX SHARPE
# -----------------------------------

max_sharpe_index = np.argmax(portfolio_sharpes)
max_sharpe_return = portfolio_returns[max_sharpe_index]
max_sharpe_volatility = portfolio_volatilities[max_sharpe_index]
max_sharpe_ratio = portfolio_sharpes[max_sharpe_index]
max_sharpe_weights = portfolio_weights[max_sharpe_index]

print("\nMonte Carlo Maximum Sharpe Portfolio:")
print("Return:", max_sharpe_return)
print("Volatility:", max_sharpe_volatility)
print("Sharpe Ratio:", max_sharpe_ratio)
print("\nWeights:")
for ticker, weight in zip(tickers, max_sharpe_weights):
    print(ticker, ":", weight)

# -----------------------------------
# MONTE CARLO MINIMUM VOLATILITY
# -----------------------------------

min_vol_index = np.argmin(portfolio_volatilities)
min_vol_return = portfolio_returns[min_vol_index]
min_vol_volatility = portfolio_volatilities[min_vol_index]
min_vol_sharpe = portfolio_sharpes[min_vol_index]
min_vol_weights = portfolio_weights[min_vol_index]

print("\nMonte Carlo Minimum Volatility Portfolio:")
print("Return:", min_vol_return)
print("Volatility:", min_vol_volatility)
print("Sharpe Ratio:", min_vol_sharpe)
print("\nWeights:")
for ticker, weight in zip(tickers, min_vol_weights):
    print(ticker, ":", weight)

# -----------------------------------
# PORTFOLIO FUNCTION
# -----------------------------------

def portfolio_stats(weights):
    port_return = np.dot(weights, annualized_returns)
    port_variance = np.dot(weights.T, np.dot(annualized_covariance, weights))
    port_volatility = np.sqrt(port_variance)
    port_sharpe = port_return / port_volatility
    return port_return, port_volatility, port_sharpe

# -----------------------------------
# TRUE MAX SHARPE OPTIMIZER
# -----------------------------------

def negative_sharpe(weights):
    return -portfolio_stats(weights)[2]

num_assets = len(tickers)
initial_guess = np.array([1 / num_assets] * num_assets)
bounds = tuple((0, 1) for asset in range(num_assets))
constraints = ({"type": "eq", "fun": lambda weights: np.sum(weights) - 1},)

optimized_result = minimize(
    negative_sharpe,
    initial_guess,
    method="SLSQP",
    bounds=bounds,
    constraints=constraints
)

optimized_weights = optimized_result.x
optimized_return, optimized_volatility, optimized_sharpe = portfolio_stats(optimized_weights)

print("\nTRUE OPTIMIZED MAX SHARPE PORTFOLIO:")
print("Return:", optimized_return)
print("Volatility:", optimized_volatility)
print("Sharpe Ratio:", optimized_sharpe)
print("\nWeights:")
for ticker, weight in zip(tickers, optimized_weights):
    print(ticker, ":", weight)

# -----------------------------------
# TRUE MINIMUM VOLATILITY OPTIMIZER
# -----------------------------------

def volatility_objective(weights):
    return portfolio_stats(weights)[1]

min_vol_result = minimize(
    volatility_objective,
    initial_guess,
    method="SLSQP",
    bounds=bounds,
    constraints=constraints
)

true_min_vol_weights = min_vol_result.x
true_min_vol_return, true_min_volatility, true_min_vol_sharpe = portfolio_stats(true_min_vol_weights)

print("\nTRUE MINIMUM VOLATILITY PORTFOLIO:")
print("Return:", true_min_vol_return)
print("Volatility:", true_min_volatility)
print("Sharpe Ratio:", true_min_vol_sharpe)
print("\nWeights:")
for ticker, weight in zip(tickers, true_min_vol_weights):
    print(ticker, ":", weight)

# -----------------------------------
# VISUALIZATION
# -----------------------------------

plt.figure(figsize=(10, 6))
plt.scatter(
    portfolio_volatilities,
    portfolio_returns,
    c=portfolio_sharpes,
    cmap="viridis",
    alpha=0.6
)
plt.colorbar(label="Sharpe Ratio")
plt.scatter(max_sharpe_volatility, max_sharpe_return, marker="*", s=250, label="Monte Carlo Max Sharpe")
plt.scatter(min_vol_volatility, min_vol_return, marker="*", s=250, label="Monte Carlo Min Volatility")
plt.scatter(optimized_volatility, optimized_return, marker="X", s=180, label="True Max Sharpe")
plt.scatter(true_min_volatility, true_min_vol_return, marker="X", s=180, label="True Min Volatility")
plt.xlabel("Volatility")
plt.ylabel("Expected Return")
plt.title("Portfolio Optimization")
plt.legend()
plt.show()

# -----------------------------------
# PORTFOLIO COMPARISON
# -----------------------------------

comparison = pd.DataFrame({
    "Portfolio": [
        "Equal Weight",
        "Monte Carlo Max Sharpe",
        "Monte Carlo Min Volatility",
        "True Max Sharpe",
        "True Min Volatility"
    ],
    "Return": [
        portfolio_return,
        max_sharpe_return,
        min_vol_return,
        optimized_return,
        true_min_vol_return
    ],
    "Volatility": [
        portfolio_volatility,
        max_sharpe_volatility,
        min_vol_volatility,
        optimized_volatility,
        true_min_volatility
    ],
    "Sharpe": [
        sharpe_ratio,
        max_sharpe_ratio,
        min_vol_sharpe,
        optimized_sharpe,
        true_min_vol_sharpe
    ]
})

print("\nPORTFOLIO COMPARISON:")
print(comparison)

comparison.to_csv("portfolio_comparison.csv", index=False)
print("\nResults saved to portfolio_comparison.csv")
