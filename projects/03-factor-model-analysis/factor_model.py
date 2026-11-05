"""Project 03: CAPM and Fama-French three-factor analysis."""

import io
import re
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests
import statsmodels.api as sm
import yfinance as yf

TICKERS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]
BENCHMARK = "SPY"
START_DATE = "2021-01-01"
END_DATE = "2026-10-22"  # yfinance end date is exclusive
OUTPUT_DIR = Path(__file__).resolve().parent / "results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def download_factors():
    """Read monthly percentage returns from Kenneth French's FF3 data ZIP."""
    url = (
        "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
        "F-F_Research_Data_Factors_CSV.zip"
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        name = next(
            name for name in archive.namelist()
            if name.lower().endswith(".csv")
        )
        source = archive.read(name).decode("utf-8-sig", errors="replace")

    rows = []
    for line in source.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) == 5 and re.fullmatch(r"\d{6}", parts[0]):
            try:
                rows.append([parts[0]] + [float(x) for x in parts[1:]])
            except ValueError:
                continue

    if not rows:
        raise ValueError("No monthly Fama-French factors could be parsed")

    factors = pd.DataFrame(
        rows, columns=["Date", "Mkt-RF", "SMB", "HML", "RF"]
    )
    factors["Date"] = pd.PeriodIndex(factors["Date"], freq="M")
    factors = factors.set_index("Date")
    factors[["Mkt-RF", "SMB", "HML", "RF"]] /= 100.0
    return factors


def run():
    prices = yf.download(
        TICKERS + [BENCHMARK],
        start=START_DATE,
        end=END_DATE,
        auto_adjust=True,
        progress=False,
    )["Close"].dropna()

    if prices.empty:
        raise ValueError("No historical prices downloaded")

    daily_returns = prices.pct_change().dropna()
    print("\nDAILY RETURNS")
    print(daily_returns.head())

    market = daily_returns[BENCHMARK]
    betas = {
        ticker: daily_returns[ticker].cov(market) / market.var()
        for ticker in TICKERS
    }
    print("\nDAILY MARKET BETAS")
    for ticker, beta in betas.items():
        print(f"{ticker}: {beta:.4f}")

    factors = download_factors()
    print("\nFAMA-FRENCH FACTORS")
    print(factors.tail())

    monthly_prices = prices.resample("ME").last()
    monthly_returns = monthly_prices.pct_change().dropna()
    monthly_returns.index = monthly_returns.index.to_period("M")
    data = monthly_returns.join(factors, how="inner").dropna()

    if len(data) < 24:
        raise ValueError("Fewer than 24 overlapping monthly observations")
    print(f"\nMonths analyzed: {len(data)}")

    capm_rows, ff3_rows = [], []
    for ticker in TICKERS:
        y = data[ticker] - data["RF"]

        capm = sm.OLS(y, sm.add_constant(data[["Mkt-RF"]])).fit()
        capm_rows.append({
            "Ticker": ticker,
            "Alpha_Monthly": capm.params["const"],
            "Alpha_Annualized": 12 * capm.params["const"],
            "Beta": capm.params["Mkt-RF"],
            "R_Squared": capm.rsquared,
            "Alpha_P_Value": capm.pvalues["const"],
        })

        ff3 = sm.OLS(
            y, sm.add_constant(data[["Mkt-RF", "SMB", "HML"]])
        ).fit()
        ff3_rows.append({
            "Ticker": ticker,
            "Alpha_Monthly": ff3.params["const"],
            "Alpha_Annualized": 12 * ff3.params["const"],
            "Market_Beta": ff3.params["Mkt-RF"],
            "SMB_Exposure": ff3.params["SMB"],
            "HML_Exposure": ff3.params["HML"],
            "R_Squared": ff3.rsquared,
            "Alpha_P_Value": ff3.pvalues["const"],
        })

    capm_df = pd.DataFrame(capm_rows)
    ff3_df = pd.DataFrame(ff3_rows)
    comparison = pd.DataFrame({
        "Ticker": TICKERS,
        "CAPM_R2": capm_df["R_Squared"],
        "FF3_R2": ff3_df["R_Squared"],
    })
    comparison["R2_Improvement"] = (
        comparison["FF3_R2"] - comparison["CAPM_R2"]
    )

    print("\nCAPM REGRESSION RESULTS")
    print(capm_df.round(4).to_string(index=False))
    print("\nFAMA-FRENCH RESULTS")
    print(ff3_df.round(4).to_string(index=False))
    print("\nMODEL COMPARISON")
    print(comparison.round(4).to_string(index=False))

    capm_df.to_csv(OUTPUT_DIR / "capm_results.csv", index=False)
    ff3_df.to_csv(OUTPUT_DIR / "fama_french_results.csv", index=False)
    comparison.to_csv(OUTPUT_DIR / "model_comparison.csv", index=False)

    plt.figure(figsize=(10, 6))
    plt.bar(list(betas.keys()), list(betas.values()))
    plt.axhline(1, linestyle="--", color="gray")
    plt.title("Historical Daily Market Beta")
    plt.xlabel("Stock")
    plt.ylabel("Beta")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "beta_comparison.png", dpi=300)
    plt.close()

    comparison.set_index("Ticker")[["CAPM_R2", "FF3_R2"]].plot(
        kind="bar", figsize=(10, 6)
    )
    plt.title("CAPM vs Fama-French Model Fit")
    plt.ylabel("R-Squared")
    plt.xlabel("Stock")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "model_comparison.png", dpi=300)
    plt.close()

    ff3_df.set_index("Ticker")[
        ["Market_Beta", "SMB_Exposure", "HML_Exposure"]
    ].plot(kind="bar", figsize=(11, 6))
    plt.title("Fama-French Factor Exposures")
    plt.ylabel("Regression Coefficient")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "factor_exposures.png", dpi=300)
    plt.close()

    print("\nPROJECT 03 COMPLETE")
    print(f"Results saved inside: {OUTPUT_DIR}")


if __name__ == "__main__":
    run()
