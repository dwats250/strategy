# METRIC PRIMER · v1.0 · 2026-08-27

An owner-learning reference for the metrics this lab uses (or may use). For each:
plain-English meaning · formula (or conceptual) · the question it answers ·
interpretation · common failure mode / misuse · lab status
(**PRIMARY** / **SECONDARY** / **NOT YET APPLICABLE**).

Lab convention: the **risk-normalized** reading (R) is primary; dollar readings are
secondary because fixed-share sizing makes them ATR-weighted (a sizing artifact, not
an edge). 1R = the frozen initial entry-to-stop distance.

---

### Expectancy (per trade, $)
Average profit per trade. `mean(pnl)`. *Q:* what does an average trade make? *Interp:*
>0 profitable on average. *Misuse:* dominated by position sizing and outliers; sign can
disagree with R. **SECONDARY.**

### Expectancy R
Average profit per trade in units of initial risk. `mean(pnl / risk_points)`. *Q:* is
the edge positive after normalizing for how much was risked? *Interp:* the lab's core
edge test; +0.02–0.05 R is small, ~0 is no edge. *Misuse:* a *relative* improvement
(less-negative) is not a positive edge — read the absolute value. **PRIMARY.**

### Profit factor (PF)
Gross profit ÷ gross loss. `Σwins / |Σlosses|`. *Q:* how many dollars won per dollar
lost? *Interp:* >1 profitable, 1.0 break-even. *Misuse:* can rise while expectancy R
falls (fewer/larger trades); undefined with no losses. **SECONDARY.**

### Win rate
Fraction of trades that are winners. `wins / n`. *Q:* how often is a trade profitable?
*Interp:* meaningless alone — a 20% win rate with a large payoff can win. *Misuse:*
optimizing win rate invites tiny-win/large-loss systems. **SECONDARY.**

### Payoff ratio
Average winner ÷ average loser magnitude. `|mean(wins)/mean(losses)|`. *Q:* how big is
a win vs a loss? *Interp:* pairs with win rate for break-even math (`win% > 1/(1+payoff)`).
*Misuse:* stop-based systems lose slightly >1R on stops (slippage). **SECONDARY.**

### Max drawdown
Largest peak-to-trough decline of the equity curve. *Q:* worst run of losses endured?
*Interp:* the pain/capital measure; the lab reads it in **R** (`max_drawdown_r`) as
primary. *Misuse:* path/sample-dependent; a single ordering. **SECONDARY** ($), the
R-space form is the primary read.

### Sharpe ratio
Mean return ÷ std of return (per unit risk). `mean/stdev`. *Q:* return per unit total
volatility? *Interp:* higher is better; annualized needs a periods/yr assumption.
*Misuse:* penalizes upside vol; assumes iid normal; trade-based ≠ daily Sharpe.
**SECONDARY** (trade-based only here).

### Sortino ratio
Like Sharpe but downside deviation only. `mean / downside_dev`. *Q:* return per unit
*downside* risk? *Interp:* higher is better; rewards asymmetric upside. *Misuse:*
few downside points → unstable. **SECONDARY.**

### CAGR
Compound annual growth rate. `(end/start)^(1/years) − 1`. *Q:* annualized compounded
return? *Interp:* headline growth. *Misuse:* requires an account/capital construction;
fixed-1-share vs $50k is arbitrary. **NOT YET APPLICABLE** (deferred).

### Calmar ratio
CAGR ÷ max drawdown. *Q:* growth per unit worst-drawdown? *Interp:* higher is better.
*Misuse:* inherits CAGR's account dependence; drawdown is sample-specific. **NOT YET
APPLICABLE** (deferred with CAGR).

### Bootstrap confidence interval
Resample trades many times (fixed seed) to bound a statistic. *Q:* how uncertain is the
mean given this sample? *Interp:* a CI that **straddles zero** = not distinguishable
from no edge. *Misuse:* IID resampling ignores serial dependence — use a moving-block
bootstrap too; not a p-value. **PRIMARY** (robustness gate).

### Outlier concentration
How much of the result rides on the few best trades. `net_excl_best_k`, `best_k % of
gross`. *Q:* is the edge broad or a handful of trades? *Interp:* if `net_excl_best_10`
flips deeply negative, the edge is fragile. *Misuse:* removals are diagnostics, **not**
alternative strategies. **PRIMARY** (descriptive robustness; non-gating by charter).

### Parameter surfaces / plateaus
Metric mapped over a parameter grid; look for broad stable regions vs isolated peaks.
*Q:* is a good result robust to nearby parameters? *Interp:* a **plateau** is
trustworthy; an **isolated peak** is likely overfit. *Misuse:* ranking by the single
best cell. **PRIMARY** (topology classification; MATERIAL_R 0.03).

### DSR — Deflated Sharpe Ratio
Sharpe adjusted for the number of trials and non-normality. *Q:* is the Sharpe real
after accounting for multiple testing? *Interp:* deflates as trials rise. *Misuse:*
needs an honest trial count — hence `trials_planned` on every manifest. **NOT YET
APPLICABLE** (tracked via the budget/trial fields; not computed at these sample sizes).

### PBO — Probability of Backtest Overfitting
Chance the in-sample-best config underperforms out-of-sample (combinatorial
cross-validation). *Q:* is my selection process overfitting? *Interp:* >0.5 = likely
overfit. *Misuse:* needs many configs/folds; conceptual guard here. **NOT YET
APPLICABLE** (the budget ceilings and single-look validation serve the same guard).

### Regression beta
Slope relating a predictor to an outcome. `Σ(x−x̄)(y−ȳ)/Σ(x−x̄)²`. *Q:* does x move y,
and how much? *Interp:* MIM's core — β>0 means early return predicts late return.
*Misuse:* leverage from outliers; needs robust SE. **PRIMARY** (for association
families like MIM).

### t-statistic / confidence interval
Estimate ÷ its standard error; CI = estimate ± z·SE. *Q:* is the estimate
distinguishable from zero? *Interp:* |t|≳2 (~95%) conventionally "significant"; the CI
shows the plausible range. *Misuse:* p-hacking, wrong SE (use a **frozen** robust
convention, no shopping). **PRIMARY.**

### R-squared
Fraction of outcome variance explained. `1 − SSE/SST`. *Q:* how much of y does x
explain? *Interp:* intraday predictive R² is *tiny* (≪1%) even for real effects — a
small R² with β>0 and a tight CI can still matter. *Misuse:* dismissing a real signal
for low R², or chasing high R² in-sample. **SECONDARY.**

### Basis points (bps)
One hundredth of a percent. `1 bp = 0.0001`. *Q:* a common small-return / cost unit.
*Interp:* MIM economics and costs are quoted in bps. *Misuse:* confusing bps with %
(100×). **SECONDARY** (economic unit).

### Turnover
How much the position/notional trades over a period. *Q:* how much trading (and cost)
does the strategy generate? *Interp:* high turnover amplifies cost sensitivity.
*Misuse:* ignoring it when judging net-of-cost viability. **NOT YET APPLICABLE**
(current families are ≤1 trade/day).

### Exposure
Fraction of time (or capital) the strategy is in the market. *Q:* how much market risk
is carried, and is the return just beta? *Interp:* low-exposure edges are more
diversifying. *Misuse:* comparing gross returns across very different exposures. **NOT
YET APPLICABLE** (intraday, flat overnight).

---

*Statuses are lab-specific and may change as families and sample sizes evolve. When a
metric becomes decision-relevant, promote it and say why in the family charter.*
