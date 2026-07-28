# EA-1 — Static Execution-Safety Map

Status: `ACTIVE — STATIC ANALYSIS ONLY. NOTHING WAS EXECUTED.`

Created: 2026-07-27 UTC

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`
Method: commit-addressed reads only (`git archive` of the pin to a read-only scratch location
outside both repositories, then static grep/read). No working-tree read, no fetch, no
checkout, no execution.

Governing plan: [`../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md) § EA-1.

---

## 0. Scope and epistemic status

**Question answered:** *if* the pinned engine were executed, what would it touch — filesystem,
network, subprocesses, imports, environment, secrets, configuration, external services?

**This document makes no claim about engine behaviour.** It reports what the source *contains*
and where control flow *could* reach. Nothing here asserts what the engine does at runtime;
that is EA-2's question, and EA-2 is separately gated.

**Analysed surface:** the executed path of `python -m cuttingboard` — `__main__.py` →
`cuttingboard.runtime.cli_main` — and the `cuttingboard/` package transitively. `tests/`,
`scripts/`, and `tools/` are **not** on that path, with one exception recorded in §3.

**Confidence labels:** `VERIFIED` — directly read at the pin, with file:line.
`INFERENCE` — derived from verified evidence. `UNDECIDABLE` — cannot be settled without
executing code; enumerated in §8.

---

## 1. Filesystem writes

### 1.1 Path-root constants — VERIFIED

| Constant | Value | Anchoring |
|---|---|---|
| `runtime/_constants.py:44` `REPORTS_DIR` | `Path("reports")` | **CWD-relative** |
| `runtime/_constants.py:45` `LOGS_DIR` | `Path("logs")` | **CWD-relative** |
| `runtime/_constants.py:46–58` `LATEST_RUN_PATH`, `LATEST_HOURLY_RUN_PATH`, `LATEST_HOURLY_CONTRACT_PATH`, `LATEST_HOURLY_PAYLOAD_PATH`, `HOURLY_REPORT_PATH`, `MARKET_MAP_PATH`, `LATEST_HOURLY_MARKET_MAP_PATH`, `TREND_STRUCTURE_PATH`, `WATCHLIST_PATH`, `DEFAULT_FIXTURE_DIR` | derived from the two above | **CWD-relative** |
| `audit.py:32` `AUDIT_LOG_PATH` | `"logs/audit.jsonl"` | **CWD-relative** |
| `evaluation.py:31` `EVALUATION_LOG_PATH` | `"logs/evaluation.jsonl"` | **CWD-relative** |
| `contract.py:47` `LATEST_CONTRACT_PATH` | `"logs/latest_contract.json"` | **CWD-relative** |
| `notifications/state.py:24` `LAST_STATE_PATH` | `"logs/last_notification_state.json"` | **CWD-relative** |
| `notifications/hourly_slot.py:19` `LAST_HOURLY_SLOT_PATH` | `"logs/last_hourly_slot.json"` | **CWD-relative** |
| `delivery/transport.py:15–16` `_DEFAULT_HTML_PATH`, `_DEFAULT_JSON_PATH` | `"reports/output/report.html"`, `"logs/latest_payload.json"` | **CWD-relative** |
| `delivery/regime_history.py:27–28` `AUDIT_LOG_PATH`, `REGIME_HISTORY_PATH` | `"logs/audit.jsonl"`, `"logs/regime_history.jsonl"` | **CWD-relative** |
| `output.py:167` `_REPORT_DIR` | `"reports"` | **CWD-relative** |
| `config.py:187` `OHLCV_CACHE_DIR` | `"data/cache"` | **CWD-relative** |
| `config.py:18–19` `_PROJECT_ROOT`, `_CONFIG_TOML` | `Path(__file__).parent.parent / "config.toml"` | **package-anchored — READ only** (§6) |

**Every write-path constant in the package is CWD-relative.** The single package-anchored path
is `config.toml`, and no write to it appears in the package.

