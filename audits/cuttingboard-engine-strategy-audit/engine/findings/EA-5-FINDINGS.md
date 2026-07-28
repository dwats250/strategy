# EA-5 — Structural and Semantic Audit: Findings

Status: `ACTIVE — BROAD DISCOVERY COMPLETE. FINDINGS PROPOSED, NOT CORRECTED.`

Created: 2026-07-28 UTC

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`
Fixtures: [`../fixtures/structural/`](../fixtures/structural/) ·
Seam results: [`../fixtures/structural/EA5-SEAM-RESULTS.txt`](../fixtures/structural/EA5-SEAM-RESULTS.txt)
Eligibility register: [`../EA-5-ELIGIBILITY.csv`](../EA-5-ELIGIBILITY.csv)

Governing plan: [`../../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](../../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md) § EA-5, § 9.

---

## 0. Method and epistemic discipline

**Discovery was broad before prioritisation.** Every defect class the plan enumerates was probed
before any finding was ranked: contract/source divergence; polarity, unit, threshold, comparison
and boundary errors; duplicate, contradictory, constructed or mis-ordered gates; hidden
fall-throughs and unsafe defaults; stale, missing, conflicting or malformed evidence;
cross-symbol/cross-run/temporal leakage; unreachable states and manufactured passes; outputs
that hide uncertainty; untraceable explanations; and behaviour correct in code but incoherent
with stated purpose.

**EA-4's seven divergences entered as evidenced observations, not predetermined rulings.** Two
of them are downgraded here on the evidence (§3, EA5-005 and EA5-008 consequence), one is
reclassified from "defect" to a documented design asymmetry (EA5-010), and three are confirmed
and elevated with fixture or probe evidence.

**Reproduction artifacts are of two kinds, and the distinction is stated rather than blurred:**

- **Runtime fixtures** — quote-fixture JSON driven through the EA-2 seam
  (`--mode fixture` under `bwrap --unshare-net`, read-only root, single writable bind). Eight
  fixtures, all deterministic.
- **Static probes** — recorded, re-runnable commands with expected output, used where the finding
  is *the absence of something* or a documentation-versus-source mismatch. **A runtime fixture
  cannot demonstrate that a module does not exist.** The plan's completion criterion ("a
  reproducing fixture or demoted to UNKNOWN") is satisfied in spirit — reproducibility — without
  demoting findings that static evidence establishes at VERIFIED. This reading is recorded
  openly as an EA-5 judgement, not smuggled.

**Claimed-contract sources stay claimed.** `docs/system_logic_map.md` and `docs/architecture.md`
are claims CuttingBoard makes about itself. Where a finding is "documentation says X, source
does Y", the finding is about the *mismatch*, and neither side is treated as evidence of
implemented behaviour on its own.

**Withheld sources remain unread.** The EA-3 withheld corpus was not consulted. No correction
was attempted — every finding below proposes a seam and stops.

---

## 1. Negative results — probed, no defect found

Recorded because a structural audit that reports only defects is not an audit. These are the
classes where the engine **passed**.

### N-01 — Kill-switch boundary handling is exactly as claimed

`docs/system_logic_map.md` claims comparisons are strict `>`, so an exact-threshold reading does
**not** trip. Six fixtures test all three legs at and just above threshold:

| Fixture | Input | Outcome | kill_switch |
|---|---|---|---|
| `EA5-F01a-vix-level-at-35` | VIX level **= 35.0** | `NO_TRADE` | `False` |
| `EA5-F01b-vix-level-above-35` | VIX level **= 35.01** | `HALT` | `True` |
| `EA5-F02a-spy-pct-at-0.03` | SPY pct **= 0.03** | `NO_TRADE` | `False` |
| `EA5-F02b-spy-pct-above-0.03` | SPY pct **= 0.0301** | `HALT` | `True` |
| `EA5-F03a-vix-pct-at-0.15` | VIX pct **= 0.15** | `NO_TRADE` | `False` |
| `EA5-F03b-vix-pct-above-0.15` | VIX pct **= 0.1501** | `HALT` | `True` |

**No off-by-one, no polarity error, no unit error, no boundary error.** Claim upheld on all three
legs. Confidence VERIFIED.

### N-02 — Validation HALT fails closed on a missing HALT symbol

`EA5-F04-missing-halt-symbol-spy` drops `SPY` (a member of
`config.HALT_SYMBOLS = ["^VIX","DX-Y.NYB","^TNX","SPY","QQQ"]`). Result: `outcome=HALT`,
`system_halted=True`, `kill_switch=False`,
`halt_reason="Failed: SPY (symbol not fetched)"`.

