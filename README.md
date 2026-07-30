# strategy

A quantitative trading research lab: Pine Script indicators/strategies,
pre-registered studies, and the raw exports/analysis behind them.

## Layout

- `indicators/` — live chart tools in current use, not tied to any one
  experiment.
- `studies/<study-name>/` — one directory per study, each with `README.md`,
  `LEDGER.csv`, `manifests/`, `scripts/`, `exports/`, `analysis/`.
- `audits/<audit-name>/` — external audits of another repository's behavior,
  where a backtest is the instrument and somebody's code is the object.
  Different lifecycle, different skeleton; see `docs/conventions.md` §h.
- `exploratory/<packet-name>/` — clearly-labelled exploratory lineage packets:
  ungoverned diagnostic work retained for reference. Not studies, not audit
  evidence; each packet's README states its own evidence boundary.
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
- [`cuttingboard-asis-proxy`](studies/cuttingboard-asis-proxy/README.md) —
  frozen, no-tuning proxy for what the present `dwats250/cuttingboard` gate
  semantics surface on declared TradingView chart history, pinned to
  `59f8279d`. **Package complete, no run executed.** Not a CuttingBoard replay,
  not a parity artifact, and makes no profitability claim.

## Audits

- [`cuttingboard-engine-strategy-audit`](audits/cuttingboard-engine-strategy-audit/README.md)
  — audit of the `dwats250/cuttingboard` decision engine, pinned to commit
  `59f8279d`. CuttingBoard is read-only evidence and is never modified or fed
  parameters. Makes no alpha or future-performance claim.

  **Current lifecycle.** The TV-0 → TV-4 Pine-proxy line is closed: TV-0 and
  TV-0R are complete, TV-1's commission is withdrawn, and TV-1R/TV-2/TV-3/TV-4
  were never commissioned — see
  [`closure/TV-LINE-CLOSURE-2026-07-27.md`](audits/cuttingboard-engine-strategy-audit/closure/TV-LINE-CLOSURE-2026-07-27.md)
  and
  [`closure/UV02-CLOSURE-2026-07-27.md`](audits/cuttingboard-engine-strategy-audit/closure/UV02-CLOSURE-2026-07-27.md).
  The successor EA engine-audit line is framed by
  [`engine/charters/EA-0-COMMISSION.md`](audits/cuttingboard-engine-strategy-audit/engine/charters/EA-0-COMMISSION.md),
  which authorizes no EA phase; its full program is
  [`plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](audits/cuttingboard-engine-strategy-audit/plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md).
  Phases EA-1 through EA-8 were each separately authorized and executed, and the
  program **closed at EA-8** — see
  [`EA-AUDIT-CLOSEOUT.md`](audits/cuttingboard-engine-strategy-audit/EA-AUDIT-CLOSEOUT.md).
  **EA-9 and every later phase are blocked and unexecuted.** The audit established
  no strategy-quality, profitability, or real-market claim and no basis for fitting
  or optimization.

  Status lines inside frozen TV-0 documents record what was true when those
  documents were frozen; current lifecycle state lives in `closure/`.

See `docs/conventions.md` before adding a new study or amending an existing
manifest.