### 1.2 Write sites — VERIFIED

| # | Site | Path expression | Root | Class | On `--mode fixture` path? |
|---|---|---|---|---|---|
| W-01 | `audit.py:319` `open(AUDIT_LOG_PATH,"a")` (+ `:315` `makedirs`) | `AUDIT_LOG_PATH` | `logs/audit.jsonl` | CWD-rel | **Yes** — `_run_pipeline` writes one record per run |
| W-02 | `evaluation.py:264` `path.open("a")` (+ `:263` `mkdir`) | `EVALUATION_LOG_PATH` default arg | `logs/evaluation.jsonl` | CWD-rel | **Yes** — `run_post_trade_evaluation` at `runtime:1143` |
| W-03 | `performance_engine.py:36` `output_path.write_text` | caller-supplied; `runtime:1146` passes `LOGS_DIR/"performance_summary.json"` | `logs/performance_summary.json` | CWD-rel | **Yes** — `runtime:1144` |
| W-04 | `ingestion.py:387` `df.to_parquet(cache_path)` (+ `:386` `mkdir`) | `_ohlcv_cache_path()` = `Path(OHLCV_CACHE_DIR)/f"{safe}_ohlcv.parquet"` | `data/cache/*.parquet` | CWD-rel | **Conditional** — only on a live `fetch_ohlcv`; patched in fixture mode (§2.3) |
| W-05 | `runtime:1750,1753` `REPORTS_DIR.mkdir` + `path.write_text` | `_write_markdown_report` | `reports/<date>.md` | CWD-rel | **Yes** — `execute_run` |
| W-06 | `runtime:1776,1786,1791` `target.write_text` | `safe_write_latest`, caller-supplied `LATEST_*` | `logs/latest_run.json` | CWD-rel | **Yes** |
| W-07 | `runtime:1796,1801,1807` `LOGS_DIR.mkdir` + summary writes | `_write_summary_files`, `_rewrite_summary_file` | `logs/` timestamped + latest | CWD-rel | **Yes** |
| W-08 | `runtime:1843` `LOGS_DIR.mkdir` + `_write_contract_file` | `LATEST_CONTRACT_PATH` | `logs/latest_contract.json` | CWD-rel | **Yes** |
| W-09 | `runtime:2009` `_write_hourly_artifacts` | `LATEST_HOURLY_*` | `logs/` | CWD-rel | **No** — hourly path only |
| W-10 | `runtime:2044,2045` `_write_market_map_file` | `MARKET_MAP_PATH` | `logs/market_map.json` | CWD-rel | **Yes** |
| W-11 | `runtime:2077,2086,2087` tmp write + `tmp.replace` | `TREND_STRUCTURE_PATH` | `logs/trend_structure_snapshot.json` (+`.tmp`) | CWD-rel | **Yes** |
| W-12 | `runtime:2115,2122,2123` tmp write + `tmp.replace` | `WATCHLIST_PATH` | `logs/watchlist_snapshot.json` (+`.tmp`) | CWD-rel | **Yes** |
| W-13 | `runtime:2136,2143` tmp write + `tmp.replace` | `_write_macro_snapshot` / `_write_payload_artifacts` | `logs/` | CWD-rel | **Yes** |
| W-14 | `runtime:575` `Path("traceback.txt").write_text` | **string literal** | `./traceback.txt` | CWD-rel | **No** — only `_execute_notify_run` exception path when `notify_mode in _HOURLY_MODES` |
| W-15 | `delivery/transport.py:82,83` `_write_file` | `_DEFAULT_HTML_PATH` / `_DEFAULT_JSON_PATH` | `reports/output/report.html`, `logs/latest_payload.json` | CWD-rel | **Conditional** — depends on delivery mode |
| W-16 | `delivery/regime_history.py:153,155,159` tmp write + replace | `REGIME_HISTORY_PATH` | `logs/regime_history.jsonl` (+`.tmp`) | CWD-rel | **Conditional** |
| W-17 | `delivery/dashboard_renderer.py:2888,2889` | **caller-supplied `output_path`** | unresolved | **dynamically supplied** | **UNDECIDABLE** — see §8 |
| W-18 | `notifications/state.py:130,131` `write_text` | `LAST_STATE_PATH` | `logs/last_notification_state.json` | CWD-rel | **Conditional** — only after a confirmed successful send |
| W-19 | `notifications/hourly_slot.py:120,125` `write_text` | `LAST_HOURLY_SLOT_PATH` | `logs/last_hourly_slot.json` | CWD-rel | **No** — hourly path only |

