# VWAP Strategy Lab — 2026-08

Status: `BOOTSTRAP SCAFFOLD — SOURCE_REQUIRED. NO RUNS. NO HOLDOUT ACCESS. AWAITING DAY-1 CONTEXT FREEZE.`

Created: 2026-08-24 · Sprint: Aug 24–28 2026

This is the setup workspace for the VWAP Strategy Lab. Everything here is **exploratory and
pre-run**. No result has been produced, ranked, or validated. The designated holdout is frozen
forward data under a frozen specification (`docs/conventions.md` §g); no slice of history serves
that role.

> **Independent study.** This lab uses **no CuttingBoard context** (frozen boundary, charter §6)
> and makes **no options claim** (frozen boundary, charter §7). It measures SPY underlying price
> relative to session VWAP, nothing more.

## The blocker, stated plainly

`VDC_SOURCE_STATUS = SOURCE_REQUIRED`. There is no exact current FastAlpha / VWAP Drift v0 Pine
source in `dwats250/strategy` or its history. The primary family's trigger/entry/stop/exit is
**not** reconstructed from chat memory, `session_compass_v2.3.pine`, older VWAP indicators, or
conceptual descriptions — those are context only. See charter §8 for the accepted source gap and
the non-authoritative lineage. Runs are blocked until Dustin supplies the actual TradingView Pine
source or commissions a brand-new VDC-0 specification.

## Contents

| Path | Role |
|---|---|
| [`manifests/STUDY_CHARTER_v0.1.md`](manifests/STUDY_CHARTER_v0.1.md) | Frozen charter: families, acceptance vocabulary, excursion metric, test budget, boundaries, source status |
| [`manifests/RUN_MANIFEST_TEMPLATE_v0.1.md`](manifests/RUN_MANIFEST_TEMPLATE_v0.1.md) | Per-run pre-registration template — fill and **freeze before capture** |
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
