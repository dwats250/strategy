# VWAP Strategy Lab — 2026-08

Status: `R0 CAPTURED + PRESERVED (2026-08-25) — manifest frozen (RUN_VDC_SPY_5m_dev_R0_v1.0.md), ledger row 1/18 VDC-dev, benchmark REFERENCE-ONLY. R1 CAPTURE AUTHORIZED (owner charge 2026-08-25, SEALED-UNINTERPRETED) — manifest frozen (RUN_VDC_SPY_5m_dev_R1_v1.0.md). First capture (2026-08-26) FAILED the mechanical identity gate (wrong window/base-v0 script; files withheld, no budget draw — Amendment 1). Corrected re-capture (2026-08-26) PASSED the mechanical R0/R1 identity gate — R1 ADMISSIBLE (SEALED-UNINTERPRETED): trade list byte-identical to the R0 export (sha256 8d2db8dc…), 1,331 dev-window trades with side/timestamps/prices/P&L identical; chart-data header carries Volume + all ten instrumentation columns (header-only read). Both files preserved byte-identical under exports/ with a SEALED-UNINTERPRETED ledger row. See RUN_VDC_SPY_5m_dev_R1_v1.0.md Amendment 2. R1 DEVELOPMENT UNSEALED (owner/HELM charge 2026-08-26) — first interpretation; VDC-dev interpreted budget now 2/18. PVAE primary comparison ran once under the frozen prereg: frozen S_9_20_50 upper-tercile boundary 1.32975781 (b_lo 0.53202165); PVAE N=263 / non-PVAE N=1068; contrasts pooled +0.0051, long -0.0824, short +0.1074 → PARK RULE C (long/short signs disagree) → SYMMETRIC PVAE PARKED, no rescue; single validation look NOT earned, R2 validation remains SEALED. See RUN_VDC_SPY_5m_dev_R1_v1.0.md Amendment 3, PVAE_ANALYSIS_PREREG Amendment P1, analysis/pvae_dev_analysis_r1_v1.0.py. Feed seam (split-only vs ADJ) noted, not repaired. Pre-existing malformed R0 ledger row (26 vs 27 cols) reiterated, left untouched (did not block analysis). STOP. PARITY: Gate 1 PARTIAL (feed-characterized), Gate 2 CORROBORATED, Gate 3 PROBED — see PARITY_GATES.md dated entries. NO VARIANTS. NO VALIDATION-WINDOW INSPECTION. NO HOLDOUT ACCESS. PVAE: NO OUTCOME INTERPRETATION. OFFLINE ENGINE (owner charge 2026-08-26, TradingView de-gated as a research dependency): deterministic local FastAlpha execution engine built (analysis/fastalpha_engine.py, execution layer only on top of the parity_foundation feature seam; broker-emulator assumptions stated a priori, not tuned). Calibrated vs preserved R0 — 89.86% of R0 reproduced by (fill bar, side); path-agreeing matched trades reconcile at the ~1% dividend feed scale (execution logic validated, NO implementation defect); absolute local net -111.61 vs R0 +25.69 dominated by corpus bad-ticks (141 spike bars; excl-spike net +17.58) → LOCAL ENGINE RESEARCH-READY for differential A/B. First controlled offline A/B V0 EMA 9/20 vs V1 EMA 10/22 on identical bars/engine (determinism-checked, spike-robust): dNet -3.02 / dExp -0.0020per-trade → V1 DEVELOPMENT NEUTRAL. Interpreted VDC-dev budget now 3/18 (owner-flagged accounting). Development window only; validation/holdout/embargo untouched. See RUN_OFFLINE_ENGINE_V0_V1_AB_v1.0.md. CORPUS INTEGRITY SCREEN (owner charge 2026-08-26, trade-blind data-quality task): frozen market-data-only anomaly screen (analysis/corpus_integrity_screen.py; imports no engine/trade code; thresholds frozen from the data distribution before any strategy effect). Corpus structurally sound (0 impossible OHLC, 0 timestamp dupes, monotonic); 9 HIGH-CONFIDENCE RTH bad-ticks (all 4 previously-known rediscovered blind) + 157 PLAUSIBLE EXT thin-market prints; raw corpus preserved byte-for-byte; frozen reversible mask CORPUS_MASK_v1.0.json (HIGH-CONFIDENCE only). Phase 4 raw-vs-screened V0 diagnostic (no budget draw): dropping the 9 bars removes 11 phantom stops → net +24.98 (−111.61→−86.64), max-DD −11.95, but does NOT reconcile to R0 (+25.69) — residual gap is the feed seam, not removable data (corrects the prior loose 141-bar 5m heuristic that over-removed). Disposition: research-clean view JUSTIFIED; proceed DUAL-REPORT for absolute metrics (screened as default corpus), either view for differential A/B. See CORPUS_INTEGRITY_SCREEN_PREREG_v0.1.md. EXPERIMENT TEAR SHEET (owner charge 2026-08-26, analysis infrastructure, no new variant, no budget draw): reusable stdlib-only tearsheet.py — trade-level + R-normalized metrics, equity/drawdown series, monthly/distribution/streaks, outlier concentration, fixed-seed IID+block bootstrap CI, trade-based Sharpe/Sortino (CAGR/Calmar deferred), raw-vs-screened dual_report (screened primary) + controlled ab_report/ab_dual mode; 1R = frozen initial stop distance now on each trade. Example V0 tear sheet (V0_TEARSHEET_2026-08-26.json/.md/.svg) surfaced V0 ~flat in R (mean_r +0.009) yet negative in $ (losses concentrate on higher-ATR trades), mean-expectancy CI straddles zero. Next single experiment (not implemented): controlled ATR-stop-multiple A/B (1.0→1.25) via ab_dual. See EXPERIMENT_TEARSHEET_v0.1.md. FIXED-RISK DIAGNOSTIC + ATR-STOP SURFACE (owner charge 2026-08-26, single-factor ATR_STOP_MULT only): Part A — V0 re-expressed under equal risk is +12.19R yet -$86.64 fixed-share (signs disagree → dollar loss is a position-sizing effect; longs +0.047R, shorts -0.032R). Parts B/C — frozen family {0.75,1.00[ctrl],1.25,1.50,1.75}, screened primary + raw: response shape FLAT in risk-adjusted R (expectancy_R spread 0.013R<0.03) while fixed-share $/PF/win% improve monotonically with wider stops = SIZING ARTIFACT, not an edge; raw/screened agree on direction; control 1.00 reasonable risk-adjusted, "too tight" only in $; best arm 1.75 marginal + view-dependent ($ +2.2 screened vs -33.4 raw). NO production value selected; no intermediate multiple interpolated. Interpreted VDC-dev budget 3→7/18 (4 new ATR-stop configs; 1.00=existing V0). Next single research question (not implemented): "Is the naked VDC edge long-only?" (short side is the R-drag) via ab_dual. See RUN_ATR_STOP_SURFACE_v1.0.md. LONG-ONLY PATH-DEPENDENT A/B (owner charge 2026-08-26, single change = short entries disabled, variant RERUN not filtered): PATH-DIFFERENCE verified by rerun = ZERO divergence (0 path-created/0 lost/0 changed-exit long trades; long-entry Jaccard 1.000 both views → V0 longs/shorts occupy mutually-exclusive VWAP regimes, shorts thesis-exit at the boundary), so long-only-vs-symmetric IS the removed net-negative short book. Long-only favorable + raw/screened-consistent (screened net -$86.64→+$31.05, cumR +12.2→+33.1, PF 0.885→1.093, maxDD_R 75.7→29.8; raw net -$111.6→+$17.2, PF 0.855→1.050) BUT not robust — bootstrap mean-expectancy CI straddles zero in $ and R, net fails best-10 removal (+31→-74 screened). DISPOSITION: LONG-ONLY DEVELOPMENT EFFECT MODEST / UNCERTAIN (development-generated → NOT confirmation). A separately pre-registered single-look validation appears plausibly warranted (small expected effect); validation NOT inspected. Interpreted VDC-dev budget 7→8/18. See RUN_LONG_ONLY_AB_v1.0.md. EMA RESPONSE SURFACE (owner charge 2026-08-26, single factor = EMA fast/slow lengths; no engine/tearsheet change): frozen 3×3 grid fast {8,9,10} × slow {18,20,22}, naked symmetric VDC, screened primary + raw. Response shape FLAT / PARAMETER-INSENSITIVE — all nine cells' pooled expectancy_R inside one 0.0096R band (<MATERIAL_R 0.03), max adjacent-cell jump 0.008R, both marginals sub-material, raw/screened agree on direction (0/8 cells disagree). Control 9/20 is the top R-cell of the flat band (well-placed); 10/22's prior NEUTRAL corroborated (Δ −0.0096R). Directional asymmetry PERSISTENT (long expectancy_R>0 and short<0 in all 9 cells both views) → descriptive support, not confirmation, for the long-only candidate; every cell's bootstrap CI straddles zero and net_excl_best_10 deeply negative (outlier-dependent family-wide). NO production EMA pair selected; no intermediate length interpolated. Interpreted VDC-dev budget 8→15/18 (7 new cells; 9/20 + 10/22 pre-existing). See RUN_EMA_SURFACE_v1.0.md. STOP.`

