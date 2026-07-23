# SPY ORB First-Break Study

Experimental record for the SPY opening-range first-break event study.
Everything here is **exploratory**. No result has been validated out of
sample. The designated holdout is forward paper trading under a frozen
specification; no slice of the historical data serves that role.

## Contents

- `RESULTS_LEDGER.csv` — one row per run.
- `ORB-T0_SPY_*_trades-*.csv` — raw TradingView List-of-Trades exports.

## Provenance — what the files can and cannot prove

Order comments (`C4|L|MKT|15`) identify cohort, direction, entry style
and timeframe per row. They do **not** carry symbol, OR duration,
cutoff, EMA/RVOL parameters, scored window, chart-hours setting, or
costs. Pre-v0.3.0 exports were re-identified from comments **plus the
known run history in conversation**; the comment alone is insufficient,
and the ledger is the required companion record. v0.3.0 adds script
version and ticker to the comment and all result-changing parameters to
the on-chart fingerprint, narrowing — not closing — this gap. The
ledger, not the export, is the authoritative record.

Filenames use `trades-<first>_<last>`: the first and last **accepted
fill**, not the scored window. For filtered cohorts these differ —
C4/C5 ending 2026-06-25 means no later event passed the filter, not
that scoring stopped. Loaded-bar ranges were not recorded pre-v0.3.0
and are marked as such in the ledger.

## Costs

All v0.2.x results are **net of 1 tick/order emulator slippage**
(~0.31 bps per round trip at these prices) with $0 commission — not
gross, despite the earlier table label. v0.3.0 sets slippage to zero;
its results are gross and belong to a new ledger generation. Do not mix
generations in one comparison.

## Configuration held constant (all runs so far)

SPY (AMEX), standard candles · 15-minute opening range · trigger window
closes 60 min after the open · first confirmed close outside the
completed range · max one event/session, no re-entry · market entry at
next bar open · time exit only, 30 min after fill · no stop/target/
trail · direction Both · EMA 9/20, chop 6 · RVOL 20-session same-slot,
min 10 real samples, hot ≥ 1.5x, common-population gate ON.

## Cohorts — parallel filters, not a ladder

| | Filter | Empirical relation (this sample) |
|---|---|---|
| C0 | none (baseline) | n=318 |
| C1 | VWAP-aligned | **= C0 exactly; rejected 0/318.** Structural during the first hour (session VWAP averages prices inside the range a first break just cleared), and empirically non-discriminating in this sample. |
| C2 | EMA-aligned | 59% retained; accepted-vs-rejected lift −0.01 bps |
| C3 | EMA-stable (⊂ C2) | 31% retained; worse than C0 |
| C4 | RVOL-hot (independent) | 16% retained; see below |
| C5 | C3 ∩ C4 (since C1 = C0) | 17 events, 3 long / 14 short; top-5 winners = 85.9% of gross profit. Unusably sparse and imbalanced. |

## Findings to date

**Primary test (C0, Both, 15m, TX30, n=318): no demonstrated edge.**
Mean −1.20 bps (net of slippage; ≈ −0.89 gross), t = −0.84, monthly-
block bootstrap CI [−3.66, +1.56]. Max |t| across all six cohorts: 0.84.

**C4 (RVOL) selected dispersion, not direction.** Mean +1.08 bps at
n=50; accepted-vs-rejected lift +2.71 bps, CI ≈ [−6.8, +12.2]; top-5
winners = 49.5% of gross profit; mean ex-top-5 = **−5.12 bps**; MFE/MAE
rose from +0.181%/−0.188% (C0) to +0.322%/−0.238%. RVOL is literature-
motivated (Stocks-in-Play is cross-sectional stock selection; this is
single-symbol time-series RVOL — related idea, different object), and
the current evidence says "more activity and wider outcomes," not
"directional edge." Any later RVOL investigation is a separately
pre-registered experiment.

**Statistics notes.** `ci_halfwidth_bps` is the 95% CI half-width
(1.96·SE) — the smallest observed effect that would reach |t|≈2, **not**
a minimum detectable effect. A properly powered MDE (80% power, 5%
two-sided) is (1.96+0.84)·SE ≈ 1.43× larger: at n=318, ≈4.0 bps.
Earlier "trades needed for t=2" figures were implicitly ~50%-power
detection thresholds; ~2× more trades are needed at 80% power. The
monthly block bootstrap (~19 blocks) is a sensitivity check, not proof
of independence.

**Validation scope.** The 124-trade ETH-on/off identity validates
session anchoring for the active C0 order path only — not the EMA,
RVOL, or dormant-cohort calculations.

**Open ledger items (post hoc, prospectively testable, NOT filters):**
the 0-for-11 5m-only failed-break sessions; the 4 direction-flip
sessions; the +1.4 bps 10:30-slot cell (n=40, smallest cell, noted as
a trap).

## Remaining pre-registered work

Horizon sweep: C0 at TX15 / TX30 / TX60 under v0.3.0 (TX30 re-run
because the slippage change starts a new ledger generation). After
that, the pre-registered plan is exhausted; anything further is a new
hypothesis and gets written down before being run.
