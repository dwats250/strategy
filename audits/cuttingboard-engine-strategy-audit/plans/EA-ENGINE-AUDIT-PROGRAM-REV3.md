# CuttingBoard Decision-Engine Audit, Evaluation, Fitting and Correction Program

Status: `PROPOSED PROGRAM — REVISION 3 — AWAITING DUSTIN APPROVAL — AUTHORIZES NOTHING`

Preserved: 2026-07-27 UTC · Source pin:
`dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`

## Standing of this document

This is a **planning artifact preserved for retrieval**, not a commission and not a record of
work performed. Four distinctions are binding and must not be collapsed by any later reader:

1. **This plan is a proposal.** It commissions nothing, authorizes nothing, and grants no
   agent permission to act. It becomes effective only if and when Dustin approves it, and even
   then it authorizes only Phase 0.
2. **Phase 0 is unexecuted.** No document named in §1 has been created. TV-1's commission has
   **not** been withdrawn and remains live as described in §1. No closure record exists. No
   hash has been registered. Nothing in this plan may be cited as evidence that cauterization
   has occurred.
3. **Every later phase (EA-1 … EA-13) is separately gated.** Approval of this plan does not
   authorize EA-1; approval of EA-1 does not authorize EA-2 execution. Each phase requires its
   own Dustin approval at its entry gate, per the dependency-DAG rule in §6.
4. **CuttingBoard remains an immutable external subject.** It is read-only evidence at the pin
   above. Nothing in this document authorizes any CuttingBoard mutation, back-feed, parameter
   change, issue, refactor, or access beyond commit-addressed reads — and no CuttingBoard
   access of any kind occurred in preserving this artifact.

Where this document and any frozen TV-0 authority appear to disagree, **the frozen authority
governs.** This plan creates no precedence and reinterprets nothing. It is filed under
`plans/` rather than `charges/` precisely so that it cannot be mistaken for a commission.

---

**Revision 3.** Revision 2 corrected the cauterization verdict, reordered the opening sequence
to put a static execution-safety map ahead of any execution, narrowed the write-path claim,
required enforced isolation, reduced the first packet to governance only, and added
decision-contract intake with independence discipline. Revision 3 applies the eleven confirmed
defects from the Fable 5 adversarial review (verdict: APPROVE AFTER MECHANICAL CORRECTIONS):
external hash registration, an effective-authority test, removal of a self-contradicting
Phase 0 verification step, a dependency-DAG sequencing rule, an authority-scope clause on the
EA commission, a structural-eligibility register gating attribution and fitting, a canonical
decision payload for reproduction claims, a documented precedence basis for the closure
record, one canonical path root, §g-correct holdout naming, and a read log replacing
attestation.

