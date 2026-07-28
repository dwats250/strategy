# EA-4 — Implemented System Map and Contract-versus-Code Adjudication

Status: `ACTIVE — TRACED FROM SOURCE AT THE PIN. NOTHING WAS EXECUTED.`

Created: 2026-07-27 UTC

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`
Method: commit-addressed reads only (`git archive` of the pin to scratch outside both
repositories), under enforced isolation. No engine import, no execution.

Companion output: [`EA-4-GATE-INVENTORY.csv`](EA-4-GATE-INVENTORY.csv)
Adjudicated against: [`EA-3-CLAIMED-CONTRACT.md`](EA-3-CLAIMED-CONTRACT.md)

Governing plan: [`../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md) § EA-4.

---

## 0. Preflight addition — `docs/system_logic_map.md` classified

Per Dustin's authorization, `docs/system_logic_map.md` is **classified as an authorized EA-4
contract source** and logged here rather than by amending EA-3.

| Field | Value |
|---|---|
| Path at pin | `docs/system_logic_map.md` |
| Git blob | `550c33fb10069c4bc23b60be8419dfabd7b3c31c` |
| SHA-256 | `647a45f7ffb62a2a055d7b8264c6b48d59f13e87ed7c2b51a37cab7b506fbab0` |
| Bytes | 9,891 |
| Read scope | **FULL** |
| Classification | **Claimed-contract source only — not evidence of implemented behaviour** |

A second contract-class document was required to resolve the mandated E-6 question and is
logged on the same terms:

| Path at pin | Git blob | SHA-256 | Bytes | Scope |
|---|---|---|---|---|
| `docs/architecture.md` | `ce2686f265e1a7836de0c5ae09c82f6074218b53` | `bdb504dbc79647087e66e489fe0e5dc48d07b959cda247e8c1d9655981ac2c17` | 19,071 | §4–§6 (`_run_decision_gates`, observational builds, contract finalize) |

Neither is a findings document; both are outside the EA-3 withheld corpus, which remains unread
in full.

**Containment re-established before any read:** DNS egress blocked (`gaierror`), direct-IP
egress blocked (`OSError [Errno 101] Network is unreachable`), in-boundary write succeeded, and
writes into both `Projects/strategy/` and `Projects/cuttingboard/` blocked (`OSError`).

---

## 1. Production entrypoint and layer order — VERIFIED

`__main__.py` → `runtime.cli_main` → `execute_run` → `_run_pipeline`.

`system_logic_map.md` claims an 11-layer strict order (config → ingestion → normalization →
validation → derived → structure → regime → qualification → options → chain_validation →
contract, then output/delivery/audit). The module set and its sequence are consistent with the
call graph traced in `_run_pipeline`. **Claim upheld as to ordering.**

**Evaluation cadence** is one invocation per CLI run; `--mode {live,fixture,sunday,verify,prefetch}`
selects the input path, `--date` and `--fixture-file` parameterize it. There is no internal
scheduler in the package; cadence is external (`run_daily.sh`, CI cron), which is outside the
analysed surface.

---

## 2. Terminal outcomes — all three traced to source

**Completion criterion: every terminal outcome traced.** Vocabulary is defined twice —
`output.py:232–234` and `notifications/formatter.py:34–36` (C-9, C-10 upheld).

| Outcome | Origin | Evidence |
|---|---|---|
| `TRADE` | `_run_decision_gates` outcome derivation | `runtime:710–716` — `TRADE` iff `any(decision_is_actionable(d))`; `decision_is_actionable` at `trade_decision.py:119` delegates to `is_actionable_trade(symbol, status, size_multiplier)` |
| `NO_TRADE` | same site, negation | `runtime:710–716` |
| `HALT` — cause 1, validation | `validation.py:104–122` — any `config.HALT_SYMBOLS` quote missing or invalid sets `system_halted=True`, `halt_cause=HaltCause.VALIDATION` | halts the pipeline entirely |
| `HALT` — cause 2, kill switch | `runtime:931–936` — sets `outcome = OUTCOME_HALT`; escalation **reuses the validation HALT carrier** so downstream consumers treat it identically, while a distinct `kill_switch` summary flag preserves the distinction | `runtime:2194–2204` |
| `HALT` — cause 3, error contract | `runtime:292` and `runtime:597` — `build_error_contract` sets `outcome = OUTCOME_HALT` on an unhandled exception | |

