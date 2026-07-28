# EA-1 — Isolation Requirements for EA-2

Status: `ACTIVE — ENFORCEMENT SPECIFICATION. AUTHORIZES NO EXECUTION.`

Created: 2026-07-27 UTC

Derived from: [`EA-1-EXECUTION-SAFETY-MAP.md`](EA-1-EXECUTION-SAFETY-MAP.md)
Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`

Governing plan: [`../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md) § EA-1, § EA-2.

---

## 0. Standing

This document specifies the enforcement EA-2 must implement **if and when Dustin approves
EA-2**. It authorizes nothing by itself. Every requirement below is derived from a section of
the safety map and cites it.

The governing principle, from the plan §8: **CWD confinement is a convenience, not the
control. The control is the enforcement layer** — because the complete write-set remains
partly undecidable (map §8).

---

## 1. Outbound network denial — MANDATORY

**Requirement R-1.** EA-2 must run the engine with outbound network denied **at process or
container level** — a network namespace with no route (`unshare --net`) or a container with
`--network=none`.

**Why enforcement, not configuration** — map §2.3, finding EA-1-N1 and EA-1-N2:

- `fetch_intraday_bars` performs `yf.download` and is **not** among the two names
  `_fixture_cache_only_ohlcv` patches. It is reachable on the fixture pipeline path.
- `cuttingboard.watch` holds its own unpatched binding of `fetch_ohlcv`.
- The only live-data guard, `_is_live_data_blocked()`, is a Sunday-mode flag, not a
  fixture-mode one.

**`--mode fixture` therefore cannot be assumed network-free.** Any isolation design that relies
on the mode flag would be relying on a property the source does not establish.

**Requirement R-2 — proof obligation.** Enforcement must be demonstrated by a **deliberate
control call to a known host that MUST FAIL**, with the failure recorded as evidence. Absence
of observed traffic is not proof.

**Requirement R-3.** Unsetting `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` (map §5, §7) is
retained as **defence in depth only** and is explicitly **not** accepted as proof of isolation.
It closes one deliberate egress path; it does nothing about the four yfinance call sites.

---

## 2. Write confinement — MANDATORY

**Requirement R-4.** The extracted source tree and every path outside the run directory must be
mounted **read-only**, with **exactly one writable directory** bound in. A write outside it must
**fail**, not merely be absent.

**Requirement R-5 — proof obligation.** Demonstrated by a **deliberate out-of-boundary write
that MUST FAIL**, recorded as evidence.

**Requirement R-6 — the writable directory must contain these roots** (map §1.3), created
before the run so that `mkdir(parents=True)` calls resolve inside the boundary:

```
<run-dir>/logs/            W-01,02,03,06,07,08,10,11,12,13,15,18
<run-dir>/reports/         W-05
<run-dir>/reports/output/  W-15
<run-dir>/data/cache/      W-04  (read path in fixture mode; present so a write cannot escape)
<run-dir>/                 W-14  ./traceback.txt — CWD-root literal
```

**Requirement R-7.** CWD must be set to `<run-dir>`. Every write-path constant in the package
is CWD-relative (map §1.1), so this places the expected write-set inside the boundary — but per
§0 this is convenience; R-4 is the control.

**Requirement R-8 — `config.toml` provenance.** `_CONFIG_TOML` is **package-anchored**, not
CWD-relative (map §6). It is read from the extracted source tree regardless of CWD. EA-2 must
record which `config.toml` was read and its hash as part of the run manifest's config identity.
It is a read, so it is a provenance requirement, not a contamination one.

**Requirement R-9 — `.env` neutralization.** `config.py:16` executes `load_dotenv()` at import
(map §4, I-1), whose search path is undecidable statically (map §8, U-04). EA-2 must ensure no
`.env` is discoverable from the run directory or the extracted tree, and must record that it
verified this. Otherwise an unknown file could silently populate `TELEGRAM_*` or `FIXTURE_MODE`.

---

## 3. Subprocess containment

