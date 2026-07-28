# EA-6 — Observability Findings

Status: `ACTIVE — SCHEMA EXERCISED. ONE COMPLETION CRITERION UNMET AND REPORTED.`

Created: 2026-07-28 UTC

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`
Schema: [`../trace/SCHEMA_v1.md`](../trace/SCHEMA_v1.md) ·
Cases: [`../trace/EA-6-cases/`](../trace/EA-6-cases/) ·
Tool: [`../tools/trace_capture/capture.py`](../tools/trace_capture/capture.py)

Governing plan: [`../../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](../../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md) § EA-6, § 8, § 9.

---

## 0. Method

Six reachable cases were captured by a Strategy-owned wrapper that **observes** the pinned
engine — running it under the EA-2 seam and mapping its own artifacts into the trace schema.
The wrapper never imports, patches, or instruments pinned source.

**No field was invented.** Every unreachable field carries the literal `NOT_OBSERVABLE` and a
note naming the reason. EA-5's classifications entered as inputs, not conclusions; EA5-002 is
confirmed here empirically and its scope sharpened.

---

## EA-6-001 — The per-gate status vector is not observable at any granularity

- **Class:** observability gap
- **Evidence:** the plan § 8 requires, per gate, one of
  `PASS | FAIL | UNKNOWN | NOT_EVALUATED | INERT`. Across all six emitted traces,
  `opportunities[].gate_results` is `NOT_OBSERVABLE` in **every** entry — 19–20 opportunities per
  non-halt run. The engine's contract exposes a single `block_reason` string per evaluated
  candidate and a single `reason` string per rejection. EA-5 EA5-002 established the cause:
  `QualificationResult.gates_passed` / `.gates_failed` are computed and discarded at the audit
  boundary.
- **What EA-6 adds beyond EA-5:** EA-5 showed the vector is absent from `logs/audit.jsonl`. EA-6
  shows it is absent from **every durable artifact the engine writes** — audit record, contract,
  run summary alike. There is no second source to fall back on.
- **Affected behaviour:** a rejection can be attributed to one reason string, never to a gate
  vector. "Which gates passed before the one that failed" is unanswerable.
- **User-facing consequence:** EA-10 cannot compute per-gate marginal contribution, redundancy,
  or interaction from captured evidence. Ablation would have nothing to ablate against.
- **Confidence:** **VERIFIED**.
- **Reproduction:** any of the four non-halt traces in `../trace/EA-6-cases/`.
- **Smallest plausible correction seam:** persist `gates_passed` / `gates_failed` on the
  per-candidate audit entry. `audit._build_record` already receives the qualification summary.
  The audit doctrine's Rule 1 requires a PRD naming a consumer — this schema is that consumer.
- **Evidence required to prove a correction worked:** a re-captured trace in which every
  `opportunities[].gate_results` is populated with the five-value vocabulary and reconciles with
  the `block_reason` already recorded.
- **Not proposed here:** no source change. Recording the seam is EA-6's job; implementing it
  requires a separate CuttingBoard charge.

## EA-6-002 — No ordering, override, or precedence event stream exists

- **Class:** observability gap
- **Evidence:** `ordering_and_precedence.gate_order_events` is `NOT_OBSERVABLE` in all six
  traces. The engine exposes `regime_short_circuited` and `regime_failure_reason` (populated when
  present) but no per-gate ordering or override record.
- **Affected behaviour:** EA-4 established a precedence structure — three system-level gates, then
  DIRECT or CONTINUATION, then the five-step decision chain. None of that ordering is emitted at
  runtime; it is recoverable only by reading source.
- **User-facing consequence:** a trace cannot show *where in the order* a candidate stopped, only
  that it stopped. Mis-ordering or an unexpected override would be invisible.
- **Confidence:** **VERIFIED**.
- **Reproduction:** all six traces.
- **Smallest plausible correction seam:** emit an append-only per-candidate stage list as gates
  execute.
- **Evidence required:** a trace whose event stream reproduces the EA-4 order index for a
  candidate that fails at a known gate.