**Divergence D4-1 — INFORMATIONAL.** `system_logic_map.md` § *Output contract* states "Every run
produces exactly one outcome" and lists three. Source confirms three *values* but **three
distinct HALT origins**, one of which (error contract) is an exception path the claimed contract
does not mention. Recorded; not a defect judgement — that is EA-5's.

---

## 3. E-6 RESOLVED — the five-gate / four-named-gate discrepancy

**This was EA-4's mandated adjudication item, and it is resolved with documentary evidence.**

The docstring at `runtime/__init__.py:635` says "PRD-236: the five-gate decision chain". EA-1
observed four `apply_*` gate functions and flagged the count as UNKNOWN.

`docs/architecture.md` §4 enumerates the chain explicitly, and it is **five steps counting the
materialization step first**:

1. `create_trade_decision` (`trade_decision.py`) — materializes a `TradeDecision` from candidate
   + qualification + setup + **chain result**
2. `apply_execution_policy_to_decisions` (`execution_policy.py`)
3. `apply_thesis_gate` (`trade_thesis.py`)
4. `apply_invalidation_gate` (`invalidation.py`)
5. `apply_entry_quality_gate` (`entry_quality.py`)

**Resolution:** the fifth member is **`create_trade_decision`** — the materialization step is
counted as gate 1 of the chain, and it is where the chain-validation result enters the decision.
The terminal outcome derivation (PRD-162) is **explicitly separate** in the same section and is
**not** counted as a sixth gate.

The docstring is therefore internally consistent with the architecture document. **EA-1's
observation was correct but incomplete**: it counted only the functions named `apply_*`. The
inventory records `DEC1_MATERIALIZE` with `contract_divergence_flag =
COUNTED_AS_GATE_IN_DOCSTRING` so the naming asymmetry stays visible — four of five members are
`apply_*` gates that can convert `ALLOW_TRADE → BLOCK_TRADE`; the first is a constructor that
cannot.

---

## 4. Gate inventory — 30 rows

[`EA-4-GATE-INVENTORY.csv`](EA-4-GATE-INVENTORY.csv) carries one row per gate with the ten
required columns, plus a `layer` column added for grouping (11 columns total). Composition:

| Layer | Rows | Note |
|---|---|---|
| System | 3 | validation HALT, kill switch, regime short-circuit |
| DIRECT | 11 | the claimed 11 gates — **C-1 upheld** |
| CONTINUATION | 9 | its own sequence — **C-6 upheld** |
| POST_HOC | 1 | `PULLBACK_IMBALANCE` upgrade — **C-6 upheld** |
| DECISION | 5 | the five-step chain of §3 |
| TERMINAL | 1 | outcome derivation |

**Hard/soft partition — C-2 and C-3 upheld.** `qualification.py:54–56`:
`HARD_GATES = {REGIME, CONFIDENCE, DIRECTION, STRUCTURE}` (4);
`SOFT_GATES = {STOP_DEFINED, STOP_DISTANCE, RR_RATIO, MAX_RISK, EARNINGS, EXTENSION, TIME}` (7).

**C-7 upheld.** Gate 9 `EARNINGS` fails open — unknown/False ⇒ PASS, and the skip is recorded in
`gates_skipped` (`qualification.py:498–507`).

**Fail-open versus fail-closed.** Gate 9 is the **only** fail-open gate on the DIRECT path.
Every other gate, the three system-level gates, and all four `apply_*` decision gates are
fail-closed.

---

## 5. Contract-versus-code divergences

Five recorded. Each is an **observation with evidence**, not a defect ruling — defect
classification is EA-5's.

### D4-2 — `Polygon fallback` is claimed but absent from the pinned source

`system_logic_map.md` § *Runtime Decision Flow* line 2 claims:
`ingestion.py — fetch RawQuote (yfinance primary, Polygon fallback)`.

A case-insensitive search for `polygon` across the entire `cuttingboard/` package at the pin
returns **zero hits**. The declared dependency set (`pyproject.toml`) names no Polygon client.
EA-1 independently enumerated the network clients as `requests` and `yfinance` only.