Fails closed, and the halt cause is correctly distinguished from a kill-switch halt. VERIFIED.

### N-03 — Quote sanity rejects malformed evidence

`EA5-F05-negative-price-spy` supplies `price = -540.0`. Result: `outcome=HALT`,
`halt_reason="Failed: SPY (price -540.0000 is not positive)"`. Malformed evidence halts rather
than propagating. VERIFIED.

---

## 2. Findings — confirmed and elevated

### EA5-001 — A designed HALT is reported as a run *failure*, indistinguishable from a crash

- **Class:** decision-design / coherence defect
- **Evidence:** `runtime/__init__.py:1279` — `"status": SUMMARY_STATUS_FAIL if
  validation_summary.system_halted or errors else SUMMARY_STATUS_SUCCESS`;
  `runtime/__init__.py:222` — `return 0 if result["status"] == SUMMARY_STATUS_SUCCESS else 1`;
  `runtime/__init__.py:1588` — `verify_run_summary` **enforces** the mapping
  (`if summary.get("system_halted") and summary.get("status") != SUMMARY_STATUS_FAIL` → error);
  and `contract.py:203–211` — `derive_run_status` maps the same halt to `STATUS_STAY_FLAT`.
- **Affected behaviour:** every HALT — validation, market-stress kill switch, and unhandled
  exception alike — yields summary `status=FAIL` and **process exit code 1**. The contract
  simultaneously reports the halt as `STAY_FLAT`. Two status vocabularies describe one event.
- **User-facing consequence:** a correct market-stress stand-down is indistinguishable, at the
  process boundary, from an engine crash. A scheduler, CI job, or alerting rule keying on exit
  code cannot tell "the engine deliberately halted on VIX 36" from "the engine threw". EA-4 §2
  established that an unhandled exception also produces HALT; this finding shows the two are
  reported identically.
- **Confidence:** **VERIFIED** — source plus five fixtures (`F01b`, `F02b`, `F03b`, `F04`,
  `F05`), all exit 1 with `status=FAIL`, against `F01a`/`F02a`/`F03a` at exit 0.
- **Reproduction:** the five HALT fixtures above through the EA-2 seam.
- **Smallest plausible correction seam:** distinguish *designed halt* from *run failure* in the
  summary vocabulary — e.g. a third summary status, or an exit-code mapping that reserves 1 for
  unhandled failure. `verify_run_summary:1588` would have to move in step, since it currently
  enforces the conflation.
- **Evidence required to prove a correction worked:** re-run all eight fixtures; the three
  boundary-pass fixtures stay exit 0; the three kill-switch and two validation fixtures report a
  designed-halt status distinct from the status produced by an injected unhandled exception.

### EA5-002 — The per-gate PASS/FAIL vector is computed for every candidate, then discarded

- **Class:** observability gap
- **Evidence:** `qualification.py` — `QualificationResult` carries `gates_passed: list[str]` and
  `gates_failed: list[str]`. `audit.py` persists `block_reason` (`:142`, `:183`) and
  `missing_conditions` (`:196`) only; a grep for `gates_passed|gates_failed|gates_skipped` across
  `audit.py` returns no hit. Empirically, the pipeline record from `EA5-F01a` has 31 top-level
  keys, and `gates_passed`, `gates_failed`, `gates_skipped`, `soft_failures` are **all absent**
  from its full JSON serialization, while `qualified_trades`, `trade_decisions`,
  `suppressed_candidates`, `excluded_symbols`, `near_a_plus`, `watchlist` are present.
- **Affected behaviour:** the engine derives exactly the per-gate evidence an audit needs and
  drops it at the persistence boundary.
- **User-facing consequence:** no consumer can answer "which gate rejected this candidate, and
  which passed" from the durable record. Combined with the doctrine's one-record-per-invocation
  rule (EA-3 C-18) and ~1-record-per-day density (C-20), per-gate history does not exist.
- **Confidence:** **VERIFIED**.
- **Reproduction:** `EA5-F01a` through the seam, then inspect `logs/audit.jsonl`.
- **Smallest plausible correction seam:** persist `gates_passed`/`gates_failed` in the
  per-candidate audit entry. `audit._build_record` already receives the qualification summary.
  Per the audit doctrine's Rule 1 this requires a PRD naming a consumer — EA-6's trace schema is
  that consumer.
