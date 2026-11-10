import pandas as pd
import yfinance as yf

from strategy import calculate_indicators, generate_signals
from backtest import run_backtest, calculate_metrics, print_report
from visualizations import generate_plots

TICKER = "SPY"
START_DATE = "2021-01-01"
END_DATE = "2026-10-23"  # End is exclusive


def main():
    print("Downloading historical SPY data...")

    df = yf.download(
        TICKER,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=True,
        progress=False,
    )

    if df.empty:
        raise RuntimeError("No historical data downloaded.")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df[["Close"]].dropna()

    print("Calculating indicators...")
    df = calculate_indicators(df)

    print("Generating trading signals...")
    df = generate_signals(df)

    print("Running backtest...")
    df = run_backtest(df)

    metrics = calculate_metrics(df)
    print_report(metrics)

    print("\nGenerating charts...")
    generate_plots(df)

    df.to_csv("backtest_results.csv")
    pd.Series(metrics).to_csv("performance_metrics.csv")

    print("\nPROJECT 05 PIPELINE COMPLETE")


if __name__ == "__main__":
    main()
