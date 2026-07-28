# EA-0 — Engine-Audit Program Commission

Status: `ACTIVE — FRAMEWORK COMMISSION ONLY. AUTHORIZES NO EA PHASE.`

Created: 2026-07-27 UTC

Governing plan:
[`../../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](../../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md)

---

## 1. Source pin

- Repository: `dwats250/cuttingboard`
- Commit: `59f8279d796335149afdec4aa507b6f927233518`
- Commit date: `2026-07-26T01:35:59Z`
- Mutation permission: **NONE**

CuttingBoard is read-only evidence, readable **only at the pin**, through
commit-addressed reads (`git show`, `git ls-tree`, `git archive`). Never from a local
working tree. See `docs/conventions.md` §i.

## 2. Scope

The EA line audits the **implemented CuttingBoard decision engine** — executing the pinned
engine offline under enforced isolation rather than translating it into a second language.
Its phases are EA-1 (static execution-safety map) through EA-13 (final synthesis), specified
in full in the governing plan §6.

The EA line **supersedes the TV-0 → TV-4 proxy line** for the purpose of answering whether
the engine is structurally correct, decision-useful, observable, replayable, and fitted. The
TV line's disposition is recorded separately in
[`../../closure/TV-LINE-CLOSURE-2026-07-27.md`](../../closure/TV-LINE-CLOSURE-2026-07-27.md).

## 3. Repository boundary

- **`dwats250/strategy`** — the sole authorized mutation target. All plans, datasets,
  manifests, tooling, traces, findings, evaluation results, fitting outputs, and correction
  proposals live here.
- **`dwats250/cuttingboard`** — a forbidden mutation target. No agent may create, update,
  delete, push, merge, comment, dispatch, configure, or otherwise mutate any CuttingBoard
  file, ref, branch, pull request, issue, review, workflow, release, setting, or remote.
  **Capability is not authorization.**
- Every GitHub or connector mutation must supply its repository target explicitly, and that
  target must be exactly `dwats250/strategy`. A missing, inferred, or ambiguous target is a
  STOP condition. A CuttingBoard target is a STOP condition outright.
- No result, parameter, threshold, code, or conclusion from this program may feed back into
  CuttingBoard. Any CuttingBoard change requires a separate Dustin-authorized charge in a
  separate session rooted in that repository.

## 4. Authority scope and lapse — binding

> **This commission authorizes the program framework and Phase 0's documentation actions
> only. No EA phase is authorized by this document. Each phase is authorized solely by
> Dustin's approval at its entry gate, and EA-2 execution solely by its separate execution
> approval. Unapproved phases hold no residual authority. If the program terminates at any
> point, a closure record for EA-0 extinguishes it, leaving no live commission.**

This clause is not boilerplate. An unscoped commission whose objective outlived its usefulness
is exactly what produced the TV-1 residual authority that Phase 0 extinguished. This document
is written so that it cannot repeat that failure: it grants nothing forward, and it can be
closed cleanly at any time without leaving a live packet behind.

### 4.1 What is authorized right now

Phase 0 only — the documentation actions enumerated in the governing plan §1. Phase 0's
completion does **not** authorize EA-1.

### 4.2 What is not authorized

EA-1 through EA-13; any execution of the CuttingBoard engine; any sandbox, environment,
dataset, tooling, trace, fixture, replay output, attribution result, or fitting output; any
CuttingBoard access beyond commit-addressed reads once a later phase authorizes them; any
CuttingBoard mutation under any circumstance.

## 5. Standing rules that apply in full

`docs/conventions.md` governs this program without exception — §b (frozen documents are never
edited in place), §e (immutable, self-describing exports), §f (the ledger is authoritative),
§g (a holdout is frozen forward data; a re-inspected historical slice is a
deferred-inspection window), §h (audits are not studies; the audited source is read-only
pinned evidence; unavailable is not the same as passing), and §i (cross-repository isolation).

## 6. Amendment rule

This charter is a frozen document from creation. It is never edited in place. A correction is
a dated amendment file or a new versioned charter, with the version in the filename
(`docs/conventions.md` §b, read across by §h).