**Not on the `python -m cuttingboard` path — VERIFIED by import analysis:**
`manual_journal.py:116,117` (`os.makedirs` + `open(path,"a")`) and `review_scorecard.py:206,208`
(`mkdir` + `open(path,"w")`). Neither module is imported by `runtime/__init__.py` or
`__main__.py`.

**No `shutil`, no `tempfile`, no `os.remove`/`os.unlink`/`os.rename` anywhere in the package** —
VERIFIED. The `.tmp` files at W-11/W-12/W-13/W-16 are `Path` objects with a `.tmp` suffix,
atomically committed via `Path.replace`.

### 1.3 Predicted `--mode fixture` write-set — INFERENCE from §1.2

All paths resolve against the **process working directory**.

| Path | Confidence |
|---|---|
| `logs/audit.jsonl` (append) | VERIFIED reachable |
| `logs/evaluation.jsonl` (append) | VERIFIED reachable |
| `logs/performance_summary.json` | VERIFIED reachable |
| `logs/latest_run.json` + timestamped summary | VERIFIED reachable |
| `logs/latest_contract.json` | VERIFIED reachable |
| `logs/market_map.json` | VERIFIED reachable |
| `logs/trend_structure_snapshot.json` + `.tmp` | VERIFIED reachable |
| `logs/watchlist_snapshot.json` + `.tmp` | VERIFIED reachable |
| `logs/` macro/payload artifacts (W-13) | VERIFIED reachable |
| `reports/<date>.md` | VERIFIED reachable |
| `logs/latest_payload.json`, `reports/output/report.html` | INFERENCE — delivery-mode dependent |
| `logs/regime_history.jsonl` + `.tmp` | INFERENCE — conditional |
| `logs/last_notification_state.json` | INFERENCE — only after a successful send |
| `data/cache/*.parquet` | INFERENCE — write patched out in fixture mode; **read** path remains |
| `./traceback.txt` | INFERENCE — not on the plain fixture path |

**Predicted roots: `logs/`, `reports/`, `data/cache/`, and the CWD root itself.**

---

## 2. Network

### 2.1 Clients and URL constants — VERIFIED

| Client | Import | Call sites |
|---|---|---|
| `requests` | `output.py:30` | `output.py:666` `requests.post(url, json=payload, timeout=10)` |
| `yfinance` | `ingestion.py:20`, `chain_validation.py:47` | `ingestion.py:179` `yf.download`, `ingestion.py:293` `yf.Ticker`, `ingestion.py:331` `yf.download`, `chain_validation.py:325` `yf.Ticker` |

No `httpx`, `urllib`, `http.client`, `socket`, or `aiohttp` import appears in the package —
VERIFIED.

| URL constant | Value | Fetched? |
|---|---|---|
| `output.py:655` | `https://api.telegram.org/bot{token}/sendMessage` | **Yes** — `requests.post` |
| `output.py:168` `DASHBOARD_URL` | `https://dwats250.github.io/cuttingboard/dashboard.html` | **No** — string embedded in report text only |

### 2.2 The only live-data guard — VERIFIED

`ingestion.py:61` `_is_live_data_blocked()` returns a `threading.local` flag. It is checked at
`ingestion.py:75` (`fetch_all_quotes`) and `ingestion.py:176` (`fetch_intraday_bars`), raising
`RuntimeError("LIVE_DATA_FORBIDDEN_IN_SUNDAY_MODE")`. Its name and message tie it to Sunday
mode. **It is not a fixture-mode guard.**

