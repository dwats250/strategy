# Candidate-fidelity artifact disposition

Prepared: 2026-07-30 UTC

This is a proposed local cleanup map. It does not authorize a repository
change, deletion, commit, or push.

## Preserve as exploratory lineage

| Current/local item | Correct name | Reason |
|---|---|---|
| v0.5 Pine source | `cuttingboard_direct_path_fidelity_v0_5.pine` | Producing script for the full export |
| `BATS_SPY, 1D.csv` | `CBF05_BATS_SPY1D_V4_bars_20131212-20260728.csv` | Final 3,173-row per-bar export |
| exploratory `README.md` | `EXPLORATORY_CANDIDATE_FIDELITY_v0.5.md` | Avoids collision with the repository root README and states the correct evidence boundary |

Keep these together outside the official frozen study until Claude proposes a
repository destination and Dustin approves it.

## Preserve locally, but do not promote by default

| Item | Disposition |
|---|---|
| `cuttingboard_direct_path_ladder_v0_4.pine` | Retired exploratory source; retain for lineage |
| five `CB_Ladder_v0.4_...csv` files | Retain temporarily until v0.5/full-run custody is settled |
| v0.5 Strategy Tester workbook currently carrying a `.csv` suffix | Rename to `.xlsx`; execution-only artifact with known margin-call contamination |
| final v0.5 chart/table screenshot | Retain as visual configuration evidence if symbol, timeframe, version, and stage are visible |

## Superseded local copies

These are partial-window chart exports and are superseded by the verified
3,173-row export:

- 300-row v0.5 export;
- 558-row v0.5 export.

Do not delete them until the final file hash
`e28aa87468d1922500b119bf02ded470c5528d327edf0bf09d2f124b1448ab8b`
is verified on Dustin's local renamed copy. After verification, they may be
moved to a non-repository local archive or deleted with Dustin's approval.

## Already represented in the closed audit

The seven
`UV02-d2420bc3-SPY-1D-STD-FULL-V{0..6}-ASOF-2026-07-24.csv`
files already have custody records under the closed audit. Do not add duplicate
copies or reopen UV02. Verify local checksums against its ledger before removing
Downloads copies.

## Do not place these directly in the frozen study

Do not drop v0.3, v0.4, v0.5, their Strategy Tester exports, or their notes into
`studies/cuttingboard-asis-proxy/` as if they were official outputs. That study
is bound to a different no-input indicator, frozen mapping, run manifest, and
ledger.

## Missing from the uploaded set

The exact exploratory file currently named `README.md` in Dustin's local
Strategy folder was not available here. The recommended replacement name is:

`EXPLORATORY_CANDIDATE_FIDELITY_v0.5.md`

Claude should inspect its contents before moving or committing it and compare
it with the prepared exploratory findings note.

