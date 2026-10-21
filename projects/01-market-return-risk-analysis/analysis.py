import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


tickers = ["SPY", "QQQ", "IWM", "TLT", "GLD"]

# Pull adjusted historical market data.
data = yf.download(
    tickers,
    start="2021-01-01",
    end="2026-10-21",
    auto_adjust=True,
)

# Keep only closing prices for the analysis.
close_prices = data["Close"]
close_prices.to_csv("data/close_prices.csv")

# Daily return = current price / previous price - 1.
daily_returns = close_prices.pct_change()
daily_returns.to_csv("data/daily_returns.csv")

# Compound daily returns through time.
cumulative_returns = (1 + daily_returns).cumprod() - 1
cumulative_returns.to_csv("data/cumulative_returns.csv")

# Basic return and risk statistics.
average_daily_return = daily_returns.mean()
daily_volatility = daily_returns.std()
annualized_return = average_daily_return * 252
annualized_volatility = daily_volatility * (252 ** 0.5)

# Drawdown compares current growth with the highest level reached so far.
growth = (1 + daily_returns).cumprod()
running_max = growth.cummax()
drawdown = growth / running_max - 1
max_drawdown = drawdown.min()
drawdown.to_csv("data/drawdowns.csv")

# First-pass Sharpe ratio using a 0% risk-free rate.
sharpe_ratio = annualized_return / annualized_volatility

summary = pd.DataFrame(
    {
        "Annualized Return": annualized_return,
        "Annualized Volatility": annualized_volatility,
        "Max Drawdown": max_drawdown,
        "Sharpe Ratio": sharpe_ratio,
    }
)
summary.to_csv("data/summary_stats.csv")

# Correlation of daily returns between every ETF pair.
correlation_matrix = daily_returns.corr()
correlation_matrix.to_csv("data/correlation_matrix.csv")

print(summary)
print()
print(correlation_matrix)

# Cumulative return chart.
cumulative_returns.plot(figsize=(10, 6))
plt.title("Cumulative Returns")
plt.ylabel("Cumulative Return")
plt.xlabel("Date")
plt.grid(True)
plt.tight_layout()
plt.savefig("data/cumulative_returns.png")
plt.close()

# Drawdown chart.
drawdown.plot(figsize=(10, 6))
plt.title("Drawdowns")
plt.ylabel("Drawdown")
plt.xlabel("Date")
plt.grid(True)
plt.tight_layout()
plt.savefig("data/drawdowns.png")
plt.close()
