# Project 06 — Options Pricing & Monte Carlo Simulation

**Quantitative Research Series | Project 6 of 10**  
**Status:** Foundational implementation complete; locally tested by project author. Advanced research extensions are planned for a later pass.

## Research question

How closely does a risk-neutral Monte Carlo estimate of a European option's value agree with the analytical Black–Scholes price, and how does the observed error vary as the number of simulations increases?

## Method

The project implements two pricing approaches for **European calls and puts on a non-dividend-paying stock**:

1. **Black–Scholes:** Calculate an analytical benchmark using spot price `S0`, strike `K`, continuously compounded risk-free rate `r`, volatility `sigma`, and time to maturity `T` (years).
2. **Monte Carlo:** Draw independent standard-normal shocks and simulate terminal prices under risk-neutral geometric Brownian motion:

   ```text
   S_T = S0 * exp((r - 0.5 * sigma**2) * T + sigma * sqrt(T) * Z)
   Z ~ N(0, 1)
   ```

   For each simulated terminal price, calculate `max(S_T - K, 0)` for a call or `max(K - S_T, 0)` for a put. Discount the average payoff by `exp(-r * T)`.

The comparison metric is **absolute pricing error**: `abs(Monte Carlo price - Black–Scholes price)`. More paths typically improve precision on average, but error need not decrease at every individual sample size.

## Default experiment

| Input | Value |
| --- | ---: |
| Spot price | $100 |
| Strike | $100 |
| Risk-free rate (annual) | 5% |
| Volatility (annual) | 20% |
| Time to maturity | 1 year |
| Simulation counts | 100; 1,000; 10,000; 100,000 |
| Random seed | 42 |
| Instruments | European call and put |

`main.py` runs each simulation count separately for both option types, prints a pricing comparison, and generates output artifacts. Values printed by the program, rather than hard-coded example values, are the authoritative experiment results.

## Repository structure

```text
06-options-pricing-monte-carlo/
├── README.md
├── main.py                 # experiment runner and artifacts
├── pricing.py              # parameters, Black–Scholes, Monte Carlo
├── requirements.txt
├── tests/
│   └── test_pricing.py     # unittest validation
└── results/                # created by main.py when run
    ├── pricing_comparison.csv
    └── convergence.png
```

## Reproduce

Requires Python 3.10+ (recommended) with NumPy and Matplotlib. From this project directory:

```bash
python -m pip install -r requirements.txt
python main.py
python -m unittest discover -s tests -v
```

The runner writes:
- `results/pricing_comparison.csv`: option type, path count, Black–Scholes price, Monte Carlo price, and absolute error.
- `results/convergence.png`: absolute pricing error against the number of paths (logarithmic x-axis).

**Note:** Generated results are local run artifacts and are not included in this documentation commit. Run `main.py` to regenerate them. The README intentionally does not invent measured pricing values.

## Validation

The committed `unittest` suite checks:
- Black–Scholes put–call parity.
- Call and put Monte Carlo estimates within $0.25 of analytical prices at 100,000 simulations for seed 42.
- Rejection of nonpositive volatility.
- Rejection of unsupported option types.

The author reports that the project was tested successfully. Test execution is **not** independently verified by this README update.

## Key takeaways

- Option pricing under these assumptions uses a **risk-neutral** expected discounted payoff, not the asset's historical expected return.
- Black–Scholes is a fast analytical benchmark; Monte Carlo approximates the same value through simulated outcomes.
- With independent draws, typical Monte Carlo sampling error scales roughly as `1 / sqrt(N)`.
- Fixed seeds aid reproducibility, but a single seed is not a full statistical convergence study.
- A call or put's expiration payoff is **not** the buyer's net profit; profit also accounts for the premium.

## Assumptions and limitations

European exercise only; no dividends; constant volatility and interest rate; lognormal terminal prices; frictionless trading and no jumps. No implied-volatility calibration, transaction costs, confidence intervals, or real market quote comparison are implemented in this foundational pass. The current Monte Carlo method draws terminal prices directly, rather than building full intermediate price paths.

## Research upgrades — second pass after all 10 projects

- Estimate implied and historical volatility and compare with market option quotes.
- Add Monte Carlo standard errors and confidence intervals across independent seeds.
- Introduce antithetic variates and control variates to reduce variance.
- Study Greeks and parameter sensitivity to spot, strike, volatility, and maturity.
- Expand to more realistic dynamics and option structures, documenting additional model assumptions.

This first pass prioritizes correct pricing intuition, reproducible baseline implementations, and a clean analytical-versus-simulation comparison.
