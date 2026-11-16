# Project 07 — Reusable Backtesting Engine

The seventh project in my 10-project quantitative research series.

## Goal

Implement a reusable **long-only, daily backtester** with explicit execution assumptions, trading costs, performance statistics, and a comparison against buy-and-hold. Demonstration strategy: **20/50-day simple moving-average crossover on SPY**.

## Run

From this directory:

```bash
pip install -r requirements.txt
python main.py
python -m unittest discover -s tests -v
```

Optional settings:

```bash
python main.py --ticker QQQ --start 2021-01-01 --end 2026-10-22 --fast 20 --slow 50 --capital 10000 --cost-bps 5
```

The end date is **exclusive**. Live price download needs internet access. Chart and CSV outputs are written to `figures/` and intentionally ignored by git.

## Design

- `strategies.py`: return a 0/1 position target computed using closes available through date t.
- `backtest.py`: shift the target one bar; execute at **next session's adjusted open** and earn subsequent **open-to-open** returns.
- `metrics.py`: total/annualized return, volatility, zero-risk-free Sharpe, max drawdown, buy-and-hold, exposure, completed trades, win rate and turnover.
- `main.py`: download adjusted historical prices, run analysis, save CSVs and two PNG charts.
- `tests/test_backtest.py`: deterministic tests of timing, fees, equity arithmetic and input validation.

## Execution assumptions and limitations

The decision at close t cannot trade at open t; it first trades at open t+1. A fixed **5 basis points per position change** is applied by default, including a last-open liquidation. The backtest assumes fully invested or fully cash, fractional shares, no leverage, no margin, no borrow, and zero interest on cash. Adjusted OHLC from Yahoo Finance approximate dividend/split-adjusted price history; data corrections and corporate actions can affect results. Costs approximate fees/slippage and not market impact or real execution. The benchmark is a continuous, frictionless buy-and-hold adjusted-price series.

Equity rows include the return from that day's open to the next day's open, and the final row applies any liquidation charge; equity should not be interpreted as an intraday live account statement. The Sharpe uses **risk-free rate = 0**. Trade win rate is net of the two entry/exit costs. The strategy is only an educational baseline, not an optimized or validated investment strategy.

## Next research pass

After all ten foundational projects are complete: run out-of-sample and walk-forward evaluations, parameter stability/sensitivity, realistic bid-ask fills and slippage, interest on cash, multiple assets, richer order sizing, survivorship-bias controls, and reproducible data snapshots.

No performance results are claimed in this README until the market-data run is actually executed.
