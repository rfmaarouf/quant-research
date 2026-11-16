"""Run the Project 07 SMA crossover backtest and export charts/results."""
from pathlib import Path
import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

from backtest import run_backtest
from metrics import performance_metrics, format_report
from strategies import moving_average_crossover


def load_prices(ticker: str, start: str, end: str) -> pd.DataFrame:
    raw = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    if raw.empty:
        raise ValueError(f"No data for {ticker} between {start} and {end}")
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)
    data = raw[["Open", "Close"]].dropna().copy()
    return data


def save_charts(daily: pd.DataFrame, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(daily.index, daily["equity"], label="SMA crossover (net)")
    ax.plot(daily.index, daily["benchmark"], label="Buy & hold")
    ax.set(title="Equity vs benchmark", ylabel="Portfolio value ($)")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output / "equity_curve.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(daily.index, 100 * daily["drawdown"].to_numpy(), 0, alpha=0.5)
    ax.set(title="Strategy drawdown", ylabel="Drawdown (%)")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output / "drawdown.png", dpi=150)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", default="SPY")
    parser.add_argument("--start", default="2021-01-01")
    parser.add_argument("--end", default="2026-10-22", help="Exclusive end date")
    parser.add_argument("--fast", type=int, default=20)
    parser.add_argument("--slow", type=int, default=50)
    parser.add_argument("--capital", type=float, default=10_000)
    parser.add_argument("--cost-bps", type=float, default=5.0)
    args = parser.parse_args()

    data = load_prices(args.ticker, args.start, args.end)
    signals = moving_average_crossover(data, args.fast, args.slow)
    result = run_backtest(data, signals, args.capital, args.cost_bps)
    report = format_report(performance_metrics(result))
    print(report)

    output = Path(__file__).resolve().parent / "figures"
    save_charts(result.daily, output)
    result.daily.to_csv(output / "daily_results.csv", index_label="Date")
    result.trades.to_csv(output / "trades.csv", index=False)
    (output / "report.txt").write_text(report + "\n", encoding="utf-8")
    print(f"\nSaved results to {output}")


if __name__ == "__main__":
    main()
