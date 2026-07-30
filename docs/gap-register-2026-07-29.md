# Gap register — 2026-07-29

**Status:** `DRAFT — OBSERVATIONAL. AUTHORIZES NOTHING.`

Created 2026-07-29 UTC. Companion to the session appraisal of the same date.

This register creates no charge, no scope, and no permission — same posture as
`EA-AUDIT-CLOSEOUT.md` §6 and `retrospective-ea-audit-2026-07-28.md`. Nothing here is a standing
rule until it is added to `conventions.md` by its own explicit change.

**Reading order.** G-01 is time-decaying and everything else keeps. G-13 … G-15 are new findings
produced this session from the existing proxy export and are the most consequential for what
"optimizing the engine" should mean.

---

## Severity vocabulary

| Class | Meaning |
|---|---|
| **DECAYING** | Evidence is being lost with time. Acting late costs more than acting badly. |
| **BLOCKING** | Downstream work cannot start until this clears. |
| **ADDITIVE** | A real gap, but nothing is blocked on it. Cheap to close. |
| **OPEN QUESTION** | Not established either way; needs a specific test. |

---

## A. Time-critical

### G-01 · Unpre-registered capture in `cuttingboard-asis-proxy` — **DECAYING**

An export exists at `studies/cuttingboard-asis-proxy/exports/CBASIS_v0_1_AMEX_SPY_1D_RTH_20150101-20260729_048f5c66.csv`
— 3,620 daily bars, first 2012-03-06, last **2026-07-29**. Meanwhile `LEDGER.csv` is header-only,
`README.md` says `NO RUN EXECUTED`, and `manifests/RUN_SPY_1D_2015-01-01.md` still shows
`run_date`, `tv_account`, `tv_plan`, `data_provider`, non-default chart settings, the export
`sha256`, all seven macro-series flags, and all six result-summary fields as unfilled.

This is the UV02 failure mode the manifest's own warning box cites.

**Now recovered from the file itself** (arithmetic, not new evidence — see Appendix A):

| Manifest field | Recovered value |
|---|---|
| Bars evaluated (from 2015-01-01) | **2,909** (warm-up 711; total 3,620) |
| Qualified | **200** |
| Watchlist | **297** |
| Rejected | **3,123** |
| Kill-switch bars | **226** |
| First-rejection distribution | code 0 → 200 · 1 → 226 · 2 → 2,500 · 5 → 165 · 7 → 373 · 10 → 156 |
| Macro series resolved | all seven — `votes_cast` = 8 on **all 3,620 rows without exception** |

**Still decaying, recoverable only from Dustin or a live chart:** `tv_plan`, the data provider in
the chart legend, `run_date`, whether any chart setting was non-default.

**Next step:** write those four down. The clean form is a dated capture record beside the
manifest, not an edit to it (§b). Nothing in this register has been written into that study.

---

### G-02 · TradingView Premium expiring — **DECAYING**

Backtesting is available for a few more weeks only. Everything requiring TradingView must be
front-loaded; everything else can wait indefinitely. See
`infrastructure-and-capture-plan-2026-07-29.md` §1, which is organised entirely around this.

**Next step:** decide the capture list before running anything, so the scarce resource buys the
exports you will wish you had rather than the ones you happened to run.

---

## B. New findings — the effective decision surface

These three came out of counting the existing export across all 3,620 rows. They are
**observations, not study findings** — a finding belongs in a document produced under the study's
own `FINDINGS_TEMPLATE_v0.1.md` process, on a run whose manifest is complete. They are recorded
here because they change what the engine program should try to do.

### G-13 · Gate 7 (RR_RATIO) carries no independent information — **BLOCKING (for tuning)**

Gate 7 partitions **perfectly** on `regime_code`:

| | g7 pass | g7 fail |
|---|---|---|
| regime_code = 3 | 0 | **1,157** |
| regime_code ≠ 3 | **2,463** | 0 |

100% of regime-3 rows fail; 100% of all other rows pass. The `rr` column has **zero** influence —
585 rows with `rr` strictly *below* 2.0 passed, and 282 rows with `rr` strictly *above* 2.0
failed. Gate 7 is functionally an alias for `regime_code != 3`.

The mechanism is the one `README.md` predicted: `_build_candidate` sets stop = 1×ATR and
target = 2×ATR, so RR ≈ 2.0 on every candidate; regime 3 demands ≥ 3.0 and everything else
demands ≥ 2.0. The README asked for boundary behaviour to be "reported as observed, not assumed."
It is now observed, and the answer is that the gate is a restatement of an upstream field.

**Why this matters more than it looks:** tuning Gate 7's threshold cannot change any decision
except by flipping the whole regime-3 population at once. Any optimization pass that treats it as
an independent risk/reward filter is tuning a constant.

### G-14 · Gate 5 (STOP_DEFINED) is a pure tautology — **ADDITIVE**