### 2.3 Fixture-mode isolation — what is and is not covered

`runtime:1692–1709` `_fixture_cache_only_ohlcv` patches **exactly two** names:

```python
patch("cuttingboard.derived.fetch_ohlcv", side_effect=_cache_only),
patch("cuttingboard.runtime.fetch_ohlcv",  side_effect=_cache_only),
```

`runtime:1629–1646` `_load_inputs` takes the fixture branch and does **not** call `fetch_all()`.
`runtime:1710` `_fixture_chain_results` substitutes chain validation.

| Network path | Covered in fixture mode? | Evidence |
|---|---|---|
| `fetch_all()` quote fetch | **Yes** — not called | `runtime:1629–1646` |
| `fetch_ohlcv` via `derived` namespace | **Yes** — patched | `runtime:1704` |
| `fetch_ohlcv` via `runtime` namespace | **Yes** — patched | `runtime:1705` |
| `fetch_ohlcv` via **`watch` namespace** | **NO — not patched** | `watch.py:20` imports it into its own namespace; used as `daily_fetcher` default at `watch.py:120,143` |
| **`fetch_intraday_bars`** | **NO — not patched anywhere** | Called `runtime:1348` (reached from `_run_pipeline:991`), `evaluation.py:160` (reached from `runtime:1143`), and `watch.py:119,142` defaults |
| Telegram `requests.post` | **No** — gated by credentials, not by mode | §7 |

**Finding EA-1-N1 — VERIFIED.** `fetch_intraday_bars` (`ingestion.py:170`) performs
`yf.download(symbol, period="7d", interval="1m", …)` at `ingestion.py:179`. It is guarded only
by `_is_live_data_blocked()`, which §2.2 shows is a Sunday-mode flag. It is **not** among the
fixture-mode patch targets, and it is reachable on the fixture pipeline path via
`_apply_intraday_short_permission` (`runtime:991` → `runtime:1348`, for every `SHORT`
candidate) and via `run_post_trade_evaluation` (`runtime:1143` → `evaluation.py:160`).

**Finding EA-1-N2 — VERIFIED.** `watch.py:20` binds `fetch_ohlcv` and `fetch_intraday_bars`
into the `cuttingboard.watch` namespace. Patching `cuttingboard.derived.fetch_ohlcv` and
`cuttingboard.runtime.fetch_ohlcv` does not rebind `cuttingboard.watch.fetch_ohlcv`.
`compute_all_intraday_metrics` and `classify_watchlist` are called at `runtime:973–974`.

**Consequence for EA-2 — this is the load-bearing result of EA-1.** Fixture mode cannot be
assumed to be network-free. Outbound denial must be enforced by the environment, not inferred
from the mode flag. Whether these paths are *taken* on any given fixture run is
**UNDECIDABLE** here (§8) and is EA-2's to observe.

---

## 3. Subprocesses

**Exactly one — VERIFIED.** `runtime/__init__.py:18` imports `subprocess`; the single call is
`runtime:2394`:

```python
result = subprocess.run(
    [sys.executable, str(_DOCTOR_PATH), "--json", "--baseline", str(_BASELINE_PATH)],
    capture_output=True, text=True, cwd=str(_ROOT),
)
```

- Enclosing function `_run_engine_health_gate` (`runtime:2385`), called from `cli_main:203`
  — **on the CLI path, before `execute_run`.**
- **Gated** at `runtime:2391` by `config.get_engine_doctor_runtime_gate()`, which reads
  `[engine_doctor] runtime_gate_enabled` from `config.toml`. At the pin that value is
  **`false`** (`config.toml`), so the gate returns early and the subprocess does not run under
  the pinned config — VERIFIED.
