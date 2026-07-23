# PREMIUM CAMPAIGN MANIFEST — frozen 2026-07-22
**Window:** purchase date → refund decision Tue Jul 28, 09:00 PT (deadline Jul 29)
**Status: FROZEN.** Hypotheses below were written before any deep run was
executed. Anything not listed here is exploratory and must be labelled as
such in the ledger. Editing this file after Run 1 voids the pre-registration.

---

## Scripts (frozen versions)

| Model | Script | Version |
|---|---|---|
| SPY experiment | `spy_orb_tier0_v0_3_0.pine` | v0.3.0-tier0 — NO edits during campaign |
| QQQ replication | superseded — see AMENDMENT A8 | **effective: v1.1.3-rep** |

If either script needs a bug fix mid-campaign, the fix gets a new version,
the ledger records which runs used which, and affected runs are repeated.

## Deep Backtesting mechanics (all runs)

- Strategy Tester → dropdown → Deep Backtesting → set date range → run.
- Deep results appear ONLY in the Strategy Report. The on-chart table
  describes chart-loaded history — ignore it during deep runs.
- Export **List of Trades** from the deep report for every run. The export
  is the evidence; the subscription is temporary.
- Chart state for every run: extended hours OFF, standard candles,
  Properties untouched (no commission override, fill-on-bar-close OFF).
- File naming: `deep_<RUNID>.csv` immediately on download.

---

## RUN LIST (in execution order)

### R0 · Data-depth probe — first, before anything else
SPY 15m chart, v0.3.0, C0/TX30. Deep range: 2010-01-01 → today.
QQQ 5m chart, replication script. Deep range: 2010-01-01 → today.
**Record the earliest trade date each produces.** These two numbers decide:
- whether the QQQ study is a full 2016–2023 replication or partial
  (label accordingly — decided by data, not preference);
- the true out-of-sample span for H3–H5 (everything before 2025-01-21,
  the start of the in-sample 318).
No hypothesis is tested on R0 output beyond reading the dates.

### Tier 1 — confirmatory (the campaign's purpose)
| Run | Chart | Config | Deep range |
|---|---|---|---|
| R1 | SPY 15m | v0.3.0 · C0 · Both · TX30 | max available |
| R2 | QQQ 5m | replication v1.0.0 · paper rules | 2016-01-01 → 2023-02-17 (or max within) |

### Tier 2 — secondary, pre-registered
| Run | Chart | Config | Deep range |
|---|---|---|---|
| R3 | SPY 15m | C0 · Both · TX15 | max |
| R4 | SPY 15m | C0 · Both · TX60 | max |
| R5 | QQQ 5m | replication · 2023-02-18 → today | post-paper out-of-sample |

### Tier 3 — exploratory, run only if time permits, labelled exploratory
| Run | Chart | Config |
|---|---|---|
| R6 | SPY 15m | C4 (RVOL-hot) · Both · TX30 · max range |
| R7 | SPY 15m | C5 (intersection) · Both · TX30 · max range |
| R8 | SPY 5m | C0 · Both · TX30 · max range (event-definition cross-check) |

---

## PRE-REGISTERED HYPOTHESES

All tests on price-derived bps from exported fills. Monthly-block
bootstrap (20k resamples, seed 7) alongside IID CIs. The out-of-sample
(OOS) segment for H3–H5 is **trades entered before 2025-01-21** in R1's
export — dates the in-sample analysis never touched.

**H1 (primary).** SPY C0/15m/TX30 full-history mean bps.
Prediction: |mean| < 2 bps with 95% CI spanning zero.
Decision rule: if CI upper bound < +1.0 bps → event closed permanently
(below even share-trading relevance). If CI lower bound > +1.0 bps →
genuine surprise; freeze everything and design a forward paper test.
Anything between → closed for options expression, discretionary for shares.

**H2 (replication).** QQQ paper rules, 2016–2023 (or available subset):
positive net P&L and PF > 1, qualitatively consistent with the paper's
direction. This validates the harness against a published answer at least
as much as it tests the market. Prediction: directionally positive,
smaller than the paper's headline (their fills were idealized).
If R2 is strongly negative where the paper was strongly positive, treat
as a harness defect first — audit fills before concluding anything.

**H3 (confirmation latency, OOS).** In R1's pre-2025 segment: mean bps of
boundary events (entry at the final legal bar, 10:30 ET) minus non-boundary
events. Two-sided Welch t at α=0.05. Mechanism: longer coil → stronger
expansion. This is the in-sample +4.72 bps anomaly given its one honest
shot on unseen data. Prediction: fails to replicate.

**H4 (short-side deficit, OOS).** Pre-2025 segment: short mean < long mean
(in-sample gap was −3.4 bps). Two-sided Welch t. Prediction: shrinks
toward zero.

**H5 (RVOL dispersion, R6, exploratory-confirmatory hybrid).** C4 vs C0
on pre-2025 trades: predicts **higher sd and higher |MFE|+|MAE|** (the
dispersion account) with mean lift CI spanning zero (no directional value).
This tests our *explanation*, not the original edge claim.

**Multiple comparisons:** four OOS tests (H3–H5 count as four contrasts).
One nominal p<0.05 among them is unremarkable; conclusions require effect
sizes coherent with in-sample magnitudes, not just a p-value.