Passes on **3,620 of 3,620** rows. Zero failures. Confirms `GATE_TRANSLATION_MATRIX.md` Q-05
(`CURRENTLY_INERT`) empirically. Harmless as an invariant; worthless as a filter; should never
appear in a sweep.

### G-15 · Gate 3 (DIRECTION) is **not** inert — the matrix classification looks wrong — **OPEN QUESTION**

`GATE_TRANSLATION_MATRIX.md` classifies Q-03 as `CURRENTLY_INERT` and semantic finding #4 states
"Direction alignment is constructed to pass." In the export it **fails on 527 of 3,620 rows
(14.6%)**.

This is either (a) a genuine falsification of a pre-registered semantic hypothesis, or (b) a
proxy artifact where the Pine implementation emits `direction_code = 0` in states the engine
never produces. Spot-check at line 703 shows `direction_code = 0 → g3 = 0`, which points at (b).

Either way this is exactly the "confirm, narrow, or falsify with evidence" that
`BACKTEST_PROTOCOL.md` §TV-2.9 asked for, and it should be resolved rather than left. **It cannot
be resolved from the export alone** — it needs the proxy's direction logic read against the
pinned source.

### G-16 · Several gates appear to be deterministic restatements of upstream fields — **OPEN QUESTION**

Exact cross-column identities, all of them suspicious:

- `posture_code = 1` count (919) **equals** g1_regime pass count (919)
- `regime_code = 2` count (619) **equals** g4_structure fail count (619)
- `regime_code = 3` count (1,157) **equals** g7_rr fail count (1,157)

Semantic finding #6 in the matrix predicted "several late decision gates re-state upstream facts."
These identities are consistent with that and put numbers on it. **The engine's real decision
surface is very likely much smaller than its 30 gates and 54 configured values suggest.**

**Next step:** a gate marginal-contribution analysis. It needs no CuttingBoard change and no new
data — the export already carries every gate boolean. See
`engine-program-draft-2026-07-29.md` §A0.

---

## C. Repository governance

### G-03 · No trial-budget field in any manifest — **ADDITIVE**

