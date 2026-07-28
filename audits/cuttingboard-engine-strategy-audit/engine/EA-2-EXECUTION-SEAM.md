# EA-2 — Execution Seam Proof Under Enforced Isolation

Status: `ACTIVE — SEAM PROVEN. CONTAMINATION PREVENTED BY ENFORCEMENT.`

Created: 2026-07-27 UTC

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`

Binding inputs:
[`EA-1-EXECUTION-SAFETY-MAP.md`](EA-1-EXECUTION-SAFETY-MAP.md) ·
[`EA-1-ISOLATION-REQUIREMENTS.md`](EA-1-ISOLATION-REQUIREMENTS.md)

Governing plan: [`../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md) § EA-2.

---

## 0. Question and epistemic boundary

**Question:** does the pinned engine run deterministically with contamination *prevented by
enforcement*, and does observed behaviour match the EA-1 prediction?

**This document reports seam properties only.** It records what the environment did — what was
written, what was blocked, whether two runs agree. It offers **no interpretation of the
engine's decision output**: no replay analysis, no attribution, no scoring, no evaluation of
trade quality. Those are EA-3 and later, and are separately gated.

---

## 1. Provenance

| Item | Identity |
|---|---|
| Source pin | `59f8279d796335149afdec4aa507b6f927233518` |
| Acquisition | `git archive <pin> \| tar -x` into scratch **outside both repositories** |
| Never used | `git worktree add`, checkout, fetch, ref change, working-tree read |
| `config.toml` consumed (EA-1 R-8) | SHA-256 `329c2ea58ee2373eb8722b738b9cc6453c4d4b359c57657b32da2db4524318cb`, from the extracted tree |
| `[engine_doctor] runtime_gate_enabled` (EA-1 R-10) | **`false`** — verified in the extracted tree before the run; the §3 subprocess therefore did not fire |
| Interpreter | CPython 3.13.5, x86_64 (engine requires `>=3.11`) |
| Environment lockfile | [`env/EA-2-ENVIRONMENT-LOCK.txt`](env/EA-2-ENVIRONMENT-LOCK.txt), 129 packages, SHA-256 `3fd88335fb95aee68a18c06e0ced50f1d35ba47f7107690a54e2df3f4c5300d0` |
| Fixture | `tests/fixtures/2026-04-12.json` from the extracted tree (read-only mount) |
| Run identity | `mode=FIXTURE`, `generation_id=fixture-fixture-2026-04-12`, `run_at_utc=2026-04-12T13:00:00Z` |

**Environment provenance note — recorded, not interpreted.** All six declared dependencies were
already present and satisfy the declared constraints, so **no network install was performed**.
The resolved versions are materially newer than the declared floors — notably
`pandas==3.0.2` against `pandas>=2.0.0`, and `yfinance==1.2.1` against `yfinance>=0.2.40`. The
lockfile is therefore a **capture of the environment actually used**, not a resolution pinned at
the engine's authoring era. Any later phase comparing results across environments must treat
this as a variable.

---

## 2. Enforcement — proven, not inferred

Full transcripts: [`runs/EA-2/isolation-enforcement-proof.txt`](runs/EA-2/isolation-enforcement-proof.txt).

Sandbox: `bwrap --unshare-net --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind $RUNDIR $RUNDIR --chdir $RUNDIR`, with `env -i` supplying an explicit environment. Entire filesystem read-only; **exactly one writable bind.**

| Control | Requirement | Result |
|---|---|---|
| **B1** DNS egress to `api.telegram.org:443` | must fail | `gaierror: [Errno -3] Temporary failure in name resolution` — **blocked** |
| **B2** direct-IP egress to `1.1.1.1:443`, `8.8.8.8:53` | must fail | `OSError: [Errno 101] Network is unreachable` — **blocked** |
| **C1** in-boundary write | must succeed | succeeded |
| **C2** write to `…/Projects/strategy/` | must fail | `OSError` — **blocked** |
| **C3** write to `…/Projects/cuttingboard/` | must fail | `OSError` — **blocked** |
| **C4** write to `/etc/` | must fail | `OSError` — **blocked** |

B2 exists because B1 alone would only prove DNS was unavailable. `Errno 101` proves **no route**.
Enforcement is at namespace level and is independent of `--mode fixture`, satisfying EA-1 R-1
and R-2.

