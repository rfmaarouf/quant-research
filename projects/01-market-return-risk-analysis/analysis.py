import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

tickers = ["SPY", "QQQ", "IWM", "TLT", "GLD"]

data = yf.download(
    tickers,
    start="2021-01-01",
    end="2026-10-21",
    auto_adjust=True
)

close_prices = data["Close"]
close_prices.to_csv("data/close_prices.csv")

daily_returns = close_prices.pct_change()
daily_returns.to_csv("data/daily_returns.csv")

# Cumulative returns
cumulative_returns = (1 + daily_returns).cumprod() - 1

# Summary statistics
average_daily_return = daily_returns.mean()
daily_volatility = daily_returns.std()

# Annualized metrics
annualized_return = average_daily_return * 252
annualized_volatility = daily_volatility * (252 ** 0.5)

# Maximum drawdown
growth = (1 + daily_returns).cumprod()
running_max = growth.cummax()
drawdown = growth / running_max - 1
max_drawdown = drawdown.min()

# Save outputs
cumulative_returns.to_csv("data/cumulative_returns.csv")

summary = pd.DataFrame({
    "Annualized Return": annualized_return,
    "Annualized Volatility": annualized_volatility,
    "Max Drawdown": max_drawdown
})

# Sharpe ratio (using 0% risk-free rate for now)
sharpe_ratio = annualized_return / annualized_volatility
summary["Sharpe Ratio"] = sharpe_ratio

# Downside volatility
downside_returns = daily_returns.where(daily_returns < 0)
downside_volatility = downside_returns.std() * (252 ** 0.5)

# Sortino ratio
sortino_ratio = annualized_return / downside_volatility
summary["Downside Volatility"] = downside_volatility
summary["Sortino Ratio"] = sortino_ratio

# Calmar ratio
calmar_ratio = annualized_return / max_drawdown.abs()
summary["Calmar Ratio"] = calmar_ratio

# 95% Historical Value at Risk
var_95 = daily_returns.quantile(0.05)
summary["VaR 95%"] = var_95

# 95% Conditional Value at Risk (Expected Shortfall)
cvar_95 = daily_returns.apply(
    lambda x: x[x <= x.quantile(0.05)].mean()
)
summary["CVaR 95%"] = cvar_95

# Beta relative to SPY
beta = {}
spy_variance = daily_returns["SPY"].var()

for ticker in tickers:
    if ticker != "SPY":
        covariance = daily_returns[ticker].cov(daily_returns["SPY"])
        beta[ticker] = covariance / spy_variance

beta["SPY"] = 1.0
summary["Beta vs SPY"] = pd.Series(beta)

# Correlation matrix
correlation_matrix = daily_returns.corr()

# Save updated outputs
summary.to_csv("data/summary_stats.csv")
correlation_matrix.to_csv("data/correlation_matrix.csv")

print(summary)
print()
print(correlation_matrix)

# Cumulative returns chart
cumulative_returns.plot(figsize=(10, 6))
plt.title("Cumulative Returns")
plt.ylabel("Cumulative Return")
plt.xlabel("Date")
plt.grid(True)
plt.tight_layout()
plt.savefig("data/cumulative_returns.png")
plt.close()

# Drawdown chart
drawdown.to_csv("data/drawdowns.csv")
drawdown.plot(figsize=(10, 6))
plt.title("Drawdowns")
plt.ylabel("Drawdown")
plt.xlabel("Date")
plt.grid(True)
plt.tight_layout()
plt.savefig("data/drawdowns.png")
plt.close()

# 30-day rolling volatility
rolling_volatility = daily_returns.rolling(window=30).std() * (252 ** 0.5)
rolling_volatility.to_csv("data/rolling_volatility_30d.csv")
rolling_volatility.plot(figsize=(10, 6))
plt.title("30-Day Rolling Annualized Volatility")
plt.ylabel("Annualized Volatility")
plt.xlabel("Date")
plt.grid(True)
plt.tight_layout()
plt.savefig("data/rolling_volatility_30d.png")
plt.close()

# 60-day rolling correlation with SPY
rolling_correlation = pd.DataFrame(index=daily_returns.index)

for ticker in tickers:
    if ticker != "SPY":
        rolling_correlation[ticker] = (
            daily_returns[ticker]
            .rolling(window=60)
            .corr(daily_returns["SPY"])
        )

rolling_correlation.to_csv("data/rolling_correlation_spy_60d.csv")
rolling_correlation.plot(figsize=(10, 6))
plt.title("60-Day Rolling Correlation with SPY")
plt.ylabel("Correlation")
plt.xlabel("Date")
plt.axhline(0)
plt.grid(True)
plt.tight_layout()
plt.savefig("data/rolling_correlation_spy_60d.png")
plt.close()

# 60-day rolling beta vs SPY
rolling_beta = pd.DataFrame(index=daily_returns.index)
spy_rolling_variance = daily_returns["SPY"].rolling(window=60).var()

for ticker in tickers:
    if ticker != "SPY":
        rolling_covariance = (
            daily_returns[ticker]
            .rolling(window=60)
            .cov(daily_returns["SPY"])
        )

        rolling_beta[ticker] = (
            rolling_covariance / spy_rolling_variance
        )

rolling_beta.to_csv("data/rolling_beta_spy_60d.csv")
rolling_beta.plot(figsize=(10, 6))
plt.title("60-Day Rolling Beta vs SPY")
plt.ylabel("Beta")
plt.xlabel("Date")
plt.axhline(1)
plt.axhline(0)
plt.grid(True)
plt.tight_layout()
plt.savefig("data/rolling_beta_spy_60d.png")
plt.close()