- **Evidence required:** a run whose audit record contains the per-gate vector for every
  evaluated candidate, reconciling with the `block_reason` already recorded.
- **Note:** the gap is **persistence, not derivation** — the most useful single result EA-5 hands
  to EA-6.

### EA5-003 — Three decision-relevant thresholds live outside `config.py`

- **Class:** fitting-readiness gap
- **Evidence:** static probe — `grep -c KILL_SWITCH_VIX_LEVEL cuttingboard/config.py` → **0**;
  `grep -n '^KILL_SWITCH_' cuttingboard/runtime/__init__.py` → `:2185 =35`, `:2186 =0.15`,
  `:2187 =0.03`.
- **Affected behaviour:** the three thresholds that can force a terminal HALT are not part of the
  `config.py` surface.
- **Declared-value accounting, stated precisely:** there are **52 `config.py` numeric constants
  plus these 3 external thresholds = 55 declared values.** Of the 52, **one
  (`INTRADAY_ALERT_COOLDOWN`) is unused** (EA5-006). An **"active configured surface" of 54
  therefore excludes that one unused `config.py` constant** — 55 declared, 54 active. Both
  figures are stated wherever either is used.
- **User-facing consequence:** a parameter-ownership map or fitting search built from `config.py`
  alone silently omits three thresholds with terminal-HALT authority.
- **Confidence:** **VERIFIED**.
- **Reproduction:** static probe P2, above.
- **Smallest plausible correction seam:** relocate the three constants to `config.py`, or record
  them in an explicit parameter registry that EA-11 consumes.
- **Evidence required:** an enumeration of the tunable surface that includes all 55 declared
  values, with the unused one flagged.

### EA5-004 — The documented "Polygon fallback" does not exist in the pinned source

- **Class:** decision-design / coherence defect (documentation overstates capability)
- **Evidence:** `docs/system_logic_map.md` § *Runtime Decision Flow* line 2 claims
  `ingestion.py — fetch RawQuote (yfinance primary, Polygon fallback)`. Static probe:
  case-insensitive `polygon` across `cuttingboard/` → **0 hits**; across `pyproject.toml` → **0
  hits**. EA-1 independently enumerated the network clients as `requests` and `yfinance` only.
- **Affected behaviour:** quote acquisition has a single provider. There is no fallback.
- **User-facing consequence:** a reader relying on the logic map believes quote acquisition
  degrades to a second provider under yfinance failure. It does not — a yfinance failure on a
  `HALT_SYMBOLS` member halts the run (demonstrated by N-02's shape).
- **Confidence:** **VERIFIED** for the mismatch.
- **Reproduction:** static probe P1. **A runtime fixture cannot demonstrate the absence of a
  module** — see §0.
- **Smallest plausible correction seam:** documentation-only — strike the fallback claim, or
  implement one. This is a CuttingBoard change and requires its own charge.
- **Evidence required:** either the claim is absent from the logic map, or a second provider is
  reachable and demonstrated.

### EA5-006 — One declared `config.py` constant is unused

- **Class:** weak / inert component
- **Evidence:** static probe P3 — `grep -rc INTRADAY_ALERT_COOLDOWN cuttingboard/` returns a
  single hit, `cuttingboard/config.py:1`, i.e. its own definition and no consumer.
- **Affected behaviour:** none. The constant is inert.
- **User-facing consequence:** a reader or a fitting search treats it as a live tunable. It is
  not.
- **Confidence:** **VERIFIED** (inert). **Harm: none demonstrated** — no evidence it misleads any
  current consumer, so no harm claim is made.
- **Reproduction:** static probe P3.
- **Smallest plausible correction seam:** delete it, or record it as reserved.
- **Evidence required:** the constant is absent, or documented as reserved with a reason.

### EA5-007 — The audit doctrine's canonical write-site citation does not resolve

- **Class:** observability gap (documentation)
- **Evidence:** `docs/audit_doctrine.md` Rule 1 states "The one canonical write site is at
  `runtime.py:1004`". Static probe P4: `cuttingboard/runtime.py` **does not exist** (the module is
  the package `cuttingboard/runtime/__init__.py`), and the sole `write_audit_record(` call site is
  at **line 1124**.
- **Affected behaviour:** none at runtime. The doctrine's substance (exactly one pipeline write
  site; none in `_execute_notify_run`) is **upheld** — EA-3 C-17.
- **User-facing consequence:** a reader verifying Rule 1 against source cannot locate the cited
  site, which weakens a doctrine whose whole purpose is to make the write surface auditable.
