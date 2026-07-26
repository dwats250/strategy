# TV-1R — Independent Pine Semantic Review

Status: CHARGED — BLOCKED ON TV-1

Reviewer: fresh-context Sol / GPT-5.6. Not the session that implemented TV-1, and not the
session that performed TV-0R.

## Authority and boundary

- Source evidence: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`
- Governing contract: the frozen TV-0 documents and the accepted TV-0R disposition
- CuttingBoard mutation permission: **NONE**
- File edit permission: **NONE**
- Merge permission: **NONE**

## Preconditions

Do not begin until all hold:

1. Pine v6 compiles.
2. The script loads on a standard SPY daily chart.
3. Named gates and variants are present and selectable.
4. Parity fixtures and known proxy exceptions are recorded.
5. The implementation SHA-256 is frozen and recorded.
6. TV-0 is frozen, with post-correction hashes recorded in `../INSTALLATION_RECORD.md`.

## Inputs

- The frozen Pine source at its recorded SHA-256
- The frozen TV-0 documents at their recorded hashes
- The accepted TV-0R disposition
- `../spec/PARITY_CASES.md` and the recorded proxy exceptions
- `../INSTALLATION_RECORD.md`
- Read-only pinned CuttingBoard source, read via
  `git show 59f8279d796335149afdec4aa507b6f927233518:<path>` — never from a local working tree

## Scope

Review implementation fidelity against the frozen contract. Specifically:

1. **Fidelity** — does each named gate, threshold, comparison operator, priority order, and
   missing-data behavior match the frozen matrix and the pinned source?
2. **Temporal safety** — can the strategy repaint? Does any value from bar `t+1` reach a
   signal computed at bar `t`? Are `request.security()` calls on the daily timeframe with
   `barmerge.lookahead_off`?
3. **Missing-data handling** — do missing cross-symbol values stay missing? Can a missing
   value silently become neutral, zero, or passing? Does expansion breadth count missing
   tradable symbols as not advancing, matching the pinned engine?
4. **Unavailable-gate honesty** — is any `EXCLUDED_*` or unavailable gate treated as PASS,
   or folded into soft-failure arithmetic it should be excluded from?
5. **Variant isolation** — do V0 through V6 differ only by gate-family activation, with
   identical thresholds and formulas, from one source producing a `variant_id`?
6. **Export visibility** — are the exports sufficient for later offline reproduction, per the
   protocol's required-export list?
7. **Execution proxy** — next-bar-open fills, geometry anchored to the actual fill, no
   same-bar reversal, one position at a time, conservative stop-first treatment of
   ambiguous intrabar bars with the ambiguity flag exposed.
8. **Change-surface compliance** — did the diff stay inside TV-1's allowed files as corrected
   by `../INSTALLATION_RECORD.md`? Were any dependencies, workflows, or generated exports added?
9. **No overclaiming** — does the source, its comments, or its on-chart display assert
   CuttingBoard parity, options profitability, or future performance?

## Out of scope

This review does **not**:

- optimize or comment on performance;
- redesign the strategy;
- tune thresholds;
- propose CuttingBoard refactoring;
- re-litigate settled TV-0 decisions;
- review its own review.

**Performance is not a test oracle.** A change that improves results but breaks a fixture is
wrong, and a fixture failure is a finding regardless of what the equity curve does.

## Output contract

Identical to TV-0R. Classify each finding `BLOCKING`, `NON-BLOCKING`, or `QUESTION`, with:

1. exact location — file and line or function;
2. exact evidence — the frozen TV-0 clause and, where applicable, the pinned-source construct;
3. consequence;
4. smallest sufficient correction.

Report "no finding" explicitly where a scope item is satisfied.

## After the review

One adjudication table prepared by Opus, dispositions approved by Dustin, then **at most one
bounded correction cycle**. Re-hash the corrected Pine source and record it.

If cross-symbol mapping or ATR initialization remains ambiguous after that cycle, **stop for
a recorded proxy decision** rather than reviewing recursively. An honest narrower proxy with
a documented exception is the correct outcome; an invented full-engine replica is not.

Review output and the adjudication table land in `../reviews/`.
