# EA-1 Execution-Safety Map — Amendment, 2026-07-27

Status: `DATED AMENDMENT — TWO REACHABILITY CORRECTIONS. NON-RETROACTIVE.`

Created: 2026-07-27 UTC

Amends: [`EA-1-EXECUTION-SAFETY-MAP.md`](EA-1-EXECUTION-SAFETY-MAP.md)
Occasioned by: [`EA-2-EXECUTION-SEAM.md`](EA-2-EXECUTION-SEAM.md) §5.2 (D-3, D-4) and §5.3

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`.
Mutation permission: **NONE**.

---

## 1. What this document is

A dated amendment under `docs/conventions.md` §b, read across to audit artifacts by §h, and
under the amended document's own § *Amendment rule*: **frozen documents are never edited in
place; a correction is a dated amendment file or a new versioned map.**

`EA-1-EXECUTION-SAFETY-MAP.md` is therefore **unedited and byte-identical**, and so is
`EA-1-ISOLATION-REQUIREMENTS.md`. This file carries the corrections; the map carries what was
said on 2026-07-27 before the seam was run.

Verify none of the three changed:

```sh
cd audits/cuttingboard-engine-strategy-audit
sha256sum engine/EA-1-EXECUTION-SAFETY-MAP.md \
          engine/EA-1-ISOLATION-REQUIREMENTS.md \
          engine/EA-2-EXECUTION-SEAM.md
# 5e7424008ffffb04cd62823f75156056adf126bfb26e80c234cb331c0a1f67ef  engine/EA-1-EXECUTION-SAFETY-MAP.md
# 5f7dfe8bbe22c1a24565279d75df6c38a06531546f3a986abc69ee45412f5dd7  engine/EA-1-ISOLATION-REQUIREMENTS.md
# fb71baf46ccaf70b6ccb0a62248f7307e3307fc53734d896e49efc59e3ae0581  engine/EA-2-EXECUTION-SEAM.md
```

---

## 2. Amendment D-3 — W-11 is mode-gated and excluded from fixture mode

### What the map says

`EA-1-EXECUTION-SAFETY-MAP.md` §1.2 row **W-11** (`runtime:2077,2086,2087`, tmp write +
`tmp.replace`, `TREND_STRUCTURE_PATH` → `logs/trend_structure_snapshot.json`) records the
column *"On `--mode fixture` path?"* as **"Yes"**, and §1.3 lists
`logs/trend_structure_snapshot.json` at confidence **"VERIFIED reachable"**.

### Correction

**That reachability claim is incorrect for fixture mode.** The write is **mode-gated**.
`_refresh_trend_structure_sidecar` (`cuttingboard/runtime/__init__.py:2092`) returns before
reaching the writer:

```python
if mode != MODE_LIVE:
    return
