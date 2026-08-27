# analysis/ — reproduction code (per `docs/conventions.md` §d)

Empty until there are runs to analyze. No headline number exists yet to reproduce.

The VDC local parity foundation lives here: `parity_foundation.py` (RTH-only 5m bar
reconstruction + Fast Alpha v0 feature calculator per the ingested source; no simulation,
no P/L) with deterministic tests in `test_parity_foundation.py`. Derived outputs stay
under the gitignored `../data/cache/derived/`. Parity status: `../PARITY_GATES.md`.

The PVAE offline analysis is pre-registered in
[`../manifests/PVAE_ANALYSIS_PREREG_v0.1.md`](../manifests/PVAE_ANALYSIS_PREREG_v0.1.md);
code implementing it lands here only after R1 passes the R0 identity gate.

**2026-08-26 — offline FastAlpha execution engine + V0/V1 A/B** (owner charge; TradingView
de-gated as a research dependency). The engine `fastalpha_engine.py` adds only the execution
layer Pine performs (orders, fills, ATR stop, thesis/EOD exits, the `flat` gate, per-trade P/L)
on top of `parity_foundation`'s feature seam; its broker-emulator assumptions are stated a priori
in the module docstring and never tuned against P/L. Tests: `test_fastalpha_engine.py` (11
engine-path cases). Calibration `v0_calibration.py` asserts the R0 headline, reproduces 89.86% of
R0 by (fill bar, side), validates the execution logic against the ~1% dividend feed scale, and
classifies the residual — the absolute-P/L gap is corpus bad-ticks (141 spike bars), not logic:
**LOCAL ENGINE RESEARCH-READY** (evidence `V0_CALIBRATION_RESULTS_2026-08-26.json`). The controlled
A/B `v0_v1_ab.py` runs V0 (EMA 9/20) vs V1 (EMA 10/22) on identical bars/engine, determinism-checked
and spike-robust: **V1 DEVELOPMENT NEUTRAL** (evidence `V0_V1_AB_RESULTS_2026-08-26.json`). Full
record: [`../manifests/RUN_OFFLINE_ENGINE_V0_V1_AB_v1.0.md`](../manifests/RUN_OFFLINE_ENGINE_V0_V1_AB_v1.0.md).
Recommended next offline step: pre-registered corpus bad-tick screening (not implemented).

**2026-08-26 — SPY corpus integrity screen** (owner charge; trade-blind data-quality task).
`corpus_integrity_screen.py` flags 1m bars on market-data properties ALONE (imports no engine or
trade code): impossible OHLC (Rule A), and isolated reverting excursions beyond both same-session
neighbours (Rule B), with thresholds frozen from the data distribution before any strategy effect
(pre-registration [`../manifests/CORPUS_INTEGRITY_SCREEN_PREREG_v0.1.md`](../manifests/CORPUS_INTEGRITY_SCREEN_PREREG_v0.1.md)).
Result: corpus structurally sound (0 impossible OHLC, monotonic timestamps); **9 HIGH-CONFIDENCE**
RTH bad-ticks (all 4 previously-known rediscovered blind) + 157 PLAUSIBLE EXT thin-market prints
(evidence `CORPUS_INTEGRITY_SCREEN_2026-08-26.json`). The raw corpus is never mutated; a frozen
reversible mask (`CORPUS_MASK_v1.0.json`, HIGH-CONFIDENCE only) is applied via
`fastalpha_engine.compute_feature_rows(..., drop_t_ms=)`. Phase 4 diagnostic
`v0_raw_vs_screened_diagnostic.py`: dropping the 9 bars removes 11 phantom stops, +24.98 net,
−11.95 max-DD, but does NOT reconcile to R0 — the residual gap is the feed seam, not removable data
(this corrects the prior loose 141-bar 5m heuristic, which over-removed). Tests
`test_corpus_integrity_screen.py` (detection, no-mutation, reversible mask, determinism). No
strategy trial, no budget draw.