- On non-zero exit it raises `SystemExit(result.returncode)` (`runtime:2418`).
- This is the one place the executed path reaches outside the `cuttingboard/` package, into
  `tools/engine_doctor.py` and `tools/baseline.json`, with `cwd=_ROOT`.

No `os.system`, `os.popen`, `os.exec*`, `pty`, or bare `Popen` appears anywhere in the package
— VERIFIED.

---

## 4. Imports

**Declared dependencies** (`pyproject.toml`) — VERIFIED: `yfinance>=0.2.40`, `pandas>=2.0.0`,
`numpy>=1.26.0`, `requests>=2.31.0`, `python-dotenv>=1.0.0`, `pyarrow>=14.0.0` (parquet I/O).
Optional: `yahooquery>=2.3.0` (`chain` extra); dev: `pytest`, `ruff==0.15.22`, `PyYAML`.

**Third-party names imported by the package** — VERIFIED: `pandas`, `yfinance`, `requests`,
`dotenv`. Everything else is stdlib (`argparse`, `collections`, `concurrent`, `contextlib`,
`copy`, `dataclasses`, `datetime`, `enum`, `hashlib`, `html`, `json`, `logging`, `math`, `os`,
`pathlib`, `re`, `statistics`, `subprocess`, `sys`, `threading`, `time`, `tomllib`, `types`,
`typing`, `unittest`, `zoneinfo`).

**Import-time side effects — VERIFIED:**

| # | Site | Effect |
|---|---|---|
| I-1 | `config.py:14,16` `from dotenv import load_dotenv` / `load_dotenv()` | **Executes at import.** Searches for and reads a `.env` file and injects its contents into `os.environ`. This is a **filesystem read outside any declared path constant** and a **secret-loading side effect** that fires merely by importing `cuttingboard.config`. |
| I-2 | `config.py:54,55` | `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` are read from `os.environ` **at import time**, after `load_dotenv()` has run — so a `.env` file can populate them. |

**Notable — VERIFIED:** `runtime/__init__.py:25` imports `from unittest.mock import patch` into
**production** code, used for the fixture-mode monkeypatching in §2.3. Recorded as an
observation about the isolation mechanism's construction; no judgement is offered here.

---

## 5. Environment and secrets

| Variable | Site | What it gates | When unset |
|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | `config.py:54` | Telegram send | `output.py:606,621` → audit reason `not_configured`, **no HTTP request** |
| `TELEGRAM_CHAT_ID` | `config.py:55` | Telegram send | same as above |
| `FIXTURE_MODE` | `runtime:2008`, `runtime:2150`, `delivery/dashboard_renderer.py:557,2993` | Compared to `"1"`; defaults `"0"` | Non-fixture rendering/artifact branch |
| `PYTEST_CURRENT_TEST` | `output.py:103` | Part of a notification run-scope key, combined with `os.getcwd()` | Empty string |
| `CUTTINGBOARD_FORCE_SLOT` | `alert_runner.py:45` | Hourly slot forcing | **Not on the `python -m cuttingboard` path** |

**All five may additionally be supplied by a `.env` file** via I-1 — VERIFIED.

Note `FIXTURE_MODE` (an env var) is **distinct** from `--mode fixture` (a CLI flag). They are
separate switches read at different sites; this map does not claim they are equivalent.

---

## 6. Configuration loading

- `config.py:18` `_PROJECT_ROOT = Path(__file__).parent.parent` — **package-anchored**, derived
  from the module's own location, not the CWD.
- `config.py:19` `_CONFIG_TOML = _PROJECT_ROOT / "config.toml"`.
- Read at `config.py:28` (`get_flow_data_path`) and `config.py:43`
  (`get_engine_doctor_runtime_gate`), both accepting an override parameter and both defaulting
  to `_CONFIG_TOML`. Parsed with `tomllib`.
- `config.py:23–26` documents `get_flow_data_path` as "Never reads from environment variables."
- `config.toml` at the pin contains `[flow] data_path = ""` and
  `[engine_doctor] runtime_gate_enabled = false` — VERIFIED.
