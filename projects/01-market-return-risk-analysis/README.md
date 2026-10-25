# Project 01 — Market Return & Risk Analysis

This is the first completed project in my quant research repo. I kept it fundamental on purpose: before building trading strategies or more complicated models, I wanted to be able to look at a group of assets and understand what their returns and risk are actually telling me.

The goal was not just to make charts. I wanted to go from a research question, to data, to the math/statistics, and then explain what I found and what I still cannot conclude from it.

## Research Question

How do the return and risk characteristics of major liquid ETFs differ across market exposures and asset classes?

More specifically, I wanted to compare which assets produced the strongest returns, which took the most risk to get there, how severe their drawdowns became, and how differently they behaved over the same historical period.

## Assets

The project compares five liquid ETFs from 2021-01-01 through 2026-10-21:

- **SPY** — S&P 500 / broad U.S. large-cap equities
- **QQQ** — Nasdaq-100 / growth and technology-heavy equities
- **IWM** — Russell 2000 / U.S. small-cap equities
- **TLT** — long-duration U.S. Treasury bonds
- **GLD** — gold

This gives the project three equity exposures plus bonds and gold rather than only comparing highly similar stock portfolios.

## Metrics Implemented

The final analysis pipeline calculates:

- Daily returns
- Cumulative returns
- Growth of $1
- Average daily return
- Annualized arithmetic return
- Compound annual growth rate (CAGR)
- Annualized volatility
- Maximum drawdown
- Sharpe ratio
- Downside volatility
- Sortino ratio
- Calmar ratio
- 95% historical Value at Risk (VaR)
- 95% Conditional Value at Risk / Expected Shortfall (CVaR)
- Correlation matrix
- Beta relative to SPY
- 30-day rolling annualized volatility
- 60-day rolling compounded returns
- 60-day rolling correlation with SPY
- 60-day rolling beta relative to SPY

The script also exports the main tables, time series, and charts to the local `data/` directory.

## Method

1. Pull adjusted historical price data with `yfinance`.
2. Align closing-price observations across all five ETFs.
3. Convert prices into daily percentage returns.
4. Compound daily returns into cumulative wealth paths.
5. Calculate return, volatility, downside-risk, drawdown, tail-risk, correlation, and beta metrics.
6. Calculate rolling statistics to show that risk relationships change through time.
7. Save the resulting data and visualizations locally.
8. Interpret the results while keeping the limitations of the sample in view.

## Main Findings

The selected historical window produced several useful observations:

- **QQQ** generated the strongest first-pass annualized return among the equity ETFs, but it also carried relatively high volatility, drawdown risk, and market sensitivity.
- **SPY** produced strong returns with lower volatility and drawdown than QQQ, making its return/risk tradeoff more balanced during this sample.
- **IWM** lagged SPY and QQQ while still experiencing substantial volatility, illustrating that higher risk does not automatically produce higher realized return.
- **GLD** behaved more independently from the equity ETFs and provided an example of how a lower-correlation asset can change the risk characteristics of a multi-asset portfolio.
- **TLT** was the weakest performer in the selected sample and experienced a severe drawdown, showing that Treasury exposure is not automatically low-risk when duration and interest-rate risk are large.
- **SPY and QQQ** had very high daily-return correlation, while GLD and TLT generally behaved more independently from equities.
- Rolling correlation and rolling beta showed that these relationships were not constant. Market sensitivity can strengthen or weaken substantially depending on the period being measured.

These are observations from one selected historical window, not forecasts about future returns.

## Visualizations

The project now produces:

- Cumulative return comparison
- Growth of $1
- Drawdown curves
- 30-day rolling annualized volatility
- 60-day rolling compounded returns
- Daily-return correlation matrix
- 60-day rolling correlation with SPY
- 60-day rolling beta relative to SPY

## What I Learned

The biggest lesson from this project is that no single metric describes risk well.

Volatility measures the dispersion of returns, while drawdown measures how far an investment fell from a previous peak. Beta measures sensitivity to a benchmark rather than total risk. Correlation describes how assets move together, but rolling correlation shows that this relationship can change. VaR gives a loss threshold, while CVaR looks deeper into the tail and estimates the average loss once that threshold has already been breached.

I also learned why compounded returns matter. Adding daily percentage returns does not correctly represent the growth of capital through time, so cumulative returns and rolling multi-day returns need to be compounded.

Finally, CAGR and the arithmetic annualized-return estimate answer slightly different questions. The arithmetic estimate annualizes the average daily return, while CAGR describes the constant compounded yearly growth rate that connects the starting value to the ending value.

## Limitations

This remains an introductory research project and has important limitations:

- Historical results do not predict future performance.
- The selected start and end dates can materially change the conclusions.
- The Sharpe and Sortino calculations use a 0% risk-free rate for simplicity.
- Arithmetic annualized return is only an approximation and can differ meaningfully from CAGR.
- Historical VaR and CVaR depend entirely on the observed sample and do not guarantee the size of future losses.
- Beta and correlation are benchmark- and window-dependent.
- Correlations can rise during periods of market stress, reducing diversification when it is needed most.
- ETFs are proxies for broader asset-class exposures and contain their own structural characteristics.
- Transaction costs, taxes, liquidity constraints, and portfolio weights are outside the scope of this project.

These limitations are part of the analysis rather than something to hide.

## Status

**Complete — Project 01 core analysis finished.**

The final pipeline now covers return, volatility, drawdown, downside risk, tail risk, correlation, beta, CAGR, and rolling risk analysis with exported tables and visualizations.

## Next Project

The natural next step is **Project 02 — Portfolio Optimization & Efficient Frontier**.

That project can build directly on the return, volatility, covariance, and correlation concepts from this one to study portfolio weights, expected portfolio return, portfolio volatility, diversification, Sharpe-maximizing portfolios, minimum-variance portfolios, and the efficient frontier.
