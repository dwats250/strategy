# strategy — Claude Code entrypoint

Claude Code is the **primary implementation harness** for this repository. You do the
reconnaissance, the writing, and the committing.

## Where the authority is

- **`docs/conventions.md`** — the standing lab rules: study layout, pre-registered manifests,
  script versioning, immutable exports, the ledger, what counts as a holdout, and how audits
  differ from studies. Read it before adding a study or audit, or amending a manifest.
- **The current committed plan** — for the CuttingBoard engine audit that is
  [`audits/cuttingboard-engine-strategy-audit/plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](audits/cuttingboard-engine-strategy-audit/plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md).
  The committed plan is authoritative for a phase's scope, paths, outputs, completion criteria,
  and stop conditions. Chat history and git history are not authority.

Neither this file nor `AGENTS.md` is a workflow authority. They point; they do not govern.

## Scope discipline

Work only the **explicitly authorized active phase**, and touch only the files that phase
authorizes. If something outside that set looks like it needs doing, say so and stop — don't
widen the packet.

Frozen records are never edited in place. A correction is a dated amendment or a new versioned
file, per `docs/conventions.md` §b (read across to audit artifacts by §h). That applies to
plans, specs, manifests, closure records, and prior-phase outputs alike.

## Repository boundary — binding in brief

An agent may mutate only `dwats250/strategy`. `dwats250/cuttingboard` — its remote, its refs and
PRs, and every local checkout — is a **read-only evidence source and a forbidden mutation
target**. Credentials that happen to permit a CuttingBoard write do not authorize one. Read it
only at the pinned SHA, commit-addressed, never from a working tree.

Every GitHub or connector mutation must name its repository target explicitly, and that target
must be exactly `dwats250/strategy`. A missing, inferred, or ambiguous target is a STOP
condition; a CuttingBoard target is a STOP condition outright.

**The complete rule is `docs/conventions.md` §i** — capability-is-not-authorization, the
pinned-SHA evidence rules, and the session preflight. Read it before acting.

## Checks to run — the phase-relevant ones, not all of them

Run what the active phase actually needs, and report it:

- **Preflight** — repository identity, branch, HEAD, remote, working-tree state, parity.
- **Provenance** — for pinned-source work, the SHA and how it was read; for run artifacts, the
  identities the plan requires.
- **Containment** — when a phase executes anything, establish and *prove* the isolation the plan
  requires before the run, and assert afterward that CuttingBoard is unchanged.

Skip checks a phase doesn't need. A preflight that reports facts irrelevant to the packet is
noise, not rigour.

## Judgement

Fix ordinary, resolvable input seams inline — a wrong path, a missing directory, a stale
reference, an arithmetic slip you catch before committing. Note it in the report and move on.
Not every rough edge is a governance event; escalating one into a correction cycle costs more
than it protects.

Reserve stopping for what actually warrants it: a real authority conflict, a containment
failure, evidence that would have to be invented, or a change to a frozen record.
