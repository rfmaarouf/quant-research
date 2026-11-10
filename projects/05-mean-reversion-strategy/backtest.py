import numpy as np
import pandas as pd

INITIAL_CAPITAL = 10_000
TRADING_DAYS = 252
COST_BPS = 5


def run_backtest(df):
    df = df.copy()

    df["Market_Return"] = df["Close"].pct_change().fillna(0)

    # Yesterday's signal determines today's exposure.
    df["Exposure"] = df["Position"].shift(1).fillna(0)

    # A position change incurs a trading cost next session.
    turnover = (
        df["Position"].diff().abs()
        .fillna(df["Position"].abs())
        .shift(1)
        .fillna(0)
    )

    df["Strategy_Return"] = (
        df["Exposure"] * df["Market_Return"]
        - turnover * COST_BPS / 10_000
    )

    df["Strategy_Equity"] = (
        INITIAL_CAPITAL
        * (1 + df["Strategy_Return"]).cumprod()
    )

    df["Benchmark_Equity"] = (
        INITIAL_CAPITAL
        * (1 + df["Market_Return"]).cumprod()
    )

    df["Equity_Peak"] = df["Strategy_Equity"].cummax()
    df["Drawdown"] = (
        df["Strategy_Equity"] / df["Equity_Peak"] - 1
    )

    return df


def calculate_metrics(df):
    returns = df["Strategy_Return"]
    benchmark = df["Market_Return"]

    years = len(df) / TRADING_DAYS
    final_equity = df["Strategy_Equity"].iloc[-1]

    total_return = final_equity / INITIAL_CAPITAL - 1
    annual_return = (
        (final_equity / INITIAL_CAPITAL) ** (1 / years) - 1
    )

    volatility = returns.std() * np.sqrt(TRADING_DAYS)

    sharpe = (
        returns.mean() / returns.std()
        * np.sqrt(TRADING_DAYS)
        if returns.std() > 0 else np.nan
    )

    downside = returns.clip(upper=0)
    downside_dev = np.sqrt((downside ** 2).mean())

    sortino = (
        returns.mean() / downside_dev
        * np.sqrt(TRADING_DAYS)
        if downside_dev > 0 else np.nan
    )

    benchmark_return = (
        (1 + benchmark).prod() - 1
    )

    metrics = {
        "Initial Capital": INITIAL_CAPITAL,
        "Final Equity": final_equity,
        "Total Return": total_return,
        "Annualized Return": annual_return,
        "Annualized Volatility": volatility,
        "Sharpe Ratio (rf=0)": sharpe,
        "Sortino Ratio (target=0)": sortino,
        "Maximum Drawdown": df["Drawdown"].min(),
        "Benchmark Return": benchmark_return,
        "Buy Signals": int((df["Signal"] == 1).sum()),
        "Sell Signals": int((df["Signal"] == -1).sum()),
        "Time in Market": df["Exposure"].mean(),
    }

    return metrics


def print_report(metrics):
    print("\n" + "=" * 50)
    print("PROJECT 05 - MEAN REVERSION BACKTEST")
    print("=" * 50)

    money = ["Initial Capital", "Final Equity"]
    percent = [
        "Total Return",
        "Annualized Return",
        "Annualized Volatility",
        "Maximum Drawdown",
        "Benchmark Return",
        "Time in Market",
    ]

    for key, value in metrics.items():
        if key in money:
            formatted = f"${value:,.2f}"
        elif key in percent:
            formatted = f"{value:.2%}"
        elif isinstance(value, (int, np.integer)):
            formatted = str(value)
        else:
            formatted = f"{value:.3f}"

        print(f"{key:<27}: {formatted}")

    print("=" * 50)