Created: 2026-08-24 · Sprint: Aug 24–28 2026

PVAE (Persistent VWAP-Aligned Expansion) was adversarially reviewed (lane 2, Fable 5) and
owner-adjudicated **TEST WITH CORRECTIONS** as a stratification hypothesis — see
`STUDY_CHARTER_v0.1.md` **Amendment A1** (acceptance rule frozen, excursion notation
corrected, tercile rule, shock metric, sealed-capture ruling, planned R0/R1/R2) and the
frozen [`PVAE_ANALYSIS_PREREG_v0.1.md`](manifests/PVAE_ANALYSIS_PREREG_v0.1.md). No run has
occurred; no PVAE outcome has been interpreted.

This is the setup workspace for the VWAP Strategy Lab. Everything here is **exploratory and
pre-run**. No result has been produced, ranked, or validated. The designated holdout is frozen
forward data under a frozen specification (`docs/conventions.md` §g); no slice of history serves
that role.

> **Independent study.** This lab uses **no CuttingBoard context** (frozen boundary, charter §6)
> and makes **no options claim** (frozen boundary, charter §7). It measures SPY underlying price
> relative to session VWAP, nothing more.

## The blocker, stated plainly — RESOLVED

*(Historical: superseded by charter Amendment A2 on 2026-08-25; retained for context.)*
`VDC_SOURCE_STATUS` was `SOURCE_REQUIRED` at scaffold time; the exact owner-supplied Pine source
is now ingested at `scripts/VWAP_Continuation_FastAlpha_v0.pine`
(sha256 `c476429225…e342c6c9e`, charter A2), windows are frozen (A3), and R0 is captured and
preserved (frozen manifest `manifests/RUN_VDC_SPY_5m_dev_R0_v1.0.md`). The §8 prohibition on
reconstructing logic from chat memory or older indicators stands — the ingested source is the
only strategy authority.

