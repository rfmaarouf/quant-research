# Project 02 — Portfolio Optimization & Efficient Frontier

Project 01 was about understanding the return and risk of individual assets. This project is the next step: instead of asking whether one asset is risky or profitable by itself, I want to understand what happens when I combine multiple assets into one portfolio.

The main thing I want to learn here is how portfolio weights, covariance, and diversification actually change total portfolio risk. I also want to see why the portfolio with the highest expected return is not automatically the best portfolio, and how optimization can be used to search for better return/risk combinations.

## Research Question

How does changing the allocation between SPY, QQQ, IWM, TLT, and GLD affect a portfolio's expected return, volatility, diversification, and risk-adjusted performance?

More specifically, I want to find out whether combining assets that behave differently can reduce total portfolio risk without giving up too much expected return, and how an optimized portfolio compares with a simple equal-weight portfolio.

## Assets

I am keeping the same five ETFs from Project 01 so I can build directly on what I already learned:

- **SPY** — S&P 500 / broad U.S. large-cap equities
- **QQQ** — Nasdaq-100 / growth and technology-heavy equities
- **IWM** — Russell 2000 / U.S. small-cap equities
- **TLT** — long-duration U.S. Treasury bonds
- **GLD** — gold

Using the same assets also makes it easier to connect this project back to the volatility, beta, drawdown, and correlation work from Project 01.

## What I Want to Measure

The first version of the project will focus on:

- Expected annual portfolio return
- Portfolio volatility
- Covariance matrix
- Portfolio weights
- Equal-weight portfolio
- Random portfolio simulation
- Sharpe ratio
- Minimum-volatility portfolio
- Maximum-Sharpe portfolio
- Efficient frontier
- Diversification effects
- Risk contribution by asset

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

## Initial Hypothesis

I expect the equity-heavy portfolios to have higher expected returns but also higher volatility. I also expect TLT and GLD to reduce portfolio risk because they have historically behaved differently from SPY, QQQ, and IWM during at least some periods.

I also expect the minimum-volatility portfolio to put more weight into lower-correlation assets, while the maximum-Sharpe portfolio will probably take more equity exposure if the extra return is enough to justify the extra risk.

I am not assuming the optimized portfolio will stay optimal outside this sample. A big part of this project is understanding that optimization depends heavily on the return and covariance estimates used as inputs.

## Plan

1. Load historical price data for the five ETFs.
2. Calculate daily returns.
3. Estimate annualized expected returns.
4. Build the annualized covariance matrix.
5. Create an equal-weight portfolio as a baseline.
6. Calculate portfolio return and volatility from a set of weights.
7. Generate thousands of random portfolios.
8. Compare their expected return, volatility, and Sharpe ratios.
9. Identify the minimum-volatility portfolio.
10. Identify the maximum-Sharpe portfolio.
11. Plot the efficient frontier.
12. Measure how much risk each asset contributes to the optimized portfolio.
13. Compare the optimized portfolios with the equal-weight portfolio.
14. Write down what the optimization can and cannot tell me.

## Things I Want to Understand, Not Just Code

By the end of this project I should be able to explain:

- Why covariance matters for portfolio risk
- Why two individually risky assets can sometimes reduce total portfolio risk when combined
- Why portfolio weights have to sum to 1
- How expected portfolio return is calculated
- How portfolio volatility is calculated
- What the efficient frontier actually represents
- What makes a portfolio minimum variance
- What makes a portfolio maximum Sharpe
- Why optimization can become unstable when expected-return estimates change
- Why an optimized historical portfolio is not automatically the best future portfolio

## Status

**In progress — project setup started.**

Next up: build the return and covariance inputs, then create the equal-weight portfolio before doing any optimization.
