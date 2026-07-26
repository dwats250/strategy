# Audit reviews

Independent-review outputs and their adjudication tables. Nothing here yet.

## What lands here

| Artifact | Produced by | When |
|---|---|---|
| TV-0R review output | Fresh-context Sol / GPT-5.6 | After the scaffold PR is open and TV-0 hashes verify |
| TV-0R adjudication table | Opus, dispositions approved by Dustin | After TV-0R reports |
| TV-1R review output | A different fresh-context Sol / GPT-5.6 | After Pine compiles, loads, and its SHA is frozen |
| TV-1R adjudication table | Opus, dispositions approved by Dustin | After TV-1R reports |

Charges: [`../charges/TV-0R-INDEPENDENT-REVIEW.md`](../charges/TV-0R-INDEPENDENT-REVIEW.md),
[`../charges/TV-1R-PINE-SEMANTIC-REVIEW.md`](../charges/TV-1R-PINE-SEMANTIC-REVIEW.md).

## Rules

**Reviews are append-only.** A review output is a record of what a reviewer said at a point in
time, against documents at known hashes. It is never edited to reflect what was later decided
— the adjudication table carries that.

**One bounded correction cycle each.** TV-0R gets one correction pass on TV-0; TV-1R gets one
on the Pine implementation. No recursive review loops, and no reviewer reviews its own review.

**Fresh context and strict separation.** The session that authored a document does not review
it. The session that implements does not review the implementation. TV-0R and TV-1R are
different sessions.

**Findings carry evidence.** Every finding is `BLOCKING`, `NON-BLOCKING`, or `QUESTION`, with
exact location, exact pinned-source evidence where applicable, consequence, and the smallest
sufficient correction. An assertion about engine behavior without a pinned-source citation is
not a finding.

**Dustin approves dispositions.** The reviewer does not self-adjudicate. A `BLOCKING` finding
is not overruled without a recorded reason.

**Reviews do not authorize CuttingBoard changes.** A review may audit CuttingBoard. Any
resulting engine change requires a separate, independent commission and an explicit
CuttingBoard decision. Backtest performance alone cannot authorize an engine change.

## Recording hashes

Each review output records the SHA-256 of every document or source file it reviewed. After a
correction pass, the new hashes go into
[`../INSTALLATION_RECORD.md`](../INSTALLATION_RECORD.md). A hash mismatch between what a
review examined and what a later stage consumes means the contract drifted, and the later
stage stops.