- **Confidence:** **VERIFIED**.
- **Reproduction:** static probe P4.
- **Smallest plausible correction seam:** update the citation to
  `runtime/__init__.py:1124`, or cite the symbol rather than a line.
- **Evidence required:** the cited path and line resolve at the pinned SHA.

---

## 3. Findings where the evidence does not support a stronger conclusion

Preserved as uncertain rather than rounded up. Per the plan's component standard, *harmful*
requires more than a suspicion, and **unknown is reported, not rounded**.

### EA5-005 — Gates 1–2 are implemented twice; no failure demonstrated

- **Class:** implementation defect (redundancy) — **consequence UNKNOWN**
- **Evidence:** the STAY_FLAT/confidence test exists at `qualification.py:803–820`
  (`_check_regime_gates`, called first by `qualify_all:166–168`, which returns immediately with
  `regime_short_circuited=True`) **and** at `qualification.py:368–377` / `:378–387`
  (`qualify_candidate` Gates 1–2), both reading `config.MIN_REGIME_CONFIDENCE`.
- **What is established:** the duplication is real (VERIFIED), and the claimed short-circuit
  behaviour is **correct** — `qualify_all` does short-circuit, so EA-3's claim is upheld.
- **What is not established:** any divergence between the two copies, or any run in which the
  per-candidate copies produce a different answer. Under `qualify_all` they are unreachable when
  the regime fails. A caller invoking `qualify_candidate` directly would bypass the
  short-circuit, but no such caller exists in the pipeline.
- **Confidence:** duplication **VERIFIED**; consequence **UNKNOWN**.
- **Reproduction:** static reading. **No fixture demonstrates a failure**, because none was
  found — reported rather than manufactured.
- **Smallest plausible correction seam:** have `qualify_candidate` delegate Gates 1–2 to
  `_check_regime_gates` so one implementation serves both paths.
- **Evidence required:** both entry paths produce identical gate results across the fixture set,
  before and after.

### EA5-008 — The kill switch treats missing stress evidence as zero stress, not unknown

- **Class:** decision-design / coherence defect — **consequence UNKNOWN, reachability blocked**
- **Evidence:** `runtime/__init__.py:2195–2198` — `spy_pct_change = … if spy is not None else
  0.0`; `vix_level = … if regime is not None and regime.vix_level is not None else 0.0`;
  `vix_pct_change` likewise. A defaulted `0.0` can never exceed 35, 0.15, or 0.03, so **the kill
  switch cannot trip on absent evidence.**
- **Coherence concern:** `docs/conventions.md` §h holds that "unavailable is not the same as
  passing." A safety mechanism that reads missing stress data as benign inverts that.
- **Why the consequence is UNKNOWN:** the primary call site (`:937`) is inside
  `elif not validation_summary.system_halted`, and `regime` is computed only on that branch
  (`:931–932`). Because `^VIX` and `SPY` are both `config.HALT_SYMBOLS` members, their absence
  halts the run at validation *before* the kill switch is consulted — demonstrated by N-02. The
  second call site (`:1256`, summary construction) **does** receive `regime=None` on a validation
  halt and correctly yields `False`, as fixtures `F04` and `F05` confirm (`kill=False`).
- **Attempted and failed to demonstrate:** the fixture schema (`_FIXTURE_QUOTE_FIELDS`) requires
  `pct_change_decimal` to be a float, so no fixture can supply a present-but-null stress reading.
  **The defect could not be made to bite through the seam.** Per the plan's completion criterion
  the consequence is therefore recorded **UNKNOWN** rather than elevated.
- **Confidence:** code shape **VERIFIED**; exploitable consequence **UNKNOWN**.
- **Smallest plausible correction seam:** make the missing case explicit — return "unknown" and
  let the caller decide, rather than substituting `0.0`.
- **Evidence required:** a run in which a stress input is genuinely unavailable does not report a
  benign kill-switch result.

### EA5-009 — The kill switch is evaluated twice per run

- **Class:** implementation defect (redundancy) — **consequence UNKNOWN**
- **Evidence:** `_kill_switch` is called at `runtime:937` (the decision) and again at
  `runtime:1256` (summary construction), rather than the decision being computed once and reused.
- **What is established:** two evaluations (VERIFIED). Across all eight fixtures the two agree —
  `kill=True` on the three trip fixtures, `False` elsewhere.
