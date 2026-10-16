# vwap-mr-2026-10 — VMR-L VWAP mean reversion

**Status (2026-10-16): PROPOSED, awaiting the strategy-definition review. No real-data run.**

The second family on the reusable lab, and its reuse demonstration: it needed a strategy module
(`src/stratlab/strategies/vwap_mean_reversion.py`), a new indicator module (`src/stratlab/volatility.py`)
and a config. Nothing in the engine, runner, metrics or report changed.

- Proposal and research card: [`manifests/VMRL_FAMILY_PROPOSAL_v0.1.md`](manifests/VMRL_FAMILY_PROPOSAL_v0.1.md)
- Machine config (PROPOSED; refuses real data): [`manifests/VMRL_EXPERIMENT_v0.1.toml`](manifests/VMRL_EXPERIMENT_v0.1.toml)
- Trade-blind displacement distribution used to declare K: `analysis/excursion_quantiles.py`, output
  `analysis/EXCURSION_QUANTILES_2026-10-16.json.txt`
- Tests: `tests/test_mean_reversion.py` (synthetic rules, plus an end-to-end run through the unchanged runner and report)

Layout follows conventions §a. `LEDGER.csv` gets one row per configuration once a frozen config is run.