**Canonical path root.** `A/` denotes `audits/cuttingboard-engine-strategy-audit/`. Every
proposed path in this plan is written relative to `A/`, per conventions §h ("an audit's
governing artifacts stay under `audits/`"). The sole exception, stated explicitly each time,
is the repository-root `README.md`.

**Context.** Strategy hosts a TradingView/Pine *proxy translation* of CuttingBoard (the
TV-0→TV-4 line). That instrument re-implements the engine and then studies the
re-implementation. Its own records show it cannot answer the mission: a trade list cannot
carry rejection evidence, the friction scenario is `UNRECOVERABLE`, the frozen v0.1 script
does not compile, and the UV02 universe departs from the pin by construction.
Reconnaissance establishes a better instrument: `dwats250/cuttingboard@59f8279d` is a Python
package with a deterministic fixture-replay mode and an existing per-run decision record. The
program therefore proposes to **execute the pinned engine offline under enforced isolation**
rather than translate it — but only after a static safety map proves what execution would do.

---

## Correction of my prior report

My previous verdict of CONTRADICTORY STATE was wrong on two of its three legs.

- I over-read `UV02_STUDY_CONTRACT.md:3` (`ACTIVE STUDY CONTRACT`) as a grant of work
  authority. It is a document-lifecycle label scoped to claim boundaries. §0 of that same
  document states it "does not register UV02 in the governing TV-0 → TV-4 protocol and confers
  no standing under it."
- I treated stale status summaries as conflicting authority. They are stale descriptions in
  documents that are not authorities on lifecycle state.

The surviving leg — TV-1 — is **residual authority**, not contradiction. Corrected verdict in
§1.

---

## 1. CAUTERIZATION STATUS

### Verdict: **RESIDUAL AUTHORITY**

No two documents in Strategy assert conflicting authority. One commissioned work packet
remains live with its objective unmet.

#### The residual authority — TV-1 (VERIFIED)

`charges/TV-1-PINE-IMPLEMENTATION.md:3` — `Status: COMMISSIONED AFTER COMPANION-REPOSITORY
PREFLIGHT`. Its objective (§*Objective*) is "one compiling Pine Script v6 strategy." Its
`Allowed files` are the four TV-1 in fact touched.

`INSTALLATION_RECORD.md` §*TV-1 is blocked* (lines 270–280) suspends it until (1) the
amendment PR merges to `main` and (2) three amendment hashes verify independently. **Both
conditions are now satisfied**: PRs #2/#4/#5/#6 are merged at `f1365be0`, and I verified all
eight recorded hashes byte-exact — `04e130a5…`, `5d45c21c…`, `b2f3c0b2…`, `a0020ae9…`,
`f01b8d93…`, `dd65f878…`, `ec56939c…`, and README at its re-issued `22d058e0…`.

Therefore: **TV-1's suspension has lapsed on its own terms, its commission is live, and its
objective is unmet** — `UV02_STUDY_CONTRACT.md` §5 records that
`pine/cuttingboard_direct_proxy_v0.1.pine` does not compile. A fresh agent reading the charge
and the installation record would correctly conclude it may proceed with the remaining TV-1
work. That is live residual authority pointed at superseded proxy work, and it is the one
thing Phase 0 must extinguish.

#### Not residual authority — UV02-E1 (VERIFIED)

UV02's documents uniformly and explicitly disclaim standing:

- `UV02_STUDY_CONTRACT.md` §0 — "does not register UV02 in the governing TV-0 → TV-4 protocol
  and confers no standing under it… creates no precedence, relaxes no rule, and reinterprets
  nothing."
- `diagnostics/README.md:13–31` — "It is not a registration… It grants no status… It repairs
  no authority issue… the governing document governs, without exception."
- `UV02_EVIDENCE_CAPABILITY.md` §7 — "Each step is separately authorized; **none is
  authorized by this document**."

`UV02-E1` is therefore a **named but uncommissioned** research gate. No document authorizes
it; its own documents deny that any of them could. It is not residual authority and does not
require supersession.

It is a **documentation hazard only**: `UV02_CAPTURE_LOG.md:93` calls it "the next research
gate" and `UV02_EVIDENCE_CAPABILITY.md` §5 specifies its first action in runnable detail, so a
careless reader could mistake a described next step for a queued one. Phase 0 remedies that
with a short closure note, not a supersession.

#### Not authority at all — stale status summaries (VERIFIED)

- Root `README.md` §*Audits* says the audit is "awaiting the independent TV-0R semantic
  review." TV-0R is complete and adjudicated. This is a **stale summary in the repository
  index**, which is not an authority on audit lifecycle state.
- `audits/…/README.md:3` says "TV-0 COMMISSIONED — CONTRACT FROZEN FOR FIRST IMPLEMENTATION."
  This is inside a frozen TV-0 authority, and it is **accurate**, not stale: TV-0 is
  commissioned and frozen. It is not in conflict with anything.

Neither is corrected by rewriting a frozen document. See §7 for how Phase 0 handles this
without an in-place edit.

### Minimum Phase 0 action

1. **`A/engine/charters/EA-0-COMMISSION.md`** *(new)* — the pin, scope, and repository
   boundary, plus an explicit **authority-scope and lapse clause**: *this commission authorizes
   the program framework and Phase 0's documentation actions only; no EA phase is authorized by
   this document; each phase is authorized solely by Dustin's approval at its entry gate, and
   EA-2 execution solely by its separate execution approval; unapproved phases hold no residual
   authority; if the program terminates at any point, a closure record for EA-0 extinguishes it,
   leaving no live commission.* This clause exists because an unscoped commission is exactly
   what produced the TV-1 residue this phase is extinguishing.
2. **`A/closure/TV-LINE-CLOSURE-2026-07-27.md`** *(new)* — records TV-0 and TV-0R complete;
   **explicitly withdraws TV-1's commission and its authorization to continue**, citing the
   lapsed suspension and the unmet objective; records TV-1R/TV-2/TV-3/TV-4 as not commissioned.
   It states its **authority basis**: it takes effect upon Dustin's merge to `main` — the merge
   is the principal's act of withdrawal, this document its record. It **enumerates by path and
   section** every frozen document whose status assertions it supersedes (the TV-1 charge status
   line; `INSTALLATION_RECORD.md` §*TV-1 is blocked*), preserving each byte-exact as history.
   It states a **narrowly scoped precedence rule**: *for the TV-0 / TV-0R / TV-1 / TV-1R /
   TV-2 / TV-3 / TV-4 workstream and for UV02 — and for nothing else — current lifecycle
   authority is the most recent Dustin-merged closure or charter record that enumerates by path
   and section the specific document text it supersedes. Within those enumerated sections,
   frozen historical status text is evidence of past state only.* **The rule reaches only the
   documents and sections enumerated in this closure record. It establishes no repository-wide
   precedence, creates no general supersession mechanism, and has no effect on any authority
   outside the enumerated TV/UV02 set** — including `docs/conventions.md`, the root `CLAUDE.md`
   and `AGENTS.md`, the SPY ORB and Faber studies, and any future workstream.
3. **`A/closure/UV02-CLOSURE-2026-07-27.md`** *(new)* — records that `UV02-E1` was never
   authorized, is not opened, and will not be; re-labels UV02 as preserved historical evidence.
   No supersession claimed, because none is needed.
4. **`A/closure/HASHES-2026-07-27.md`** *(new)* — the external hash register. After each new
   document is finalized, its SHA-256 is computed and recorded **here**, not inside itself.
   The register records no hash of its own; the Dustin-merged commit SHA attests the register.
5. **Repository-root `README.md`** *(edited)* — corrects the stale audit status line and points
   to `A/closure/` and `A/engine/charters/`. This is the repository index, not a frozen document.

**Nothing else is touched.** No frozen document is edited. No UV02 artifact changes. No
previously recorded hash changes (§7.3).

### Confirmation

Prior proxy work will not be resumed, repaired, rerun, extended, or administered. No
TradingView run, Pine edit, v0.3, `UV02-E1` probe, or UV02 capture is proposed here or
permitted under this plan.

---

## 2. VERIFIED CURRENT STATE

### Repository — VERIFIED

`/home/dustin/Projects/strategy`; `origin https://github.com/dwats250/strategy.git`; `main` @
`f1365be0dd8d53feba9ab9f82ed4a1c719b4e4f3`; working tree **clean** (`git status --porcelain
-uall` empty). No user-owned changes overlap anything inspected.

### Audit lifecycle — VERIFIED

TV-0 commissioned, installed byte-identical, frozen, five hashes recorded and re-verified
today. TV-0R performed outside this repository by fresh-context GPT-5.6/Sol, delivered to
Dustin, adjudicated; `reviews/` empty by design. TV-1 commissioned, **partially executed**
(script written, README link edited under its `Allowed files`), **objective unmet — the script
does not compile**. TV-1R/TV-2/TV-3/TV-4 not started; TV-4 never chartered. UV02: seven
immutable captures, ledger, contract — uncommissioned throughout.

### Pin — VERIFIED

`59f8279d796335149afdec4aa507b6f927233518` resolves in the local checkout; `git cat-file -t` →
`commit`. Every read this session was commit-addressed (`git show`, `git ls-tree`), never from
the working tree. **CuttingBoard was not modified.**

### Engine facts from pinned source — VERIFIED

| # | Fact | Evidence at pin |
|---|---|---|
| E-1 | Python CLI: `python -m cuttingboard --mode {live,fixture,sunday,verify,prefetch} --fixture-file --date` | `runtime/__init__.py:164–223`; `__main__.py` |
| E-2 | Deterministic fixture-replay mode exists: `run_at_utc = max(fetched_at_utc)` over the fixture; `run_id = "{mode}-fixture-{stem}"` — no wall-clock dependence | `runtime/__init__.py:2293–2312` |
| E-3 | In fixture mode OHLCV is served cache-only from parquet by monkeypatching `fetch_ohlcv` in two modules; missing cache returns `None` | `runtime/__init__.py:1692–1709` |
| E-4 | **See §3 — narrowed claim.** The specific path constants inspected are relative; `config.toml` is package-anchored | `runtime/_constants.py:44–58`; `config.py:18–19,187`; `audit.py:32` |
| E-5 | An append-only per-run decision record exists with `outcome ∈ {TRADE, NO_TRADE, HALT}`, regime, validation summary, qualification summary, option setups, trade decisions, `suppressed_candidates`, halt reason | `audit.py:35–80`; `logs/audit.jsonl` |
| E-6 | Terminal decision assembly applies **four named gate functions** — execution policy, thesis, invalidation, entry quality — around a materialization step and a terminal outcome derivation. Its docstring calls this "the five-gate decision chain." **The discrepancy is unresolved — see §7.** | `runtime/__init__.py:622–724` |
| E-7 | Tunable numeric surface is concentrated: **52** module-level numeric constants in `config.py`; `config.toml` carries 2 operational flags | `config.py` |
| E-8 | Options-chain validation is **stubbed** in fixture mode | `runtime/__init__.py:1710–1726` |
| E-9 | The engine carries its own decision-contract documentation (`docs/decision_quality_map.md` 41 KB, `docs/DECISIONS.md` 220 KB, `docs/trade_qualification.md`, `docs/artifact_flow_map.md`, `docs/PROJECT_STATE.md`) and a large prior-audit corpus (~40 documents under `audits/`, plus `docs/audit/gate_recon_2026-06-12.md`) | `git ls-tree` at pin |

### INFERENCE

- **I-1** Because the inspected path constants are relative, setting the process CWD is
  *likely* sufficient to confine writes — but this is a hypothesis EA-1 must test statically
  and EA-2 must prove under enforcement. It is **not** a basis for running the engine.
- **I-2** From E-3: `_cache_only` returns the cached frame **untruncated**, so a full-history
  cache would leak future bars into EMA/ATR/structure computations. **As-of truncation is
  Strategy's responsibility and is the program's primary leakage control.**
- **I-3** From E-5: the engine is partially observable already; the gap is per-candidate,
  per-gate granularity, not absence.
- **I-4** From E-8: options profitability is not reproducible offline at this pin. Underlying
  directional outcomes and options P&L must be reported as different quantities.
- **I-5** From E-9: a substantial prior-audit corpus exists inside the subject. Reading it
  early would anchor this audit's findings to someone else's conclusions. Independence
  discipline in EA-3/EA-4/EA-11 addresses this.

### UNKNOWN

- **The complete filesystem write-set of an engine run.** Established by EA-1, not assumed.
- All outbound network paths, subprocess invocations, dynamic imports, environment and secret
  reads, and external-service calls. EA-1.
- Whether the pinned package imports under a pinned environment; whether
  `_run_engine_health_gate()` passes in a sandbox. EA-2.
- Whether two identical fixture runs are byte-identical. EA-2.
- Which construct is the fifth "gate" in E-6. EA-4.
- How far back as-of inputs can be reconstructed. EA-7.
- Whether Dustin holds TV-0R or engine material outside the repository.

---

## 3. NARROWED WRITE-PATH CLAIM

My prior report claimed "all outputs are CWD-relative." That overstated the evidence.

**What is VERIFIED** — the following path constants are declared relative and therefore
resolve against the process working directory:

- `runtime/_constants.py:44–57` — `REPORTS_DIR = Path("reports")`, `LOGS_DIR = Path("logs")`,
  and the derived `LATEST_RUN_PATH`, `LATEST_HOURLY_RUN_PATH`,
  `LATEST_HOURLY_CONTRACT_PATH`, `LATEST_HOURLY_PAYLOAD_PATH`, `HOURLY_REPORT_PATH`,
  `MARKET_MAP_PATH`, `LATEST_HOURLY_MARKET_MAP_PATH`, `TREND_STRUCTURE_PATH`,
  `WATCHLIST_PATH`
- `runtime/_constants.py:58` — `DEFAULT_FIXTURE_DIR = Path("tests/fixtures")` (read)
- `config.py:187` — `OHLCV_CACHE_DIR = "data/cache"`
- `audit.py:32` — `AUDIT_LOG_PATH = "logs/audit.jsonl"`

**Also VERIFIED** — one path is package-anchored, not CWD-relative: `config.py:18–19`,
`_PROJECT_ROOT = Path(__file__).parent.parent`, `_CONFIG_TOML = _PROJECT_ROOT / "config.toml"`.
It is read, not written, in the code inspected.

**What remains UNKNOWN** — the *complete* write-set. Not established: whether any module
computes an absolute path; whether `_PROJECT_ROOT` is used for any write; whether any write
occurs through a subprocess, a third-party library with its own path defaults, a temp-file
API, or a dynamically constructed path; whether `os.chdir` is called anywhere. **The write-set
is UNKNOWN until EA-1 establishes it by static analysis and EA-2 confirms it by observation
under enforcement.** No phase may rely on CWD confinement before then.

---

## 4. OBJECTIVE RECONCILIATION

**Carries forward:** the governance apparatus (conventions §b/§e/§f/§g/§h/§i — immutable
exports, the authoritative ledger, pre-registered manifests, hash-gated stage consumption,
pinned-SHA read rules); `spec/GATE_TRANSLATION_MATRIX.md` as a **gate-inventory hypothesis to
be re-tested against source**, never as settled fact; the three literal-recovery amendments
(real, hash-verified work product — a genuine head start on the system map); and two hard-won
negative lessons — a trade list cannot carry rejection evidence, and configuration not
recorded at capture time is unrecoverable. Both are designed into the trace schema and run
manifest.

**Does not carry forward:** any UV02 numeric result (different universe, different script,
FULL-history window, friction `UNRECOVERABLE`) — not a baseline, benchmark, or prior; the
"not profitable" conclusion as a verdict on the *engine* — and note it is **not recorded
anywhere in Strategy as a finding**, since UV02 §7.8 forbids treating counts as results and
no analysis document exists (Phase 0 records the gap without repairing it); Pine as the
instrument; the 2022-01-01 – 2026-07-24 window as a holdout (inspected; per §g its
pre-inspection status cannot be restored); and fixed stop/target geometry as the definition of
trade quality.

**Why one connected program.** A structurally inert gate and a correct-but-non-binding gate
produce identical attribution signatures unless the structural map distinguishes them. An
attribution result is only as trustworthy as the replay determinism underneath it. **Fitting a
defective gate optimizes the defect** — so structural findings must gate what enters the
parameter search. A passing test suite proves neither usefulness nor calibration; historical
profitability proves neither correctness nor stability; a failed proxy proves neither about
the engine. Reconciling the three requires shared identities — source SHA, config SHA, dataset
SHA, environment hash, trace schema version — carried across every phase. That shared spine is
the program.

---

## 5. EXISTING-PLAN VERDICT

**SUPERSEDE** the TV proxy line. **RETAIN AND EXTEND** the governance layer.

**Evidence.** The TV line's own records make its product unusable for the mission
(`UV02_EVIDENCE_CAPABILITY.md` §2 — "rejections never become trades"; §1.1 — "no
scenario-valid friction-adjusted return"; `UV02_STUDY_CONTRACT.md` §5 — "not comparable to the
pinned engine, by construction"). Its next step is translation *fidelity* (TV-2 parity), not
engine *behaviour*; mission items 2–7 are not reachable along it. And
`PRIMARY-CHARGE-…` §*Preliminary-round scope* explicitly excludes an offline runner, deferring
it to "likely TV-4," which was never chartered — so the new program occupies a vacancy rather
than conflicting with a live charge.

**Minimum governance change:** exactly the four Phase 0 items in §1. No frozen document
edited, no hash invalidated, no evidence deleted.

**Declared deviation requiring approval.** Execute the actual pinned engine offline under
enforced isolation instead of continuing the Pine translation. *Evidence:* E-1…E-6, E-9.
*Payoff:* eliminates translation-fidelity risk; makes per-candidate rejection evidence
obtainable; makes determinism a configuration rather than a re-implementation. *Displaces:*
TV-1's remaining work, TV-1R, TV-2, TV-3 — all unexecuted.

---

## 6. PROPOSED PROGRAM — full phase specifications

Line prefix **EA**. **Universal stop conditions, binding on every phase:** any proposed
CuttingBoard mutation of any kind; any GitHub or connector call with a missing, inferred, or
ambiguous repository target; any target that is not exactly `dwats250/strategy`; any hash
mismatch between what a reviewer examined and what the stage consumes; any need to modify
pinned source to make a step work.

**Universal approval gate — dependency-DAG rule.** Each phase ends in a draft PR held for
Dustin. **No phase begins before every phase named in its entry criteria is merged by Dustin
and its own entry approval is given.** "Complete" in any entry criterion means *merged*.
Phases that do not name each other in entry criteria may run in parallel.

---

### Phase 0 — Governance cauterization *(governance only; no engine work)*

- **Question:** what work is authorized in this repository right now?
- **Authorized work:** create the four new documents in §1; edit repository-root `README.md`
  only. Documentation only.
  **No-access criterion — precise.** *Textual* references to CuttingBoard inside Strategy
  governance documents are **permitted and expected**: the closure records and the EA-0
  commission necessarily name `dwats250/cuttingboard` and the pin
  `59f8279d796335149afdec4aa507b6f927233518`. What is prohibited is **any filesystem
  operation, command, tool invocation, or repository action that targets or inspects a
  CuttingBoard checkout, remote, ref, or working tree** — no `git` invocation against
  CuttingBoard, no read of its files, no execution, no tooling, no data acquisition.
- **Outputs:** `A/engine/charters/EA-0-COMMISSION.md`;
  `A/closure/TV-LINE-CLOSURE-2026-07-27.md`; `A/closure/UV02-CLOSURE-2026-07-27.md`;
  `A/closure/HASHES-2026-07-27.md`; edited repository-root `README.md`.
- **Entry criteria:** this plan approved by Dustin.
- **Completion criteria:** merged to `main`; **the effective-authority test passes** —
  `A/closure/TV-LINE-CLOSURE-2026-07-27.md` is merged and explicitly withdraws TV-1's
  commission, and a grep for the commissioning/authorization terms of TV-1, TV-1R, TV-2,
  TV-3, TV-4 and `UV02-E1` finds hits **only inside frozen historical documents enumerated by
  path as superseded in the closure record**, with zero hits outside that enumerated set
  (frozen commission text **plus** recorded withdrawal equals no live authorization); all
  eight historical hashes re-verified byte-exact, three new document hashes registered in
  `A/closure/HASHES-2026-07-27.md`, and the hash register itself attested by the Dustin-merged
  commit SHA; `git diff` shows no frozen document and no
  UV02 artifact changed; exactly one pre-existing file (repository-root `README.md`) modified
  and four files added.
- **Stop conditions:** any proposed in-place edit to a frozen document; any deletion or
  modification of UV02 evidence; any hash change to `A/README.md`; **any CuttingBoard access**;
  scope creep into engine work of any kind.
- **Approval gate:** Dustin reviews and merges the PR. **Nothing else proceeds until merged.**

---

### EA-1 — Static execution-safety map *(read-only; no execution)*

- **Question:** if the pinned engine were executed, exactly what would it touch — filesystem,
  network, subprocesses, imports, environment, secrets, configuration, external services?
- **Authorized work:** static analysis of pinned source only, via commit-addressed reads
  (`git show` / `git ls-tree` / `git archive` to a read-only location). Enumerate and classify:
  1. **Filesystem writes** — every `open(...,"w"/"a")`, `write_text`, `to_parquet`, `to_csv`,
     `mkdir`, `Path.touch`, `shutil`, `tempfile`, and every path expression reaching them;
     classify each as CWD-relative, package-anchored, absolute, or dynamically computed.
  2. **Network** — every HTTP/socket client, `yfinance`/vendor SDK call, every URL constant,
     and which are reachable in `--mode fixture` versus only in `live`.
  3. **Subprocesses** — `subprocess`, `os.system`, `os.popen`, shell-outs.
  4. **Imports** — full transitive third-party set; anything with import-time side effects.
  5. **Environment and secrets** — every `os.getenv`/`os.environ` read, what it gates, and
     what happens when unset.
  6. **Configuration loading** — `config.toml` resolution, `_PROJECT_ROOT` uses, any other
     config discovery.
  7. **External services** — Telegram and any other transport; the exact conditions under
     which each fires.
  Produce the **predicted** write-set and network-reachability set for `--mode fixture`, with
  a confidence label per item, and a list of everything that cannot be settled statically.
- **Outputs:** `A/engine/EA-1-EXECUTION-SAFETY-MAP.md` (the map, per-item evidence with file and
  line references at the pin); `A/engine/EA-1-ISOLATION-REQUIREMENTS.md` (the enforcement
  specification EA-2 must implement, derived from the map).
- **Entry criteria:** Phase 0 merged and verified.
- **Completion criteria:** every write site, network path, subprocess, env/secret read,
  config load, and external-service path is enumerated with pinned-source evidence or
  explicitly recorded as statically undecidable; the predicted fixture-mode write-set is
  stated; isolation requirements are specified and reviewable **without having run anything**.
- **Stop conditions:** the map cannot be completed from source without executing code; a
  network or write path is found that no isolation mechanism available here can contain
  *(that is a stop and a finding, not a reason to proceed carefully)*; any temptation to "just
  run it to see."
- **Approval gate:** Dustin reviews the map and the isolation requirements. **Execution is
  authorized only by a separate approval of EA-2, granted after reading this map.**

---

### EA-2 — Execution seam proof under enforced isolation *(first execution; separately authorized)*

- **Question:** does the pinned engine run deterministically with contamination *prevented by
  enforcement*, and does observed behaviour match the EA-1 prediction?
- **Authorized work:** extract the pin with `git archive 59f8279d | tar -x` into a
  git-ignored sandbox — **never `git worktree add`, which mutates CuttingBoard git metadata**.
  Pin the Python environment and record its lockfile hash. Then run **once**, under:
  - **Outbound-network denial enforced at process or container level** — a network namespace
    with no route (`unshare --net`) or a container with `--network=none`. Proof of enforcement
    is a deliberate control call to a known host that must **fail**. Unsetting `TELEGRAM_*` is
    retained as defence in depth and is explicitly **not** accepted as proof of isolation.
  - **Write confinement enforced at the filesystem level** — the extracted source and every
    other path mounted read-only, with exactly one writable directory bound in
    (`bwrap`/container mount policy). A write outside it must **fail**, not merely be absent.
  Snapshot before and after; diff to obtain the **observed** write-set; compare against EA-1's
  prediction and record every divergence as a finding. Repeat into a second clean sandbox and
  diff the two write-sets for determinism. Assert `git -C ~/Projects/cuttingboard rev-parse
  HEAD` and `git status --porcelain` byte-identical before and after.
- **Outputs:** `A/engine/EA-2-EXECUTION-SEAM.md`; `A/engine/env/` lockfile and hash;
  `A/engine/runs/EA-2/` probe evidence including the isolation-enforcement proof;
  `A/engine/LEDGER.csv` first rows.
- **Entry criteria:** EA-1 merged **and** separately approved by Dustin for execution.
- **Completion criteria:** isolation enforcement demonstrated by failed control calls (network
  and write); observed write-set enumerated and entirely inside the writable directory;
  prediction-versus-observation divergences recorded; determinism demonstrated or honestly
  refuted; CuttingBoard byte-unchanged.
- **Stop conditions:** any write outside the confinement boundary; any successful outbound
  connection; any divergence from the EA-1 map that the map did not anticipate as possible
  (stop and re-map); any need to edit pinned source to make it run; any CuttingBoard
  git-metadata change.
- **Approval gate:** Dustin reviews the seam report before any further execution.

---

### EA-3 — Decision-contract intake *(read-only; independence discipline begins)*

- **Question:** what does CuttingBoard *say* its decision system does?
- **Authorized work:** read the engine's own decision contract at the pin — `docs/
  decision_quality_map.md`, `docs/DECISIONS.md`, `docs/trade_qualification.md`,
  `docs/artifact_flow_map.md`, `docs/PROJECT_STATE.md`, `cuttingboard/contract.py`,
  `contract_types.py`, and the audit doctrine referenced by `audit.py`. Extract the **claimed**
  contract: intended gates and order, intended terminal outcomes, intended invariants,
  intended explanations, intended observability.
  **Independence discipline — binding:** prior *audit findings* are **withheld** at this stage
  and until EA-11. That means `audits/FINDINGS.md`, `audits/RECONCILED_FINDINGS.md`,
  `audits/CODEX_REVIEW.md`, `audits/FABLE_REVIEW.md`,
  `audits/qualification-tuning-2026-07-05/findings.md`,
  `audits/codebase-review-2026-07-03/mentor-review.md`, the `alignment-*`, `inventory-*`,
  `recon-*`, `cleanup-*`, `prd-lifecycle-*` sets, `docs/audit/gate_recon_2026-06-12.md`, and
  every `docs/prd_history/*.review.*`. The distinction is deliberate: **contract documents are
  the specification and are read now; findings documents are somebody's conclusions and are
  read only after this audit has formed its own.** **All commit-addressed reads in this phase
  are logged**, so independence is provable rather than attested.
- **Outputs:** `A/engine/EA-3-CLAIMED-CONTRACT.md`; `A/engine/EA-3-WITHHELD-SOURCES.md`;
  `A/engine/EA-3-READ-LOG.csv`.
- **Entry criteria:** Phase 0 merged. Names no other phase, so under the DAG rule it may run
  in parallel with EA-1 and EA-2.
- **Completion criteria:** the claimed contract is stated in testable terms; every withheld
  document is listed; **the phase read log contains no withheld path**.
- **Stop conditions:** reading any withheld document; treating a contract document as evidence
  of implemented behaviour.
- **Approval gate:** Dustin reviews the claimed contract and the withheld list.

---

### EA-4 — Implemented system map and contract-versus-code adjudication

- **Question:** what does the engine actually do, and where does implementation diverge from
  its own stated contract?
- **Authorized work:** trace from source — production entrypoints; evaluation cadence and
  candidate-generation rules; input providers, timestamps, provenance, freshness, missing-data
  rules; decision objects and terminal outcomes (confirming `TRADE`/`NO_TRADE`/`HALT` as
  actually implemented per E-5); state owners and mutation boundaries; configuration and
  threshold ownership for all 52 constants; gate ordering, precedence, overrides, fail-open
  versus fail-closed; symbol, run and temporal isolation; explanation and reason generation;
  downstream execution assumptions. Adjudicate against EA-3's claimed contract. **Resolve the
  E-6 gate-count discrepancy here** (§7). Re-test the TV-0 gate inventory and record every
  divergence.
- **Outputs:** `A/engine/EA-4-SYSTEM-MAP.md`; `A/engine/EA-4-GATE-INVENTORY.csv` — one row per
  gate: id, module, line range, inputs, threshold owner, order index, precedence, failure
  mode, observability status, contract-divergence flag.
- **Entry criteria:** EA-2 and EA-3 complete.
- **Completion criteria:** every terminal outcome traced to source; every `config.py` constant
  assigned an owning gate or marked unused; the gate-count discrepancy resolved with evidence.
- **Stop conditions:** the map cannot be completed without executing undocumented behaviour;
  any withheld findings document consulted.
- **Approval gate:** Dustin reviews the map and inventory.

---

### EA-5 — Structural and semantic audit *(broad finding discovery)*

- **Question:** what is broken, contradictory, inert, unreachable, unobservable, or misleading?
- **Authorized work:** evidence-backed tests for contract/source divergence; polarity, unit,
  threshold, comparison and boundary errors; duplicate, contradictory, constructed or
  mis-ordered gates; hidden fall-throughs and unsafe defaults; stale, missing, conflicting or
  malformed evidence; cross-symbol, cross-run and temporal state leakage; unreachable states
  and manufactured passes; outputs that hide uncertainty or overstate confidence; explanations
  not traceable to the inputs that caused them; behaviour correct in code but incoherent with
  stated purpose. **Every candidate defect must have a deterministic fixture that demonstrates
  it** through the EA-2 seam. Discovery is broad before prioritisation. Withheld sources stay
  withheld.
- **Outputs:** `A/engine/findings/EA-5-*.md`; `A/engine/fixtures/structural/`;
  **`A/engine/EA-5-ELIGIBILITY.csv`** — the structural-eligibility register.
- **Entry criteria:** EA-4 complete.
- **Completion criteria:** every finding has a reproducing fixture or is demoted to UNKNOWN;
  discovery is recorded as broad-then-prioritised, not prioritised-then-searched; every gate
  carries an eligibility classification.
- **Stop conditions:** a finding can only be demonstrated by modifying pinned source; any
  correction attempted rather than proposed.
- **Approval gate:** Dustin reviews the finding set before prioritisation **and approves
  `A/engine/EA-5-ELIGIBILITY.csv`**, classifying every gate `ELIGIBLE` /
  `EXCLUDED-DEFECTIVE` / `CONDITIONAL(finding-id)`. **Exclusion is implemented only in the
  Strategy-owned harness configuration, never by modifying pinned source.** This is the
  structural-eligibility decision point, and it sits **before** attribution and fitting.

---

### EA-6 — Decision observability

- **Question:** can every evaluation opportunity be explained and reproduced?
- **Authorized work:** specify the trace schema (§8) and implement capture in a
  **Strategy-owned wrapper that observes the engine** — never by instrumenting pinned source.
  Where a field is unreachable without a source change, label it `NOT_OBSERVABLE`, record an
  observability finding with the smallest correction seam, and **do not invent the value**.
- **Outputs:** `A/engine/trace/SCHEMA_v1.md`; `A/engine/tools/trace_capture/`;
  `A/engine/findings/EA-6-observability-*.md`.
- **Entry criteria:** EA-4 complete.
- **Completion criteria:** full-fidelity traces emitted for at least one accepted, one
  rejected, one halted, one stale-data, one missing-data and one boundary-value case; every
  schema field either populated or explicitly `NOT_OBSERVABLE`.
- **Stop conditions:** any proposal to patch pinned source to close a gap; any field
  synthesised to fill a hole.
- **Approval gate:** Dustin approves the schema before capture is built at scale.

---

### EA-7 — Deterministic offline replay

- **Question:** does the same observation always produce the same decision, and where exactly
  does parity end?
- **Authorized work:** harden EA-2 into a replay harness over many dates, under the same
  enforced isolation. Separate **logic parity** (engine code path) from **data-provider
  parity** (whether reconstructed inputs match what live CuttingBoard saw). Build the
  deterministic fixture library. Document every behaviour not reproducible without modifying
  CuttingBoard.
- **Outputs:** `A/engine/EA-7-REPLAY-DESIGN.md`; `A/engine/tools/replay/`; `A/engine/fixtures/`;
  `A/engine/runs/<run-id>/manifest.md`.
- **Entry criteria:** EA-2 and EA-6 complete.
- **Completion criteria:** **re-running any archived manifest reproduces its canonical
  decision payload byte-for-byte** (§8); envelope fields are enumerated in the manifest as
  excluded-by-design; the non-reproducible set is enumerated rather than hand-waved; isolation
  enforcement holds across the full range.
- **Stop conditions:** determinism unachievable without source change; isolation weakened for
  convenience at scale.
- **Approval gate:** Dustin reviews the replay design and the non-reproducible set.

---

### EA-8 — As-of dataset and look-ahead control

- **Question:** can inputs be reconstructed per date with **no look-ahead**?
- **Authorized work:** build per-date quote fixtures and **as-of-truncated** OHLCV parquet
  caches (I-2 — the leakage crux). Record provenance per `spec/DATA_PROVENANCE_CONTRACT.md`:
  source, retrieval timestamp, vendor and canonical symbol, timeframe, timezone, exchange
  session and calendar, raw versus adjusted semantics, split and dividend treatment,
  missing- and duplicate-bar policy, date range, row count, checksum. Build an explicit
  **look-ahead assertion suite**: for every replay date, no input row may carry a timestamp
  after the as-of boundary. Raw vendor data untracked unless redistribution rights are known;
  manifests and checksums tracked.
- **Outputs:** `A/engine/data/README.md`; `A/engine/data/manifests/`; `A/engine/tools/dataset/`;
  `A/engine/EA-8-ASOF-CONTRACT.md`.
- **Entry criteria:** EA-7 complete.
- **Completion criteria:** the look-ahead suite passes across the full replay range; every
  dataset carries an immutable manifest and checksum; the evaluable range is stated with its
  coverage limits.
- **Stop conditions:** a required input cannot be reconstructed as-of — **narrow the evaluable
  range and record the limit; never approximate**.
- **Approval gate:** Dustin approves the as-of contract and the evaluable range.

---

### EA-9 — Evaluation target and outcome design *(pre-registered)*

- **Question:** what is a "great trade," stated testably **before** any fitting?
- **Authorized work:** decompose and evaluate separately — setup selection, direction, entry
  timing, stop placement, target/exit policy, position sizing, instrument and options-contract
  selection, friction and execution quality. Pre-register a **panel** of exit policies (fixed
  R multiples, time-based, trailing) plus the **MFE/MAE oracle as a non-deployable diagnostic
  upper bound only** (§7). Define outcome labels and horizons from available data. Per I-4,
  report underlying directional outcomes separately from options P&L and fabricate no parity.
  Choose the final metric set **only now**, after EA-4 and EA-8 have shown what the data
  supports. Freeze and hash before any result is computed.
- **Outputs:** `A/engine/EA-9-EVALUATION-CONTRACT.md`, frozen with a recorded hash.
- **Entry criteria:** EA-8 complete.
- **Completion criteria:** targets, labels, horizons, metric families and the exit-policy
  panel frozen and hashed; every metric traceable to available data.
- **Stop conditions:** any metric requiring unavailable data; any result computed before the
  contract is frozen.
- **Approval gate:** Dustin approves and freezes the contract. Later changes require a new
  versioned contract, never an edit.

---

### EA-10 — Component attribution

- **Question:** what actually works?
- **Authorized work:** per-gate and per-component diagnostics; cumulative and marginal
  ablation; accepted / rejected / halted cohort comparison; first-rejection and all-rejection
  analysis; redundancy and interaction analysis; confirmation of constructed or unreachable
  gates; threshold sensitivity; regime-conditional performance; defensible counterfactuals for
  rejected candidates; comparison against transparent baselines (always-long, regime-only,
  single-gate). **Evidence standards:** *useful* requires demonstrated improvement in
  discrimination, calibration, stability or risk against a predeclared objective — never mere
  presence in profitable trades. *Harmful* requires more than an in-sample improvement from
  deletion. Absent either, the classification is **unknown**, and unknown is reported.
- **Outputs:** `A/engine/EA-10-ATTRIBUTION.md`; per-gate result tables; run manifests.
- **Entry criteria:** EA-7 and EA-8 complete, EA-9 frozen, **and the EA-5 eligibility register
  approved**. Attribution over `CONDITIONAL` gates is reported as *as-built-with-defect* and
  labelled as such.
- **Completion criteria:** every gate classified works / inert / redundant / harmful /
  unknown, with evidence and confidence.
- **Stop conditions:** attribution requires changing the frozen evaluation contract — that is a
  new pre-registration, not an edit.
- **Approval gate:** Dustin reviews attribution before fitting is authorized.

---

### EA-11 — Fitting and validation

- **Question:** can a stable, explainable configuration improve the engine **outside the data
  used to fit it**?
- **Authorized work:** immutable pre-fit baseline; versioned datasets, features, configuration
  and outcome definitions; chronological fitting, validation and **untouched final-evaluation**
  periods; walk-forward or rolling evaluation; embargo and purging where overlapping labels
  could leak; explicit parameter ownership and defensible ranges drawn from EA-4's
  threshold-ownership map; a **bounded search budget declared in advance**; a log of **all**
  attempted fits including failures; multiple-comparison and researcher-degree-of-freedom
  controls; threshold and parameter stability analysis; regime and subperiod robustness;
  comparison against simpler configurations; realistic sensitivity to data, friction, timing
  and execution. **The EA-5 eligibility register gates what may enter the search — a defective
  gate is EXCLUDED at the harness or DEFERRED to a post-correction re-run, never tuned. No fix
  occurs within this program**; fixes happen only under a separate Dustin-authorized
  CuttingBoard charge, after which §9's regression sequence re-runs affected attribution and
  fitting. Naming follows conventions §g.
- **Outputs:** `A/engine/EA-11-FITTING-PROTOCOL.md` (frozen first);
  `A/engine/fits/<fit-id>/manifest.md`; `A/engine/fits/ATTEMPT_LOG.csv` (every attempt).
- **Entry criteria:** EA-10 complete **and the EA-5 eligibility register approved**.
- **Completion criteria:** the untouched final-evaluation window — **a deferred-inspection
  window per conventions §g, not a holdout** — is evaluated exactly once; any frozen *forward*
  holdout later constituted is likewise touched exactly once; a candidate configuration is
  either supported outside the fitting data or **honestly reported as not supported**.
- **Stop conditions:** any second tuning pass against the holdout; any automatic write of a
  fitted value into CuttingBoard; any fitted value proposed without human approval.
- **Hard rule:** the goal is **not** to force historical profitability.
- **Approval gate:** Dustin approves the protocol before fitting, and the result after.

---

### EA-12 — Findings consolidation and prior-audit cross-check

- **Question:** what must change, in what order — and what did we miss or get wrong?
- **Authorized work:** consolidate findings; classify per §9; propose the smallest correction
  seam per finding. **Only now** read the withheld prior-audit corpus listed in
  `EA-3-WITHHELD-SOURCES.md`, and cross-check: which of our findings they corroborate, which
  they contradict, which they raise that we missed, and which of theirs the evidence does not
  support. Record agreements and disagreements separately — a prior finding is corroboration,
  not authority. **Findings stay separate from implementation.** Any approved CuttingBoard
  change requires a separate Dustin-authorized charge in a separate session rooted in that
  repository; this program never implements one.
- **Outputs:** `A/engine/findings/` (one file per finding);
  `A/engine/EA-12-PRIOR-AUDIT-CROSSCHECK.md`; `A/engine/EA-12-CORRECTION-SEQUENCE.md`.
- **Entry criteria:** EA-5 and EA-10 merged; **EA-11 merged if fitting was authorized,
  otherwise Dustin's recorded decision that EA-12 proceeds without EA-11.**
- **Completion criteria:** every material finding carries all required fields; every withheld
  document is read and cross-checked; **independence is demonstrable from the EA-3 read log
  and the phase timeline**.
- **Stop conditions:** any attempt to implement a correction in CuttingBoard; any finding
  revised to match a prior audit without independent evidence.
- **Approval gate:** Dustin approves the findings and the correction priority.

---

### EA-13 — Final synthesis

- **Question:** what is the verdict on this engine?
- **Authorized work:** reconcile all evidence into one verdict.
- **Outputs:** `A/engine/EA-13-ENGINE-VERDICT.md` — component-level map of what works, what does
  not, what remains unknown; structural trust verdict; empirical usefulness verdict; replay
  and observability verdict; fitting-readiness verdict; overall recommendation (retain,
  repair, simplify, refit, redesign, or stop); ordered correction sequence by evidence and
  leverage.
- **Entry criteria:** EA-12 complete.
- **Completion criteria:** all four verdicts stated and reconciled, **with disagreements
  between them stated rather than averaged away**.
- **Stop conditions:** any verdict asserted beyond its evidence; any recommendation to change
  CuttingBoard presented as authorization.
- **Approval gate:** Dustin accepts or returns the verdict.

---

## 7. FOUR RESOLUTIONS

### 7.1 The five-gate / four-named-gate discrepancy

**VERIFIED discrepancy, deliberately unresolved.** The docstring at
`runtime/__init__.py:629` calls this "the five-gate decision chain." The body applies **four**
named gate functions — `apply_execution_policy_to_decisions`, `apply_thesis_gate`,
`apply_invalidation_gate`, `apply_entry_quality_gate` — around a materialization step
(`create_trade_decision`, which consumes `chain_results`) and a terminal outcome derivation
(`decision_is_actionable`). Whether the fifth "gate" is chain validation, the materialization
step, the outcome derivation, or upstream qualification is **UNKNOWN**.

My prior report listed four constructs under a "five-gate" label without flagging it. It is
now registered as **EA-4 adjudication item #1** and as the first candidate contract-versus-code
divergence. It is not resolved in planning, because resolving it *is* audit work.

### 7.2 "Nothing edited in place" versus status-line edits

The two are reconciled by which documents are protected. Conventions §b, read across by §h,
protects **frozen specification, manifest, and audit documents** from in-place edits.

- `audits/cuttingboard-engine-strategy-audit/README.md` **is** a frozen TV-0 authority with a
  recorded hash. **Phase 0 does not touch it.**
- Root `README.md` is the repository index. It is not a frozen document, carries no recorded
  hash anywhere, and is edited freely by ordinary repository work.

So Phase 0 edits exactly one pre-existing file — the root index — and otherwise only creates
new files. The claim is now precise: **no frozen document is edited in place; one
non-protected index file is updated.**

The stale line in the frozen audit README is left standing **by design**. That is what §b
intends: a frozen document records what was true when it was frozen. Current lifecycle state
lives in `A/closure/TV-LINE-CLOSURE-2026-07-27.md`, and the root index points there.

### 7.3 Exact README and hash consequences of Phase 0

**Zero recorded hashes change.**

- `A/README.md` is untouched, so its effective hash stays `22d058e0e88f623ecdf7443beb
  5d93226db08ba966903ab2f844bd2baef93850`. **No hash re-issue is required or performed**, and
  the historical TV-0R-examined value `95b8fc4b…` remains on the record unchanged.
- The other four recorded TV-0 hashes and the four amendment hashes are untouched.
- Root `README.md` changes content and therefore changes hash — but **no hash of the root
  README is recorded in any document**, so nothing is invalidated and nothing must be
  re-issued.
- The four new Phase 0 documents are new files. **No document records its own hash** — that is
  self-referential and unsatisfiable, since writing a file's hash into the file changes the
  hash. Instead, after each new document is finalized its SHA-256 is computed and registered
  **externally** in `A/closure/HASHES-2026-07-27.md`, and echoed as ledger rows. The register
  records no hash of its own; **the Dustin-merged commit SHA attests the register.** This
  matches existing repository precedent — `INSTALLATION_RECORD.md` records the hashes of other
  documents, never its own.

Phase 0 completion is verified as: **eight historical hashes re-verified** byte-exact via
`sha256sum`, **three new document hashes registered**, and **the hash register itself attested
by the Dustin-merged commit SHA.**

### 7.4 MFE/MAE as a non-deployable diagnostic upper bound

The MFE/MAE "oracle" exit selects the best achievable exit **with hindsight**. It is therefore
**not implementable in real time and is never a candidate configuration.**

Its only legitimate use is diagnostic: it bounds how much of the outcome spread is
attributable to **exit policy** versus **selection**. If accepted and rejected candidates
separate under the oracle, selection carries information the deployable exits are failing to
harvest; if they do not separate under the oracle, no exit policy can rescue selection.

Binding constraints: every oracle-derived metric is labelled `UPPER_BOUND_NON_DEPLOYABLE`; the
oracle never enters EA-11 fitting; no oracle number may appear in a performance claim,
a recommendation, or the EA-13 empirical verdict except as an explicitly labelled bound.

---

## 8. REPLAY AND TRACE DESIGN

**Architecture boundary.** Strategy holds all tooling, data, sandboxes, traces, runs, fits and
findings. CuttingBoard is read-only at the pin, accessed by `git show` / `git ls-tree` /
`git archive` — **never `git worktree add`, `checkout`, `fetch`, or any working-tree read**.

**Execution model.** Extract the pin into a git-ignored sandbox; run with CWD set to a
Strategy-owned run directory, under **enforced** network denial and write confinement per
EA-1's isolation requirements. The wrapper observes the engine; it never patches pinned source.
CWD confinement is a convenience, not the control — **the control is the enforcement layer**,
because the complete write-set is UNKNOWN until EA-1 and EA-2 establish it (§3).

**Canonical payload versus run envelope.** `SCHEMA_v1.md` partitions every trace into (i) a
**canonical decision payload** — deterministic decision-relevant fields, canonically
serialized (sorted keys, fixed encoding), **engine-derived timestamps only** (`run_at_utc`),
no wall-clock capture times, no absolute paths, no host- or sandbox-specific values — and
(ii) a **run-metadata envelope** (capture wall-clock, sandbox path, host incidentals)
**excluded from equality by enumeration**. Every reproduction claim in this program applies to
the canonical payload only; the envelope is recorded but never compared.

**Trace schema — required fields.** Snapshot SHA, config SHA, environment hash, wrapper
version, schema version · evaluation timestamp and as-of boundary · symbol and candidate
identity · input provenance, timestamps, freshness, missing-data mask · raw and normalized
evidence · intermediate questions, classifications, scores, state transitions · **per gate:
`PASS | FAIL | UNKNOWN | NOT_EVALUATED | INERT`** · ordering, override and precedence events ·
terminal decision and machine-readable reason codes · human-readable explanation · proposed
entry, invalidation, target, sizing and execution assumptions · realized outcomes with
provenance, attached later and versioned separately.

**Every evaluation opportunity is preserved — accepted, rejected and halted.** Rejections are
where "are good trades being filtered out?" is answered; a trade list cannot answer it, which
is precisely the lesson UV02 paid for.

**Contamination protections.** Enforced outbound-network denial with a failed control call as
proof; enforced write confinement with a failed control write as proof; commit-addressed reads
only; sandbox git-ignored; pre/post assertion that CuttingBoard `HEAD` and `git status` are
byte-identical; `TELEGRAM_*` unset as defence in depth only.

---

## 9. FINDING AND VERDICT CONTRACT

**Required fields per finding:** id · class (implementation defect / decision-design or
coherence defect / observability gap / data limitation / weak, redundant, inert or harmful
component / trade-geometry or execution confound / fitting-readiness gap) · exact evidence
(file, line range, pinned SHA, or run-manifest id) · affected behaviour · user-facing
consequence · confidence (VERIFIED / INFERENCE / UNKNOWN) · reproduction method (fixture or
manifest id) · smallest plausible correction seam · **evidence required to prove the
correction worked**.

**Component evidence standard.** *Useful* requires demonstrated improvement in discrimination,
calibration, stability or risk against a predeclared objective. *Harmful* requires more than an
in-sample gain from deletion. Otherwise **unknown** — reported, not rounded.

**Verdict criteria.** *Structural* — no unresolved defect changes a terminal outcome without a
recorded finding. *Empirical* — accepted candidates measurably outperform the rejected
population and the baselines on predeclared metrics, excluding non-deployable bounds.
*Replay* — archived manifests reproduce their **canonical decision payload** byte-for-byte and
the non-reproducible set is enumerated. *Fit-readiness* — inputs, labels, splits and leakage
controls are sufficient for the search actually run.

**Correction and regression sequence.** Finding → Dustin approves finding and priority →
**separate CuttingBoard implementation charge, in a separate session rooted in that
repository, outside this program** → on return, re-run the same structural fixtures, replay
manifests, attribution studies and untouched evaluations to detect regression or real
improvement.

---

## 10. STRATEGY PATH AND PERMISSION MAP

**Canonical root:** `A/` = `audits/cuttingboard-engine-strategy-audit/`. Every path below is
written relative to it, except the single repository-root entry, which is marked as such.

| Path | Purpose | Status |
|---|---|---|
| `README.md` — **repository root** | Repository index — **edited in Phase 0**, no recorded hash | VERIFIED |
| `A/README.md`, `A/INSTALLATION_RECORD.md`, `A/spec/`, `A/charges/`, `A/adjudications/` | TV-line authorities — **untouched** | VERIFIED |
| `A/diagnostics/uv02/` | UV02 evidence — **frozen, closed, byte-identical** | VERIFIED |
| `A/closure/` | TV-line and UV02 closure records, plus `HASHES-2026-07-27.md` | PROPOSED |
| `A/engine/charters/` | EA commission and per-phase charges | PROPOSED |
| `A/engine/EA-*.md`, `A/engine/EA-5-ELIGIBILITY.csv`, `A/engine/EA-3-READ-LOG.csv` | Phase deliverables and registers | PROPOSED |
| `A/engine/env/` | Pinned environment lockfile and hash | PROPOSED |
| `A/engine/sandbox/` | Extracted pinned source and per-run CWD — **git-ignored** | PROPOSED |
| `A/engine/tools/{replay,trace_capture,dataset}/` | Strategy-owned tooling, versioned per §c/§d | PROPOSED |
| `A/engine/data/{manifests,raw,normalized}/` | As-of datasets; raw untracked unless rights known | PROPOSED |
| `A/engine/{fixtures,trace,runs,fits,findings}/` | Fixtures, schemas, immutable runs, fit manifests, findings | PROPOSED |
| `A/engine/LEDGER.csv` | Authoritative run record (§f) | PROPOSED |

**Permissions.** `dwats250/strategy` — read/write; the only authorized mutation target; draft
PRs only; no merge without Dustin. `dwats250/cuttingboard` — **read-only, at the pin only,
commit-addressed**; no fetch, checkout, branch, worktree, stash, commit, reset, merge, rebase,
push, remote change, issue, PR, comment, review, workflow, release, or setting. Capability is
not authorization. `~/Projects/cuttingboard` — read-only inspection of git objects only, never
the working tree.

---

## 11. UNKNOWNS AND BLOCKERS

| # | Unknown | Resolved by | Blocks |
|---|---|---|---|
| U-1 | Complete filesystem write-set | EA-1 static map, confirmed EA-2 | EA-2 authorization |
| U-2 | All network paths, subprocesses, dynamic imports, env/secret reads, external services | EA-1 | EA-2 authorization |
| U-3 | Package imports under a pinned environment; `_run_engine_health_gate()` in a sandbox | EA-2 | EA-2 exit |
| U-4 | Two-run byte-reproducibility | EA-2 | EA-7 design |
| U-5 | Which construct is the fifth "gate" | EA-4 | EA-4 exit |
| U-6 | Trace fields unreachable without source change | EA-6 | Observability findings |
| U-7 | How far back as-of inputs reconstruct | EA-8 | Evaluable range |
| U-8 | Does Dustin hold TV-0R or engine material outside the repository? | **Dustin** | Nothing now |
| U-9 | Is the proxy "not profitable" conclusion recorded anywhere outside Strategy? | **Dustin** | Nothing; Phase 0 records the gap |

**No blocker prevents Phase 0.** U-1 and U-2 block *execution*, which is exactly why EA-1
precedes EA-2. U-8 and U-9 are the only questions repository evidence cannot answer, and
neither gates Phase 0.

---

## 12. DEFERRED

| Tangent | Possible payoff | Why not on the critical path |
|---|---|---|
| Repairing v0.1's `input.time()` compile defect | Would make TV-1 runnable | The Pine instrument is superseded; fixing it buys a translation nobody needs |
| The `UV02-E1` `data_window` export probe | Would unlock per-bar rejection data in Pine | Direct engine execution yields per-candidate rejection data without a TradingView dependency |
| Early reading of CuttingBoard's prior-audit corpus | Possible head start | Would anchor findings to others' conclusions; deliberately withheld to EA-12 |
| Migrating `studies/spy-orb-first-break/`; filling the Faber draft manifest | Tidier repository | Unrelated to the engine audit |
| Intraday/hourly path (`intraday_state_engine.py`, hourly contract) | Broader coverage | Establish the daily path first; scope decision belongs at EA-4 exit |
| Options-chain reconstruction | True options P&L | Stubbed in fixture mode (E-8); needs a data source that may not exist |
| Recording a retrospective UV02 profitability analysis | Would close a documented gap | UV02 §7 forbids the claim class; the engine audit supersedes the question |

---

## 13. SMALLEST FIRST WORK PACKET

**Phase 0 alone — governance cauterization. No engine work of any kind.**

- **Decision advanced:** what work is authorized in this repository right now. Specifically:
  extinguishing TV-1's live commission, which is the only residual authority found.
- **Repositories and permissions:** `dwats250/strategy` — write, one branch, one draft PR, no
  merge. `dwats250/cuttingboard` — **not accessed at all in this packet.**
- **Inputs:** the eight verified hashes; `A/charges/TV-1-PINE-IMPLEMENTATION.md`;
  `A/INSTALLATION_RECORD.md`; `A/diagnostics/README.md`; `A/diagnostics/uv02/
  UV02_STUDY_CONTRACT.md`; repository-root `README.md`.
- **Bounded actions:** create `A/engine/charters/EA-0-COMMISSION.md` **with its
  authority-scope and lapse clause**; create `A/closure/TV-LINE-CLOSURE-2026-07-27.md`
  withdrawing TV-1's commission **and stating its authority basis, supersession enumeration,
  and precedence rule**; create `A/closure/UV02-CLOSURE-2026-07-27.md` recording `UV02-E1` as
  never authorized and not to be opened; create `A/closure/HASHES-2026-07-27.md` registering
  the three other new documents' hashes externally — the register itself is attested by the
  Dustin-merged commit SHA; update the repository-root `README.md` audit
  status line; branch; draft PR; **hold for Dustin's merge.**
- **Expected evidence and deliverable:** a repository in which exactly one lifecycle status is
  documented, that status has a stated authority basis, and no superseded packet retains
  effective authority.
- **Completion criteria:** PR held for Dustin; eight historical hashes re-verified byte-exact,
  three new document hashes registered, and the hash register itself attested by the
  Dustin-merged commit SHA; the **effective-authority test** passes; `git diff`
  shows exactly one pre-existing file modified (repository-root `README.md`) and four files
  added; no frozen document and no UV02 artifact changed.
- **Stop conditions:** any proposed in-place edit to a frozen document; any change to a
  recorded hash; any UV02 artifact modification; any drift into engine work.
- **Explicit exclusions:** no CuttingBoard access; no source extraction; no sandbox; no
  environment setup; no execution; no static safety map (that is EA-1, separately approved);
  no TradingView, Pine, `UV02-E1` probe, v0.3, data download, tuning, backtest, or metric
  computation; no merge.

---

## Verification

**Phase 0** verifies by: eight historical hashes re-verified byte-exact via `sha256sum`, three
new document hashes registered in `A/closure/HASHES-2026-07-27.md`, and the hash register
itself attested by the Dustin-merged commit SHA; the **effective-authority
test** — a grep for TV-1/TV-1R/TV-2/TV-3/TV-4/`UV02-E1` commissioning terms returning hits only
inside frozen documents enumerated as superseded in the closure record, and zero hits outside
that set; `git diff --stat` confirming exactly one pre-existing file modified and four added.

**Phase 0 performs no CuttingBoard check of any kind.** Its no-access guarantee is established
**by construction over the recorded action set**: no command, filesystem operation, tool
invocation, or repository action in the packet targets or inspects a CuttingBoard checkout,
remote, ref, or working tree. **This is a test on operations, not on text** — the Phase 0
documents necessarily *mention* `dwats250/cuttingboard` and the pin SHA, and such textual
references are permitted and expected. A `git status` against the local CuttingBoard checkout would
itself be access, and could not prove absence of mutation anyway: the checkout is already dirty
and ahead of the pin, Phase 0 takes no baseline, and a point-in-time status says nothing about
the remote. Pre/post `HEAD` and `status` assertions belong only to phases that actually perform
commit-addressed reads — first at EA-1/EA-2, where they are relative before/after comparisons
and therefore valid.

**EA-1** verifies by review of the static map against pinned-source line references — no
execution occurs, so verification is reading, not running.

**EA-2** verifies by: a deliberate outbound control call that **must fail**; a deliberate
out-of-boundary write that **must fail**; filesystem diff before and after (observed
write-set); comparison of observed against EA-1's predicted write-set; two-run comparison of
the **canonical decision payload** (determinism); `git -C ~/Projects/cuttingboard rev-parse
HEAD && git status --porcelain` byte-identical before and after. Every claim in every
deliverable carries the command that reproduces it.

---

# Amendment — 2026-07-28: the accepted-path constraint (EA-6-006)

Status: `ACTIVE — NARROW CROSS-PHASE LIMITATION. AUTHORIZES NOTHING NEW.`

A dated amendment appended under `docs/conventions.md` §b, read across to audit artifacts by
§h. Everything above this line is **unchanged**.

**Occasioned by:** [`../engine/findings/EA-6-observability-findings.md`](../engine/findings/EA-6-observability-findings.md)
§ EA-6-006, evidenced by [`../engine/trace/EA-6-cases/`](../engine/trace/EA-6-cases/).

## 1. The constraint

`_fixture_chain_results` (`runtime/__init__.py:1710–1725`, selected at `:1028` in fixture mode)
returns `classification=MANUAL_CHECK` for **every** option setup unconditionally. EA-6 captured
the pipeline reaching the decision layer in full — eight qualified symbols, eight option setups
— with every candidate carrying `decision_status="BLOCK_TRADE"` and `block_reason="fixture mode
skips live chain validation"`, and `outcome=NO_TRADE`.

**The accepted path (`outcome = TRADE`) is therefore structurally unobservable under the
authorized fixture method at this pin.**

## 2. What this amendment permits

**EA-7 and EA-10 may proceed using observable evidence only** — the selection surface from
qualification through the decision chain, plus the rejected and halted populations, which EA-6
demonstrated are captured with per-symbol fidelity.

## 3. What this amendment forbids

- **No accepted-path conclusion may be inferred, reconstructed, or synthesized.** Absence of an
  observable `TRADE` outcome is not evidence about accepted-trade quality, frequency, or value.
  Any metric, verdict, or comparison that would require an accepted population must be reported
  as unavailable, not estimated.
- **This authorizes no live data, no source modification, no instrumentation, and no expansion
  of the fixture method.** EA-1's isolation requirements R-1 through R-19 remain in force
  unchanged.
- Every downstream result touching this boundary must carry the limitation explicitly.

## 4. Closing the gap later

Closing the accepted-path gap requires **separate explicit authorization and evidence** — a
Dustin-authorized charge naming the mechanism (for example a Strategy-owned chain-data
substitution seam, or a CuttingBoard change under its own charge). No such mechanism is
authorized by this amendment, and none may be assumed by a later phase.

## 5. Scope limits — binding

- **This does not alter EA-6's frozen record.** `EA-6-observability-findings.md`,
  `SCHEMA_v1.md`, the emitted traces, and their manifest are unchanged and remain the evidence
  of record.
- **This does not classify the constraint as an engine defect.** EA-6 classed it a *data
  limitation of the harness*, and that classification stands. Fixture mode skipping live chain
  validation is deliberate engine behaviour.
- It changes no phase scope beyond the cross-phase limitation stated in §2 and §3, creates no
  new authority document, and alters no recorded hash.
- It reads, references, and mutates nothing in `dwats250/cuttingboard`.

## 6. Amendment rule

A correction to this amendment is a further dated amendment or a new versioned plan, with the
version in the filename (`docs/conventions.md` §b).
