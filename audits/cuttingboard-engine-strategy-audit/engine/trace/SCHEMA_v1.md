# EA-6 — Decision Trace Schema v1

Status: `ACTIVE — SCHEMA SPECIFIED AND EXERCISED. HELD FOR DUSTIN APPROVAL BEFORE SCALE CAPTURE.`

Schema version: `EA-6-trace/v1` · Wrapper version: `EA-6-capture/1.0.0`

Created: 2026-07-28 UTC

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`
Capture tool: [`../tools/trace_capture/capture.py`](../tools/trace_capture/capture.py)
Emitted cases: [`EA-6-cases/`](EA-6-cases/)

Governing plan: [`../../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](../../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md) § EA-6, § 8.

---

## 0. Binding principles

1. **The wrapper observes; it never instruments.** `capture.py` runs the pinned engine under
   the EA-2 seam and reads the artifacts the engine itself wrote. It does not import engine
   modules, patch them, or modify pinned source in any way.
2. **No value is ever invented.** Where the engine does not expose a field, the trace carries
   the literal string `NOT_OBSERVABLE`, plus a `_note` naming why. Inference, reconstruction,
   and synthesis are all forbidden — a hole is recorded as a hole.
3. **Canonical payload versus run envelope.** Every trace is partitioned. Only the canonical
   payload is ever compared.

---

## 1. Partition

### 1.1 `canonical_decision_payload` — deterministic, compared

Canonically serialized: `sort_keys=True`, UTF-8, `indent=2`, newline-terminated. Contains
**engine-derived timestamps only** (`run_at_utc`, itself `max(fetched_at_utc)` in fixture
mode). Contains **no** wall-clock capture time, **no** absolute path, and **no** host- or
sandbox-specific value.

### 1.2 `run_metadata_envelope` — recorded, never compared

`run_dir_basename`, `pipeline_record_count`, `artifacts_present`. Enumerated in every trace
under `envelope_excluded_from_equality`, so exclusion is explicit rather than implied.

**Every reproduction claim in this program applies to the canonical payload only.**

---

## 2. Field map — required field → source → status

| § 8 requirement | Trace path | Source artifact | Status |
|---|---|---|---|
| Snapshot SHA | `identities.snapshot_sha` | supplied at capture, pinned | **populated** |
| Config SHA | `identities.config_sha256` | `config.toml` in the extracted pin | **populated** |
| Environment hash | `identities.environment_lock_sha256` | EA-2 lockfile | **populated** |
| Wrapper version | `identities.wrapper_version` | tool constant | **populated** |
| Schema version | `identities.schema_version` | tool constant | **populated** |
| Fixture identity | `identities.fixture_sha256` | computed | **populated** |
| Evaluation timestamp | `temporal.run_at_utc` | `logs/latest_run.json` | **populated** |
| — | `temporal.generation_id`, `temporal.session_date` | run summary / contract | **populated** |
| **As-of boundary** | `temporal.as_of_boundary` | — | **`NOT_OBSERVABLE`** — the engine derives `run_at_utc` from `max(fetched_at_utc)` and publishes no distinct as-of field |
| Symbol identity | `inputs[].symbol` | fixture | **populated** |
| Input provenance | `inputs[].source`, `.units`, `.fetched_at_utc` | fixture | **populated** |
| Input timestamps / freshness | `inputs[].fetched_at_utc`, `.age_seconds` | fixture | **populated** — see §4 on `age_seconds` fidelity |
| Missing-data mask | `missing_data_mask.*` | fixture + audit record | **partially populated** — see finding EA-6-003 |
| Raw + normalized evidence | `inputs[]` | fixture | **populated (raw)**; normalized values are not republished by the engine |
| Intermediate classifications / scores | `intermediate_state.regime`, `.posture`, `.confidence`, `.router_mode`, `.energy_score`, `.index_score`, `.kill_switch`, `.system_halted` | run summary | **populated** |
| — regime vote detail | `intermediate_state.regime_vote_detail` | — | **`NOT_OBSERVABLE`** |
| — structure labels | `intermediate_state.structure_labels` | — | **`NOT_OBSERVABLE`** |
| Candidate identity | `opportunities[].symbol` | contract | **populated** |
| **Per gate: PASS/FAIL/UNKNOWN/NOT_EVALUATED/INERT** | `opportunities[].gate_results` | — | **`NOT_OBSERVABLE`** — finding EA-6-001, the central gap |
| Ordering / override / precedence events | `ordering_and_precedence.gate_order_events` | — | **`NOT_OBSERVABLE`** — finding EA-6-002 |
| — regime short-circuit | `ordering_and_precedence.regime_short_circuited`, `.regime_failure_reason` | audit record | **populated when present** |
| Terminal decision | `terminal.outcome` | run summary / contract | **populated** |
| — statuses | `terminal.contract_status`, `.summary_status`, `.process_exit_code` | both | **populated** |
| **Machine-readable reason codes** | `terminal.machine_reason_codes` | — | **`NOT_OBSERVABLE`** — finding EA-6-004; the engine emits prose |
| Human-readable explanation | `opportunities[].explanation` | contract | **populated when the engine supplies it** |
| Proposed entry / invalidation / target / sizing | `opportunities[].geometry.*` | contract | **populated for evaluated candidates** |
| Execution assumptions | `opportunities[].decision_trace`, `.block_reason` | contract | **populated** |
| Realized outcomes | `canonical.realized_outcomes` | — | **`NOT_OBSERVABLE` by design** — attached later, versioned separately (plan § 8) |

