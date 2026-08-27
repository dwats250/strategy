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

**2026-08-26 — compact EMA fast/slow response surface** (owner charge; single factor
= EMA fast/slow lengths). `ema_surface.py` maps a frozen 3×3 grid — fast {8,9,10} ×
slow {18,20,22} — around the V0 control with naked **symmetric** VDC (no engine or
tearsheet change; it composes the existing `compute_feature_rows(fast, slow, …)` seam
and tear-sheet metrics, so all prior results stay byte-identical), screened primary +
raw sensitivity, determinism-checked. **Response shape FLAT / PARAMETER-INSENSITIVE**:
all nine cells' pooled expectancy_R sit inside one 0.0096R band (< MATERIAL_R 0.03),
max adjacent-cell jump 0.008R, both marginals sub-material, raw/screened agree on
direction (0/8 cells disagree). Control 9/20 is the top R-cell of the flat band
(well-placed); 10/22's prior NEUTRAL is corroborated (Δ −0.0096R). The one coherent
feature is a **PERSISTENT** long-positive / short-negative asymmetry (long expectancy_R
> 0 and short < 0 in all 9 cells, both views) — descriptive support, not confirmation,
for the standing long-only candidate; every cell's bootstrap CI straddles zero and
`net_excl_best_10` is deeply negative (outlier-dependent family-wide). **No production
EMA pair selected.** Tests `test_ema_surface.py` (classifier branches on synthetic
surfaces). Evidence `EMA_SURFACE_2026-08-26.json`/`.csv`; interpreted VDC-dev budget
**15/18** (7 new cells; 9/20 + 10/22 pre-existing). Manifest
[`../manifests/RUN_EMA_SURFACE_v1.0.md`](../manifests/RUN_EMA_SURFACE_v1.0.md).

**2026-08-26 — long-only SINGLE-LOOK validation** (owner/HELM charge; the one
authorized validation look). `long_only_validation.py` reruns symmetric V0 (control)
and long-only (variant) through the frozen engine over the **validation** window
2026-01-06→2026-04-30 (80 sessions). Firewall/holdout hygiene: the corpus extends to
2026-08-21, so — because EMA/ATR/VWAP are causal — the 1m stream is truncated at
2026-04-30 before 5m aggregation (no engine change), guaranteeing no post-window bar
enters the indicator or trade path; the pre-registration was frozen and pushed
**before** any outcome (commit 401c1bb), with results recorded only by dated
manifest amendment. The frozen dev-mask flags 0 bars in-window, so screened == raw
in-window (pre-disclosed); the block-bootstrap CI is the STRONG-vs-DIRECTIONAL
discriminator. **Result: FAILS VALIDATION** — screened primary criteria: A (long-only
expectancy R > 0) **FAILS** at −0.01872, while B (long-only −0.01872 > symmetric
−0.05233) and C (symmetric short −0.08977 < 0) **hold**. The directional structure
replicated (removing shorts helps; shorts are the R-drag) but the standalone
long-only edge did not (negative, block CI R [−0.283,+0.323] straddles zero, 1/4
months positive); zero path divergence (Jaccard 1.000). Per the frozen **no-rescue**
rule the long-only hypothesis is **PARKED**; no holdout or portability work opened.
Tests `test_long_only_validation.py` (A/B/C + strength classifier on synthetic
inputs). Evidence `LONG_ONLY_VALIDATION_2026-08-26.json`; validation-class look —
interpreted VDC-development remains 15/18. Manifest
[`../manifests/RUN_LONG_ONLY_VALIDATION_v1.0.md`](../manifests/RUN_LONG_ONLY_VALIDATION_v1.0.md).