- **What is not established:** any input under which they could disagree. On a validation halt the
  second call receives `regime=None` and returns `False`, which is the correct answer for a
  validation halt — so the divergence in inputs currently produces the right result.
- **Confidence:** duplication **VERIFIED**; harm **UNKNOWN**.
- **Smallest plausible correction seam:** compute once, thread the result.
- **Evidence required:** a single evaluation reproduces all eight fixtures' `kill_switch` values.

### EA5-010 — CONTINUATION omits the ATR stop floor DIRECT enforces (documented, deliberate)

- **Class:** trade-geometry confound — **comparability UNKNOWN**
- **Evidence:** DIRECT Gate 6 enforces `config.STOP_ATR_FLOOR_K` with `config.MIN_STOP_PCT`
  (`qualification.py:422–444`). The CONTINUATION stop check applies **no** ATR floor, and the
  source states why (`:741–753`, PRD-240 R6): adding one would combine with the R:R ceiling into
  "a ~0.5×ATR-wide qualifying band — a de facto path shutdown deliberately not enacted."
- **Reclassification from EA-4:** this is **not** a defect. It is a documented, reasoned design
  asymmetry, and EA-5 records it as such rather than carrying EA-4's observation forward as a
  fault.
- **What remains open:** both paths emit `qualified=True` results, on different stop geometry.
  Whether those results are **comparable for attribution** is unresolved and is **EA-10's**
  question. It must not be assumed.
- **Confidence:** asymmetry **VERIFIED**; comparability **UNKNOWN**.
- **Smallest plausible correction seam:** none proposed — the asymmetry is intentional. The
  correction, if any, belongs to EA-10's method: attribute the two paths separately unless
  comparability is established.
- **Evidence required:** an attribution design that either demonstrates comparability or reports
  the paths separately.

---

## 4. Prioritisation — after discovery, not before

| Rank | Finding | Class | Confidence | Why ranked here |
|---|---|---|---|---|
| 1 | **EA5-002** | observability gap | VERIFIED | Blocks EA-6 directly; the data exists and is thrown away |
| 2 | **EA5-001** | coherence defect | VERIFIED | A correct stand-down is indistinguishable from a crash at the process boundary |
| 3 | **EA5-003** | fitting-readiness gap | VERIFIED | EA-11 would otherwise search an incomplete parameter surface |
| 4 | **EA5-004** | coherence defect | VERIFIED | Documentation asserts resilience the engine lacks |
| 5 | **EA5-007** | observability (docs) | VERIFIED | Cheap to fix; weakens an auditability doctrine |
| 6 | **EA5-006** | inert component | VERIFIED / no harm | Housekeeping |
| 7 | **EA5-008** | coherence | UNKNOWN consequence | Unsafe shape, currently masked by validation |
| 8 | **EA5-005** | redundancy | UNKNOWN consequence | No demonstrated failure |
| 9 | **EA5-009** | redundancy | UNKNOWN harm | No demonstrated divergence |
| 10 | **EA5-010** | geometry confound | UNKNOWN comparability | Method constraint on EA-10, not a fault |

---

## 5. Completion statement

- **Every finding has a reproducing artifact or is recorded UNKNOWN.** Six findings carry runtime
  fixtures or static probes at VERIFIED; four carry VERIFIED code-shape evidence with an
  explicitly **UNKNOWN** consequence, reported rather than rounded.
- **Discovery is recorded broad-then-prioritised** — §0 through §3 enumerate the classes probed,
  including three negative results (§1); ranking appears only in §4.
- **Every gate carries an eligibility classification** — [`../EA-5-ELIGIBILITY.csv`](../EA-5-ELIGIBILITY.csv), 30 rows.

**No stop condition fired.** No finding required modifying pinned source to demonstrate — where a
finding could not be demonstrated without that, it was recorded UNKNOWN instead (EA5-008). **No
correction was attempted**; every finding proposes a seam and stops.

**Containment:** DNS and direct-IP egress blocked (`gaierror`; `OSError [Errno 101] Network is
unreachable`); in-boundary write succeeded; writes into `Projects/strategy/` and
`Projects/cuttingboard/` blocked (`OSError`). CuttingBoard `HEAD` and `status --porcelain`
byte-identical before and after.

**EA-6 is not authorized by this document.** The plan gates it on Dustin's review of this finding
set **and** approval of the eligibility register.

## 6. Amendment rule

Frozen from creation; never edited in place. A correction is a dated amendment file or a new
versioned document, with the version in the filename (`docs/conventions.md` §b, read across by
§h).
