# EA-3 — The Claimed Decision Contract

Status: `ACTIVE — WHAT CUTTINGBOARD SAYS IT DOES. NOT EVIDENCE OF WHAT IT DOES.`

Created: 2026-07-27 UTC

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`
Read set and scope: [`EA-3-READ-LOG.csv`](EA-3-READ-LOG.csv) ·
Withheld corpus: [`EA-3-WITHHELD-SOURCES.md`](EA-3-WITHHELD-SOURCES.md)

Governing plan: [`../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md) § EA-3.

---

## 0. Epistemic status — binding

**Every statement in this document is a CLAIM made by CuttingBoard about itself.** Nothing here
is evidence that the implementation behaves this way. Treating a contract document as evidence
of implemented behaviour is an explicit EA-3 stop condition, and this document does not do it.

Claims are written as **testable propositions** (`C-n`) precisely so EA-4 can adjudicate each
one against source and EA-5 can attempt to falsify it with a fixture. A claim's presence here
means only: *the engine's own documentation asserts this.*

---

## 1. Claimed decision architecture

**C-1 — Gate count and sequence.** Every trade candidate passes through **11 gates in
sequence**: `REGIME`, `CONFIDENCE`, `DIRECTION`, `STRUCTURE`, `STOP_DEFINED`, `STOP_DISTANCE`,
`RR_RATIO`, `MAX_RISK`, `EARNINGS`, `EXTENSION`, `TIME`.
*(`docs/trade_qualification.md` §Overview, §The 11 Gates)*

**C-2 — Hard/soft partition.** Gates 1–4 are **hard stops**: failure rejects immediately with
no watchlist eligibility. Gates 5–11 are **soft stops**.

**C-3 — Soft-failure arithmetic.** Exactly **one** soft failure ⇒ `WATCHLIST`. **Two or more**
⇒ `REJECT`.

**C-4 — No partial credit.** "Every gate either passes or fails."

**C-5 — Claimed outcome logic**, verbatim structure from §Outcome Logic:

| Condition | `qualified` | `watchlist` | Other |
|---|---|---|---|
| Hard gate 1–4 fails | `False` | `False` | `hard_failure = "{GATE}: {reason}"`; `max_contracts = None`; `dollar_risk = None` |
| All soft gates pass | `True` | `False` | `hard_failure = None`; `watchlist_reason = None` |
| Exactly 1 soft fails | `False` | `True` | `watchlist_reason` = the single failure reason |
| 2+ soft fail | `False` | `False` | `hard_failure = "N soft gates failed: …"` |

**C-6 — Three entry modes, not one.** The 11-gate sequence describes **DIRECT** only.
**CONTINUATION** is an EXPANSION-only breakout path with *its own gate sequence* in
`_qualify_continuation_candidate()`. **PULLBACK_IMBALANCE** is an FVG-based upgrade applied
**post-hoc to an already-qualified DIRECT result** in `_resolve_entry_mode()`.

> **Note for EA-4.** C-6 is the single most consequential claim in this document. If the
> narrative "11 gates in sequence" is read as the whole decision system, two further paths with
> different gate logic are missed — one of which mutates an already-qualified result. C-1 and
> C-6 must be adjudicated together.

**C-7 — Gate 9 fails open.** `EARNINGS` is "Soft, Fail-Open": `None` (unknown) or `False` ⇒
**PASS**.

**C-8 — Watchlist is conditional, not failed.** "A watchlist symbol is not a failed trade — it
is a conditional trade." The system **does not auto-promote** watchlist symbols on the next run;
"every run is evaluated fresh."

---

## 2. Claimed terminal outcomes

**C-9 — Three terminal outcomes:** `TRADE`, `NO_TRADE`, `HALT`.
*(`cuttingboard/output.py:232–234`; duplicated at `notifications/formatter.py:34–36`)*

**C-10 — Duplicated outcome vocabulary.** The three constants are defined in **two** modules.
Recorded as a claim about structure, not as a defect.