**2026-08-26 — VDC terminal disposition + FPC family opened** (owner/HELM charge;
PREP/infrastructure, **no FPC outcome inspected**). Naked VDC is retired as a
strategy candidate (retained as benchmark/control; final interpreted-development
15/18, 3 slots intentionally unused) — `../manifests/VDC_TERMINAL_DISPOSITION_v1.0.md`.
A new independent family **FPC — First Pullback Continuation** is opened: entry is
restricted to the FIRST opposing-color pullback after a FRESH VWAP/EMA regime (vs
VDC's every-opposing-candle rule), symmetric. The engine gained an additive
`simulate(..., signal_mode="vdc"|"fpc")`; **`"vdc"` is the default and reproduces
every prior result byte-identical** (re-verified: `V0_V1_AB_RESULTS` and
`EMA_SURFACE` JSONs unchanged), while `"fpc"` adds a per-side arm-state (arm on fresh
regime, first red/green bar while flat, one entry per continuous regime) that reads
only precomputed parity_foundation fields and re-implements no indicator. New engine
sha `26e1fb07…`. Tests `test_fpc_signals.py` (8 cases incl. a VDC(2)-vs-FPC(1)
contrast proving the first-pullback restriction). Charter
[`../manifests/FPC_CHARTER_v0.1.md`](../manifests/FPC_CHARTER_v0.1.md) (provenance
trace + H3 evidentiary flag; proposed budget ≤12; confirmation policy — the consumed
VDC validation window may not be FPC validation); first dev run pre-registered but
**not executed** in
[`../manifests/RUN_FPC0_DEV_PREP_v0.1.md`](../manifests/RUN_FPC0_DEV_PREP_v0.1.md).

**2026-08-27 — FPC-0 first development run** (owner/HELM charge; FPC config 1/12).
`fpc0_dev.py` runs FPC-0 symmetric (`signal_mode="fpc"`) against the VDC symmetric
benchmark on the same engine/corpus over the development window, screened primary +
raw, with the classification frozen and pushed pre-outcome (commit be03f0c; results
by dated manifest amendment). HELM adjudications carried in: flat-state
interpretation (a) (engine already conforms) and the H3 provenance attestation
(`../manifests/FPC_CHARTER_v0.1.md` Amendment 1). **Result: FPC DEVELOPMENT WORSE** —
mean expectancy R VDC +0.00900 vs FPC −0.02319 screened (delta_R −0.03219 < −0.03),
raw −0.00910 vs −0.03961 (delta_R −0.03051 < 0, agrees); FPC absolute expR −0.02319
(negative). The first-pullback restriction lowers expectancy R on both sides
(long +0.047→+0.014, short −0.032→−0.065); the $ improvement (−86.64→−43.65) is the
fixed-share sizing artifact, not the metric. Entry geometry: VDC 1354→FPC 1069
(72.4% retained, 27.6% suppressed by one-per-regime, 89 path-created); 908 bull
regimes (565 signalled), 807 bear (504); bars-from-fresh median 2. Mechanical
invariants asserted from the trade set (≤1 signal/regime; none on a fresh bar);
`test_fpc_signals.py` covers the rest. Per the frozen no-rescue rule: report and
stop, no FPC-1. Evidence `FPC0_DEV_2026-08-27.json`; FPC-dev budget 1/12 (independent
of VDC 15/18). Manifest
[`../manifests/RUN_FPC0_DEV_v1.0.md`](../manifests/RUN_FPC0_DEV_v1.0.md).

**2026-08-27 — continuation lane closed + VMR family opened (DESIGN ONLY)** (owner/HELM
charge; no VMR outcome inspected). The whole VWAP continuation lane is concluded NO
EDGE FOUND (`../manifests/CONTINUATION_TERMINAL_DISPOSITION_v1.0.md`; VDC 15/18 and FPC
1/12 budgets closed intentionally unused). A new independent family **VMR — VWAP Mean
Reversion** is designed: fade extreme VWAP extension toward VWAP, structurally opposite
to continuation. Its only new parameter — the extension threshold **K = 4.0916 ATR** —
is derived **trade-blind** by `vmr_excursion_profile.py` as the development-window P90
of `|(close−session_vwap)/ATR14|` (the charter-frozen §5/§A1.3 excursion metric),
frozen before any VMR outcome; a naive canonical 2.0-ATR was rejected (39% of bars
exceed it — the session-anchored-VWAP distribution is wide: median 1.54, P90 4.09 ATR).
Evidence `VMR_EXCURSION_PROFILE_2026-08-27.json` (no strategy run, no P/L). The VMR-0
mechanics (extension + opposing-color reversal → enter toward VWAP; target = session
VWAP; 1×ATR further-extension stop; symmetric) are pre-registered in
[`../manifests/VMR_CHARTER_v0.1.md`](../manifests/VMR_CHARTER_v0.1.md); the
`signal_mode="vmr"` engine support is **not** implemented in this design packet (it is
authored in the run packet). First dev run pre-registered but **not executed**:
[`../manifests/RUN_VMR0_DEV_PREP_v0.1.md`](../manifests/RUN_VMR0_DEV_PREP_v0.1.md).

**2026-08-27 — research cockpit + MIM family (BLOCKED — DATA/SEMANTIC)** (owner/HELM
charge). A permanent research-learning layer was added at repo level under
`docs/research/` (research ledger, metric primer, Mermaid research map, family-autonomy
protocol). MIM — Market Intraday Momentum (Gao/Han/Li/Zhou) was opened and its exact
MIM-0 baseline frozen: `mim.py` implements the clock semantics (previous_close, 09:59
close, 15:30 open, 15:59 close), the sign strategy, an OLS/HC1 regression (β>0 primary),
sign-strategy economics in bps, and three frozen cost views; tested by `test_mim.py`
(6/6 synthetic). **Outcome access is BLOCKED (status C):** MIM-0's `early_return`
crosses the previous RTH close, but the corpus is dividend-**unadjusted** (Polygon
`adjusted=true` = splits only). The trade-blind `mim_overnight_diagnostic.py` shows SPY
ex-dividend drops (~30–40 bps) sit at the **median** of the overnight `|gap|`
distribution (27.6 bps; the twelve largest gaps are genuine macro/news, e.g. the April
2025 tariff sequence −346/−323/−260 bps) — so no OHLCV threshold cleanly separates
dividends from real overnight momentum. Per the charge, **STOP** before the regression/
economics rather than guess; needs an external ex-dividend calendar or a
dividend-adjusted previous-close series. Evidence
`MIM_OVERNIGHT_DIAGNOSTIC_2026-08-27.json`; MIM-dev budget ≤4, 0 spent. Manifests
[`../manifests/MIM_CHARTER_v0.1.md`](../manifests/MIM_CHARTER_v0.1.md),
[`../manifests/RUN_MIM0_DEV_PREP_v0.1.md`](../manifests/RUN_MIM0_DEV_PREP_v0.1.md).

**2026-08-27 — MIM-0 unblocked (State Street ex-dividend seam) + run → FAMILY DEAD**
(owner/HELM charge; MIM config 1/4). The blocker was cleared by an authorized narrow
State Street/SPDR SPY distributions seam (corporate-action normalization only): the six
dev-window ex-dividend distributions were independently verified before freezing
(`../data/SPY_EX_DIVIDENDS_v1.0.json`). `mim.py` gained the frozen **dividend-neutral**
`early_return` (ex-date adds the cash distribution to the 10:00 price; all other MIM-0
semantics unchanged) and a development `main()`; the convention was pushed pre-outcome
(commit 8eabc76), then run once. **Result (N=328, dividend-neutral screened primary):
β = −0.01674** (HC1 SE 0.0317, t −0.53, CI95 [−0.079, +0.045], R² 0.002) → the primary
β>0 condition **FAILS**; sign-strategy gross **−0.59 bps**, fails the 5 bps cost stress,
bootstrap CI straddles zero. Robust: raw == screened (mask bars are not MIM clock bars)
and the ex-dividend-excluded sensitivity (β −0.0157) agrees. **VERDICT: MIM FAMILY DEAD**
(β≤0; gross≤0; fails cost stress) — SPY shows no previous-close→10:00 intraday-momentum
edge here; no rescue (STOP at A). Tests `test_mim.py` (7/7). Evidence
`MIM0_DEV_2026-08-27.json`; MIM-dev 1/4 (remaining ≤3 not earned). Manifest
[`../manifests/RUN_MIM0_DEV_v1.0.md`](../manifests/RUN_MIM0_DEV_v1.0.md) Amendment 1.

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