**Requirement R-10.** The single subprocess (map §3, `runtime:2394`) is gated by
`[engine_doctor] runtime_gate_enabled`, which is `false` in the pinned `config.toml`. EA-2 must
**verify that value in the extracted tree before running** and record it. If it is ever `true`,
the run reaches `tools/engine_doctor.py` with `cwd=_ROOT` — outside the analysed package
surface (map §8, U-08) — and EA-2 must stop rather than proceed.

**Requirement R-11.** Because the subprocess would inherit the sandbox, R-1 and R-4 remain in
force for it; no separate mechanism is required, only the verification in R-10.

---

## 4. Environment control

**Requirement R-12.** EA-2 must run with an explicit, recorded environment. At minimum:

| Variable | Required state | Source |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | unset | map §5, §7 |
| `TELEGRAM_CHAT_ID` | unset | map §5, §7 |
| `FIXTURE_MODE` | set deliberately and recorded — **not** left to inherit | map §5 |
| `PYTEST_CURRENT_TEST` | unset | map §5 |
| `CUTTINGBOARD_FORCE_SLOT` | unset | map §5 |

**Requirement R-13.** `FIXTURE_MODE` (env var) and `--mode fixture` (CLI flag) are **distinct
switches read at different sites** (map §5). EA-2 must record both independently and must not
treat one as implying the other.

---

## 5. Environment pinning and identity

**Requirement R-14.** The Python environment must be pinned and its lockfile hash recorded. The
declared dependency set is `yfinance`, `pandas`, `numpy`, `requests`, `python-dotenv`, `pyarrow`
(map §4); the full transitive closure is undecidable statically (map §8, U-07) and must be
captured from the resolved environment.

**Requirement R-15.** The extracted source must come from `git archive` of the pin to a
git-ignored location — **never `git worktree add`**, which mutates CuttingBoard git metadata.

**Requirement R-16 — CuttingBoard integrity assertion.** `git -C <cb-checkout> rev-parse HEAD`
and `git status --porcelain` must be byte-identical before and after the run.

---

## 6. Observation obligations for EA-2

**Requirement R-17.** EA-2 must produce the **observed** write-set by filesystem diff and
compare it against the map's **predicted** set (map §1.3). Every divergence is recorded as a
finding.

**Requirement R-18.** EA-2 must specifically report whether the map §8 undecidables resolved:

- U-01 — were the unpatched network paths taken? (Observable as blocked-connection attempts
  under R-1.)
- U-02 — did any third-party library write a cache or temp file inside the boundary?
- U-03 — was `dashboard_renderer` `output_path` exercised, and to what path?
- U-04 — was any `.env` discovered?
- U-05 — what happened on read-only or absent output directories?
- U-06 — did any dependency perform network I/O at import time?

**Requirement R-19.** A blocked outbound connection is **evidence, not a failure**. It confirms
finding EA-1-N1 empirically. It must be recorded as an observation and must not be worked
around by relaxing R-1.

---

## 7. Stop conditions for EA-2 — derived

EA-2 must stop and report, rather than proceed, on any of:

1. Any write that lands outside the single writable directory.
2. Any **successful** outbound connection.
3. `runtime_gate_enabled` found `true` in the extracted `config.toml` (R-10).
4. A `.env` discovered that the run did not deliberately place (R-9).
5. Any divergence from this map that the map did not anticipate as possible.
6. Any need to edit pinned source to make the run work.
7. Any change to CuttingBoard git metadata (R-16).

---

## 8. What this document does not do

- It authorizes no execution. EA-2 begins only on Dustin's separate approval.
- It asserts nothing about engine behaviour — only about what the source can reach.
- It proposes no change to CuttingBoard and no correction to any finding. Findings are EA-5's
  and EA-12's to consolidate.
- It reads, references, and mutates nothing in `dwats250/cuttingboard`.

## 9. Amendment rule

Frozen from creation; never edited in place. A correction is a dated amendment file or a new
versioned specification, with the version in the filename (`docs/conventions.md` §b, read
across by §h).