## What is NOT licensed by this manifest
- No new cohorts, filters, horizons, or symbols mid-campaign.
- No re-running a hypothesis with tweaked parameters after seeing results.
- The 10:30-slot, 0-for-11, and direction anomalies get exactly the tests
  above — no variants.
- "Interesting pattern in the deep data" → open-items ledger, next campaign.

## Refund-decision criterion (restated from calendar event)
Keep Premium only if H1's surprise branch triggers or an ongoing Deep
Backtesting need emerges. Null results = refund by Jul 29. The exports
are permanent either way.

---

# AMENDMENT 1 — 2026-07-22, PRE-RESULT
Appended after external audit of the manifest and QQQ script, before any
run was executed. Zero deep runs exist as of this amendment; the
pre-registration remains intact. Corrections:

**A1. QQQ script version.** v1.0.0 is retired UNRUN: compile blocker
(global mutated in a function) and a critical bracket-timing defect (the
exit was submitted one bar after the fill, leaving the entire second bar
unprotected — a different strategy, not a deviation). R2/R5 use
**v1.1.0-rep**: same-execution bracket (stop live from the fill tick),
estimated-then-corrected target, working ambiguity counter, fill-vs-
intent audits (leverage cap, 1% risk, gap-through-stop), and
`use_bar_magnifier = false` frozen in the declaration.

**A2. H3 frozen to R4/TX60.** The original text cited the +4.72 boundary
mean (a TX60 figure) against R1 (TX30). H3 now reads: in **R4's**
pre-2025 segment, boundary-entry events minus non-boundary events,
two-sided Welch t, α = 0.05. In-sample contrast being tested:
**+5.52 bps** (TX60: +4.72 vs −0.81). TX30/TX15 boundary contrasts are
descriptive only.

**A3. H5 comparator and primary statistic.** Comparator is now disjoint:
C4-ACCEPTED events vs C0 events REJECTED by C4 (pre-2025 segment).
Primary statistic: **sd ratio** (accepted/rejected), bootstrap CI,
predicted > 1. Mean lift and MFE/MAE deltas are descriptive. The OOS
inferential set is exactly **three contrasts: H3, H4, H5-primary**.

**A4. Governing interval.** Where a decision rule references "the CI"
(H1's branches), the **monthly-block bootstrap CI** governs. IID
intervals are reported for continuity but decide nothing.

**A5. H2 harness gates.** Direction alone cannot validate the harness.
R2 must additionally pass known-answer checks before any market
interpretation: trade count ≈ trading days in range minus dojis and
zero-qty skips (order 1,700–1,800 for full 2016–2023.02; reconcile
exactly against the export); long/short split near 51/49; first session
of the range produces a trade or an identifiable doji; zero
gap-through-stop-driven margin events; equity path strongly positive
with PF > 1.2 and ending equity a multiple of start (generous tolerance
for feed/fill differences — the paper's headline is idealized). Fail any
gate → harness audit before market conclusions.

**A8. Effective configuration, slices, and gate language (2026-07-22,
pre-result — zero valid deep runs exist).**
(a) EFFECTIVE VERSIONS: SPY `spy_orb_tier0_v0_3_0.pine` (v0.3.0-tier0);
QQQ `qqq_orb_replication_v1_1_3.pine` (v1.1.3-rep). v1.0.0/1.1.0/1.1.1/
1.1.2 all retired unrun; the top table now points here.
(b) LEVERAGE LANGUAGE (supersedes any enforcement claim): "Position
size is capped using the first-bar close estimate. Emulator margin
enforcement is disabled. Actual fills may slightly exceed 4x; frequency
and magnitude are audited offline (reconstruct leverage as qty x entry
/ running equity rebuilt from $25,000 + cumulative net P&L)."
(c) H2 ANALYSIS SLICES from the single full-depth R2 export: H2 tests
ONLY entries 2016-01-01 through 2023-02-17; R5/post-paper is
2023-02-18 onward; anything pre-2016 is depth diagnostics, exploratory.
(d) A5 GATE CORRECTIONS: the "zero margin events" gate is replaced by
"report leverage-excess frequency/magnitude and gap-through-stop
frequency from the offline reconstruction." The trade-count gate is
approximate, not exact: sessions-in-range minus exported entries equals
dojis + zero-qty skips + data gaps, which the export cannot decompose;
exact decomposition is spot-checked on the chart-loaded window only.
(e) ONE-TRADE-PER-SESSION GATE, precise form: exactly one ENTRY per
session in the export, and zero emulator-generated partial closures
(no same-session trades sharing an entry timestamp with split sizes) —
not merely one CSV trade number per day.

**A7. QQQ margin model (2026-07-22, still pre-result).** Chart-loaded
verification of v1.1.1 revealed emulator margin-call trims: cap-sized
positions opened fractionally over 4x at the actual fill (D3) and were
force-trimmed by 1 share, creating phantom same-session micro-trades
that would corrupt H2's trade-count gate. R2/R5 use **v1.1.2-rep**:
emulator margin enforcement off, the paper's 4x cap enforced by the
sizing rule alone, nLevBreach still measuring the deviation. No valid
deep QQQ run existed before this change.

**A6. R0 folded into R1/R2.** Both Tier 1 runs use deep range
2010-01-01 → today; the earliest trade date in each export IS the depth
probe. The QQQ full-vs-partial label and the OOS span are read from
those dates. A separate probe run is unnecessary.

