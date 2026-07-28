# Retrospective — CuttingBoard engine audit (EA line)

Created: 2026-07-28 UTC · Scope: the EA-0 … EA-8 program, closed at
[`audits/cuttingboard-engine-strategy-audit/EA-AUDIT-CLOSEOUT.md`](../audits/cuttingboard-engine-strategy-audit/EA-AUDIT-CLOSEOUT.md).

Five concrete improvements the audit actually surfaced. Each names the failure mode it
prevents. **This is not a governance framework and not a backlog** — nothing here is a standing
rule until it is added to `conventions.md` by its own change.

---

## 1. Test evidence feasibility before committing to a multi-phase program

**Do this:** before chartering a program whose later phases consume data or observability,
verify that the required evidence is *obtainable under the boundary the program will run
under*. A one-session feasibility probe is enough.

**Failure mode it prevents:** discovering at phase 6 of 13 that a terminal case is structurally
unreachable. EA-6 found that `_fixture_chain_results` returns `MANUAL_CHECK` unconditionally, so
`outcome = TRADE` cannot occur in fixture mode — which retroactively bounded EA-7 and EA-10 and
forced a plan amendment. The same probe at EA-0 would have cost hours and reshaped the whole
program. EA-8 hit the sibling case: no authorized historical OHLCV existed, so EA-9 could never
have run.

## 2. Keep one live current-status authority, distinct from frozen records

**Do this:** maintain exactly one document that says what is authorized *right now*, and let
frozen records say only what was true when they were frozen.

**Failure mode it prevents:** a superseded packet reading as live. The audit opened by finding
TV-1 commissioned, its blocking conditions silently satisfied, and its objective unmet — a live
commission pointed at a script that does not compile. Meanwhile two READMEs described a
lifecycle stage that had already passed. Phase 0 existed only to resolve that.

## 3. Require the provenance manifest before any result is interpreted

**Do this:** no result is read until its manifest records source, retrieval, symbol identity,
timeframe, timezone, session, bar-timestamp convention, adjustment semantics, coverage, and
checksum — with no field left blank.

**Failure mode it prevents:** unrecoverable configuration. UV02's friction scenario is
permanently `UNRECOVERABLE` because Properties were never captured before export; seven
otherwise-clean captures cannot support a friction-adjusted claim. The cost is not the missing
field, it is that the field cannot be recovered later at any price.

## 4. Reuse a phase-charge template instead of re-deriving one

**Do this:** keep one template carrying question / authorized work / outputs / entry criteria /
completion criteria / stop conditions / approval gate, and instantiate it per phase.

**Failure mode it prevents:** phases that cannot be closed because their exit test was never
written down, and drift between phases in what "done" means. The EA phases that ran cleanly were
the ones whose completion criteria were mechanically checkable; where a criterion was
under-specified — EA-5's "a reproducing fixture or demoted to UNKNOWN" against findings that are
documentary rather than runtime — the phase had to resolve the ambiguity mid-flight and record
the reading.

## 5. Spend independent review at semantic decision seams, not routine mechanics

**Do this:** commission independent review where a *judgement* is encoded — a claimed contract
against source, a defect classification, a parity boundary. Do not spend it on mechanical steps
whose output is already checkable.

**Failure mode it prevents:** plausible-but-wrong findings surviving, while review budget is
consumed by work a checksum would have caught. The Fable review of the Revision 3 plan returned
eleven confirmed defects, three of which made Phase 0 unable to satisfy its own completion
criteria — none of which a mechanical check would have surfaced. By contrast, hash verification
and diff-scope checks needed no reviewer at all.

---

## What is deliberately not here

No new directory conventions, no process layers, no proposals for CuttingBoard, and no
prioritisation of the above beyond the order in which the evidence appeared. Adding any of these
five to the standing rules is a separate, explicit change to `conventions.md`.
