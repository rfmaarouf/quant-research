# Project 06 — Options Pricing & Monte Carlo Simulation

## Research question
How closely do Monte Carlo estimates of European option prices match the Black–Scholes theoretical price, and how does simulation accuracy change with path count?

## Hypothesis
Under the same geometric Brownian motion assumptions, the discounted Monte Carlo payoff converges toward the Black–Scholes value as the number of simulated price paths increases.

## Scope — foundational pass
- Implement European call and put pricing using Black–Scholes.
- Simulate terminal stock prices under risk-neutral geometric Brownian motion.
- Estimate call and put values using discounted average payoffs.
- Compare analytical and simulated prices at several simulation sizes.
- Save a convergence plot and a small results table after running the script.

## Models
Black–Scholes uses spot price `S0`, strike `K`, risk-free continuously compounded rate `r`, annualized volatility `sigma`, and time to maturity in years `T`.

Monte Carlo simulates:
```
S_T = S0 * exp((r - 0.5 * sigma**2) * T + sigma * sqrt(T) * Z)
```
where `Z` is standard normal. Call payoff = `max(S_T-K, 0)`; put payoff = `max(K-S_T, 0)`. Both are discounted by `exp(-r*T)`.

## Run
From this directory:
```bash
python -m pip install -r requirements.txt
python main.py
python -m unittest discover -s tests -v
```

## Study goals
Understand call vs put, strike and expiration, risk-neutral pricing, discounted expectation, sampling error, and why more simulations generally improve precision.

## Limitations
European exercise only; constant volatility and interest rate; no dividends; no transaction costs; no volatility smile; no market-data calibration. Monte Carlo estimates have random sampling error even with a fixed reproducible seed.

## Second-pass research extensions (after all 10 projects)
Historical/implied volatility calibration, confidence intervals, variance reduction, Greeks, parameter sensitivity, convergence studies, and out-of-sample comparison to option market quotes.

## Results
Pending first local run. Do not report theoretical or simulated output as observed until generated and reviewed.