`CAMPAIGN_MANIFEST_v2.4.md` already does trial budgeting in prose ("Exactly **three OOS
inferential contrasts: H3, H4, H5**"; the "Not licensed" block). The slot exists. The number does
not.

Evidence it binds: the shallow ORB campaign logged **11 configuration rows** over ~1.5 years.
MinBTL at target SR 1.0 gives ≈ 1.4 yr for N=5 and 1.9 yr for N=7 — so ~1.5 years supports 5–6
independent configs. Nothing was mis-concluded (the study closed at no-edge), but the budget was
spent before the answer arrived. Also note rows C0 and C1 are numerically identical on every
field, so nominal N overcounts effective N.

**Next step:** add `trials_planned` and `dsr_threshold_implied` to the run-manifest template and
`LEDGER.csv`. Both computable before any data exists. Highest leverage per unit effort in this
register.

### G-04 · No embargo rule anywhere — **ADDITIVE**

`BACKTEST_PROTOCOL.md` sets OOS beginning 2022-01-01, the day after IS ends 2021-12-31. Zero gap.
The word "embargo" does not appear in the file. With EMA50/ATR14 on daily bars the leakage window
is ~50 trading days.

**Next step:** one sentence in `conventions.md` §g — a deferred-inspection window is separated
from the fitted window by at least the longest indicator lookback.

### G-05 · Holdout vocabulary vs. framework vocabulary — **ADDITIVE**

§g is *stricter* than the eight-gate framework, not looser. Under §g, Gate 5's entire
walk-forward apparatus produces deferred-inspection windows, never holdouts.

**Next step:** adopt the framework's ratios (IS:OOS 4:1–6:1, 20–40 windows) as *construction
rules* for deferred-inspection windows; do **not** import the term "out of sample." Importing the
vocabulary with the arithmetic would quietly undo the strongest rule in the conventions.

### G-06 · The exploratory tier has no pre-registration path — **ADDITIVE, and the main sprint risk**

`exploratory/cuttingboard-candidate-fidelity-v0_5/` was developed outside governed studies, has
no pre-registered manifest, and carries provenance gaps "recorded, not fixable retroactively."
Its disposition amendment (2026-07-30) records a guardrail crossed. The tier works as a
catch-basin, not as prevention.

**Next step:** a one-page exploratory pre-registration — N, window, symbol, script hash, explicit
"no edge claim" label. Five minutes. Converts an uncitable packet into a weak but citable one.
This should exist **before** the sprint starts, or the sprint will reproduce the pattern at
higher volume.

---

## D. Measurement layer

### G-07 · No performance-statistics layer exists anywhere — **BLOCKING**

`BACKTEST_PROTOCOL.md`'s required exports include trade count, exposure, win rate, average trade,
profit factor, max drawdown, long/short split. The word "Sharpe" does not appear in the file at
all. Absent everywhere in the repo: DSR, PBO/CSCV, WFE, multiple-testing-adjusted t, Calmar,
Sortino, Ulcer, rolling Sharpe, implementation shortfall.

Partial credit: `studies/spy-orb-first-break/LEDGER.csv` carries `t_stat` with monthly-block
bootstrap CI, 20k resamples, seed 7 — Gate 6 machinery, unadjusted for multiplicity.

**Next step:** a Python harness consuming exported trade lists. Gates 3, 4, and 5 structurally
cannot run inside TradingView, so this is required regardless of how the sprint goes, and it
needs no TradingView access to build.

### G-08 · Zero-risk-free-rate trap — **ADDITIVE, pre-emptive**

Does not currently apply, because nothing in the repo computes a Sharpe ratio. Becomes live the
instant anything does. The framework's own finding is that paperswithbacktest's entire library is
inflated by `0.045 / annual_vol` from exactly this default.

**Next step:** whatever computes the first Sharpe takes `risk_free_rate` as a required argument
with no default.

### G-09 · TradingView Sharpe annualization unresolved — **OPEN QUESTION, cheap**

TV's documented formula uses average monthly return with no √12 term, and no TV page states the
answer. If not annualized, a true annualized Sharpe of 1.0 displays ≈ 0.29.

**Next step:** one long smooth backtest, export monthly equity, compute annualized Sharpe by
hand, check whether TV's figure is yours or yours ÷ 3.46. Ten minutes, day one, recorded once.

---

## E. Engine limitations carried from the closed audit

Recorded for completeness; all four are the closeout's, unchanged and not relitigated.

| ID | Gap | Class | Source |
|---|---|---|---|
| **G-10** | Per-candidate gate vectors computed then discarded; `gates_passed`/`gates_failed` in no durable artifact | BLOCKING | L-2 / EA5-002 / EA-6-001 |
| **G-11** | Accepted path structurally unobservable; `_fixture_chain_results` returns `MANUAL_CHECK` unconditionally | BLOCKING | L-1 / EA-6-006 |
| **G-12** | No authorized, provenance-bearing historical OHLCV dataset | BLOCKING | Closeout §2 — real-data evaluable range EMPTY |
| G-17 | Reason codes are prose with interpolated numerals, not a stable enum | ADDITIVE | EA-6-004 |
| G-18 | No ordering / override / precedence event stream | ADDITIVE | EA-6-002 |
| G-19 | Stale-symbol exclusions reach stderr only; `excluded_symbols` stays empty | ADDITIVE | EA-6-003 |
| G-20 | A designed HALT is indistinguishable from an unhandled-exception HALT | ADDITIVE | EA5-001 |
| G-21 | Three terminal-HALT thresholds live outside `config.py` | ADDITIVE | EA5-003 — fitting-readiness |

**G-10, G-11 and G-12 together are the reason no statistics work can start on the engine.**
Without an observable accepted path and authorized data, no accepted-population metric is
computable, which blocks all eight framework gates upstream of any statistics.

---

## F. Infrastructure

### G-22 · No local run/test loop — **BLOCKING for iteration**

The engine cannot be run against data and inspected without the full audit containment
apparatus. This is what pushed the v0.5 work outside the repo (G-06).

### G-23 · CuttingBoard is a forbidden mutation target from this repo — **structural**

§i. Improving the engine means changing it somewhere, and nowhere is currently authorized.
Three options with their consequences are laid out in `engine-program-draft-2026-07-29.md` §C.
**No option is selected here.**

---

## Appendix A — provenance of the recovered counts

Counts in G-01 and G-13 … G-16 were produced this session by anchored-regex line counting over
the export, with no shell available. Every partition was checked for consistency:

- `votes_cast = 8` → 3,620 / 3,620
- qualified + watchlist + rejected = 200 + 297 + 3,123 = **3,620** (mutually exclusive, exhaustive)
- first-rejection distribution sums to **3,620**
- every gate's pass + fail = **3,620**
- the three `rr` buckets' g7-pass counts sum to 585 + 591 + 1,287 = **2,463**, matching the
  independent column-25 count

One methodological correction was made and is recorded: the first cross-tab regex was off by one
column and was testing g6 rather than g7. It was corrected and the arithmetic self-check above is
what caught it.

**Interpretive limit.** The `first_rejection` integer codes are reported raw. Only two are
anchored by an exact count identity — 0 → 200 = qualified, 1 → 226 = kill-switch bars. Mapping
codes 2, 5, 7, 10 to named gates requires `manifests/RULE_MAPPING_v0.1.md`, which was **not read**
this session. Do not assume the codes are gate numbers.

**Status limit.** These counts are arithmetic on a file that already exists. They complete a
result summary; they do not convert an unpre-registered capture into a governed run, and they
establish no claim about edge, profitability, or engine quality.