Per EA-1 R-3, the unset `TELEGRAM_*` variables are recorded as defence in depth and are
**explicitly not** treated as isolation proof.

---

## 3. Observed write-set

Two clean sandboxes, pre-snapshot empty (only `logs/`, `reports/output/`, `data/cache/`
pre-created per EA-1 R-6). Engine exit code **0** on both runs.

**Nine files, all inside the writable boundary. Nothing escaped.**

| Path (relative to run dir) |
|---|
| `logs/audit.jsonl` |
| `logs/latest_contract.json` |
| `logs/latest_payload.json` |
| `logs/latest_run.json` |
| `logs/macro_drivers_snapshot.json` |
| `logs/market_map.json` |
| `logs/run_2026-04-12_130000.json` |
| `reports/2026-04-12.md` |
| `reports/output/report.html` |

Per-file SHA-256: [`runs/EA-2/run1-writeset.sha256`](runs/EA-2/run1-writeset.sha256) and
[`runs/EA-2/run2-writeset.sha256`](runs/EA-2/run2-writeset.sha256).

**Only manifests and hashes are preserved in this repository — not the engine payloads.** EA-2
proves the seam; it does not create datasets.

---

## 4. Determinism

**Result: byte-identical across two independent clean sandboxes.**

- File sets identical (`diff` of sorted path lists: empty).
- **Every one of the nine files byte-identical** (`diff` of the two SHA-256 manifests: empty).

No canonical-payload / run-envelope partition (plan §8) was required, because **no
nondeterministic metadata leaked into any artifact**. This is consistent with the fixture-mode
identity derivation EA-1 recorded: `run_at_utc` comes from the fixture rather than the wall
clock, and `run_id` is fixture-derived. Determinism is **demonstrated**, not refuted.

---

## 5. Prediction versus observation

EA-1 §1.3 predicted a write-set. **Observed is a strict subset of predicted — the map
over-predicted, and nothing unpredicted appeared.** Every divergence is recorded below, as the
plan requires.

### 5.1 Predicted and observed — 9 of 9 observed items were predicted

`logs/audit.jsonl`, `logs/latest_run.json` + timestamped summary (`run_2026-04-12_130000.json`),
`logs/latest_contract.json`, `logs/market_map.json`, W-13 macro/payload artifacts
(`macro_drivers_snapshot.json`, `latest_payload.json`), `reports/<date>.md`, and — from the
INFERENCE-conditional tier — `reports/output/report.html`.

**No unpredicted write occurred.**

### 5.2 Divergences — predicted but not observed

| # | Predicted item | EA-1 label | Cause in pinned source | Assessment |
|---|---|---|---|---|
| D-1 | `logs/evaluation.jsonl` | VERIFIED reachable | `evaluation.py:50–51` — `run_post_trade_evaluation` returns early when `prior_record is None`; a fresh sandbox has no prior same-day run | **Data/state-dependent branch.** Map over-predicted by not qualifying the precondition |
| D-2 | `logs/performance_summary.json` | VERIFIED reachable | `performance_engine.py:30–31` — returns early when `evaluation_log_path` does not exist; a direct consequence of D-1 | **Data/state-dependent branch**, same class as D-1 |
| D-3 | `logs/trend_structure_snapshot.json` | VERIFIED reachable | `runtime:2101–2102` — `_refresh_trend_structure_sidecar` returns on `if mode != MODE_LIVE`. Its docstring states "Fixture/Sunday modes are excluded" | **Mode-gated. The map's fixture-path claim for W-11 was wrong** |
| D-4 | `logs/watchlist_snapshot.json` | VERIFIED reachable | `_write_watchlist_snapshot` is called only at `runtime:564`, inside `_execute_notify_run` — the notify path, not the plain `--mode fixture` path | **Call-site attribution error. The map's fixture-path claim for W-12 was wrong** |

Conditional predictions that correctly did not fire: `logs/regime_history.jsonl`,
`logs/last_notification_state.json` (no send occurred), `data/cache/*.parquet` (write patched
out in fixture mode), `./traceback.txt` (not on this path).

### 5.3 Confirmed EA-1 map defects — D-3 and D-4