- **No write to `config.toml` appears in the package** — VERIFIED.

**Consequence:** `config.toml` is read from the *extracted source tree*, wherever that is
placed — it does **not** follow the CWD. An isolation design that redirects only the CWD leaves
this read pointed at the source tree. It is a read, not a write, so it is a provenance concern
rather than a contamination one.

Second config-ish surface: `load_dotenv()` (I-1) discovers `.env` by its own search rules,
which are neither CWD-constant nor package-constant from the source alone — **UNDECIDABLE**
(§8).

---

## 7. External services

**One — VERIFIED: Telegram.**

- Endpoint `https://api.telegram.org/bot{token}/sendMessage`, `output.py:655`.
- Transport `requests.post(url, json=payload, timeout=10)`, `output.py:666`.
- Single dispatch point `send_notification` (`output.py:748`); duplicate suppression by logical
  hash at `output.py:761–772`.
- **Firing conditions:** `output.py:606–607` reads `config.TELEGRAM_BOT_TOKEN` and
  `config.TELEGRAM_CHAT_ID`; when absent it records `not_configured` (`output.py:621,629`) and
  returns without issuing a request.
- Reachable from `_run_pipeline` via `runtime:821,829` (`alert_sent = send_notification(…)`)
  and from `_execute_notify_run` at `runtime:494,580`.

**GitHub Pages** (`DASHBOARD_URL`) is a literal embedded in report text; no fetch of it appears
— VERIFIED.

No other transport, webhook, email, or cloud SDK appears in the package — VERIFIED.

---

## 8. Statically undecidable — explicitly recorded

Per EA-1's completion criteria, these cannot be settled without executing code. Each is EA-2's
to observe under enforcement.

| # | Item | Why undecidable |
|---|---|---|
| U-01 | Whether the §2.3 unpatched network paths are actually *taken* on a given fixture run | Depends on candidate generation and whether any `SHORT` candidate exists — a data-dependent branch |
| U-02 | Whether `yfinance`, `pandas`, or `pyarrow` write caches or temp files of their own | Third-party internals; not visible in the package source |
| U-03 | `delivery/dashboard_renderer.py:2889` `output_path` (W-17) | Caller-supplied parameter; no default in the module |
| U-04 | Where `load_dotenv()` (I-1) searches and whether a `.env` exists there | Depends on `python-dotenv` search behaviour and the filesystem at run time |
| U-05 | Behaviour when `logs/`, `reports/`, or `data/cache/` is read-only or absent | Exception paths not traceable to a definite outcome statically |
| U-06 | Whether any dependency performs network I/O at import time | Third-party internals |
| U-07 | The full transitive dependency closure beyond the declared six | Requires resolving the environment, which is EA-2's pinned-lockfile step |
| U-08 | Whether `tools/engine_doctor.py` (§3) writes anything, if the gate were enabled | Outside the analysed package surface; gate is `false` at the pin |

---

## 9. Completion statement

Every write site, network path, subprocess, environment/secret read, configuration load, and
external-service path on the executed surface is enumerated above with pinned-source evidence,
or explicitly recorded as undecidable in §8. The predicted fixture-mode write-set is stated in
§1.3. The isolation requirements derived from this map are specified separately in
[`EA-1-ISOLATION-REQUIREMENTS.md`](EA-1-ISOLATION-REQUIREMENTS.md), and both are reviewable
**without having run anything**.

**No stop condition fired.** The map was completed from source without executing code; no
network or write path was found that the §2/§3 mechanisms cannot contain (see the companion
document); and nothing was run.

**EA-2 is not authorized by this document.** Execution requires Dustin's separate approval,
granted after reading this map.

## 10. Amendment rule

Frozen from creation; never edited in place. A correction is a dated amendment file or a new
versioned map, with the version in the filename (`docs/conventions.md` §b, read across by §h).
