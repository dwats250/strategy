# EA-7 — Deterministic Offline Replay: Design and Results

Status: `ACTIVE — LOGIC PARITY DEMONSTRATED. DATA-PROVIDER PARITY UNAVAILABLE.`

Created: 2026-07-28 UTC

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`

Harness: [`tools/replay/replay.py`](tools/replay/replay.py) (`EA-7-replay/1.0.0`) ·
Input library: [`fixtures/build_inputs.py`](fixtures/build_inputs.py) ·
Capture wrapper: [`tools/trace_capture/capture.py`](tools/trace_capture/capture.py) (`EA-6-capture/1.0.0`) ·
Manifests: [`runs/`](runs/)

Governing plan: [`../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md) § EA-7, § 8,
and the dated **2026-07-28 amendment (EA-6-006)**.

---

## 0. Question and answer

**Question:** does the same observation always produce the same decision, and where exactly does
parity end?

**Answer:** within logic parity, yes — demonstrated, not asserted. Six archived manifests each
reproduce their canonical decision payload **byte-for-byte** when replayed from scratch. Parity
ends precisely at the data-provider boundary and at the accepted path; both are enumerated in
§5 as unavailable rather than estimated.

---

## 1. Architecture

Three composable Strategy-owned tools, none of which imports, patches, or instruments pinned
source:

| Tool | Role |
|---|---|
| `fixtures/build_inputs.py` | Regenerates every input from a base fixture and a declarative case table. No RNG, no wall-clock read, no network. |
| `tools/trace_capture/capture.py` | Runs the pinned engine and maps its own artifacts into the EA-6 trace schema; unreachable fields become `NOT_OBSERVABLE`. |
| `tools/replay/replay.py` | Orchestrates: regenerate inputs → run → capture → hash the canonical payload → compare against the archived manifest. |

**Every replay regenerates its inputs from scratch.** Nothing is carried between passes, so a
match is evidence about the engine and the generator together, not about a cached artifact.

**Execution model** is EA-2's, unchanged: `bwrap --unshare-net`, entire filesystem read-only,
exactly one writable bind, `env -i` with an explicit environment. Isolation was re-established
and proven before every batch (§6).

---

## 2. What is compared, and what is excluded

Comparison is over the **canonical decision payload only**, serialized `sort_keys=True`,
`ensure_ascii=False`, `separators=(",",":")`, UTF-8, then SHA-256.

**Envelope fields are excluded by enumeration, not by implication.** Every trace and every
manifest lists them:

- `run_dir_basename`
- `pipeline_record_count`
- `artifacts_present`

These carry sandbox- and host-specific values. They are recorded and never compared.

**Input identity is content-addressed, not container-addressed.** Parquet embeds writer
metadata, so its bytes are not a stable cross-version identity. `build_inputs.py` therefore
digests the numeric OHLCV content (index plus the five float columns) rather than the file
bytes. Observed at this pin and environment, parquet bytes happened to be stable across
regenerations as well — recorded as an observation, deliberately **not** relied upon.

---

## 3. Results — six archived manifests, all reproducing

Each case was first run twice with independently regenerated inputs (self-consistency), then
replayed a third time **against its archived manifest hash**.

| Run id | Case | Canonical payload SHA-256 | Self-consistent (2 passes) | Reproduces from manifest |
|---|---|---|---|---|
| `EA-7-rejected` | baseline; rejected + evaluated-candidate population | `50982145e651deff…` | ✅ | ✅ |
| `EA-7-boundary-vix-at-35` | `^VIX` exactly 35.0 — strict `>` must not trip | `1839e9653c7047c1…` | ✅ | ✅ |
| `EA-7-halted-killswitch` | `^VIX` 35.01 — must trip to terminal HALT | `e7ed6816332bb098…` | ✅ | ✅ |
| `EA-7-halted-validation` | `SPY` removed — validation HALT | `a8ff926c05ff0aa2…` | ✅ | ✅ |
| `EA-7-stale-data` | `PAAS` timestamp skewed 2h — freshness gate fires | `5969b6b7eeb6af90…` | ✅ | ✅ |
| `EA-7-missing-data` | `PAAS` removed — reduced universe | `f2715eb76dbea417…` | ✅ | ✅ |

**6 of 6 reproduce byte-for-byte.** No case required a source change, and no tolerance,
normalization, or field exclusion beyond the three enumerated envelope keys was introduced to
make a comparison pass.

These hashes differ from the EA-6 trace hashes for the same case names. The reason is recorded
rather than glossed: EA-7 regenerates fixtures canonically (sorted keys, newline-terminated), so
`identities.fixture_sha256` differs, and the fixture identity is part of the payload by design.
EA-6's traces remain valid as EA-6's evidence; EA-7's manifests are the replay contract.

---

## 4. Logic parity versus data-provider parity — kept apart

The plan requires these be separated. They are, and only one of them is testable here.

### 4.1 Logic parity — TESTED, HOLDS

*Definition:* the same inputs, through the same pinned code path, produce the same canonical
decision payload.

*Evidence:* §3. Eighteen engine executions (six cases × two self-consistency passes × one
manifest verification), every canonical payload matching its recorded hash.

*Scope:* covers ingestion of fixture quotes, normalization, validation, derived metrics,
structure, regime, qualification, options, the five-step decision chain, contract assembly, and
terminal outcome derivation — everything the fixture seam reaches.