**Consequence:** the claimed contract asserts provider redundancy the implementation does not
have. A reader relying on this document would believe quote acquisition degrades to a second
provider; at the pin it does not.

### D4-3 — kill-switch thresholds live outside `config.py`

`system_logic_map.md` presents `KILL_SWITCH_VIX_LEVEL` (35), `KILL_SWITCH_VIX_PCT_CHANGE`
(0.15), `KILL_SWITCH_SPY_PCT_CHANGE` (0.03) in a table headed "Constant".

They are named constants — but they are defined at **`runtime/__init__.py:2185–2187`**, not in
`config.py`. The strict-`>` comparison claim is **upheld** (`runtime:2200–2202`).

**Consequence for EA-11 (fitting).** The `config.py` surface of 52 numeric constants is **not**
the complete tunable surface. Three thresholds that can force a terminal HALT sit outside it.
Any parameter-ownership map built only from `config.py` would silently omit them.

### D4-4 — Gates 1–2 are implemented twice

The STAY_FLAT/confidence test exists at two sites:

- **System-level:** `_check_regime_gates` (`qualification.py:803–820`), called first by
  `qualify_all` (`qualification.py:166–168`), which returns immediately with
  `regime_short_circuited=True` — no per-symbol work runs.
- **Per-candidate:** `qualify_candidate` Gate 1 (`:368–377`) and Gate 2 (`:378–387`), reading the
  same `config.MIN_REGIME_CONFIDENCE`.

**C-claim upheld:** `system_logic_map.md`'s "STAY_FLAT posture short-circuits all per-symbol
qualification; no gates run" is **correct** — `qualify_all` does short-circuit.

**But the duplication is real.** Under `qualify_all` the per-candidate copies are unreachable
when the regime fails; a caller invoking `qualify_candidate` directly bypasses the
short-circuit and hits the duplicated logic instead. Two code paths, one threshold.
`verify_run_summary` (`runtime:1584–1585`) adds a third, post-hoc assertion —
"STAY_FLAT runs must not qualify trades".

### D4-5 — the audit doctrine's canonical write site does not resolve

`docs/audit_doctrine.md` Rule 1 states: "The one canonical write site is at
`runtime.py:1004` via `write_audit_record(...)`."

At the pin there is no `cuttingboard/runtime.py` — the module is the package
`cuttingboard/runtime/__init__.py`, and the sole `write_audit_record(` call site is at
**line 1124**.

**C-17 upheld in substance** — exactly one pipeline write site exists, and
`_execute_notify_run` contains none. The *citation* is stale in both module path and line
number.

### D4-6 — CONTINUATION omits the ATR stop floor that DIRECT enforces

Gate 6 on the DIRECT path enforces `config.STOP_ATR_FLOOR_K` alongside `config.MIN_STOP_PCT`
(`qualification.py:422–444`). The CONTINUATION path's stop check deliberately does **not**
apply an ATR floor, and the source states why (`qualification.py:741–753`, PRD-240 R6): adding
one would combine with the R:R ceiling into "a ~0.5×ATR-wide qualifying band — a de facto path
shutdown deliberately not enacted."

Recorded as an intentional, documented asymmetry between two paths that both produce
`qualified=True` results. Flagged `ASYMMETRIC_WITH_GATE6` in the inventory. Whether the two
paths' outputs are comparable for attribution is **EA-10's** question, and it must not be
assumed.

---

## 6. Threshold ownership — all 52 `config.py` constants assigned

**Completion criterion met.** Mechanical sweep of `config.py` for module-level numeric
constants, then a package-wide reference scan excluding the definition file.

- **Constants found: 52** — matches EA-1 E-7 exactly.
- **Assigned an owning consumer: 51.**
- **Unused within the package: 1.**

| Constant | Site | Finding |
|---|---|---|
| `INTRADAY_ALERT_COOLDOWN` | `config.py:117` | **No reference anywhere in `cuttingboard/` outside its own definition.** Marked UNUSED |

