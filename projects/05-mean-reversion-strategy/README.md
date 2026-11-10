# Project 05 — Mean Reversion Trading Strategy

**Quantitative Research Portfolio | Python | Algorithmic Trading | Backtesting**

## Overview

This project develops and backtests a systematic long-only mean-reversion strategy on SPY historical data. A 20-day rolling moving average and standard deviation define a Z-score, which drives entry and exit signals.

## Strategy Rules

| Parameter | Setting |
|---|---|
| Asset | SPY |
| Sample | January 2021–October 22, 2026 |
| Rolling window | 20 trading days |
| Buy | Z-score ≤ -2.0 |
| Sell | Z-score ≥ 0.0 |
| Starting capital | $10,000 |
| Transaction-cost assumption | 5 basis points per position change |
| Return accounting | Lagged position (avoids same-bar return lookahead) |

Z-score = (Close − 20-day moving average) / 20-day rolling standard deviation.

## Backtest Results

| Metric | Value |
|---|---:|
| Final equity | $16,321.21 |
| Total return | 63.21% |
| Annualized return | 8.84% |
| Annualized volatility | 10.75% |
| Sharpe ratio (risk-free = 0) | 0.841 |
| Sortino ratio (target = 0) | 1.324 |
| Maximum drawdown | -10.45% |
| SPY buy-and-hold return | 123.65% |
| Buy / Sell signals | 29 / 29 |
| Time invested | 17.90% |

The strategy underperformed buy-and-hold by **60.44 percentage points**, but had much less time in the market. These are historical simulation results, not a prediction of future performance.

## Files

- `main.py`: pulls adjusted SPY data and runs the pipeline.
- `strategy.py`: computes indicators, entries, exits, and positions.
- `backtest.py`: computes portfolio returns, benchmark, drawdown, and performance statistics.
- `visualizations.py`: generates three figures.
- `performance_metrics.csv`: summary performance metrics.
- `figures/`: generated charts, created locally when the script is run.
- `backtest_results.csv`: full daily output, created locally when the script is run.

## Run

```bash
pip install -r requirements.txt
python main.py
```

The script generates a performance report and the following plots:
1. Trading signals over the SPY price and 20-day SMA.
2. Strategy versus SPY buy-and-hold equity curves.
3. Strategy drawdown over time.

## Limitations and Future Research

This is an initial research implementation, not a live-trading system. Daily-close execution is simplified, cash earns no interest, and transaction costs use a fixed model. Further work will include out-of-sample and walk-forward validation, parameter sensitivity, slippage/execution modeling, and testing across market regimes. All 10 portfolio projects will be completed before this advanced research pass.

*Educational research only; not investment advice.*
