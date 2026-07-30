# Strategy–CuttingBoard Interface Charter — v0.1

**Status:** `ADOPTED v0.1 — 2026-07-30 UTC, by owner instruction. Companion to docs/conventions.md §i.`

**Prepared:** 2026-07-30 UTC. Reconciled against `conventions.md` §i (including the
Development-boundary amendment of 2026-07-30), `docs/owner-decisions-2026-07-30.md`,
`docs/PROBE_TEMPLATE_v0.1.md`, and the §b trial-budget amendment.

## 1. Purpose

`strategy` and `cuttingboard` are complementary but separate projects.

- `strategy` is an independent research workspace for explicitly declared historical studies
  and strategy probes.
- `cuttingboard` is a discretionary decision-support engine.

This charter governs their interface. It protects both projects from accidental coupling:
research results must not silently change engine behavior, and engine implementation work must
not rewrite, invalidate, or consume a study as though it were an implementation specification.

This is a boundary document. It does not commission a study, capture campaign, engine change,
or migration.

## 2. Standing, precedence, and topology

**Precedence.** This charter is the interface companion to `conventions.md` §i. It restates
nothing §i already rules on; where the two appear to conflict, **§i controls** and the conflict
is itself a defect to be fixed by dated amendment here.

**Bindingness.** This charter directly binds conduct in `strategy`. Its CuttingBoard-side
provisions (for example §7.C's test and non-goal requirements) take effect only when adopted on
the CuttingBoard side by an **ADOPTED LOCALLY** record (§8) in that repository. Neither
repository has implied authority over the other.

**Topology.** Per the §i Development-boundary amendment and
`docs/owner-decisions-2026-07-30.md`, the CuttingBoard side has two nodes:

- **production** `dwats250/cuttingboard`, including the audited pin `59f8279d…` — read-only,
  commit-addressed evidence for `strategy` sessions, with the per-change charge rule for
  anything touching the audited pin's evidentiary record;
- **the Dustin-owned development fork** — the sole authorized mutation target of
  fork-rooted development charters, in their own sessions; merge-back into production is its
  own governance event.

Everything this charter says about "CuttingBoard" applies to both nodes unless a rule names one.

## 3. Separate authority

Each repository governs its own work.

| Matter | Authority |
| --- | --- |
| Research question, hypothesis, method, data, run record, and findings | The relevant `strategy` study documents |
| CuttingBoard behavior, code, configuration, PRDs, and release decisions | The relevant CuttingBoard documents and an explicit CuttingBoard-side commission |
| Development-fork work and any merge-back into production | Fork-rooted charters; merge-back separately authorized (§i amendment) |
| Whether a research finding merits any engine investigation | Dustin, through a new explicit CuttingBoard-side decision |
| Whether an engine trace, fixture, or explanation may be used as research evidence | The relevant `strategy` study manifest and provenance record |

## 4. Core separation rules

1. **No back-feed without commission.** No result in `strategy` authorizes a CuttingBoard code,
   threshold, configuration, document, issue, or workflow change. Stronger, per the §i
   amendment: any change **derived from audit or study evidence requires its own explicit
   Dustin commission naming that derivation, wherever the change lands** — production, fork, or
   elsewhere.
2. **No implied validation.** CuttingBoard behavior, a proxy match, or an engine trace does not
   validate a strategy's economic merit or future performance.
3. **No shared mutable source of truth.** A document may cite the other repository; it must not
   become the living specification for both.
4. **No unpinned references.** A cross-repository technical claim cites a commit, release,
   content hash, or immutable exported artifact — not a moving branch.
5. **No silent translation.** When an engine concept is represented in a study, the study
   records its translation, exclusions, proxies, and unavailable observables.
6. **No custody laundering.** Artifacts copied between repositories retain their source
   location, immutable identifier, capture method, and hash.

## 5. What may cross the boundary

The following are permitted only as explicitly labelled inputs (§8); none changes the receiving
repository by itself.

| From | To | Permitted item | Required record |
| --- | --- | --- | --- |
| CuttingBoard | strategy | Pinned source snapshot, public contract, reason-code taxonomy, trace schema, or exported trace | Source commit/hash, read per §i mechanics (commit-addressed; never a working tree); interpretation status; any proxy or omission |
| strategy | CuttingBoard | Factual finding, defect hypothesis, fixture candidate, or observability requirement | Study/run identifier; scope; evidence; limits; explicit statement that it is not a change request |
| Either | Either | Reusable process practice such as manifests, provenance fields, or capture checklist | Adopted independently in the receiving repository; no shared mutable file |

Raw data, credentials, account details, live operational state, and unredacted private logs do
not cross by default. Their transfer needs its own documented provenance and privacy decision.

## 6. The completed AS-IS proxy study

The completed AS-IS proxy work is historical evidence in `strategy`, not an ongoing CuttingBoard
workstream. Its results are bounded to its registered instrument, timeframe, date window, source
pin, and proxy contract.

It may be cited for its actual conclusions — such as a verified classification correspondence or
a documented translation limitation. It may not be cited as authority to alter CuttingBoard
gates, thresholds, or production behavior.

Any subsequent observation about CuttingBoard requires a new, separately registered `strategy`
study or a separately commissioned CuttingBoard review. It does not amend the closed study.

## 7. How future work proceeds

### A. A strategy-native probe

For a strategy idea that is independent of CuttingBoard: pre-register it under
`docs/PROBE_TEMPLATE_v0.1.md` — including the §b-required `trials_planned` and
`dsr_threshold_implied` — run and preserve evidence under that probe's own record, and report
conclusions only within its scope. Do not describe it as a CuttingBoard validation or a
candidate for automatic engine adoption.

### B. A CuttingBoard observation or concern

For a possible engine defect, contradiction, or improvement:

1. Record the observation as an evidence-limited finding; include the pinned source and exact
   reproduction or trace evidence.
2. Do not edit CuttingBoard — production or fork — from the `strategy` workflow.
3. Dustin decides whether to open a new CuttingBoard-side commission.
4. The CuttingBoard commission independently confirms, rejects, or narrows the observation
   before any change.
5. If a change is made, its tests and release record live on the CuttingBoard side. The
   `strategy` finding remains historical evidence and is not rewritten.

### C. CuttingBoard observability work

Trace, dry-run, reason-code, and outcome-semantics work belongs to the CuttingBoard side
because it changes or formalizes engine behavior. It may use an independently adopted schema
informed by prior research, but it requires:

- a fork-rooted (or CuttingBoard-rooted) charter naming its mutation target per §i;
- explicit non-goals, including no threshold tuning or execution automation;
- fixture and regression tests on the CuttingBoard side; and
- a separate decision before any trace becomes input to a `strategy` study.

## 8. Required language for cross-repository records

Every cross-repository reference includes: source repository and immutable identifier; receiving
record and its status; what was used (source, exported evidence, schema, or finding); what was
*not* established; whether the reference is descriptive, a proxy, or a proposal; and the
authorization required for any next action.

Use one of these labels:

- **EVIDENCE REFERENCE** — factual, scoped evidence; no requested change.
- **TRANSLATION / PROXY** — a study representation of a source concept; not engine parity
  unless independently demonstrated.
- **OBSERVATION FOR REVIEW** — a possible CuttingBoard concern; not a defect or change request.
- **ADOPTED LOCALLY** — a process practice independently accepted by the receiving repository.

## 9. STOP conditions

Same posture as §i: stop, report, and wait for Dustin — do not resolve by guessing — when any
of the following appears: a cross-repository mutation whose target is missing, inferred, or
ambiguous; a CuttingBoard target (production or fork) in a `strategy` session; an unpinned
cross-repository technical claim; a cross-repository record with none of the §8 labels; or an
instruction that would edit a closed study, a frozen record, or the other repository's doctrine
from the wrong side of the boundary.

## 10. Current operating posture

1. The closed AS-IS study remains preserved as completed research evidence.
2. The Q-03 documentation correction is complete; it does not create further implementation
   authority.
3. The next `strategy` work, if any, is separately chartered — for example a strategy-native
   probe under §7.A or a new registered translation study; it is not a continuation of the
   AS-IS study.
4. The first substantive CuttingBoard engineering work, if desired, begins only through a
   fork-rooted charter for outcome semantics and deterministic dry-run/trace capability.
5. Metrics, data acquisition, tuning, and cross-project operational integration remain
   uncommissioned until they have a defined consumer and their own scope.

## 11. Amendment rule

This charter is amended only by a dated, reviewable change in `strategy`; any
substance-changing edit bumps the version (§c) — v0.1 is superseded by v0.2, never rewritten.
An amendment changes this interface prospectively; it never silently changes a closed study, a
pinned source snapshot, or CuttingBoard doctrine.