**2026-08-26 — standard experiment tear sheet** (owner charge; analysis infrastructure, no new
variant, no budget draw). `tearsheet.py` (stdlib-only) computes trade-level + R-normalized
metrics, equity/drawdown series, monthly/distribution/streak stats, outlier-concentration
diagnostics, a fixed-seed IID+block bootstrap CI, and trade-based Sharpe/Sortino, with a
raw-vs-screened `dual_report` (screened primary) and a controlled `ab_report`/`ab_dual` mode
(deltas, entry overlap, Jaccard, screened/raw direction agreement). 1R = the frozen initial stop
distance now recorded per trade by the engine (`risk_points`/`pnl_r`). CAGR/Calmar deferred
(account-construction-dependent). Example driver `v0_tearsheet.py` → `V0_TEARSHEET_2026-08-26.json`
(+ `.md`, equity `.svg`); it surfaced that V0 is ~flat in R (mean_r +0.009) yet negative in $
(losses concentrate on higher-ATR trades) and its mean-expectancy CI straddles zero. Tests
`test_tearsheet.py` (formulas, R, drawdown, PF edges, A/B overlap, dual reporting, bootstrap
determinism, numpy reference cross-check). Manifest
[`../manifests/EXPERIMENT_TEARSHEET_v0.1.md`](../manifests/EXPERIMENT_TEARSHEET_v0.1.md).

**2026-08-26 — fixed-risk diagnostic + ATR-stop response surface** (owner charge; single-factor
`ATR_STOP_MULT` only). Part A `v0_fixed_risk_diagnostic.py` re-expresses V0 under equal risk
(no new trial): V0 is **+12.19R** yet **−$86.64** at fixed 1 share (signs disagree) — the dollar
loss is a position-sizing effect (losses on higher-ATR trades), longs +0.047R vs shorts −0.032R.
Parts B/C `atr_stop_surface.py` freeze `ATR_STOP_MULT ∈ {0.75, 1.00[control], 1.25, 1.50, 1.75}`
before outcomes and run the family screened(primary)+raw: **response shape FLAT in risk-adjusted R**
(expectancy_R spread 0.013R < 0.03) while fixed-share $/PF/win% improve monotonically with width —
a **sizing artifact**, not an edge; raw/screened agree on direction; control 1.00 reasonable
risk-adjusted, "too tight" only in $. **No production value selected.** Engine gained additive
`atr_stop_mult` (default 1.0 = V0); tearsheet gained additive `r_equity`. Evidence
`V0_FIXED_RISK_DIAGNOSTIC_2026-08-26.json`, `ATR_STOP_SURFACE_2026-08-26.json`/`.csv`. Interpreted
VDC-dev budget **7/18** (4 new ATR-stop configs; 1.00 = existing V0). Manifest
[`../manifests/RUN_ATR_STOP_SURFACE_v1.0.md`](../manifests/RUN_ATR_STOP_SURFACE_v1.0.md).

**2026-08-26 — long-only VDC path-dependent A/B** (owner charge; single change = short entries
disabled). `long_only_ab.py` reruns the long-only strategy through the engine (not a filter) and
compares vs symmetric V0, screened primary + raw. **Verified by rerun: ZERO path divergence** —
0 path-created / 0 lost / 0 changed-exit long trades, long-entry Jaccard 1.000 in both views (V0
longs/shorts occupy mutually-exclusive VWAP regimes; shorts thesis-exit at the boundary), so the
long-only-vs-symmetric gap **is** the removed net-negative short book. Long-only is directionally
favorable and raw/screened-consistent (screened net −$86.64→+$31.05, cumR +12.2→+33.1, PF
0.885→1.093, max-DD-R 75.7→29.8) **but not robust** — bootstrap mean-expectancy CI straddles zero
in $ and R, and net fails best-10 removal (+31→−74). Disposition **MODEST / UNCERTAIN** (not
confirmation — development-generated); a pre-registered single-look validation appears plausibly
warranted (small expected effect), not inspected. Engine gained additive `enable_longs`/`enable_shorts`;
a synthetic test proves it models short→long path creation. Evidence `LONG_ONLY_AB_2026-08-26.json`;
budget **8/18**; manifest
[`../manifests/RUN_LONG_ONLY_AB_v1.0.md`](../manifests/RUN_LONG_ONLY_AB_v1.0.md).

Analysis code here is part of the experiment, not a scratch step: it is versioned, committed, and
held to the same rigor as the manifest and scripts. When runs exist, a reproduction script here
must, at minimum:

- assert the headline numbers the study reports and **fail loudly** (nonzero exit) if they don't
  reproduce;
- print the package versions it ran under;
- print the checksum of every input file it reads (the ledger and the exports it consumes).

`reproduce_campaign.py` in `studies/spy-orb-first-break/` is the template for this pattern.

No analysis runs during the bootstrap scaffold: no ranked backtests, no parameter comparisons, no
performance interpretation.