**C-11 — Single canonical contract builder.** `contract.py` is "the only place that translates
internal runtime objects into the canonical output shape. Renderers read from this dict; they do
not inspect runtime internals after contract creation."

---

## 3. Claimed machine contract

**C-12 — `PipelineContract` is schema_version v2** with keys: `schema_version`,
`generation_id`, `generated_at`, `session_date`, `mode`, `status`, `timezone`, `system_state`,
`market_context`, `trade_candidates`, `rejections`, `audit_summary`, `artifacts`, `correlation`,
`regime`, `macro_drivers`, and a runtime-injected `outcome`.
*(`contract_types.py:111–133`)*

**C-13 — `rejections` is a first-class contract key.** The contract carries a `rejections` list
alongside `trade_candidates`.

> **Note for EA-6.** C-13 matters for observability: the *contract* claims a rejection channel.
> Whether it is populated, and with what fidelity, is EA-4/EA-6's to establish.

**C-14 — `DecisionTrace` requires three non-empty strings:** `stage`, `source`, `reason`, per
candidate. *(`contract_types.py:60–66`)*

**C-15 — `SystemState` carries `stay_flat_reason`** plus `router_mode`, `market_regime`,
`intraday_state`, `time_gate_open`, `tradable`, and — required at finalization but never at
build — `outcome`, `permission`, `reason`. `confidence` is absent from
`build_error_contract`'s block. *(`contract_types.py:40–58`)*

---

## 4. Claimed observability contract

From `docs/audit_doctrine.md`, read in full.

**C-16 — Two record families share one file "by historical accident, not by design."**
`logs/audit.jsonl` holds *pipeline records* and *notification-event records*, interleaved.

**C-17 — Rule 1: pipeline records are written only from `_run_pipeline`,** at one canonical
write site. `_execute_notify_run` "intentionally does not write pipeline records. This is
design, not omission."

**C-18 — Rule 2: exactly one pipeline record per invocation.** "Not one per symbol, not one per
decision event, not one per mode, not one per evaluated candidate." A record is a flattened
snapshot of full run state.

**C-19 — Consumers must filter.** "Any consumer reading `logs/audit.jsonl` as a pipeline log
MUST filter out records where `event == "notification"`." Canonical filter:
`record.get("event") != "notification"`.

**C-20 — Claimed density: ~1 record per trading day.** "A consumer that needs denser coverage
than ~1 record per trading day must either change the doctrine … or read a different artifact
entirely."

**C-21 — Explicit non-guarantees.** The doctrine declares itself **not** a schema lock, **not**
a density guarantee ("sparseness is permitted, expected, and not a defect"), **not** a position
on intraday coverage, and **not** a write-ordering guarantee between the two families.

> **Note for EA-6 — the central observability tension.** C-18 and C-20 together mean the
> engine's own canonical log is, by design, **one snapshot per run, roughly daily**. EA-6's
> trace schema requires per-candidate, per-gate granularity across *every* evaluation
> opportunity. The gap between C-18/C-20 and that requirement is **claimed by CuttingBoard
> itself**, not asserted by us — and closing it in CuttingBoard would require a PRD under Rule 1
> naming a consumer. This is the sharpest input EA-3 hands forward.

---

## 5. Claimed artifact contract

**C-22 — Artifacts are categorized** as runtime-critical, dashboard, or audit, with named
writers and readers per artifact. *(`docs/artifact_flow_map.md` §Artifact Inventory, §Artifact
Writers, §Runtime-Critical Artifacts, §Dashboard Artifacts, §Audit Artifacts)*

**C-23 — Graceful degradation is claimed:** "If any runtime-critical artifact is missing, the
pipeline degrades gracefully (returns None / …)". *(§Runtime-Critical Artifacts, L255)*