D-3 and D-4 are not data-dependence; they are **incorrect reachability claims** in EA-1 §1.2
rows W-11 and W-12, of the same class the map got right for W-09 and W-19. D-1 and D-2 are
weaker: the call sites are genuinely on the path, but the map asserted `VERIFIED reachable`
without qualifying the runtime preconditions.

**Direction matters.** All four divergences are **over-predictions**. The observed set is a
strict subset of the predicted set, no unpredicted write occurred, and no isolation reasoning
depended on the four items — EA-1 R-6 pre-creates `logs/`, which covers them whether or not
they fire. The map was conservative, which is the safe direction for an isolation
specification.

**EA-1's outputs are not edited by this document.** Under `docs/conventions.md` §b (read
across by §h) a correction is a dated amendment or a new versioned file, and this packet
authorizes neither. **Recorded for Dustin's decision:** whether to amend EA-1 §1.2/§1.3 for
W-11 and W-12 before EA-3.

### 5.4 EA-1 undecidables — resolution status (R-18)

| # | Item | Resolution |
|---|---|---|
| U-01 | Were the unpatched network paths (EA-1-N1/N2) taken? | **Not taken on this input.** No network-attempt evidence in either run's stderr. Consistent with `total_candidates=0`, so `_apply_intraday_short_permission` had no `SHORT` candidate to fetch for. **This does not retire EA-1-N1** — it remains a source-level fact about an unpatched path; this input simply did not reach it. R-1 must stay in force |
| U-02 | Third-party cache/temp writes inside the boundary? | **None observed.** The nine observed files are all engine artifacts; no library cache appeared |
| U-03 | `dashboard_renderer` `output_path` (W-17) | **Resolved to `reports/output/report.html`** on this path — inside the boundary |
| U-04 | Any `.env` discovered? | **None.** Verified absent from the run dir and the extracted tree before the run |
| U-05 | Behaviour on read-only/absent output dirs | **Not exercised** — directories were pre-created per R-6. Remains undecidable |
| U-06 | Dependency network I/O at import time | **None observed** — imports completed inside a no-route namespace without error |
| U-07 | Full transitive closure | **Captured** — 129 packages in the lockfile |
| U-08 | `engine_doctor` writes | **Not exercised** — gate verified `false`; subprocess did not fire. Remains undecidable |

---

## 6. Stop conditions — none fired

| Stop condition | Result |
|---|---|
| Any write outside the confinement boundary | **None.** All nine writes inside; three deliberate escape attempts blocked |
| Any successful outbound connection | **None.** Both control calls blocked; no engine network attempt observed |
| Divergence the map did not anticipate as possible | **None in the dangerous direction.** All four divergences are over-predictions; no unpredicted write or connection occurred. D-3/D-4 are recorded as map defects for amendment, per §5.3 |
| Any need to edit pinned source to make it run | **None.** The engine ran unmodified at the pin |
| Any CuttingBoard git-metadata change | **None.** `HEAD` and `status --porcelain` byte-identical before and after |

One environment-construction iteration occurred before the successful run: an initial attempt
used `env -i` with a remapped `HOME`, which hid the user site-packages and produced
`ModuleNotFoundError: No module named 'pandas'` **before any engine code executed**. The
dependency path was added to `PYTHONPATH` and the run repeated in a clean sandbox. Recorded for
completeness; it changed no control and no scope.

---

## 7. Completion statement

Every EA-2 completion criterion is met:

- **Isolation enforcement demonstrated by failed control calls** — network (DNS *and* direct-IP)
  and write (three out-of-boundary targets). §2.
- **Observed write-set enumerated and entirely inside the writable directory** — nine files. §3.
- **Prediction-versus-observation divergences recorded** — four, all over-predictions, two of
  them confirmed EA-1 map defects. §5.
- **Determinism demonstrated** — all nine artifacts byte-identical across two clean sandboxes. §4.
- **CuttingBoard byte-unchanged** — `HEAD` and `status` identical before and after. §1, §6.

**EA-3 is not authorized by this document.** The plan gates further work on Dustin's review of
this seam report.

## 8. Amendment rule

Frozen from creation; never edited in place. A correction is a dated amendment file or a new
versioned report, with the version in the filename (`docs/conventions.md` §b, read across by §h).
