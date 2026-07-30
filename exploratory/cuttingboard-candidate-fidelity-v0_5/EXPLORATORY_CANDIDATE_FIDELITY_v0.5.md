# Exploratory Candidate Fidelity v0.5

Status: `EXPLORATORY LINEAGE — NOT THE FROZEN AS-IS PROXY RUN`

Prepared: 2026-07-30 UTC

## Purpose

Record what the separate v0.5 TradingView strategy established before the
repository's frozen `cuttingboard-asis-proxy` baseline is executed. This file
must not be read as an amendment to the closed engine audit or as a result from
the frozen AS-IS proxy study.

## Artifact identity

| Artifact | SHA-256 |
|---|---|
| `cuttingboard_direct_path_fidelity_v0_5.pine` | `3136a812c285878d416490f25dfbb62110fb39a863e47b34ef23b495d1b75726` |
| `CBF05_BATS_SPY1D_V4_bars_20131212-20260728.csv` | `e28aa87468d1922500b119bf02ded470c5528d327edf0bf09d2f124b1448ab8b` |

CSV coverage: 3,173 daily rows, 2013-12-12 through 2026-07-28.
Evaluation begins 2015-01-01.

## What the export established

| Funnel point | Count |
|---|---:|
| V2 structure-qualified candidates | 602 |
| Both direct-risk checks pass | 179 |
| ATR-floor only failure | 103 |
| Extension only failure | 150 |
| Both fail | 170 |
| V4 after kill-switch exclusion | 170 |
| Blocked only by an open simulated position | 52 |
| Selected entry attempts | 118 |

Additional checks:

- all eight market-state inputs were available on every exported row;
- 125 V4 candidates were long-direction and 45 were short-direction;
- the kill switch removed 9 of the 179 both-pass candidates;
- candidate accounting reconciles exactly;
- TradingView exported the script's `display.data_window` diagnostic series;
- Strategy Tester execution artifacts do not equal candidate counts.

## The important correction

v0.5 used:

`ATR-floor pass AND extension pass`

as a mandatory combined candidate condition.

The pinned CuttingBoard semantics instead treat the representable Gates 5–11
as soft gates: one miss is `WATCHLIST`; two or more misses are `REJECT`.

In this export:

- 239 non-kill V2 bars missed exactly one of ATR floor or extension;
- 170 non-kill V2 bars missed both.

Therefore, v0.5 correctly describes its own strict funnel but under-surfaces
the broader CuttingBoard attention stream. The 239 single-miss bars are
potential watchlist cases, subject to the other mapped soft gates and the
known Gate 6/Gate 7 floating-boundary uncertainty.

2017 illustrates the distinction:

| Item | Count |
|---|---:|
| V2 bars | 51 |
| Both checks pass / v0.5 V4 | 0 |
| Exactly one check fails outside kill switch | 23 |
| Both fail outside kill switch | 28 |

The year was not upstream-dead. v0.5 reported zero final candidates because it
required both soft checks to pass.

## What remains useful

- The structure repair is mechanically testable and produced coherent output.
- The export path and long-history chart loading procedure work.
- Per-bar gate diagnostics are much more useful for fidelity than List of
  Trades.
- The v0.5 file is valuable exploratory lineage and a regression reference.

## What this artifact cannot establish

- the official frozen proxy's `QUALIFIED`, `WATCHLIST`, and `REJECT` counts;
- parity with a live CuttingBoard run;
- the accepted option-chain path;
- profitability, edge, expectancy, or future performance;
- a basis for threshold fitting or a CuttingBoard change.

## Next step

Execute the existing frozen
`studies/cuttingboard-asis-proxy/scripts/cuttingboard_asis_proxy_v0_1.pine`
baseline once, under its pre-capture manifest, and inspect its full per-gate
export. Do not change v0.1 or tune anything first.

