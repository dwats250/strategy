# Audit runs

One directory per run. Every run is preserved through a manifest.

Nothing here yet — runs begin at TV-3, after TV-0R acceptance, TV-1 implementation, and TV-2
parity.

## What a run must preserve

A run is not preserved unless it has **both** of:

1. the **full simulated trade ledger** — every trade, not a summary;
2. a **run manifest** — enough to identify exactly what produced that ledger.

Screenshots and summary tables are supplementary. They never substitute for either. When a
screenshot, an export, and the manifest disagree, the manifest and ledger are authoritative —
the same principle as `LEDGER.csv` in the studies.

## Required manifest fields

From [`../spec/BACKTEST_PROTOCOL.md`](../spec/BACKTEST_PROTOCOL.md):

- CuttingBoard source SHA (`59f8279d796335149afdec4aa507b6f927233518` for this study)
- Pine source SHA-256
- Pine version
- Run timestamp
- SPY chart symbol, timeframe, timezone, and session setting
- **All** cross-symbol IDs actually used
- Variant (`V0`–`V6`)
- Date window
- Every threshold
- Commission and slippage
- Missing-data counts
- Known parity exceptions
- Raw export filenames

Every result carries the pinned CuttingBoard SHA and the Pine source hash. A result that
cannot name the code that produced it is not evidence.

## Required ledger contents

Per the protocol: signal date and next-open fill date; direction, variant, entry, stop,
target, and signal ATR; every gate boolean; first rejection gate and all rejection gates;
regime, posture, confidence, net score, and vote coverage; structure label and derived inputs;
the missing-data mask; exit reason and the ambiguous-intrabar flag; gross and
friction-adjusted return; MFE/MAE where available; cumulative gate rejection counts; and the
incremental deltas from each prior variant.

## Rules

- **Runs are immutable once written.** A re-run producing new numbers is a new run directory,
  never an edit to an old one. This mirrors `docs/conventions.md` §e.
- **Raw vendor files are not duplicated here.** Reference them by manifest and checksum. See
  [`../data/README.md`](../data/README.md).
- **Friction scenarios are recorded, not chosen.** `PARITY`, `BASE`, and `STRESS` all run;
  headline comparisons show both frictionless signal behavior and the base-friction result.
- **No threshold changes between variants.** Every variant runs from the same source and
  produces a `variant_id`. Separate scripts with drifting formulas are forbidden.
- **The out-of-sample window may be inspected only after TV-2 parity acceptance,** and no
  threshold may change after it is inspected.

## Terminology constraint

Pending TV-0R adjudication of declared finding **D-1** — see
[`../charges/TV-0R-INDEPENDENT-REVIEW.md`](../charges/TV-0R-INDEPENDENT-REVIEW.md) — no run
report, manifest note, or summary may describe the 2022-01-01 → 2026-07-24 historical window
as a genuine forward holdout under `docs/conventions.md` §g. It is a deferred-inspection
historical slice with guard conditions. That is a weaker claim, and it is the one the evidence
supports.