---

## 3. Evaluation-opportunity preservation

The plan requires **every** evaluation opportunity preserved — accepted, rejected and halted.
The schema models this as one `opportunities[]` list with an explicit `disposition`:

- `EVALUATED_CANDIDATE` — reached the decision layer; carries decision status, block reason,
  decision trace, entry mode, geometry.
- `REJECTED` — carries `stage`, `reason`, `detail` from the contract's `rejections` list.

Observed counts across the emitted cases: **19–20 opportunities per non-halt run** (7–8
evaluated candidates plus 12–13 rejections). The contract's `rejections` key is genuinely
populated with per-symbol reasons — EA-3 claim C-13 upheld **with fidelity**, not merely as a
declared key.

**On a HALT the list is empty.** Both halt cases emit zero opportunities, because the halt
suppresses the qualification block entirely. Recorded as finding **EA-6-005**.

---

## 4. Fidelity limits of the fixture seam — stated, not worked around

**`age_seconds` in a fixture is inert for validation.** `runtime._fixture_validation_clock`
patches `cuttingboard.validation.datetime` so `now()` returns `max(fetched_at_utc)` across the
fixture; `validation.py:177–179` then **recomputes** age from timestamps. The fixture's declared
`age_seconds` field is carried into the trace but does not drive the freshness gate.

Consequence for fixture design, learned by doing: a stale-data case must be built by making one
symbol's `fetched_at_utc` older than the newest, not by setting `age_seconds`. The emitted
`stale-data` case does this (PAAS at `11:00:00Z` against `13:00:00Z`), and the engine correctly
reports `INVALID PAAS: age 7200s exceeds 300s freshness threshold`.

---

## 5. Emitted cases

Six reachable cases, each a canonical payload with a recorded SHA-256:

| Case | Outcome | Exit | Opportunities | Payload SHA-256 (prefix) |
|---|---|---|---|---|
| `rejected` | `NO_TRADE` | 0 | 20 (8 cand / 12 rej) | `93afb505…` |
| `boundary-vix-at-35` | `NO_TRADE` | 0 | 20 (7 / 13) | `aaad8958…` |
| `missing-data` | `NO_TRADE` | 0 | 19 (7 / 12) | `f4f01213…` |
| `stale-data` | `NO_TRADE` | 0 | 19 | `e11517fe…` |
| `halted-killswitch` | `HALT` | 1 | 0 | `9da27621…` |
| `halted-validation` | `HALT` | 1 | 0 | `119b11f2…` |

**The `accepted` case is absent and cannot be produced — see finding EA-6-006.** EA-6's
completion criteria are therefore **met for five of six required case types**, and the sixth is
recorded as an unmet requirement with its blocking evidence rather than fabricated.

---

## 6. Reproduction

```sh
# under bwrap --unshare-net, read-only root, single writable bind:
python3 capture.py --src <extracted-pin> --fixture EA-6-cases/fixture-<case>.json \
                   --run-dir <writable> --case-id <case> [--cache <ohlcv-dir>] \
                   --snapshot-sha 59f8279d796335149afdec4aa507b6f927233518 \
                   --env-lock-sha <EA-2 lockfile sha256> --out <trace.json>
```

Case fixtures and emitted traces are in [`EA-6-cases/`](EA-6-cases/) with a `MANIFEST.sha256`.

## 7. Amendment rule

Frozen from creation; never edited in place. A correction is a dated amendment or a new
versioned schema, with the version in the filename (`docs/conventions.md` §b, read across by §h).
