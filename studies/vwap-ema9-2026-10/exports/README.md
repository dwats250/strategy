# exports

`runs/<experiment_id>__<UTC timestamp>/` — one immutable directory per run, written by
`stratlab run`. The runner refuses to overwrite an existing run directory. Contents:
`run_record.json` (config + hashes + code/data identity), `metrics.json`, `trades/`, `equity/`,
`report.html` (self-contained; opens offline).