**C-24 — Several artifacts are explicitly declared non-decision-affecting sidecars**, including
`logs/trend_structure_snapshot.json` and `logs/watchlist_snapshot.json` ("Sidecar; not
runtime-critical for decisions"), and `logs/macro_drivers_snapshot.json` ("Dashboard display,
fallback only").

> **Consistency note.** C-24 is *consistent with* the EA-1 amendment's D-3 and D-4 corrections:
> the two artifacts EA-2 observed as absent from the fixture write-set are the two the engine's
> own artifact contract labels non-decision-affecting sidecars. Recorded as an agreement between
> the claimed contract and EA-2's observation — not as proof of either.

---

## 6. Claimed gaps — the engine's own self-assessment

`docs/decision_quality_map.md` §Known Gaps enumerates four. **These are CuttingBoard's claims
about its own shortfalls**, read from an authorized contract document. They are *not* withheld
findings (§EA-3-WITHHELD-SOURCES), and they are *not* our findings.

**C-25** — No structured `block_reason` rollup across runs.
**C-26** — No threshold-friction summary: `decision_trace`, `regime_failure_reason`,
`excluded_symbols`, `near_a_plus[*].reason`, `watchlist[*].missing_conditions` are "**not
consumed by any aggregator today**."
**C-27** — No weekly decision-quality summary artifact.
**C-28** — No documented evidence-to-PRD calibration convention; `config.py` has no stated rule
for when a numeric constant may be re-tuned or what evidence a re-tuning must cite.

> **Note for EA-10/EA-11.** C-28 is directly load-bearing for fitting readiness: the engine
> itself claims it has **no convention governing when a threshold may change**. That is a
> fitting-readiness gap asserted by the subject, awaiting our independent adjudication.

**C-29 — `decision_quality_map.md` disclaims normative force:** "This document is documentation
only. No source code, schemas, sidecars, aggregation, dashboards, notifications, or thresholds
are changed by this audit," and "This map does not introduce new architecture rules."

---

## 7. Document-kind findings about the read set

Recorded because they affect how later phases should weight these sources.

**C-30 — `docs/DECISIONS.md` is a project-governance log, not a trading-decision contract.**
102 top-level entries, titled with rulings on process matters (PRD lifecycle, reviewer
independence, tooling traps, permission deny sets). It is **not** a specification of the
decision system, and must not be cited as one.

**C-31 — `docs/PROJECT_STATE.md` carries a self-declared "Known technical debt" section** plus
"Parked (reopen only under the stated condition)" and "Alignment check". Claims about state, not
a contract.

---

## 8. Scope boundary recorded

`docs/decision_quality_map.md` anchors on `docs/system_logic_map.md` for runtime decision flow,
decision-affecting vs display-only module sets, sidecar boundary rules, and forbidden mutation
paths. That document is **on neither EA-3's authorized read set nor the withheld list**, so it
was **not read**. See [`EA-3-WITHHELD-SOURCES.md`](EA-3-WITHHELD-SOURCES.md) §5. It is
contract-class and EA-4 will likely need it; adding it is Dustin's call.

---

## 9. Completion statement

- **The claimed contract is stated in testable terms** — 31 propositions C-1…C-31, each cited to
  an authorized document, each adjudicable by EA-4 against source.
- **Every withheld document is listed** — 7 named files, 8 directories, 127 glob-matched files,
  in `EA-3-WITHHELD-SOURCES.md`.
- **The phase read log contains no withheld path** — all 8 entries in `EA-3-READ-LOG.csv` are
  authorized contract documents, with per-file SHA-256 and exact read scope.

**No stop condition fired.** No withheld document was read, and no contract document is treated
here as evidence of implemented behaviour.

**EA-4 is not authorized by this document.** The plan gates it on Dustin's review of this
claimed contract and the withheld list.

## 10. Amendment rule

Frozen from creation; never edited in place. A correction is a dated amendment file or a new
versioned document, with the version in the filename (`docs/conventions.md` §b, read across by
§h).
