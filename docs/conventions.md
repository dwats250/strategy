# Lab conventions

Standing rules for this research lab, learned the hard way across the SPY
ORB first-break campaign. Every study follows these unless a manifest
explicitly and deliberately overrides one, in writing, with a reason.

## a. Study layout

Every study lives in `studies/<study-name>/` with a fixed skeleton:

```
studies/<study-name>/
  README.md
  LEDGER.csv
  manifests/
  scripts/
  exports/
  analysis/
```

`indicators/` at the repo root is a separate thing: live chart tools in
current use, not tied to any one experiment. Don't put experiment scripts
there, and don't put live indicators in a study's `scripts/`.

## b. Manifests are pre-registered, never edited

A manifest is written and frozen *before* data is collected. Once written,
it is never edited in place. Corrections are either:

- a dated amendment appended to the existing manifest text, or
- a new manifest version, with the version **in the filename**
  (`CAMPAIGN_MANIFEST_v2.1.md`, `v2.2.md`, ...).

All prior versions stay in `manifests/` — they are the audit trail for how
and why the design changed, not clutter to be cleaned up.

## c. Scripts are versioned; retired versions are kept

Any script change that can change results (not just comments/formatting)
bumps the version. Retired versions stay in `scripts/` alongside the
current one — they are what makes past runs reproducible and past claims
checkable.

## d. Analysis code is part of the experiment

Analysis code is not a disposable scratch step — it is versioned, committed,
and treated with the same rigor as the manifest and the scripts. A study's
`analysis/` reproduction script should, at minimum:

- assert the headline numbers the study reports, and fail loudly (nonzero
  exit) if they don't reproduce;
- print the package versions it ran under;
- print the checksum of every input file it reads.

`reproduce_campaign.py` is the template for this pattern.

## e. Exports are self-describing and immutable

Export filenames encode what produced them (symbol, cohort, timeframe,
session, exit rule, direction, date range, script version) so a file's name
tells you most of what you need before opening it. Once written, an export
is never modified — a new run producing new numbers gets a new file, not an
edit to an old one.

## f. The ledger is authoritative

`LEDGER.csv` is one row per run. When an export, a chart screenshot, and the
ledger disagree, the ledger wins — it is the record of what was actually run
and under what config, independent of any single artifact's ability to prove
that on its own.

## g. The holdout is frozen forward data

The designated holdout for any hypothesis is forward data collected under a
frozen specification going forward from pre-registration — never a slice of
history that has already been examined. Slicing history after the fact to
manufacture an "out of sample" test does not produce a real holdout.

A historical window held back and inspected only once, under a rule that no
threshold may change afterward, is *better* than an unguarded in-sample fit —
but it is still not a §g holdout. Call it a deferred-inspection window and
state what it can support. Do not call it out of sample.

## h. Audits are not studies

`audits/<audit-name>/` is a sibling of `studies/<study-name>/`, for external
audits of another repository's behavior — where a market backtest is the
instrument, not the object. The object is somebody's code.

An audit is **exempt from the §a study skeleton**. Its shape follows its own
lifecycle — freeze the contract, review it independently, implement, prove
parity, evaluate — which produces `spec/`, `charges/`, `reviews/`, `parity/`,
and `runs/` rather than `manifests/`, `scripts/`, `exports/`, and `analysis/`.
Forcing an audit into the study skeleton would misfile the review record,
which is the part that matters most.

Everything else here still applies, with §b reading across to the audit's
frozen specifications: **an audit's frozen spec documents are never edited in
place.** Post-review corrections are dated amendments or versioned files, same
as a manifest. Frozen documents carry recorded hashes, and a hash mismatch
between what a reviewer examined and what a later stage consumes stops the
later stage.

An audit may produce runs and datasets that look study-like. Its **governing
artifacts stay under `audits/`** regardless — the run is evidence for the
audit, not a study in its own right.

Two further rules follow from an audit's subject being someone else's code:

- **The audited source is read-only evidence, pinned to a commit.** Every
  result carries that SHA. A result may audit the source; it can never mutate
  it, and no parameter, threshold, or conclusion feeds back into it. Changing
  the audited system requires its own separate commission and decision —
  backtest performance alone does not authorize it.
- **Unavailable is not the same as passing.** Where an audit cannot reproduce
  a check honestly, it labels it unavailable and excludes it from the
  arithmetic. Silently treating an unreproducible check as satisfied
  manufactures a result the evidence does not support.
