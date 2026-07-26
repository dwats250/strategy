# TV-0R — Dustin Adjudication Record

Status: `ADJUDICATED — AUTHORIZES TWO NARROW AMENDMENTS`

Adjudicated: 2026-07-26

Adjudicator: **Dustin Watson.**

## What this document is, and is not

This is an **adjudication record**, not a review. It records Dustin's dispositions
on TV-0R and the exact scope of amendment those dispositions authorize.

It is **not** the TV-0R review output, and it does not substitute for one.

## Chain of custody

TV-0R was charged in
[`../charges/TV-0R-INDEPENDENT-REVIEW.md`](../charges/TV-0R-INDEPENDENT-REVIEW.md),
which names the reviewer as fresh-context Sol / GPT-5.6.

- The review was **performed substantively by fresh-context GPT-5.6 / Sol, outside
  this repository.**
- Its result was **delivered directly to Dustin.** No repository review artifact was
  created, and `reviews/` therefore holds no TV-0R review output.
- A controller session run under Claude Opus 5 on 2026-07-26 reached the TV-0R
  invocation gate, established that the charged GPT-5.6 / Sol reviewer was not
  available to it, and halted with
  `BLOCKED — CHARGED GPT-5.6/SOL REVIEWER UNAVAILABLE` rather than substituting a
  different model. It wrote nothing.
- **Claude did not perform the independent review**, is not the TV-0R reviewer, and
  makes no reviewer claim here. Claude's only role in this packet is scribe: drafting
  the amendment records that carry Dustin's adjudicated dispositions, under this
  charge.
- The reviewer's own report is held by Dustin outside this repository. It is not
  hashed or quoted here, because this record cannot vouch for an artifact it does not
  contain.

Consequence for later stages: the TV-0R review output slot remains unfilled. Any
stage that requires the reviewer's full text must obtain it from Dustin. This record
carries the *dispositions*, not the review.

## Accepted findings

Dustin **accepts both** blocking findings.

### F-1 — D-1 holdout terminology overclaim (accepted, `BLOCKING`)

`spec/BACKTEST_PROTOCOL.md` designates 2022-01-01 through 2026-07-24 an "untouched
out-of-sample window." `docs/conventions.md` §g reserves holdout status for forward
data collected under a frozen specification going forward from pre-registration, and
states that slicing history after the fact does not produce a real holdout.

**Disposition.** Accepted. The 2022–2026 period is a **deferred-inspection
descriptive window**, explicitly not a forward out-of-sample holdout. The protocol's
guard conditions are retained unchanged; only the terminology and the claims it
licenses are corrected.

Recorded in
[`../spec/TV-0R-BACKTEST-INTERPRETATION-AMENDMENT.md`](../spec/TV-0R-BACKTEST-INTERPRETATION-AMENDMENT.md).

### F-2 — Literal-rule gap in the frozen gate matrix (accepted, `BLOCKING`)

`spec/GATE_TRANSLATION_MATRIX.md` classifies several gates as `EXACT_FORMULA` or
`FORMULA_EXACT_DATA_PROXY` while omitting implementation literals those gates require.
TV-1 could not implement them without inventing policy. The gap covers:

| Gate | Omitted literals |
|---|---|
| R-01 | configured breadth and leadership lists |
| R-02 | all eight vote cutoffs and the aggregation rule |
| R-05 | posture cutoffs and evaluation logic |
| E-04 | macro component cutoffs, aggregation, conflict-only behavior, and the directly coupled execution constraints required to state that behavior faithfully |

**Disposition.** Accepted. The missing literals are supplied as a narrow active
appendix, sourced entirely from the pinned CuttingBoard commit with resolvable
citations, adding nothing the pinned source does not contain.

Recorded in
[`../spec/TV-0R-LITERAL-RULE-APPENDIX.md`](../spec/TV-0R-LITERAL-RULE-APPENDIX.md).

## Exactly what this amendment is authorized to change

**Authorized:**

1. Create this adjudication record.
2. Create `../spec/TV-0R-LITERAL-RULE-APPENDIX.md`, stating only literals, operators,
   lists, aggregation rules, outcomes, and conflict-only constraints that are present
   in `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`, each with a
   citation resolvable at that commit.
3. Create `../spec/TV-0R-BACKTEST-INTERPRETATION-AMENDMENT.md`, correcting the holdout
   terminology and nothing else.
4. Add a post-TV-0R effective-authority section to
   [`../INSTALLATION_RECORD.md`](../INSTALLATION_RECORD.md), leaving the original
   frozen hashes unchanged.

**Not authorized by this adjudication:**

- editing any frozen TV-0 authority in place;
- redesigning, adding, removing, relaxing, or tuning any gate, threshold, or parameter;
- introducing a fallback, proxy, default, or interpretation absent from the pinned
  source;
- normalizing, reformatting, or repairing any other document or artifact;
- writing Pine, acquiring data, or producing any implementation artifact;
- any mutation of `dwats250/cuttingboard`, its remote, refs, PRs, issues, or any local
  checkout;
- starting TV-1.

## Resulting effective-authority rule

The frozen TV-0 authorities remain intact and byte-for-byte unchanged. They continue
to govern everything.

These two amendments are **narrow overlays**. Each controls only within its adjudicated
gap:

1. For **R-01, R-02, R-05, and E-04 implementation literals**, the literal-rule
   appendix is the active clarification. It supplements the frozen matrix for those
   four gates; it silently redefines nothing else.
2. For the **naming and interpretation of the 2022-01-01 – 2026-07-24 period**, the
   backtest interpretation amendment supersedes the frozen protocol to that extent
   and no further.

Where an amendment is silent, the frozen document governs. Where this record and a
TV-0 document disagree about anything other than these two adjudicated gaps, the
TV-0 document governs.

The precise precedence order and the TV-1 effective-authority manifest are recorded in
[`../INSTALLATION_RECORD.md`](../INSTALLATION_RECORD.md).

## Status of TV-1

**TV-1 is not started, and remains blocked** until this amendment is merged and the
new record hashes are independently verified against
[`../INSTALLATION_RECORD.md`](../INSTALLATION_RECORD.md).

## Standing constraints, unchanged

- CuttingBoard is read-only evidence at the pinned SHA. No finding, disposition, or
  amendment here authorizes any CuttingBoard change. See `docs/conventions.md` §i.
- Backtest performance alone cannot authorize an engine change.
- No document, commit message, report, or summary produced by this project may describe
  the 2022–2026 historical slice as a genuine forward holdout.
- Reviews and adjudications are append-only records of what was said at a point in
  time. This record is never edited to reflect what is later decided.
