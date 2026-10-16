# START HERE — strategy research lab

The pipeline this lab supports: **idea → explicit rules → baseline and named variants → repeatable
runs → an interactive report.**

## Run it

```bash
uv sync                       # pinned environment (uv.lock); Python 3.13
uv run pytest                 # 50+ tests on synthetic fixtures; one parity test needs the local corpus
uv run stratlab demo          # SYNTHETIC end-to-end demo -> local_runs/<run>/report.html
uv run stratlab run <experiment.toml>     # real data: baseline + variants -> studies/<study>/exports/runs/<run>/
uv run stratlab data verify  spy-1m-polygon-20240901-20260822-a4afaa70
uv run stratlab data validate spy-1m-polygon-20240901-20260822-a4afaa70 --mask integrity-mask-v1.0
```

`report.html` is a single file. It opens offline on a phone or desktop, with no server and no network.

## Where things are

| Path | What |
|---|---|
| `src/stratlab/data/` | Dataset registry and SHA-256 checks (`store.py`), XNYS sessions and session-anchored bars (`sessions.py`), trade-blind validation (`validate.py`) |
| `src/stratlab/engine.py` | Backtesting.py on 1-minute bars: completed-bar signals, next-minute fills, calendar flatten, per-share costs, trade bookkeeping. Read its docstring. |
| `src/stratlab/strategies/` | One module per strategy. **A new strategy needs only a module and a config.** |
| `src/stratlab/metrics.py`, `windows.py` | Equity metrics (session-close, √252) kept separate from trade R metrics; full / calendar-half / recent windows with exact dates |
| `src/stratlab/experiment.py` | Config → runs → immutable run directory, ledger row, report |
| `src/stratlab/report/` | Self-contained HTML (Plotly and DataTables inlined) |
| `datasets/REGISTRY.json` | Identities of local-only datasets. The data itself is never committed. |
| `studies/<study>/` | Conventions §a skeleton: README, LEDGER.csv, manifests, scripts, exports, analysis |
| `docs/conventions.md` | Standing lab rules. Read before adding a study. |
| `docs/lab/` | `HANDOFF.md` (current state), `ENGINE_BEHAVIOR.md`, `DATA_BACKUP_RECOVERY.md`, recovery findings |

## Adding a strategy

1. Write `src/stratlab/strategies/<name>.py`: subclass `LabStrategy` and set `signal_minutes`.
2. Implement `build_features(sig_bars, **params)`, which is causal and computed on completed signal bars.
3. Implement `on_signal_bar()`, using `self.f(...)`, `self.enter(side, stop, target)` and `self.exit_all(reason)`.
4. Add tests with hand-built bars, like `tests/test_strategies.py`.
5. Write the experiment TOML and freeze it as a versioned file. A config marked `status = "PROPOSED"`
   refuses to run on real data.

Accounting, sessions, costs, metrics and reporting need no changes.

## Rules that bite

- Runs are immutable. The runner refuses to overwrite a run directory.
- Every configuration evaluated gets a ledger row, failures included.
- The latest-N-months window is exploratory and not a holdout (conventions §g).
- Only `dwats250/strategy` is ever mutated (conventions §i).