```

Its docstring states the exclusion explicitly: *"refresh logs/trend_structure_snapshot.json
from any MODE_LIVE pipeline run. **Fixture/Sunday modes are excluded.**"*

**Corrected reading of W-11:** *On `--mode fixture` path?* → **No — mode-gated, excluded in
fixture and Sunday modes.** `logs/trend_structure_snapshot.json` is removed from the predicted
fixture-mode write-set in §1.3.

The write-site inventory itself (the three line references, the path constant, and the
CWD-relative classification) is **unchanged and correct**. Only the fixture-path reachability
column and the corresponding §1.3 entry are corrected.

---

## 3. Amendment D-4 — W-12 is reachable only from `_execute_notify_run`

### What the map says

§1.2 row **W-12** (`runtime:2115,2122,2123`, tmp write + `tmp.replace`, `WATCHLIST_PATH` →
`logs/watchlist_snapshot.json`) records *"On `--mode fixture` path?"* as **"Yes"**, and §1.3
lists `logs/watchlist_snapshot.json` at confidence **"VERIFIED reachable"**.

### Correction

**That reachability claim is incorrect.** `_write_watchlist_snapshot` is defined at
`runtime:2111`, but its **only call site is `runtime:564`, inside `_execute_notify_run`** — the
notify path. `_execute_notify_run` is not reached by `cli_main` → `execute_run` →
`_run_pipeline`; per the map's own §1.2 note it is invoked from `alert_runner.py:97`.

**Corrected reading of W-12:** *On `--mode fixture` path?* → **No — reachable only from
`_execute_notify_run` (the notify path), not from the plain `--mode fixture` path.**
`logs/watchlist_snapshot.json` is removed from the predicted fixture-mode write-set in §1.3.

This is a **call-site attribution error** of the same class the map classified correctly for
W-09 and W-19, both of which it marked "No" on identical grounds. The write-site inventory for
W-12 is otherwise unchanged and correct.

---

## 4. Both corrections are conservative over-predictions

**Confirmed by EA-2 observation, not by re-reading source alone.** EA-2 ran the pinned engine
twice under enforced isolation and recorded a nine-file write-set
(`EA-2-EXECUTION-SEAM.md` §3, §5).

- The **observed** write-set is a **strict subset** of the map's **predicted** write-set.
- **No unpredicted write occurred**, and no write left the confinement boundary.
- Both D-3 and D-4 are therefore **over-predictions**: the map named writes that do not occur
  on the fixture path, rather than missing writes that do.

**Direction matters, and this direction is the safe one.** An isolation specification that
predicts more writes than occur is conservative. EA-1 R-6 pre-creates `logs/`, which covers
both corrected items whether or not they fire, so **no isolation requirement changes as a
result of these corrections** and no control was ever under-specified.

---

## 5. This amendment is non-retroactive

- It does **not** invalidate `EA-1-EXECUTION-SAFETY-MAP.md`, which stands as the record of what
  the static analysis concluded before the seam was run.
- It does **not** invalidate `EA-1-ISOLATION-REQUIREMENTS.md`. **Every requirement R-1 through
  R-19 remains in force, unchanged.**
- It does **not** invalidate `EA-2-EXECUTION-SEAM.md` or any EA-2 evidence record. EA-2's
  observations are what established these corrections.
- It does **not** alter any recorded hash, any Phase 0 record, or any frozen TV-line document.
- It applies **forward only**: a later phase consuming the predicted write-set must read the
  map together with this amendment. Nothing already recorded is re-attributed.

---

## 6. EA-1-N1 remains an active finding

**Finding EA-1-N1 is not retired, weakened, or closed by this amendment.**

`fetch_intraday_bars` (`ingestion.py:170`) performs `yf.download` at `ingestion.py:179`; it is
**not** among the two names `_fixture_cache_only_ohlcv` patches (`runtime:1704–1705`); and its
only guard, `_is_live_data_blocked()`, is a Sunday-mode flag rather than a fixture-mode one.
That remains true at the pin.

EA-2 recorded (`EA-2-EXECUTION-SEAM.md` §5.4, U-01) that the path was **not taken on that
input** — `total_candidates=0`, so `_apply_intraday_short_permission` had no `SHORT` candidate
to fetch for. **Not-taken-on-one-input is not unreachable.** EA-1-N1 stands as a source-level
fact about an unpatched network path.

Finding **EA-1-N2** (`cuttingboard.watch` holds its own unpatched `fetch_ohlcv` binding,
`watch.py:20`) likewise stands unchanged.

---

## 7. Controls remain mandatory for EA-3 and every later phase

> **External outbound-network denial and filesystem write confinement remain mandatory.**

Specifically, and without relaxation:

- **Outbound denial enforced at process or container level** (EA-1 R-1), proven by a deliberate
  control call that must fail (R-2). Unsetting `TELEGRAM_*` remains defence in depth only and
  is **not** accepted as proof (R-3).
- **Write confinement enforced at the filesystem level** (R-4), proven by a deliberate
  out-of-boundary write that must fail (R-5).
- A blocked outbound attempt is **containment evidence**, never grounds to weaken the boundary
  (R-19).
- `--mode fixture` must never be treated as implying network isolation. §6 is why.

EA-2 demonstrated these controls are achievable and cost nothing: `bwrap --unshare-net` with a
read-only root and a single writable bind, verified by `Errno 101 Network is unreachable` on
direct-IP egress and `OSError` on three out-of-boundary writes.

---

## 8. What this amendment does not do

- It does not edit `EA-1-EXECUTION-SAFETY-MAP.md`, `EA-1-ISOLATION-REQUIREMENTS.md`,
  `EA-2-EXECUTION-SEAM.md`, or any EA-2 evidence record.
- It does not broaden EA-1's scope, add enumeration surfaces, or revisit any other row.
- It does not interpret engine behaviour, decision output, or trade quality.
- It does not authorize EA-3 or any later phase.
- It reads, references, and mutates nothing in `dwats250/cuttingboard`.

## 9. Amendment rule

Frozen from creation; never edited in place. A correction is a further dated amendment or a new
versioned file, with the version in the filename (`docs/conventions.md` §b, read across by §h).
