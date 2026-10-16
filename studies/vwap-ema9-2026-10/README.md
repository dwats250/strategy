# vwap-ema9-2026-10 — VWAP/EMA9 research family + Instagram reel interpretation

**Status (2026-10-16): seam 1, PROPOSED. No real-data strategy run has been made.**

This is the first study built on the reusable lab (`src/stratlab`, see `START_HERE.md` at the
repository root). It holds two strategies that are kept apart on purpose:

| Strategy | Origin | Definition |
|---|---|---|
| **VWR family** (VWR0 baseline + VWR1–VWR4) | Lab-defined research strategy | [`manifests/VWR_FAMILY_PROPOSAL_v0.1.md`](manifests/VWR_FAMILY_PROPOSAL_v0.1.md), code `src/stratlab/strategies/vwap_reclaim.py` |
| **IG-AUSTIN-P0** | Provisional interpretation of an Instagram reel by @austin.daytrades (shared by Marc) | [`manifests/SOURCE_RULES_IG_AUSTIN_v0.1.md`](manifests/SOURCE_RULES_IG_AUSTIN_v0.1.md), code `src/stratlab/strategies/instagram_austin_vwap_ema9.py` |

Machine-readable experiment: [`manifests/VWR0_EXPERIMENT_v0.1.toml`](manifests/VWR0_EXPERIMENT_v0.1.toml)
(PROPOSED). It is frozen as v1.0 after review, and only then run.

## Layout (conventions §a)

- `manifests/` — the source rule table and its evidence, the family proposal, and the experiment config.
  Frozen versions are never edited (§b).
- `scripts/` — strategy code lives in the package (`src/stratlab/strategies/`), so it can be reused and
  tested. A run records the code-tree SHA-256 and the git commit (see `scripts/README.md`).
- `exports/runs/<run_id>/` — immutable run directories: `run_record.json`, `metrics.json`, trades,
  session equity and `report.html`.
- `LEDGER.csv` — one row per configuration per run, failures included. The ledger is authoritative (§f).
- `analysis/` — interpretation notes written after a run is reviewed.

## Relationship to the August study

`studies/vwap-lab-2026-08` is preserved unchanged. Its corpus (`a4afaa70…`) is reused by identity.
Its terminal dispositions stand: VDC continuation **NO EDGE FOUND**, FPC worse, MIM and ODR **FAMILY DEAD**.
None of its failed configurations are re-proposed here as new candidates. Its data use makes every
result on this corpus **exploratory** for VWAP/EMA ideas (see the proposal's "prior exposure" section).
