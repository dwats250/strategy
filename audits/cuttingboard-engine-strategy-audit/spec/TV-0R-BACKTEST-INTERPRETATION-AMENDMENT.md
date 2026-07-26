# TV-0R Backtest Interpretation Amendment — 2022–2026 Window

Status: `ACTIVE NARROW INTERPRETATION CORRECTION`

Created: 2026-07-26

Authorized by:
[`../adjudications/TV-0R-DUSTIN-ADJUDICATION.md`](../adjudications/TV-0R-DUSTIN-ADJUDICATION.md)
finding F-1, adjudicated by Dustin.

## Scope

This amendment corrects **terminology and the claims that terminology licenses**, for
**one period only**: 2022-01-01 through 2026-07-24, as designated in
[`BACKTEST_PROTOCOL.md`](BACKTEST_PROTOCOL.md) § *Predetermined study windows*.

It changes nothing else. The frozen protocol remains byte-for-byte unedited and
governs everywhere this amendment is silent.

## The correction

1. **The 2022-01-01 – 2026-07-24 period is a `deferred-inspection descriptive
   window`.** That is its name in this project from this point forward.

2. **It is not a forward out-of-sample holdout.** Under `docs/conventions.md` §g, a
   holdout is forward data collected under a frozen specification going forward from
   pre-registration. This period is a slice of history that already existed when the
   specification was written, so it cannot be one.

3. **Any contrary "out-of-sample" or "forward holdout" reading of the frozen protocol
   is superseded — only to that extent.** Specifically, the phrase "Untouched
   out-of-sample window" in `BACKTEST_PROTOCOL.md` § *Predetermined study windows* is
   to be read as naming a deferred-inspection descriptive window. No other line, rule,
   window, threshold, variant, export, or acceptance criterion in that document is
   altered, relaxed, or reinterpreted.

4. **This correction makes no claim about performance, alpha, tradability, or future
   outcomes.** It is a naming and evidentiary-strength correction. It says nothing
   about what the study will find, and it neither strengthens nor weakens any result.

## What is unchanged

The protocol's guard conditions on this window are **retained in full and remain
binding**:

- the window may be inspected only after TV-2 parity acceptance;
- no threshold may change after it is inspected;
- a provider with later history does not justify silently shortening the sample, and
  affected bars must carry a data-availability flag.

These guards are what make the window meaningfully stronger than an unguarded
in-sample fit. They are not what would make it a holdout, and retaining them is not a
claim that it is one.

The other three predetermined windows — the 2015 warm-up observation, the 2016–2021
in-sample descriptive window, and the 2016–2026 combined descriptive window — are
untouched.

## What this window can and cannot support

**Can support.** Descriptive statements about how the reproducible gate families
behaved over a period that was held back from inspection until after parity was
accepted, under a rule freezing thresholds at the moment of inspection.

**Cannot support.** Any claim of genuine out-of-sample validation, forward
generalization, predictive validity, alpha, or expected future performance. Deferred
inspection reduces the opportunity for fitting; it does not create data the
specification could not have seen.

## Standing constraint

**No document, commit message, report, summary, chart annotation, export filename, or
run manifest produced by this project may describe the 2022–2026 historical slice as a
genuine forward holdout or as out-of-sample.** This constraint was already in force
under the TV-0R charge's D-1 declaration and `docs/conventions.md` §g; this amendment
records its resolution and keeps it in force.

Where a later artifact needs a short label, use `deferred-inspection descriptive
window`.
