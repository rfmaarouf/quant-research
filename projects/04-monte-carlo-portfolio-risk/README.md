# Project 04 — Monte Carlo Portfolio Risk Simulation

## Overview

This project uses Monte Carlo simulation to estimate the potential future values and downside risk of a diversified ETF portfolio.

## Portfolio Universe

- **SPY:** S&P 500
- **QQQ:** Nasdaq-100
- **IWM:** Russell 2000
- **TLT:** Long-term U.S. Treasuries
- **GLD:** Gold

## Methodology

1. Download adjusted close prices from Yahoo Finance (`2021-01-01` through `2026-10-21`; end date is exclusive).
2. Compute daily arithmetic returns, sample mean vector and covariance matrix.
3. Use Cholesky decomposition to generate correlated normal return shocks.
4. Simulate 10,000 buy-and-hold portfolio paths over 252 trading days, starting with $10,000 and 20% per ETF.
5. Compute 95% and 99% Value at Risk (VaR), Conditional Value at Risk (CVaR), loss probability, and pathwise maximum drawdowns.
6. Produce five charts: portfolio paths, terminal-value distribution, drawdown distribution, loss distribution, and percentile paths.

## Previously Reported Simulation Results

| Metric | Value |
|---|---:|
| Initial capital | $10,000 |
| Mean final value | $11,111.25 |
| Median final value | $10,977.87 |
| Probability of loss | 24.33% |
| 95% VaR | $1,205.73 |
| 95% CVaR | $1,654.73 |
| 99% VaR | $1,939.17 |
| 99% CVaR | $2,306.80 |
| Average maximum drawdown | −11.84% |
| Worst simulated maximum drawdown | −35.20% |

These are results from an earlier reported run, not independently reverified from the uploaded source. Run the code to calculate outputs from the data returned at execution time. A fixed random seed supports reproducibility when the historical input data and dependencies remain unchanged.

## Run

```bash
python -m pip install -r requirements.txt
python monte_carlo.py
```

The script prints a risk report and displays five Matplotlib figures.

## Files

- `monte_carlo.py`: data retrieval, model configuration, and Monte Carlo simulation
- `risk_metrics.py`: VaR, CVaR, drawdown, and risk report
- `visualizations.py`: five diagnostic figures
- `requirements.txt`: dependencies

## Limitations

- The model assumes normally distributed daily arithmetic returns; real markets can have heavier tails, volatility clustering, and regime shifts.
- Normally distributed simple returns can theoretically be below −100%, producing unrealistic negative asset values.
- Historical means/covariances need not persist in the future, especially during crises.
- Starting weights are equal, but the strategy is buy-and-hold, so allocations drift as prices change.
- The simulation ignores transaction costs, taxes and other market frictions.

This is a research demonstration, not investment advice.