### 4.2 Data-provider parity — UNAVAILABLE, NOT ESTIMATED

*Definition:* whether reconstructed inputs match what a live CuttingBoard run actually saw.

*Status:* **cannot be tested by this harness, and is not.** Establishing it would require a live
CuttingBoard run's inputs and outputs to compare against, which requires live market data —
forbidden by this charge and by EA-1 R-1.

*What that means concretely:* every EA-7 result is a statement about the engine's behaviour
**given the inputs supplied**. It is **not** a statement that those inputs resemble any real
trading day. The OHLCV series is synthetic by construction and supports no market claim.

*Not inferred:* no attempt is made to argue from logic parity to data-provider parity. They are
different claims and only the first is evidenced.

---

## 5. The non-reproducible set — enumerated

Per the completion criterion, enumerated rather than hand-waved.

| # | Item | Why not reproducible here | Would require |
|---|---|---|---|
| NR-1 | **The accepted path (`outcome = TRADE`)** | Structurally unobservable under the authorized fixture method: `_fixture_chain_results` returns `MANUAL_CHECK` for every setup unconditionally, so every candidate blocks on `"fixture mode skips live chain validation"`. Binding per the 2026-07-28 amendment (EA-6-006). **No accepted-trade quality, frequency, or value claim is made anywhere in EA-7.** | Separate explicit authorization naming a mechanism |
| NR-2 | **Data-provider parity** | §4.2 | Live CuttingBoard inputs/outputs |
| NR-3 | **Per-gate PASS/FAIL vector** | Computed in `QualificationResult`, discarded at the audit boundary (EA5-002 / EA-6-001). Absent from every durable artifact, so replay reproduces its absence faithfully — the hole is stable, not filled | Persisting the vector; a CuttingBoard change under its own charge |
| NR-4 | **Gate ordering / override event stream** | No such stream is emitted (EA-6-002) | Instrumentation, not authorized |
| NR-5 | **Validation-excluded symbols** | Reach stderr only; `excluded_symbols` stays `{}` (EA-6-003). Reproducible as stderr text, **not** as durable structured evidence | Populating the mask |
| NR-6 | **Machine-readable reason codes** | Engine emits prose with interpolated numerals (EA-6-004) | A stable code enum |
| NR-7 | **Opportunity records on a HALT** | A halt suppresses the qualification block; both halt cases legitimately reproduce zero opportunities (EA-6-005) | A design decision, not a replay fix |
| NR-8 | **Realized outcomes** | Out of scope by design — attached later, versioned separately (plan § 8) | A later phase |
| NR-9 | **Live-mode-only artifacts** | `logs/trend_structure_snapshot.json` is mode-gated (`mode != MODE_LIVE`), and `logs/watchlist_snapshot.json` is reachable only from `_execute_notify_run` — per the EA-1 amendment. Neither is produced or replayed by the fixture path | Live mode |

**NR-3 through NR-7 are reproduced faithfully as absences.** That is the correct behaviour for a
replay harness: it reproduces what the engine emits, including what it does not emit. None of
these holes was filled, estimated, or worked around.

---

## 6. Isolation enforcement across the full range

Re-established and proven before every batch, not assumed from EA-2:

| Control | Result |
|---|---|
| DNS egress to `api.telegram.org:443` | blocked — `gaierror` |
| Direct-IP egress to `1.1.1.1:443` | blocked — `OSError [Errno 101] Network is unreachable` |
| In-boundary write | succeeded |
| Write to `/home/dustin/Projects/strategy/` | blocked — `OSError` |
| Write to `/home/dustin/Projects/cuttingboard/` | blocked — `OSError` |

**Isolation was not weakened for convenience at scale.** Every one of the eighteen executions ran
under the same `bwrap --unshare-net`, read-only-root, single-writable-bind policy as EA-2's
single run. Batching changed the loop, never the boundary.

**CuttingBoard integrity:** `HEAD` and `git status --porcelain` byte-identical before and after
the phase, at `9e6b7728b7e9f1c3b63c0fc23f02e3ec031c2f94`. Source obtained by `git archive` at
the pin only.

---

## 7. Completion statement

| Criterion | Status |
|---|---|
| Re-running any archived manifest reproduces its canonical decision payload byte-for-byte | **MET** — 6 of 6 |
| Envelope fields enumerated in the manifest as excluded-by-design | **MET** — three keys, listed in every manifest and every trace |
| The non-reproducible set enumerated rather than hand-waved | **MET** — NR-1 … NR-9 |
| Isolation enforcement holds across the full range | **MET** — §6 |

**No stop condition fired.** Determinism was achieved without any source change, and isolation
was never relaxed.

**Binding limitation carried forward and honoured:** EA-7 ran on observable evidence only — the
selection surface from qualification through the decision chain, plus the rejected and halted
populations. **No accepted-path conclusion is inferred, reconstructed, synthesized, or
estimated anywhere in this document**, and NR-1 records the gap as unavailable. The limitation is
a harness constraint, **not** an engine defect.

**EA-8 is not authorized by this document.** The plan gates it on Dustin's review of this design
and the non-reproducible set.

## 8. Amendment rule

Frozen from creation; never edited in place. A correction is a dated amendment or a new
versioned design, with the version in the filename (`docs/conventions.md` §b, read across by §h).