## EA-6-003 — Symbols dropped by validation leave no mark in the durable record

- **Class:** observability gap
- **Evidence:** in the `stale-data` case, `PAAS` is invalidated —
  `WARNING cuttingboard.validation — INVALID PAAS: age 7200s exceeds 300s freshness threshold`
  — yet the captured trace shows `missing_data_mask.excluded_symbols = {}` and
  `missing_data_mask.data_status = "ok"`. The exclusion reaches **stderr only**.
- **Affected behaviour:** a symbol silently leaves the evaluable universe. The run reports `ok`.
- **User-facing consequence:** the missing-data mask the plan requires cannot be built from
  durable artifacts. A later analysis cannot distinguish "symbol was evaluated and rejected" from
  "symbol never entered evaluation because its quote was stale". That distinction is load-bearing
  for opportunity-coverage metrics in EA-9.
- **Confidence:** **VERIFIED**.
- **Reproduction:** `EA-6-trace-stale-data.json` against `runs/stale-data/stderr.txt`.
- **Smallest plausible correction seam:** populate `excluded_symbols` with the validation
  failure reason per dropped symbol, and reflect degradation in `data_status`.
- **Evidence required:** a re-captured stale-data trace whose mask names `PAAS` and its reason.

## EA-6-004 — Reason codes are prose, not a stable machine vocabulary

- **Class:** observability gap
- **Evidence:** `terminal.machine_reason_codes` is `NOT_OBSERVABLE` in all six traces. Observed
  reason strings include `"R:R 2.00 below 2.0 minimum"`, `"stop distance 6.39 below 1× ATR14
  (6.39)"`, `"fixture mode skips live chain validation"` — human prose with embedded numerals,
  not enum values.
- **Affected behaviour:** grouping rejections by cause requires string parsing, and the strings
  interpolate run-specific numbers.
- **User-facing consequence:** any cross-run aggregation is brittle. This is the durable-record
  form of the engine's own claimed gap C-26 ("not consumed by any aggregator today").
- **Confidence:** **VERIFIED**.
- **Reproduction:** the `rejections` entries in any non-halt trace.
- **Smallest plausible correction seam:** emit a stable `reason_code` enum alongside the prose.
- **Evidence required:** rejections carrying a code that groups without parsing.
- **Note — the CONTINUATION path already does this.** EA-4 recorded nine named counters
  (`DATA_INCOMPLETE`, `VIX_BLOCKED`, `NO_BREAKOUT`, …). The pattern exists in the engine; it is
  the DIRECT path that lacks it.

## EA-6-005 — A HALT preserves no evaluation opportunities at all

- **Class:** observability gap / decision-design coherence
- **Evidence:** both halt traces (`halted-killswitch`, `halted-validation`) emit
  `opportunities: []` — zero candidates, zero rejections. The halt suppresses the qualification
  block, so nothing per-symbol is evaluated or recorded.
- **Affected behaviour:** on a halted day the engine records that it halted and why, but nothing
  about what it would have been looking at.
- **User-facing consequence:** the plan § 8 requires "every evaluation opportunity preserved —
  accepted, rejected **and halted**." On a halt there are no opportunity records to preserve. A
  halted day is a hole in any opportunity-coverage series, and cannot be distinguished from a day
  with genuinely no candidates without reading `halt_reason`.
- **Confidence:** **VERIFIED**.
- **Reproduction:** the two halt traces.
- **Smallest plausible correction seam:** none proposed inside EA-6. Whether a halted run *should*
  evaluate candidates is a design question, not an observability bug — recording it as such rather
  than assuming the engine is wrong.
- **Evidence required:** a decision from Dustin on whether halted-day opportunity capture is
  wanted at all.

---

## EA-6-006 — The `accepted` case is unreachable through the authorized seam *(unmet completion criterion)*

**This is reported as an unmet requirement, not worked around.**

