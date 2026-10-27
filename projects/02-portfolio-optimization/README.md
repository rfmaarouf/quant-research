# Project 02 — Portfolio Optimization & Efficient Frontier

Project 01 was about understanding the return and risk of individual assets. This project is the next step: instead of looking at one asset by itself, I wanted to understand what happens when I combine multiple assets into one portfolio.

The main goal was to see how portfolio weights, covariance, and diversification change total portfolio risk, and how optimization can find better return/risk combinations than a simple equal-weight portfolio.

## Research Question

How does changing the allocation between SPY, QQQ, IWM, TLT, and GLD affect a portfolio's expected return, volatility, diversification, and risk-adjusted performance?

## Assets

- **SPY** — S&P 500 / broad U.S. large-cap equities
- **QQQ** — Nasdaq-100 / growth and technology-heavy equities
- **IWM** — Russell 2000 / U.S. small-cap equities
- **TLT** — long-duration U.S. Treasury bonds
- **GLD** — gold

## Methodology

I started with an equal-weight portfolio where each asset had a 20% allocation. This gave me a baseline that I could compare the optimized portfolios against.

I then generated 5,000 random portfolios using Monte Carlo simulation. Each portfolio had different weights, and I calculated its expected return, volatility, and Sharpe ratio.

From those portfolios, I found:

- The portfolio with the highest Sharpe ratio
- The portfolio with the lowest volatility

After that, I used SciPy's SLSQP optimizer to find more precise solutions instead of relying only on random simulations.

The optimizer follows two main rules:

- All portfolio weights must add up to 100%
- Each asset weight must stay between 0% and 100%

Finally, I plotted the simulated portfolios and compared the Monte Carlo results with the portfolios found by the optimizer.

## Core Math

Expected portfolio return:

\[
E[R_p] = w^T \mu
\]

Portfolio variance:

\[
\sigma_p^2 = w^T \Sigma w
\]

Portfolio volatility:

\[
\sigma_p = \sqrt{w^T \Sigma w}
\]

where:

- `w` = portfolio weights
- `mu` = expected asset returns
- `Sigma` = covariance matrix

The important idea is that portfolio risk does not come from just adding each asset's volatility. The way the assets move together matters too.

## Portfolio Metrics

### Expected Return

Expected portfolio return is calculated using the asset weights and their annualized historical returns.

### Volatility

Volatility measures the portfolio's risk. The calculation uses the covariance matrix, so it takes into account how the assets move relative to each other.

### Sharpe Ratio

The Sharpe ratio compares return to volatility. A higher Sharpe ratio means the portfolio produced more return relative to the amount of risk it took.

For this project I used:

`Sharpe Ratio = Portfolio Return / Portfolio Volatility`

I did not include a risk-free rate in the current version.

## Results

Using historical data from 2021 through October 2026, the equal-weight portfolio produced an expected annual return of about 9.99% with 13.52% volatility and a Sharpe ratio of 0.74.

The optimized maximum Sharpe portfolio improved the expected return to about 14.97% while slightly lowering volatility to 13.27%. This resulted in a Sharpe ratio of about 1.13.

The optimizer allocated approximately:

- SPY: 58.6%
- GLD: 41.4%
- QQQ: 0%
- IWM: 0%
- TLT: 0%

The minimum volatility portfolio lowered expected volatility to about 10.89%, but this came with a lower expected return of about 5.78%.

The results show the tradeoff between maximizing risk-adjusted returns and minimizing overall portfolio risk.

## Visualization

The graph shows the 5,000 randomly generated portfolios. Each point represents a different combination of asset weights.

The x-axis represents volatility and the y-axis represents expected return. The graph also highlights:

- Monte Carlo maximum Sharpe portfolio
- Monte Carlo minimum volatility portfolio
- True optimized maximum Sharpe portfolio
- True optimized minimum volatility portfolio

This makes it easy to see the tradeoff between taking more risk and targeting a higher expected return.

## What I Learned

This project helped me understand that portfolio optimization is not just about picking the assets with the highest returns.

The covariance between assets matters because combining assets that behave differently can reduce the total risk of the portfolio.

I also learned the difference between using Monte Carlo simulation to search through thousands of possible portfolios and using an optimizer to directly search for the best solution under specific constraints.

The optimized historical portfolio is also not automatically the best future portfolio. The result depends heavily on the historical return and covariance estimates used as inputs.

## Status

**Complete.**

The project now includes an equal-weight baseline, Monte Carlo simulation, maximum-Sharpe and minimum-volatility optimization, visualization, portfolio comparison, and CSV export.
