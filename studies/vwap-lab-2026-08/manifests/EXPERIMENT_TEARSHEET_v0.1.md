# Standard experiment tear sheet — v0.1 · 2026-08-26

Reusable, deterministic analysis-infrastructure layer for FastAlpha-family LOCAL
research. **Infrastructure, not a strategy experiment:** it defines no signal,
runs no new variant, interprets no validation/holdout, and draws no interpreted-
run budget. Authorization: owner charge 2026-08-26, "STANDARD EXPERIMENT TEAR
SHEET v0.1." Frozen on commit; corrections are dated amendments or a new
versioned file (§b/§c/§d).

## Data policy (frozen)

- **Primary research view:** the screened corpus (frozen `CORPUS_MASK_v1.0.json`).
- **Sensitivity view:** the raw corpus.
- Every summary exposes **screened + raw + delta** (`tearsheet.dual_report`).
- The raw corpus and the anomaly mask are **never altered**.

## Files (versioned, §c/§d)

| File | SHA256 | Role |
|---|---|---|
| `analysis/tearsheet.py` | `76535ed2ec281c3642eef4437d826052a58d4bac51a324e2feda28a50340251d` | The metric/report layer (stdlib-only) |
| `analysis/v0_tearsheet.py` | `0753cc9d24c5ad90a644c26f4ee1ee2d9573fc8b4ea37effa31f8843de19c678` | Example driver: V0 dual report → JSON+MD+SVG |
| `analysis/test_tearsheet.py` | `07c4a1f6b3fcf0692d2631955102c5f09038e12885c369902806802a9ca13482` | 11 tests (formulas, R, drawdown, PF edges, A/B, dual, bootstrap, numpy cross-check) |
| `analysis/V0_TEARSHEET_2026-08-26.json` | `a824f623e4f6c2c2922a190ceec495fcc4c40fe4f308e3948d01ce7e09584282` | Canonical V0 example evidence |
| `analysis/V0_TEARSHEET_2026-08-26.md` | (regenerated) | Human summary |
| `analysis/V0_TEARSHEET_equity_2026-08-26.svg` | (regenerated) | Equity + underwater figure (pure SVG) |

The layer is **stdlib-only** so it runs without numpy; the reference cross-check
against numpy lives in the tests (numpy is never a runtime dependency, and
QuantStats/Empyrical are not installed or required).

## Frozen conventions (descriptive defaults — NOT optimized against results)

- **1R** = the frozen initial entry-to-stop distance `risk_points`
  (= `atr_stop_ticks × mintick`), recorded per trade by the engine.
  `pnl_r = pnl / risk_points`. Trades exiting via thesis/EOD/stop **all** use this
  initial-R denominator (**no retroactive resizing**); a realized stop-out loses
  slightly more than 1R because of the 1-tick exit slippage.
- Monthly P/L is attributed to a trade's **exit month** (realized).
- Rolling stats use a **trade-index** window of **50 trades** (not a calendar
  window; not optimized).
- Bootstrap uses a **fixed seed** (20260826). The **IID** bootstrap is labelled
  **PROVISIONAL** (trade outcomes may be serially dependent); a **moving-block**
  bootstrap with block length `round(n^(1/3))` is also emitted (rule-of-thumb,
  not tuned).
- Sharpe/Sortino are **trade-based** (per-trade P/L series); an annualized form is
  emitted with the exact trades/year assumption labelled.

## Metric inventory

- **Trade-level:** total trades, net P/L, expectancy, median P/L, win rate, avg
  winner, avg loser, payoff ratio, profit factor, largest win, largest loss,
  stdev P/L, avg + median holding duration, exit-reason counts, and long/short
  blocks (N / net / expectancy / PF).
- **R-normalized:** total R, mean R, median R, avg winner R, avg loser R, stdev R,
  R histogram (denominator + exit treatment documented above).
- **Equity / risk (deterministic series):** cumulative equity, underwater curve,
  max drawdown, longest drawdown duration (trades), rolling expectancy, rolling
  profit factor, cumulative long P/L, cumulative short P/L.
- **Consistency / distribution:** monthly P/L, monthly count, monthly expectancy,
  % profitable months, P/L histogram, R histogram, holding-duration histogram,
  max consecutive win/loss streaks.
- **Outlier concentration (robustness only):** contribution of best 1/5/10/20 and
  top-1% trades (as % of gross profit — a stable denominator when net < 0), and
  net with best 1/5/10 removed. Removals are **not** alternate strategies.
- **Uncertainty:** IID bootstrap 95% CI of mean expectancy (PROVISIONAL) +
  moving-block bootstrap 95% CI.
- **Portfolio:** trade-based Sharpe, Sortino, downside deviation; labelled
  annualized Sharpe/Sortino. **CAGR / Calmar DEFERRED** (fixed-1-share vs $50k is
  arbitrary capital utilization → account-construction-dependent, not a discovery
  metric).
- **Modes:** `dual_report` (screened+raw+delta); `ab_report` (metric deltas,
  entry-set overlap, Jaccard, trades added/removed, changed-exit-same-entry,
  long/short deltas — causality not inferred beyond the changed parameter);
  `ab_dual` (A/B under both views + whether screened and raw agree on the sign of
  the headline net-P/L effect).
- **Outputs:** canonical JSON (primary), human markdown, and a pure-SVG equity +
  underwater figure derived from the canonical series (no plotting library, no
  dashboard/web UI).

## Example — V0 (EMA 9/20), screened primary

From `analysis/V0_TEARSHEET_2026-08-26.json`:

| metric | screened | raw | Δ (screened−raw) |
|---|---:|---:|---:|
| trades | 1354 | 1363 | −9 |
| net P/L | −86.64 | −111.61 | +24.98 |
| expectancy | −0.0640 | −0.0819 | +0.0179 |
| profit factor | 0.885 | 0.855 | +0.030 |
| win rate | 21.71% | 21.35% | +0.36 |
| max drawdown | 131.98 | 143.94 | −11.95 |

- **R vs $ (the informative one):** `mean_r = +0.009` while $-expectancy is
  −0.064. In risk-adjusted terms V0 is ~flat; in dollars it is slightly negative,
  because losing trades concentrate on **higher-ATR (higher-risk)** entries.
  Winners ~+2.99R, losers ~−0.82R, payoff ~3.19, win rate ~22%.
- **Uncertainty:** mean-expectancy 95% CI straddles 0 — IID [−0.176, +0.056]
  (provisional), block(L=11) [−0.211, +0.072] — V0 expectancy is not
  distinguishable from zero.
- **Concentration:** best 10 trades = 22% of gross profit; max losing streak 28.

## Deferred metrics (stated)

- **CAGR / Calmar** — account-construction-dependent (see above).
- **Calendar-window** rolling stats — trade-index windows used instead (no frozen
  calendar convention exists to adopt).
- **Extra SVG panels** (rolling expectancy, monthly bars, histograms) — the
  canonical numeric data is emitted; only the equity + underwater figure is
  rendered, to avoid a heavyweight plotting layer.

## Recommended next SINGLE experiment (not implemented)

A controlled **ATR-stop-multiple** offline A/B — e.g. `ATR_STOP_MULT 1.0 → 1.25`,
one factor changed, everything else identical — reported through this layer under
the screened view with `ab_dual` (screened/raw direction agreement). The R-vs-$
divergence above points at stop distance / risk sizing as the live lever; a single
stop-multiple look is the smallest test of it. One factor, one look; no new metric,
no validation/holdout.

## Amendments

*(append dated amendments here; never edit the text above in place)*
