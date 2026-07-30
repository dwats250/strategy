# Claude technical onboarding — CuttingBoard candidate fidelity

Prepared: 2026-07-30 UTC

## Your role

Work in Dustin's local `dwats250/strategy` repository as the primary
implementation harness. Begin read-only. The immediate job is to reconcile and
preserve recent TradingView candidate-fidelity artifacts, then execute the
repository's already-frozen AS-IS proxy baseline correctly. This is not
authorization to redesign the research program.

## Mandatory authority and repository boundary

Before proposing any change:

1. Read `CLAUDE.md`, `AGENTS.md`, `docs/conventions.md`, and the current root
   `README.md` completely.
2. Confirm the repository is exactly `dwats250/strategy`, report branch, HEAD,
   origin, working-tree state, and parity with `origin/main`.
3. Treat `dwats250/cuttingboard` as read-only evidence pinned to
   `59f8279d796335149afdec4aa507b6f927233518`. Do not access a mutable
   CuttingBoard working tree and do not mutate CuttingBoard in any way.
4. Do not infer mutation authority from this onboarding. Hold before editing,
   moving, staging, committing, pushing, or opening a PR until Dustin approves
   an exact file plan.

The inspected remote `main` was
`c77cc0c05503fea03624b7bee39a9ed9e45c50f4` on 2026-07-30. Verify locally;
do not assume it remains current.

## Current documented state

- The CuttingBoard engine audit is closed at EA-8.
- EA-9 and every later audit phase are blocked and unexecuted.
- The old TV and UV02 lines are closed. Do not reopen or extend them.
- A separate study now exists at
  `studies/cuttingboard-asis-proxy/`.
- That study is `PACKAGE COMPLETE — NO RUN EXECUTED`.
- Its governing artifacts are:
  - `studies/cuttingboard-asis-proxy/README.md`
  - `studies/cuttingboard-asis-proxy/manifests/RULE_MAPPING_v0.1.md`
  - `studies/cuttingboard-asis-proxy/manifests/RUN_MANIFEST_TEMPLATE_v0.1.md`
  - `studies/cuttingboard-asis-proxy/manifests/FINDINGS_TEMPLATE_v0.1.md`
  - `studies/cuttingboard-asis-proxy/scripts/cuttingboard_asis_proxy_v0_1.pine`
  - `studies/cuttingboard-asis-proxy/LEDGER.csv`
- The frozen Pine baseline has SHA-256:
  `048f5c66eefa3fdb8df9cec882006b1d8cf5fc9772d8694614559ba0a1bce3b5`.

Read all of those files before deciding where any recent artifact belongs.

## What happened outside the frozen study

A separate exploratory TradingView strategy evolved through:

- v0.3: collapsed gate stack and produced almost no useful diagnostic
  separation;
- v0.4: exposed V0–V4 cumulative gate stages;
- v0.5: corrected the price-relative TREND/PULLBACK structure translation and
  exported per-bar diagnostic series.

The v0.5 full chart export is:

`CBF05_BATS_SPY1D_V4_bars_20131212-20260728.csv`

It contains 3,173 daily rows from 2013-12-12 through 2026-07-28. The strategy
evaluation window begins 2015-01-01. All eight regime inputs were available in
the exported window.

Validated v0.5 accounting:

| Item | Count |
|---|---:|
| V2 structure-qualified bars | 602 |
| Both ATR-floor and extension pass | 179 |
| ATR-floor only failure | 103 |
| Extension only failure | 150 |
| Both fail | 170 |
| V4 after kill switch | 170 |
| V4 blocked by an open simulated position | 52 |
| Selected entry attempts | 118 |

The CSV is internally coherent. It also proves that TradingView's chart-data
export includes Pine series declared with `display.data_window`, resolving the
uncertainty recorded in the frozen study README.

## Critical semantic distinction

Do not treat v0.5 as the official AS-IS proxy run.

v0.5 combined the ATR floor and extension check into one hard `directRiskPass`
condition. At the pinned CuttingBoard source, Gates 5–11 are soft gates:

- zero representable soft misses → `QUALIFIED`;
- exactly one representable soft miss → `WATCHLIST`;
- two or more representable soft misses → `REJECT`.

Within the v0.5 export, 239 V2 bars outside the kill switch failed exactly one
of ATR floor or extension. v0.5 suppressed all 239 from V4. They are potential
`WATCHLIST` bars under the actual soft-fail model, subject to the other mapped
soft gates and the recorded Gate 6/Gate 7 floating-boundary uncertainty.

This is the highest-value lesson from v0.5: the TradingView plumbing works and
the gate funnel is observable, but the v0.5 final-candidate count is not a
faithful measure of the full CuttingBoard attention surface.

## Artifact handling

The exploratory artifacts must not be inserted into
`studies/cuttingboard-asis-proxy/` as though they were produced by its frozen
v0.1 script. Their producing script, lifecycle, and claims differ.

Begin by inventorying Dustin's local repository root and Downloads directory.
Propose, but do not perform, a disposition for:

- `cuttingboard_direct_path_fidelity_v0_5.pine`
- `CBF05_BATS_SPY1D_V4_bars_20131212-20260728.csv`
- the exploratory notes currently named `README.md`
- any v0.3/v0.4 Pine files
- five v0.4 Strategy Tester exports
- partial 300-row and 558-row v0.5 chart exports
- the v0.5 Strategy Tester workbook that may still have a `.csv` suffix
- the seven UV02 CSVs already represented in the closed audit's custody
  records

Rename the exploratory `README.md` to:

`EXPLORATORY_CANDIDATE_FIDELITY_v0.5.md`

Do not leave it as a second root `README.md`. Do not commit duplicates of UV02
evidence already in the closed audit. Do not delete any local artifact until
the final full export and hashes are verified.

## Next technical objective

The next official evidence step is the single frozen run already declared by
`studies/cuttingboard-asis-proxy/`, not another edit to v0.5.

1. Verify the frozen v0.1 Pine file hash.
2. Copy and fill the run manifest before capture, using exact TradingView chart,
   session, timezone, provider, adjustment, timestamp, account-plan, and macro
   resolution facts. Use `UNRECOVERABLE` where a fact genuinely cannot be
   established; never guess.
3. Run only the one declared baseline with the unmodified no-input indicator.
4. Export chart data and preserve the required screenshot/table evidence.
5. Verify the exported series include the per-gate fields, `soft_fail_count`,
   `first_rejection`, `qualified`, `watchlist`, and `rejected`.
6. Compute the export SHA-256, add the single authoritative ledger row, and
   draft findings from the frozen findings template.
7. Report counts and representative chronology only.

## Stop conditions

Stop and ask Dustin before:

- modifying a frozen manifest or the frozen v0.1 Pine file;
- creating a new script version or study;
- deciding a permanent repository location for v0.5 exploratory artifacts;
- changing any threshold or gate;
- running variants, other symbols, or other timeframes;
- interpreting profitability, edge, expectancy, or future performance;
- feeding any conclusion back into CuttingBoard;
- staging, committing, pushing, or opening a PR.

## First response requested from Claude

Return only:

1. preflight facts;
2. a short table classifying each local/Downloads artifact as `OFFICIAL
   STUDY`, `EXPLORATORY LINEAGE`, `SUPERSEDED LOCAL COPY`, `ALREADY CUSTODIED`,
   or `UNKNOWN`;
3. exact proposed source and destination paths for files that should move;
4. any missing provenance required before the official frozen run;
5. `HELD FOR DUSTIN FILE-PLAN APPROVAL`.