- **Class:** data limitation (harness), not an engine defect
- **Evidence:** `runtime/__init__.py:1028` selects `_fixture_chain_results(option_setups)` in
  fixture mode (`:1031` selects live `validate_option_chains` otherwise).
  `_fixture_chain_results` (`:1710–1725`) returns, **for every setup unconditionally**,
  `ChainValidationResult(classification=MANUAL_CHECK, reason="fixture mode skips live chain
  validation", spread_pct=None, open_interest=None, volume=None, expiry_used=None,
  data_source=None)`.
  Empirically, with a synthetic OHLCV cache the pipeline reaches the decision layer in full —
  regime `EXPANSION`, posture `EXPANSION_LONG`, confidence `1.0`, eight symbols QUALIFIED, eight
  option setups built — and **every** resulting candidate carries
  `decision_status: "BLOCK_TRADE"`, `block_reason: "fixture mode skips live chain validation"`.
  `outcome` is `NO_TRADE`.
- **Therefore `outcome = TRADE` is structurally unreachable in fixture mode at this pin.**
- **The three routes to an accepted case are each forbidden:**
  1. **Live chain validation** — requires live market data. Forbidden by this charge and by EA-1's
     mandatory outbound-network denial.
  2. **Patching pinned source** to bypass the stub — an explicit EA-6 stop condition ("any
     proposal to patch pinned source to close a gap").
  3. **Synthesising an accepted trace** — an explicit EA-6 stop condition ("any field synthesised
     to fill a hole").
- **Confidence:** **VERIFIED** that the case is unreachable by authorized means.
- **Consequence carried forward — this is the important part.** The constraint is not confined to
  EA-6. **EA-7 replay and EA-10 attribution cannot observe an accepted trade through the fixture
  seam either.** Any phase whose evidence requires a `TRADE` outcome inherits this blocker. It
  should be resolved before EA-7 is chartered, not discovered inside it.
- **Options for Dustin (none taken here):** charter a separately-authorized chain-data
  substitution seam owned by Strategy; or accept that the program evaluates the *selection*
  surface (qualification through the decision chain) while treating chain validation as an
  unavailable terminal gate, with every downstream metric labelled accordingly; or authorize a
  CuttingBoard change under its own charge.

---

## Completion status — stated plainly

| Required case | Emitted | Note |
|---|---|---|
| rejected | ✅ | 12 rejections with per-symbol reasons |
| halted | ✅ | two causes: kill switch and validation |
| stale-data | ✅ | freshness gate genuinely exercised |
| missing-data | ✅ | non-halt symbol dropped |
| boundary-value | ✅ | VIX exactly 35.0 |
| **accepted** | ❌ | **unreachable — EA-6-006** |

| Criterion | Status |
|---|---|
| Every schema field populated **or** explicitly `NOT_OBSERVABLE` | **MET** — §2 of the schema maps all § 8 fields; six are `NOT_OBSERVABLE`, each with a recorded reason |
| Full-fidelity traces for six case types | **MET FOR FIVE OF SIX** |

**EA-6 is therefore substantially complete but not fully complete against its own criteria.** The
schema is specified and exercised, the wrapper works, five case types are captured — and the
sixth is blocked by an authorized-method limit that is documented rather than papered over.

**No stop condition fired**: no source patch was proposed and no field was synthesised. The
accepted-case gap is reported *because* those were the only ways to close it.

**Containment:** DNS and direct-IP egress blocked (`gaierror`; `OSError [Errno 101] Network is
unreachable`); in-boundary write succeeded; writes into `Projects/strategy/` and
`Projects/cuttingboard/` blocked (`OSError`). CuttingBoard `HEAD` and `status --porcelain`
byte-identical before and after.

**EA-7 is not authorized by this document.** The plan gates capture-at-scale on Dustin's approval
of the schema, and EA-6-006 warrants a decision before EA-7 is chartered.

## Amendment rule

Frozen from creation; never edited in place. A correction is a dated amendment or a new versioned
document, with the version in the filename (`docs/conventions.md` §b, read across by §h).