## Contents

| Path | Role |
|---|---|
| [`manifests/STUDY_CHARTER_v0.1.md`](manifests/STUDY_CHARTER_v0.1.md) | Frozen charter: families, acceptance vocabulary, excursion metric, test budget, boundaries, source status |
| [`manifests/RUN_MANIFEST_TEMPLATE_v0.1.md`](manifests/RUN_MANIFEST_TEMPLATE_v0.1.md) | Per-run pre-registration template — fill and **freeze before capture** |
| [`manifests/PVAE_ANALYSIS_PREREG_v0.1.md`](manifests/PVAE_ANALYSIS_PREREG_v0.1.md) | Frozen PVAE offline-analysis pre-registration (primary comparison, park conditions) |
| [`data/README.md`](data/README.md) | Offline SPY market-data seam — infrastructure, not strategy evidence; corpus captured and verified (`DATA CORPUS PASS`), evidence record in `data/CORPUS_SPY_1m_2024-09-01_2026-08-22.md` |
| [`manifests/RUN_VDC_SPY_5m_dev_R0_v1.0.md`](manifests/RUN_VDC_SPY_5m_dev_R0_v1.0.md) | **Frozen R0 run manifest** — owner-attested TV context, preserved artifacts + hashes, reference metrics (supersedes the retained PREP v0.1) |
| [`scripts/VWAP_Continuation_FastAlpha_v0.pine`](scripts/VWAP_Continuation_FastAlpha_v0.pine) | Exact ingested VDC v0 Pine source (immutable; sha256 in provenance record) |
| [`scripts/VWAP_Continuation_FastAlpha_v0_R1_instrumented_v1.0.pine`](scripts/VWAP_Continuation_FastAlpha_v0_R1_instrumented_v1.0.pine) | R1 instrumented variant — v0 trading byte-identical, observational A1/PVAE covariate exports only |
| [`scripts/VWAP_Continuation_FastAlpha_V1_EMA10_22.pine`](scripts/VWAP_Continuation_FastAlpha_V1_EMA10_22.pine) | V1 controlled perturbation — v0 byte-identical except EMA pair 9/20→10/22 (sole semantic change) + identity; PREP `manifests/RUN_VDC_SPY_5m_dev_V1_EMA10_22_PREP_v0.1.md`, proof `analysis/v1_ema1022_diff_proof.py` |
| [`manifests/RUN_VDC_SPY_5m_dev_R1_v1.0.md`](manifests/RUN_VDC_SPY_5m_dev_R1_v1.0.md) | **Frozen R1 run manifest** — owner capture authorization (SEALED-UNINTERPRETED), source pin, identity-gate mechanics (supersedes the retained PREP v0.1) |
| [`manifests/RUN_OFFLINE_ENGINE_V0_V1_AB_v1.0.md`](manifests/RUN_OFFLINE_ENGINE_V0_V1_AB_v1.0.md) | **Offline engine + V0/V1 A/B run record** — engine spec + broker-emulator assumptions, R0 calibration (RESEARCH-READY), V0 9/20 vs V1 10/22 A/B (NEUTRAL); code `analysis/fastalpha_engine.py`, `v0_calibration.py`, `v0_v1_ab.py`, `test_fastalpha_engine.py` |
| [`manifests/CORPUS_INTEGRITY_SCREEN_PREREG_v0.1.md`](manifests/CORPUS_INTEGRITY_SCREEN_PREREG_v0.1.md) | **Corpus integrity screen (trade-blind)** — frozen anomaly rules + thresholds, 9 HIGH-CONFIDENCE / 157 PLAUSIBLE flags, reversible mask, raw-vs-screened V0 diagnostic; code `analysis/corpus_integrity_screen.py`, `v0_raw_vs_screened_diagnostic.py`, `test_corpus_integrity_screen.py`; mask `analysis/CORPUS_MASK_v1.0.json` |
| [`manifests/EXPERIMENT_TEARSHEET_v0.1.md`](manifests/EXPERIMENT_TEARSHEET_v0.1.md) | **Standard experiment tear sheet (infrastructure)** — reusable metric/report layer (trade + R + equity/drawdown + distribution + outliers + bootstrap + Sharpe/Sortino), raw-vs-screened dual report + A/B mode; code `analysis/tearsheet.py`, `v0_tearsheet.py`, `test_tearsheet.py`; example `analysis/V0_TEARSHEET_2026-08-26.json` |
| [`manifests/RUN_ATR_STOP_SURFACE_v1.0.md`](manifests/RUN_ATR_STOP_SURFACE_v1.0.md) | **Fixed-risk diagnostic + ATR-stop surface** — Part A fixed-risk V0 (R vs $ divergence = sizing), Parts B/C frozen 5-arm `ATR_STOP_MULT` family (FLAT in R; sizing artifact in $); code `analysis/v0_fixed_risk_diagnostic.py`, `atr_stop_surface.py`; evidence `analysis/ATR_STOP_SURFACE_2026-08-26.json`/`.csv` (budget 7/18) |
| [`manifests/RUN_LONG_ONLY_AB_v1.0.md`](manifests/RUN_LONG_ONLY_AB_v1.0.md) | **Long-only path-dependent A/B** — symmetric V0 vs long-only (rerun); verified zero path divergence, MODEST/UNCERTAIN (favorable but CI straddles 0, fails best-10 removal); code `analysis/long_only_ab.py`; evidence `analysis/LONG_ONLY_AB_2026-08-26.json` (budget 8/18) |
| [`manifests/RUN_EMA_SURFACE_v1.0.md`](manifests/RUN_EMA_SURFACE_v1.0.md) | **Compact EMA fast/slow response surface** — frozen 3×3 grid ({8,9,10}×{18,20,22}), symmetric VDC; FLAT / PARAMETER-INSENSITIVE in R (all cells within 0.0096R), 9/20 well-placed, 10/22 corroborated; long+/short− asymmetry PERSISTENT; code `analysis/ema_surface.py`; evidence `analysis/EMA_SURFACE_2026-08-26.json`/`.csv` (budget 15/18) |
| [`scripts/VWAP_Continuation_FastAlpha_v0_PROVENANCE.md`](scripts/VWAP_Continuation_FastAlpha_v0_PROVENANCE.md) | Source provenance + mechanical characterization |
| [`PARITY_GATES.md`](PARITY_GATES.md) | DATA / SEMANTIC / EXECUTION parity status record |
| [`LEDGER.csv`](LEDGER.csv) | One row per interpreted run (header only until source ingest). Authoritative per §f |
| [`exports/README.md`](exports/README.md) | Immutable export naming + TradingView capture requirements |
| [`scripts/README.md`](scripts/README.md) | Strategy scripts — currently `SOURCE_REQUIRED`; none present |
| [`analysis/README.md`](analysis/README.md) | Reproduction expectations per `docs/conventions.md` §d |

