# Project 01 — Market Return & Risk Analysis

This is the first actual project in my quant research repo. I am keeping it pretty fundamental on purpose: before trying to build trading strategies or more complicated models, I want to be able to look at a group of assets and understand what their returns and risk are actually telling me.

The goal is not just to make a few charts and call it quantitative research. I want to go from a question, to the data, to the math/statistics, and then explain what I found and what I still cannot conclude from it.

## Research Question

How do the return and risk characteristics of major liquid ETFs differ across market exposures and asset classes?

More specifically, I want to see which assets produced the strongest returns, which took the most risk to get there, how bad their drawdowns became, and how differently they behaved from one another over the same period.

## Assets

I am starting with five liquid ETFs that give me a few different exposures without making the first project unnecessarily huge:

- **SPY** — S&P 500 / broad U.S. large-cap equities
- **QQQ** — Nasdaq-100 / growth and technology-heavy equities
- **IWM** — Russell 2000 / U.S. small-cap equities
- **TLT** — long-duration U.S. Treasury bonds
- **GLD** — gold

This gives me three different equity exposures plus bonds and gold, which should make the comparison more interesting than only looking at stocks that tend to move together.

## What I Want to Measure

The first version of the project will focus on:

- Daily returns
- Cumulative returns
- Average and annualized returns
- Volatility
- Sharpe ratio
- Maximum drawdown
- Correlation
- Beta
- Rolling returns and rolling volatility

I am also going to keep notes on what each metric actually means instead of treating the formulas like black boxes.

## Initial Hypothesis

Before looking at the results, I expect QQQ to have higher returns but also higher volatility than SPY, IWM to behave differently because of its small-cap exposure, and TLT and GLD to have lower correlations with the equity ETFs.

I am not assuming that this will be true in every period. Part of the point of the project is to see where the data agrees with that intuition and where it does not.

## Method

1. Pull historical adjusted price data for each ETF.
2. Clean and align the data so every asset is being compared over the same dates.
3. Calculate daily percentage returns.
4. Build the main return and risk metrics in Python.
5. Compare the assets with summary statistics and visualizations.
6. Look at correlations and how the relationships change through time.
7. Interpret the results instead of only dumping numbers into a table.
8. Write down limitations, mistakes, and things I would change in a more rigorous version.

## Visualizations

Planned charts include:

- Growth of $1
- Cumulative return comparison
- Drawdown curves
- Rolling volatility
- Rolling returns
- Correlation matrix

I may add more if they help answer the research question, but I do not want charts just for the sake of having charts.

## Why I Am Starting Here

A lot of the projects I eventually want to work on — factor models, portfolio optimization, statistical arbitrage, volatility models, options, and systematic strategies — depend on understanding returns, volatility, correlation, and drawdowns first.

So this project is basically the foundation. I want to understand the numbers well enough that later projects are built on something I actually understand rather than code I copied without knowing what it means.

## Limitations to Keep in Mind

This is an introductory research project, so there are going to be limitations. Historical results do not tell me what will happen next, the chosen time period can change the conclusions, Sharpe ratios depend on assumptions, correlations are not constant, and ETFs are only proxies for the exposures I am trying to study.

Those limitations are part of the analysis rather than something to hide at the end.

## Status

**In progress.**

Starting with data collection and return calculations.

## Possible Extensions

Once the base analysis works, I may extend it by:

- Comparing different market regimes
- Adding a risk-free rate to the Sharpe calculation
- Comparing rolling beta and correlation
- Testing sector ETFs
- Separating bull, bear, and high-volatility periods
- Using the results as a bridge into the portfolio optimization and factor-model projects