Ownership concentrates as follows: `qualification.py` owns 18 (the DIRECT gates, the FVG set,
and the CONTINUATION set), `regime.py` 5, `derived.py` 5, `ingestion.py` 4,
`overnight_policy.py` 4, `flow.py` 3, `correlation.py` 3, `structure.py` 3,
`execution_policy.py` 2, `evaluation.py` 1, `contract.py` 1, `validation.py` 1,
`market_map.py` 1 (several are read by more than one module; the full first-consumer mapping is
reproducible with the sweep described above).

**Plus the three kill-switch constants outside `config.py`** (D4-3), giving a decision-relevant
threshold surface of **54**, not 52.

---

## 7. Observability — where per-gate detail is lost

**Finding D4-7.** `QualificationResult` (`qualification.py`) carries `gates_passed: list[str]`
and `gates_failed: list[str]` — the full per-gate vector, computed for every candidate.

`audit.py` does **not** persist them. Its per-candidate entries carry `block_reason`
(`audit.py:142,183`) and `missing_conditions` (`audit.py:196`). A grep for
`gates_passed|gates_failed|gates_skipped` across `audit.py` returns **no hit**.

**Consequence:** the engine computes the per-gate PASS/FAIL vector and **discards it at the
audit boundary.** This is recorded in the inventory as `COMPUTED_NOT_PERSISTED` on all 11
DIRECT gates.

This is the concrete, source-level form of the tension EA-3 recorded as C-18/C-20 (one flattened
snapshot per invocation, ~1 record per trading day) and C-26 (the reason fields exist but "are
not consumed by any aggregator today"). **The information EA-6's trace schema needs is already
computed in memory** — the gap is persistence, not derivation. That is the single most useful
result EA-4 hands to EA-6.

By contrast, the CONTINUATION path's rejection reasons **are** aggregated, into per-reason
counters via `_build_continuation_audit` (`qualification.py:965`) — the nine counters EA-2
observed emitted on its run. So the two paths have **asymmetric observability**: CONTINUATION
rejections are counted; DIRECT per-gate results are not.

---

## 8. State owners, isolation, and mutation boundaries

**Claimed** (`system_logic_map.md`): sidecars must not mutate contracts, payloads, trade
decisions, qualification gates, market_map grades, notifications, or existing dashboard
artifacts; `contract.py:build_pipeline_output_contract` output is "final".

**Traced:** `contract.py`'s module docstring states it is "the only place that translates
internal runtime objects into the canonical output shape. Renderers read from this dict; they do
not inspect runtime internals after contract creation" — **C-11 upheld**.

However `architecture.md` §6 describes `_build_and_finalize_contract` as "contract build + every
post-build runtime **mutation**", and `contract_types.py:40–58,111–133` marks `outcome`,
`permission`, `reason` as `NotRequired` runtime injections "required at finalization, never at
build".

**Recorded, not adjudicated:** "output is final" and "every post-build runtime mutation"
describe the same boundary from two directions. The reconciling reading is that mutation is
confined to the finalizer and forbidden to *sidecars*. Whether any sidecar in fact mutates is
**EA-5's** question; EA-4 records only that the contract *permits* post-build injection by the
finalizer.

**Temporal isolation.** In fixture mode `run_at_utc = max(fetched_at_utc)` over the fixture and
`run_id = "{mode}-fixture-{stem}"` (`runtime:2293–2312`) — no wall-clock dependence. EA-2
demonstrated this empirically (byte-identical output across two clean sandboxes).

**Symbol isolation.** Qualification is per-symbol within `qualify_all`; the system-level regime
gate is evaluated once and applied to all. `_run_decision_gates` raises `RuntimeError` on a
candidate-join miss (`runtime:655–661`, PRD-260 R5) rather than silently dropping — a
fail-loud invariant.

---

## 9. Re-test of the TV-0 gate inventory

The TV-0 line is closed (`closure/TV-LINE-CLOSURE-2026-07-27.md`) and its
`GATE_TRANSLATION_MATRIX.md` is retained as a **gate-inventory hypothesis** to re-test, per the
plan §4.

**Result: the DIRECT gate inventory is confirmed and now carries source line ranges.** The 11
gate identifiers in `qualification.py:42–52` match the eleven-gate structure TV-0 catalogued, and
the hard/soft partition matches. What TV-0's matrix could not capture, and what this map adds:

- the **CONTINUATION** path's nine-step sequence with its own thresholds (`C1`–`C9` in the
  inventory);
