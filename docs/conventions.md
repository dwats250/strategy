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

**Amendment 2026-07-30 — trial budget (adopted from gap register G-03).** Every future run
manifest, campaign manifest, and probe pre-registration records `trials_planned` — the number of
independent configurations committed before the first run, the one quantity that cannot be
reconstructed afterward — and `dsr_threshold_implied`, the observed performance needed at that N
and sample length. Frozen templates and existing ledgers are not retrofitted; new templates and
new ledger columns carry both fields.

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

**Amendment 2026-07-30 — embargo (adopted from gap register G-04).** A deferred-inspection
window is separated from the fitted window by an embargo of at least the longest indicator
lookback the strategy uses (for EMA50/ATR14 on daily bars, on the order of 50 trading days). A
zero-gap boundary leaks fitted indicator state into the inspection window, and the leak is
indistinguishable from look-ahead in results.

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

## i. Cross-repository isolation

This section is binding on every agent and every session. `CLAUDE.md` and
`AGENTS.md` at the repository root carry the rule in brief and point here for
the complete text.

### The rule

> When operating under this repository or any CuttingBoard audit charge, an
> agent may mutate only `dwats250/strategy`. The repository
> `dwats250/cuttingboard`, every local CuttingBoard checkout, and every
> CuttingBoard remote are read-only evidence sources. Possession of credentials
> capable of writing to CuttingBoard does not grant authority to use them. No
> agent may create, update, delete, push, merge, comment, dispatch, configure,
> or otherwise mutate any CuttingBoard file, ref, branch, pull request, issue,
> review, workflow, release, setting, or remote. If the work appears to require
> a CuttingBoard mutation, stop and request a separate Dustin-authorized
> CuttingBoard charge in a separate session rooted in that repository.

### No back-feeding

> Results from this audit may become evidence for a later independent
> CuttingBoard review. They do not authorize refactoring, issue creation,
> parameter changes, documentation changes, or any other back-feed into
> CuttingBoard.

### Capability is not authorization

The credentials available in a session may technically permit writes to
CuttingBoard. That is a fact about the key, not a grant of permission. The
authorization boundary is this document, not what the token happens to allow.
An action is authorized because a charge permits it — never because it
succeeded.

### Explicit targets only

Every GitHub or connector mutation must supply its repository target
explicitly, and that target must be exactly `dwats250/strategy`. A missing,
inferred, defaulted, or ambiguous target is a STOP condition, not something to
resolve by guessing. A CuttingBoard target is a STOP condition outright.

### Reading CuttingBoard evidence

CuttingBoard may be read **only at the pinned source SHA**. Prefer immutable
remote content or commit-addressed evidence
(`git show <pinned-sha>:<path>`).

If a local checkout is consulted, use read-only inspection only. Do **not**
fetch, checkout, switch, branch, stash, commit, reset, merge, rebase, push,
modify remotes, or run any command that changes its Git metadata or working
tree. A local checkout is typically ahead of the pin and often dirty; reading
its working tree silently substitutes unpinned code for pinned evidence, which
is an evidence-integrity failure even though nothing was written.

### Mandatory session preflight

Every TV-0R, TV-1, and TV-1R session reports all of the following **before**
acting:

1. `pwd -P`
2. Resolved Git repository root
3. Exact `origin` URL
4. Current branch and HEAD
5. Working-tree status
6. Sole authorized mutation target: `dwats250/strategy`
7. Forbidden mutation target: `dwats250/cuttingboard`

**If the working repository or remote is not exactly `dwats250/strategy`,
STOP.** Do not switch repositories or branches to make the preflight pass —
report the mismatch and wait for Dustin.

### Development boundary — amendment 2026-07-30

The audit that motivated this section closed at EA-8. For CuttingBoard development going
forward, Dustin adopts the **hybrid** boundary
(`docs/owner-decisions-2026-07-30.md`; options analyzed in
`docs/engine-program-draft-2026-07-29.md` §C):

1. Development happens on a Dustin-owned **fork** of CuttingBoard. That fork is the sole
   authorized mutation target of development charges rooted in it — in separate sessions, never
   from this repository. `dwats250/cuttingboard` itself, its refs and PRs, and the audited pin
   `59f8279d…` remain read-only, commit-addressed evidence exactly as above.
2. Anything touching the audited pin's evidentiary record stays under the per-change charge
   rule (Option 1) — one explicit Dustin-authorized charge per change.
3. **No back-feeding is unchanged and now explicit for the lab:** any change derived from audit
   evidence — including this repository's studies and analyses — requires its own explicit
   Dustin commission naming that derivation, regardless of where the change lands.
4. Merge-back from the fork into production CuttingBoard is itself a governance event requiring
   its own explicit authorization; it is never implied by work having been done on the fork.

For sessions rooted in this repository nothing changes: `dwats250/strategy` remains the only
authorized mutation target, and the fork joins `dwats250/cuttingboard` on the forbidden list
until a charge rooted in the fork says otherwise.

**Interface companion — 2026-07-30.** Cross-repository interface conduct (what may cross, the
required labels, and the probe/observation/observability paths) is specified in
`docs/INTERFACE_CHARTER_v0.1.md`. On any conflict, this section controls.
