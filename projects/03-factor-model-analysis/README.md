# Project 03 — CAPM & Fama-French Factor Analysis

## Objective
Estimate and compare systematic risk exposures for AAPL, MSFT, NVDA, GOOGL, and AMZN using the Capital Asset Pricing Model (CAPM) and Fama-French three-factor model (FF3).

**Market proxy:** SPY. **Price history:** January 2021 through October 21, 2026 (the configured yfinance end date is exclusive). **Frequency:** daily for standalone beta estimates and monthly for factor regressions.

## Method
1. Download adjusted daily closing prices with yfinance.
2. Compute daily returns and historical SPY betas using covariance / variance.
3. Download monthly Mkt-RF, SMB, HML, and RF series from the [Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).
4. Aggregate prices to month-end and join monthly stock returns to monthly factor data.
5. Fit OLS regressions of stock excess returns on market excess returns (CAPM) and market, size, and value factors (FF3).
6. Compare coefficients, alpha p-values, and in-sample R² and export CSV/PNG outputs.

### Models
CAPM: `R_i - R_f = alpha + beta_m * (Mkt-RF) + error`

FF3: `R_i - R_f = alpha + beta_m * (Mkt-RF) + s * SMB + h * HML + error`

Annualized alpha uses **12 × monthly regression intercept** (a simple annualization approximation).

## Observed results
The following **rounded results were transcribed from a successful VS Code run displayed on November 5, 2026**. These are historical in-sample results, not live estimates.

| Stock | Daily beta vs SPY | CAPM beta (monthly) | CAPM R² | FF3 R² | R² increase |
|:--|--:|--:|--:|--:|--:|
| AAPL | 1.1824 | 1.0361 | 0.4199 | 0.4720 | 0.0521 |
| MSFT | 1.1320 | 1.0607 | 0.3826 | 0.6185 | 0.2359 |
| NVDA | 2.1133 | 2.1536 | 0.4647 | 0.5819 | 0.1172 |
| GOOGL | 1.2590 | 1.2241 | 0.3759 | 0.4225 | 0.0466 |
| AMZN | 1.4617 | 1.4460 | 0.4599 | 0.5924 | 0.1325 |

The run reported **68 overlapping monthly observations**. NVDA had the highest historical daily beta (2.1133). MSFT displayed the largest improvement in in-sample explanatory fit from adding size and value factors (approximately 0.236 R² points).

**Important:** More factors mechanically cannot reduce ordinary in-sample R², so improved fit alone does not establish better predictive performance. Alpha estimates should be assessed alongside statistical uncertainty. Daily SPY betas and monthly CAPM betas have different sampling and market-return definitions.

## Run locally
From this project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe factor_model.py
```

Outputs are generated in `results/`:
- `capm_results.csv`
- `fama_french_results.csv`
- `model_comparison.csv`
- `beta_comparison.png`
- `model_comparison.png`
- `factor_exposures.png`

## Limitations
This is an exploratory, backward-looking, in-sample analysis. It uses a SPY proxy for daily betas but the Kenneth French market factor for regressions. A tech-heavy sample is not representative of the full market. Inference is sensitive to sample period, monthly return alignment, model assumptions, and errors in variables. The code does not implement out-of-sample tests, robust standard errors, or trading-cost adjustments.

## Tools
Python, pandas, NumPy, yfinance, statsmodels, matplotlib, requests.
