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
