# scripts

Strategy code for this study lives in the lab package so that it is tested and reusable:

- `src/stratlab/strategies/vwap_reclaim.py` — VWR family (lab-defined)
- `src/stratlab/strategies/instagram_austin_vwap_ema9.py` — IG-AUSTIN-P0 (provisional interpretation)

Versioning (conventions §c): a change that can alter results gets a NEW strategy class or module
(e.g. `VwapReclaimV2`); the old one stays. Each run records the git commit and the SHA-256 of the
whole `src/stratlab` tree in `run_record.json`, so any past run can be checked out and re-run.