## Test budget (charter §9)

| Class | Family / role | Max interpreted runs |
|---|---|---|
| Development | VDC | ≤ 18 |
| Development | VMR | ≤ 12 |
| Development | VREV | 0 |
| Validation | cross-family | ≤ 6 |
| Holdout | cross-family | ≤ 2 |
| **Total interpreted** | | **≤ 38** |

Ceiling, not a target. No holdout access during scaffold or development.

## Ledger schema

`LEDGER.csv` is one row per interpreted run (authoritative, `docs/conventions.md` §f). Columns:

`run_id`, `run_date`, `family`, `budget_class`, `symbol`, `timeframe`, `session`, `timezone`,
`chart_data_convention`, `extended_hours`, `date_window_start`, `date_window_end`, `embargo_desc`,
`source_status`, `script_file`, `script_sha256`, `trials_planned`, `dsr_threshold_implied`,
`tv_account`, `tv_capture_method`, `export_file`, `export_sha256`, `bars_evaluated`, `n_trades`,
`vwap_state`, `acceptance_result`, `notes`.

`trials_planned` and `dsr_threshold_implied` carry the §b (2026-07-30) trial-budget fields on every
row. The header is present now; no data row is written until source ingest.

## Conventions used

Study skeleton and rules per [`docs/conventions.md`](../../docs/conventions.md): §a (layout),
§b (pre-registered frozen manifests + trial-budget amendment), §c (versioned scripts), §d (analysis
reproduction), §e (immutable self-describing exports), §f (authoritative ledger), §g (frozen
forward holdout + embargo), §i (cross-repo isolation — CuttingBoard untouched).

## Tonight's stop line (binding)

No ranked backtests. No parameter comparisons. No performance interpretation. No holdout access.
No VMR implementation. No fresh VDC implementation. This bootstrap is repository/setup work only.
