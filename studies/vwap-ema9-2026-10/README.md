# vwap-ema9-2026-10 — VWAP/EMA9 research family + Instagram reel interpretation

**Status (2026-10-16): seam 2.** Configurations frozen before any real-data run, then run once each.
**The data ends 2026-08-21.** Nothing here is October-current.

This is the first study built on the reusable lab (`src/stratlab`; see `START_HERE.md` at the
repository root). It holds three things, kept apart on purpose:

| Configuration | Origin | Frozen definition |
|---|---|---|
| **VWR family** (VWR0 baseline + VWR1–VWR4, plus the VWR0 raw-corpus rerun) | Lab-defined research strategy | [`manifests/VWR_FAMILY_v1.0.md`](manifests/VWR_FAMILY_v1.0.md), code `src/stratlab/strategies/vwap_reclaim.py` |
| **IG-AUSTIN-P0** | Provisional, underlying-only interpretation of an Instagram reel by @austin.daytrades (shared by Marc) | [`manifests/SOURCE_RULES_IG_AUSTIN_v1.0.md`](manifests/SOURCE_RULES_IG_AUSTIN_v1.0.md), code `src/stratlab/strategies/instagram_austin_vwap_ema9.py` |
| **SPY-SESSION-HOLD** | Benchmark, not a trial | `VWR_FAMILY_v1.0.md`, code `src/stratlab/strategies/benchmarks.py` |

Runnable frozen configs: [`manifests/VWR0_EXPERIMENT_v1.1.toml`](manifests/VWR0_EXPERIMENT_v1.1.toml) and
[`manifests/VWR0_RAW_ROBUSTNESS_v1.1.toml`](manifests/VWR0_RAW_ROBUSTNESS_v1.1.toml), pinned to the code
tree. The v1.0 TOMLs carry a placeholder hash and are never run (see the dated amendment in
`VWR_FAMILY_v1.0.md`). The v0.1 files are the seam-1 proposal record.

## Layout (conventions §a)

- `manifests/`: source rule tables and evidence, family definitions, experiment configs. Frozen versions
  are never edited (§b); corrections are dated amendments or new versions.
- `scripts/`: strategy code lives in the package. See `scripts/README.md` for the written §c override and
  the enforced code-tree pin.
- `exports/runs/<run_id>/`: immutable run directories (`run_record.json`, `metrics.json`, trades, session
  equity, `report.html`).
- `LEDGER.csv`: one row per configuration per run, failures included. The ledger is authoritative (§f).
- `analysis/`: `reconcile_run.py`, which asserts the reconciliation (§d), and the interpretation notes.

## Relationship to the August study

`studies/vwap-lab-2026-08` is preserved unchanged, and its corpus (`a4afaa70…`) is reused by identity. Its
terminal dispositions stand, and none of its failed configurations is re-proposed. Its use of the same
data makes every result here **exploratory** for VWAP/EMA ideas.
