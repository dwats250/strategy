# TV-0R — Independent Semantic Review of the Frozen TV-0 Contract

Status: CHARGED — NOT STARTED

Reviewer: fresh-context Sol / GPT-5.6. Not the session that authored TV-0, and not the
session that installed this scaffold.

## Authority and boundary

- Source evidence: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`
- CuttingBoard mutation permission: **NONE**
- File edit permission: **NONE** — this reviewer reports findings; it does not apply them
- Merge permission: **NONE**

This review may audit CuttingBoard. It may not mutate CuttingBoard, and no finding here
authorizes a CuttingBoard change. Backtest performance alone cannot authorize an engine
change; this review sees no performance results at all.

## Mandatory repository preflight

Report all of the following **before** acting:

1. `pwd -P`
2. Resolved Git repository root
3. Exact `origin` URL
4. Current branch and HEAD
5. Working-tree status
6. Sole authorized mutation target: `dwats250/strategy`
7. Forbidden mutation target: `dwats250/cuttingboard`

**If the working repository or remote is not exactly `dwats250/strategy`, STOP.** Do not
switch repositories or branches to make the preflight pass — report the mismatch and wait
for Dustin.

This reviewer edits nothing in any repository, so the boundary matters here for evidence
integrity rather than write safety: a session rooted in the wrong repository will cite the
wrong source. See `docs/conventions.md` §i.

## Preconditions

Do not begin until all hold:

1. The scaffold PR is open and its document inputs are stable.
2. The four TV-0 documents hash-match `../INSTALLATION_RECORD.md`. A mismatch means the
   frozen contract drifted — **stop and report** rather than reviewing drifted text.
3. The pinned CuttingBoard commit resolves.

## Inputs

- `../README.md`
- `../spec/GATE_TRANSLATION_MATRIX.md`
- `../spec/BACKTEST_PROTOCOL.md`
- `TV-1-PINE-IMPLEMENTATION.md`
- The pinned CuttingBoard SHA and read-only access to the pinned source
- `../spec/DATA_PROVENANCE_CONTRACT.md` — **for boundary and provenance review only**; it
  is a draft and is not part of the frozen contract
- `../INSTALLATION_RECORD.md` — for the approved path correction and declared deviations

**No performance results.** No backtest output, trade ledger, equity curve, or return
statistic may enter this review. There are none to supply; do not seek them.

### Reading pinned source

Read pinned evidence with `git show 59f8279d796335149afdec4aa507b6f927233518:<path>`.

Do **not** read the working tree of any local CuttingBoard clone. The known local clone is
ahead of the pin with uncommitted changes; reading it would silently substitute unpinned
code for pinned evidence and invalidate every citation in this review.

Read-only inspection only. Do not fetch, checkout, switch, branch, stash, commit, reset,
merge, rebase, push, modify remotes, or run any command that changes a CuttingBoard
checkout's Git metadata or working tree. Prefer immutable remote content or
commit-addressed evidence.

## Review questions

1. Is the gate inventory complete for the declared direct-path scope?
2. Does each formula, threshold, comparison operator, priority rule, and missing-data
   behavior match pinned source?
3. Are the `EXACT_FORMULA`, `FORMULA_EXACT_DATA_PROXY`, `CURRENTLY_INERT`,
   `EXECUTION_PROXY`, `EXCLUDED_EXTERNAL`, `EXCLUDED_OPERATIONAL`, and `DEFERRED_PATH`
   classifications defensible?
4. Are the seven semantic hypotheses properly derived and testable?
5. Are completed-bar, next-open, session, adjustment, and cross-symbol assumptions
   explicit and honest?
6. Can the proposed Pine implementation repaint, leak future data, or accidentally treat
   unavailable gates as passing?
7. Do the incremental variants isolate gate-family effects without changing thresholds?
8. Are the required exports sufficient for later offline reproduction?
9. Does any language overclaim CuttingBoard parity, options profitability, or future
   performance?
10. Does the separation from CuttingBoard prevent back-feeding?

## Declared inputs requiring adjudication

These were identified during repository organization. They are handed to the reviewer as
declared questions, not as pre-adjudicated findings. **No TV-0 document was edited to
address them** — TV-0 is frozen for this scaffold packet.

### D-1 — Holdout terminology conflict (treat as potentially `BLOCKING`)

`spec/BACKTEST_PROTOCOL.md` designates 2022-01-01 through 2026-07-24 as an "untouched
out-of-sample window."

This repository's standing convention, `docs/conventions.md` §g, states that the designated
holdout for any hypothesis is *forward data collected under a frozen specification going
forward from pre-registration* — and explicitly that "slicing history after the fact to
manufacture an 'out of sample' test does not produce a real holdout."

The 2022–2026 window is a slice of already-existing history. The protocol does guard it
(inspect only after TV-2 parity acceptance; no threshold may change after inspection), which
is meaningfully stronger than an unguarded in-sample fit. It is nonetheless not a §g holdout.

Assess:

- whether the protocol's language overclaims what a historical slice can establish
  (this bears directly on review question 9);
- whether the guard conditions are sufficient for the descriptive claims the study actually
  makes, given that the study disclaims alpha and future-performance claims;
- the smallest sufficient correction — the expected shape is terminology, not redesign
  (for example, naming it a *deferred-inspection descriptive window* rather than a holdout,
  and stating what it can and cannot support).

**Until this is adjudicated and dispositioned, no document, commit message, report, or
summary produced by this project may describe the 2022–2026 historical slice as a genuine
forward holdout under this repository's convention.** This constraint is already in force.

### D-2 — TV-1 companion-repository path correction

`TV-1-PINE-IMPLEMENTATION.md` names a separate `cuttingboard-gate-lab` companion repository;
the primary charge names the existing `strategy` repository as the writable target. Dustin
approved treating `strategy` as the companion repository, recorded as a binding path-only
correction in `../INSTALLATION_RECORD.md`.

Confirm the correction changes only repository paths and does not widen TV-1's change
surface, relax its CuttingBoard-mutation ban, or weaken its no-merge rule.

### D-3 — Residual credential capability

Disposition: `KNOWN RESIDUAL CAPABILITY — GOVERNED BY EXPLICIT DENY RULE`

The factual observation stands: the operator's GitHub credentials carry write access to
`dwats250/cuttingboard`, and no technical barrier prevents a write.

Since this finding was first raised, that capability has been bound by an explicit deny rule
rather than procedural convention alone — `docs/conventions.md` §i, carried in brief in the
root `CLAUDE.md` and `AGENTS.md`, with the mandatory repository preflight and STOP condition
now imposed on every TV-0R, TV-1, and TV-1R session.

Assess whether that binding is sufficient: whether the rule's prohibited-operation list is
complete, whether the preflight would actually catch a misrooted session, and whether any
gap remains between what the credential can do and what the rule forbids.

**Out of scope for this review:** the credential itself. Do not propose rotating, scoping,
restricting, or inspecting Dustin's keys, tokens, remotes, GitHub settings, or Claude
permission settings. The question is whether the governing rule is adequate, not how the key
is provisioned.

## Output contract

Classify every finding as exactly one of:

- `BLOCKING` — TV-1 must not begin until resolved
- `NON-BLOCKING` — should be corrected, does not gate implementation
- `QUESTION` — needs a Dustin decision, not a reviewer judgment

Every finding must include:

1. **Exact document location** — file and section or table row.
2. **Exact pinned-source evidence** where applicable — file path and the specific
   construct at the pinned SHA. Assertions about engine behavior without a pinned-source
   citation are not findings.
3. **Consequence** — what goes wrong if it stands.
4. **Smallest sufficient correction** — the minimal change that resolves it. Not a redesign.

Report "no finding" explicitly where a review question is satisfied. Silence is not
evidence of review.

## Reviewer prohibitions

The reviewer may **not**:

- edit any file;
- write Pine;
- tune or propose thresholds;
- propose CuttingBoard refactoring;
- expand the audit beyond the declared direct path;
- review performance; or
- begin a review of its own review.

## After the review

1. Opus prepares **one** adjudication table: finding, classification, proposed disposition.
2. **Dustin approves the dispositions.** The reviewer does not self-adjudicate, and the
   adjudicator does not overrule a `BLOCKING` finding without a recorded reason.
3. At most **one bounded correction pass** is applied to the TV-0 documents. Corrections are
   appended amendments or versioned files per `docs/conventions.md` §b — never silent
   in-place edits to frozen text.
4. Re-hash the corrected documents and record the new hashes in `../INSTALLATION_RECORD.md`.
5. TV-0 is then **frozen for TV-1**.

No recursive review loops. This review gets exactly one bounded correction pass.

Review output and the adjudication table land in `../reviews/`.