- the **PULLBACK_IMBALANCE** post-hoc upgrade;
- the **three system-level gates** ahead of all per-candidate work;
- the **five-step decision chain** after qualification;
- three thresholds outside `config.py` (D4-3).

A translation that reproduced only the 11 DIRECT gates would model a strict subset of the
implemented decision system. Recorded as the substantive vindication of superseding the proxy
line — the engine's decision surface is materially larger than the proxy's.

---

## 10. Adjudication summary against EA-3's claims

| Claim | Verdict | Evidence |
|---|---|---|
| C-1 11 gates in sequence | **UPHELD** | `qualification.py:42–52`, comment markers 368–540 |
| C-2 hard/soft partition 4/7 | **UPHELD** | `qualification.py:54–56` |
| C-3 soft arithmetic 1⇒watchlist, 2+⇒reject | **UPHELD** | `qualification.py:416–540`, `_hard_reject:922` |
| C-4 no partial credit | **UPHELD** | binary append to `gates_passed`/`soft_failures` |
| C-5 outcome logic table | **UPHELD** structurally | `QualificationResult` fields match the four claimed states |
| C-6 three entry modes | **UPHELD** | `ENTRY_MODE_*` at `:37–39`; `_qualify_continuation_candidate:687`; `_resolve_entry_mode:823` |
| C-7 Gate 9 fails open | **UPHELD** | `:498–507`, `gates_skipped` |
| C-8 no auto-promotion of watchlist | **NOT ADJUDICATED** — requires cross-run behaviour, not statically decidable | — |
| C-9 three terminal outcomes | **UPHELD** | §2 |
| C-10 duplicated outcome vocabulary | **UPHELD** | `output.py:232–234`, `formatter.py:34–36` |
| C-11 single canonical contract builder | **UPHELD**, with the finalizer-injection nuance | §8 |
| C-12 `PipelineContract` v2 keys | **UPHELD** | `contract_types.py:111–133` |
| C-13 `rejections` first-class key | **UPHELD as declared**; population fidelity not traced | `contract_types.py:123` |
| C-14 `DecisionTrace` three non-empty strings | **UPHELD as declared** | `contract_types.py:60–66` |
| C-15 `SystemState` fields | **UPHELD** | `contract_types.py:40–58` |
| C-16 two record families in one file | **UPHELD** | `audit.py` two writers |
| C-17 one pipeline write site, none in notify | **UPHELD in substance; citation stale** | D4-5 |
| C-18 one record per invocation | **UPHELD** | single call site `runtime:1124` |
| C-19/C-20/C-21 consumer filter, density, non-guarantees | **UPHELD as doctrine** | `audit_doctrine.md` |
| C-22/C-23/C-24 artifact categorization, degradation, sidecars | **UPHELD as declared** | `artifact_flow_map.md` |
| C-25…C-28 the four claimed gaps | **CORROBORATED for C-26 and C-28** by §6 (unused constant, no re-tuning convention) and §7 (per-gate vector discarded) | — |
| C-29/C-30/C-31 document-kind claims | **UPHELD** | — |
| **New divergences** | **D4-1 … D4-7**, none of which EA-3's claims predicted | §2, §5, §7 |

---

## 11. Completion statement

- **Every terminal outcome traced to source** — three values, five origins (§2).
- **Every `config.py` constant assigned an owning gate or marked unused** — 52 found, 51
  assigned, 1 UNUSED, plus 3 decision-relevant thresholds located outside `config.py` (§6).
- **The gate-count discrepancy resolved with evidence** — `docs/architecture.md` §4; the fifth
  member is `create_trade_decision` (§3).
- Gate inventory delivered with all ten required columns, 30 rows (§4).
- TV-0 inventory re-tested; divergences recorded (§9).

**No stop condition fired.** The map was completed without executing any engine behaviour, and
**no withheld findings document was consulted** — the EA-3 withheld corpus remains unread.

**EA-5 is not authorized by this document.** Defect classification, fixture construction, and
finding discovery are EA-5's, gated on Dustin's review of this map and inventory.

## 12. Amendment rule

Frozen from creation; never edited in place. A correction is a dated amendment file or a new
versioned map, with the version in the filename (`docs/conventions.md` §b, read across by §h).
