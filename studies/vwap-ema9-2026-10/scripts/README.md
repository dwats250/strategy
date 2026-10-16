# scripts

Strategy code for this study lives in the lab package so that it is tested and reusable:

- `src/stratlab/strategies/vwap_reclaim.py` — VWR family (lab-defined)
- `src/stratlab/strategies/instagram_austin_vwap_ema9.py` — IG-AUSTIN-P0 (provisional interpretation)

## Script versioning (conventions §c) — written override

§c asks that retired script versions stay in `scripts/`. This study **overrides that by design**
(allowed by the conventions preamble: "a manifest explicitly and deliberately overrides one, in
writing, with a reason"). The reason: strategy code shares tested modules (engine, sessions,
indicators, metrics), and copying single files would not reproduce a run. Copying only the strategy
module would give false confidence.

What replaces it, and is enforced in code:

1. A FROZEN experiment config pins `code_tree_sha256`, a SHA-256 over every file under
   `src/stratlab/`, including the report template. Get it from `uv run stratlab identity`.
2. `stratlab run` refuses a real-data run unless the config is `status = "FROZEN"`, the current tree
   hash equals the pinned one, and `src/` has no uncommitted changes.
3. Each run records the git commit and tree hash in `run_record.json` and `LEDGER.csv`. Any past run
   is reproduced by checking out that commit; the tree hash proves it is the same code.
4. A rule change that can alter results gets a new class or parameter value, plus a new frozen config.
   Old classes stay importable while any frozen config references them.
