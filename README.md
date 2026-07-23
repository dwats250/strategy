# strategy

A quantitative trading research lab: Pine Script indicators/strategies,
pre-registered studies, and the raw exports/analysis behind them.

## Layout

- `indicators/` — live chart tools in current use, not tied to any one
  experiment.
- `studies/<study-name>/` — one directory per study, each with `README.md`,
  `LEDGER.csv`, `manifests/`, `scripts/`, `exports/`, `analysis/`.
- `docs/conventions.md` — the standing rules for how studies here are
  pre-registered, versioned, and reported.
- `CHECKSUMS_PRE_REORG.txt` — sha256 snapshot of every `.csv`/`.pine` file
  as of the initial reorganization into this layout, for audit purposes.

## Studies

- [`spy-orb-first-break`](studies/spy-orb-first-break/README.md) — SPY
  opening-range first-break event study. **Closed**: no demonstrated edge.
- [`faber-taa-2006`](studies/faber-taa-2006/MANIFEST_v0.1_DRAFT.md) —
  replication of Faber's Tactical Asset Allocation (2006/2007). **Not
  started**; manifest is an unfilled draft pending pre-registration.

See `docs/conventions.md` before adding a new study or amending an existing
manifest.
