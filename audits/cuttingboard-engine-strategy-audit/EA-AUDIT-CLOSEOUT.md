# CuttingBoard Engine Strategy Audit — Closeout at EA-8

Status: `ACTIVE — PROGRAM CLOSED AT EA-8. EA-9 AND LATER BLOCKED / UNEXECUTED.`

Created: 2026-07-28 UTC

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`

Governing plan: [`plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md),
including its dated **2026-07-28 amendment (EA-6-006)**.

**This document is observational. It authorizes nothing.** It creates no charge, no scope, and
no permission — see §6.

---

## 1. Executive conclusion

### What the audit established

- **Bounded engine and harness behaviour on the observable reject and halt paths.** The
  qualification gate structure, the five-step decision chain, and both HALT causes are mapped to
  source with line references and exercised by deterministic fixtures.
  ([`engine/EA-4-SYSTEM-MAP.md`](engine/EA-4-SYSTEM-MAP.md),
  [`engine/EA-4-GATE-INVENTORY.csv`](engine/EA-4-GATE-INVENTORY.csv) — 30 gates;
  [`engine/findings/EA-5-FINDINGS.md`](engine/findings/EA-5-FINDINGS.md))
- **Deterministic replay.** Six archived run manifests each reproduce their canonical decision
  payload byte-for-byte, with the run-metadata envelope excluded by enumeration.
  ([`engine/EA-7-REPLAY-DESIGN.md`](engine/EA-7-REPLAY-DESIGN.md) §3 — "6 of 6 reproduce
  byte-for-byte"; [`engine/runs/EA-7-*/manifest.md`](engine/runs/))
- **As-of and look-ahead-control machinery.** Truncation, provenance capture, and an assertion
  suite that is demonstrated to *catch* injected leakage, not merely to pass.
  ([`engine/EA-8-ASOF-CONTRACT.md`](engine/EA-8-ASOF-CONTRACT.md) §3.1;
  [`engine/data/manifests/EA-8-LOOKAHEAD-SUITE-RESULT.txt`](engine/data/manifests/EA-8-LOOKAHEAD-SUITE-RESULT.txt))
- **Contamination control.** Every execution ran under enforced outbound-network denial and
  filesystem write confinement, each proven by a control that had to fail.
  ([`engine/EA-2-EXECUTION-SEAM.md`](engine/EA-2-EXECUTION-SEAM.md),
  [`engine/runs/EA-2/isolation-enforcement-proof.txt`](engine/runs/EA-2/isolation-enforcement-proof.txt))
- **A decision-trace schema** with every required field either populated or explicitly
  `NOT_OBSERVABLE`. ([`engine/trace/SCHEMA_v1.md`](engine/trace/SCHEMA_v1.md))

### What the audit did **not** establish

Stated as plainly as the above, because the distinction is the point of this document:

- **No strategy quality claim.**
- **No profitability claim.**
- **No accepted-trade frequency, value, or quality claim.**
- **No real-market representativeness.** All datasets exercised are synthetic.
- **No basis for fitting or optimization.**

Nothing in the EA-1 … EA-8 record supports any of these, and no such conclusion was drawn
anywhere in it.

---

## 2. Evidence boundary and final disposition

### EA-9 is BLOCKED / UNEXECUTED — not failed

EA-9 (evaluation target and outcome design) never began. The reason is an evidence boundary, not
a defect and not a failed attempt: **the repositories contain no authorized,
provenance-bearing historical OHLCV dataset suitable for empirical evaluation.**

**This is a statement about authorization and provenance within this audit — not about the
world.** Real market data plainly exists. It was **not selected, not retrieved, and not
authorized** within this audit: `spec/DATA_PROVENANCE_CONTRACT.md` is
`DRAFT / EXPLORATORY — FROZEN IMPLEMENTATION NOT AUTHORIZED` and "selects no provider,
authorizes no download, and specifies no acquisition code," and every EA charge forbade access
to live services and market data. Asserting that suitable data does not exist would be a
different and false claim.

EA-8's stop condition engaged exactly as designed: the evaluable range was **narrowed and the
limit recorded**, never approximated
([`engine/EA-8-ASOF-CONTRACT.md`](engine/EA-8-ASOF-CONTRACT.md) §4.3 — "Real-data evaluable
range: **EMPTY**").

### Carried forward — four standing limitations

| # | Limitation | Record |
|---|---|---|
| L-1 | **The accepted path is structurally unobservable under the authorized fixture method.** `_fixture_chain_results` returns `MANUAL_CHECK` for every setup unconditionally, so `outcome = TRADE` cannot occur in fixture mode at this pin | [`engine/findings/EA-6-observability-findings.md`](engine/findings/EA-6-observability-findings.md) EA-6-006; plan amendment 2026-07-28 |
| L-2 | **Per-candidate gate vectors are computed but not durably persisted.** `QualificationResult.gates_passed` / `.gates_failed` exist in memory and appear in no durable artifact | EA5-002; EA-6-001 |
| L-3 | **Synthetic data validates harness mechanics only, never market behaviour.** Every manifest records this explicitly rather than by omission | [`engine/EA-8-ASOF-CONTRACT.md`](engine/EA-8-ASOF-CONTRACT.md) §4.2; [`engine/data/README.md`](engine/data/README.md) |
| L-4 | **Data-provider parity is unavailable** without an authorized real dataset; it was never estimated from logic parity | [`engine/EA-7-REPLAY-DESIGN.md`](engine/EA-7-REPLAY-DESIGN.md) §4.2, NR-2 |

**L-1 is a harness constraint, not an engine defect.** That classification is EA-6's and stands
unchanged here.

---

## 3. Findings that matter

Summarized with their existing classifications and uncertainty preserved. **Nothing is
relitigated and no unresolved finding is upgraded.**

### Verified

| ID | Finding | Class | Record |
|---|---|---|---|
| EA5-002 / EA-6-001 | The per-gate PASS/FAIL vector is computed for every candidate, then discarded at the audit boundary — absent from **every** durable artifact | observability gap | EA-5 §2; EA-6-001 |
| EA5-001 | A designed HALT is reported as summary `status=FAIL` with process exit 1, indistinguishable from an unhandled-exception HALT, while the contract reports the same event as `STAY_FLAT` | decision-design / coherence | EA-5 §2 |
| EA5-003 | Three terminal-HALT thresholds live outside `config.py`. **55 declared values** = 52 `config.py` constants + 3 external; an *active configured surface* of 54 excludes the one unused constant | fitting-readiness gap | EA-5 §2 |
| EA5-004 | The documented "Polygon fallback" is absent from the pinned source entirely | coherence | EA-5 §2 |
| EA5-006 | One `config.py` constant (`INTRADAY_ALERT_COOLDOWN`) is unused. Inert; **no harm claimed** | inert component | EA-5 §2 |
| EA5-007 | The audit doctrine's canonical write-site citation resolves to no file | observability (docs) | EA-5 §2 |
| EA-6-002 | No ordering / override / precedence event stream exists | observability gap | EA-6 |
| EA-6-003 | A symbol invalidated for staleness leaves `excluded_symbols` empty and `data_status` `ok`; the exclusion reaches stderr only | observability gap | EA-6 |
| EA-6-004 | Reason codes are prose with interpolated numerals, not a stable enum — though the CONTINUATION path already has named counters | observability gap | EA-6 |
| EA-6-005 | A HALT preserves zero evaluation opportunities | observability / coherence | EA-6 |

### Negative results — the engine passed

Recorded because an audit that reports only defects is not an audit. Kill-switch boundary
handling is exactly as claimed on all three legs (strict `>`, tested at and just above
threshold); validation halts fail closed on a missing HALT symbol; quote sanity rejects a
negative price. ([`engine/findings/EA-5-FINDINGS.md`](engine/findings/EA-5-FINDINGS.md) §1)

### Left uncertain, and still uncertain

EA5-005 (Gates 1–2 duplicated), EA5-008 (kill switch reads missing stress evidence as `0.0`
rather than unknown — reachability blocked by validation), EA5-009 (kill switch evaluated
twice), EA5-010 (CONTINUATION omits the ATR stop floor DIRECT enforces — a documented, reasoned
design asymmetry, with path comparability open). **Each remains UNKNOWN in consequence. None is
upgraded here.**

### Structural eligibility

[`engine/EA-5-ELIGIBILITY.csv`](engine/EA-5-ELIGIBILITY.csv) classifies all 30 gates: **6
ELIGIBLE, 24 CONDITIONAL, 0 EXCLUDED-DEFECTIVE.** No finding demonstrated a gate reaching a
wrong pass/fail decision, so no exclusion was justified; most CONDITIONALs are attribution
constraints arising from L-2, not correctness doubts.

---

## 4. Future change candidates — non-authorizing observations

**These are observations, not bugs to fix, not a roadmap, and not permission to modify
CuttingBoard.** Each names the measurement it would unlock and the current limitation it
addresses. No benefit is estimated and no priority beyond the evidence is implied. Ordering
within each group reflects how directly the item removes a recorded blocker, nothing more.

### 4.1 Engine observability

| Candidate | Measurement it would unlock | Current limitation |
|---|---|---|
| Durable per-candidate gate vectors | Per-gate marginal contribution, redundancy, and interaction analysis | L-2 / EA5-002 / EA-6-001 — nothing to attribute against |
| Structured reason codes alongside the prose | Cross-run grouping of rejections without string parsing | EA-6-004 — prose with interpolated numerals |
| An ordered decision / override event stream | Where in the gate order a candidate stopped, and whether ordering behaved as mapped | EA-6-002 — no such stream exists |
| Explicit persistence of stale and excluded evidence | Opportunity-coverage series that distinguish "evaluated and rejected" from "never entered evaluation" | EA-6-003 — exclusions reach stderr only |
| A clear distinction between evaluated candidates and emitted opportunities | Denominator integrity for any selectivity or coverage measure | EA-6-005 — a HALT preserves zero opportunities |

### 4.2 Evaluation evidence

| Candidate | Measurement it would unlock | Current limitation |
|---|---|---|
| A provenance-complete, explicitly authorized historical OHLCV dataset | Any empirical outcome measure at all | §2 — no authorized dataset; real-data evaluable range EMPTY |
| Documented timestamp, session, and adjustment conventions | Confidence that results are not an artifact of convention mismatch | EA-8 §4.4 — an off-by-one bar convention is indistinguishable from look-ahead, and the suite cannot detect it |
| Reproducible as-of-bounded dataset manifests on that dataset | Leakage-controlled evaluation over real history | EA-8 §3 — machinery proven, but only against synthetic input |
| A separately authorized mechanism for observing the accepted path | Accepted-versus-rejected separation; any accepted-population metric | L-1 / EA-6-006 |

---

## 5. Re-entry conditions

The smallest set of conditions required before empirical evaluation could be authorized again:

1. **Separately authorized, provenance-bearing historical OHLCV** — carrying every field
   `spec/DATA_PROVENANCE_CONTRACT.md` requires, with none left blank.
2. **Validated as-of controls on that dataset** — the EA-8 look-ahead suite passing on it,
   including its negative control.
3. **An explicitly authorized resolution of accepted-path observability**, *if and only if* an
   analysis needs accepted-path metrics.
4. **A new, separately approved scope for any fitting or optimization.** None is authorized by
   this program or by this document.

---

## 6. Final status

**The program ended honestly at EA-8, under its evidence boundary.** It stopped where the
evidence stopped rather than continuing on estimated inputs.

- **EA-9 and all dependent work are BLOCKED / UNEXECUTED.**
- **No engine defect was fixed.**
- **No strategy logic was changed.**
- **No empirical performance conclusion was made.**
- **CuttingBoard was never modified.** It was read only at the pin, commit-addressed, with
  `HEAD` and `git status --porcelain` asserted byte-identical before and after every executing
  phase.

This document creates no charge, no scope, and no permission. Any future work — data
acquisition, accepted-path observability, fitting, or a CuttingBoard change — requires its own
explicit Dustin authorization.

## 7. Amendment rule

Frozen from creation; never edited in place. A correction is a dated amendment or a new
versioned closeout, with the version in the filename (`docs/conventions.md` §b, read across
by §h).
