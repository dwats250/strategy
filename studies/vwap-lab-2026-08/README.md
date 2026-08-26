# VWAP Strategy Lab — 2026-08

Status: `R0 CAPTURED + PRESERVED (2026-08-25) — manifest frozen (RUN_VDC_SPY_5m_dev_R0_v1.0.md), ledger row 1/18 VDC-dev, benchmark REFERENCE-ONLY. R1 INSTRUMENTED SOURCE BUILT + CONTAINMENT-VERIFIED (2026-08-25) — PREP manifest only; R1 CAPTURE NOT AUTHORIZED. PARITY: Gate 1 PARTIAL (feed-characterized), Gate 2 CORROBORATED, Gate 3 PROBED — see PARITY_GATES.md dated entries. NO VARIANTS. NO VALIDATION-WINDOW INSPECTION. NO HOLDOUT ACCESS. PVAE: NO OUTCOME INTERPRETATION.`

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
| [`manifests/RUN_VDC_SPY_5m_dev_R1_PREP_v0.1.md`](manifests/RUN_VDC_SPY_5m_dev_R1_PREP_v0.1.md) | R1 manifest PREP (not frozen, not a run authorization) — containment proofs, field list, identity gate, owner capture procedure |
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
