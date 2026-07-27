# Run manifest — template

Copy this file into `runs/<run-id>/RUN_MANIFEST.md` and fill every field. A run is not
preserved unless it has **both** this manifest and the full simulated trade ledger. Runs are
immutable once written: a re-run producing new numbers is a new run directory, never an edit
to an old one (`docs/conventions.md` §e).

Runs begin at **TV-3**, after TV-2 parity acceptance. This template exists so TV-1's output is
recordable; creating it does not authorize a run.

Fields marked `AUTO` are readable from the script's data window or state table. Fields marked
`OPERATOR` are not observable from Pine and must be transcribed by hand.

---

## Identity

| Field | Value |
|---|---|
| Run ID | `<YYYY-MM-DD>-<variant>-<window>-<friction>-<nn>` |
| Run timestamp (UTC) | |
| Operator | |
| Packet | TV-3 |

## Source and code

| Field | Value | Source |
|---|---|---|
| CuttingBoard source SHA | `59f8279d796335149afdec4aa507b6f927233518` | frozen |
| CuttingBoard commit date | `2026-07-26T01:35:59Z` | frozen |
| CuttingBoard mutation permission | **NONE** | frozen |
| Pinned SHA resolved for this run? | `YES` / `NO` — if `NO`, say so plainly | OPERATOR |
| Pine source file | `audits/cuttingboard-engine-strategy-audit/pine/cuttingboard_direct_proxy_v0.1.pine` | |
| Pine source SHA-256 | | OPERATOR (`sha256sum` of the exact file pasted into TradingView) |
| Pine version | `v6` | |
| strategy repository commit | | OPERATOR |

If the pasted script differs from the committed file by even one byte, the run is attributed
to code that does not exist in the repository. Re-hash before recording.

## Chart and instrument

| Field | Value | Source |
|---|---|---|
| Chart symbol | | AUTO (state table) |
| Timeframe | `1D` — the script refuses anything else | AUTO |
| Candle type | standard OHLC — the script refuses Heikin-Ashi, Renko, Range, Kagi, Line Break, Point & Figure | AUTO |
| Chart timezone | | OPERATOR |
| Session setting | | OPERATOR |
| Extended hours | | OPERATOR |
| Data provider / exchange feed | | OPERATOR |

## Cross-symbol IDs actually used

Record what the inputs contained for this run, not the defaults.

| Role | Configured ID | Resolved? | Notes |
|---|---|---|---|
| SPY | | | |
| QQQ | | | |
| IWM | | | |
| VIX (`^VIX`) | | | |
| DXY (`DX-Y.NYB`) | | | |
| TNX (`^TNX`) | | | |
| BTC (`BTC-USD`) | | | |
| GLD | | | |
| SLV | | | |
| GDX | | | |
| PAAS | | | |
| USO | | | |
| XLE | | | |
| NVDA | | | |
| TSLA | | | |
| AAPL | | | |
| META | | | |
| AMZN | | | |
| COIN | | | |
| MSTR | | | |
| SMCI (leadership list, verbatim) | | **never requested** | Not in `ALL_SYMBOLS` at the pin, so it can never be in `valid_quotes`. Recorded as found; not substituted or dropped |

Formula parity and data parity are separate. A formula can pass while a provider or session
mapping remains `PROXY`. Record the mapping status honestly.

## Variant and window

| Field | Value | Source |
|---|---|---|
| Variant | `V0` / `V1` / `V2` / `V3` / `V4` / `V5` / `V6` | AUTO |
| Variant definition | per `spec/BACKTEST_PROTOCOL.md` § Incremental variants — gate-family activation only | frozen |
| Window name | | AUTO |
| Window start / end | | AUTO |
| Bars evaluated | | AUTO (`evaluated bars` in the rejection table) |

**Window naming constraint (binding).** The 2022-01-01 – 2026-07-24 period is a
`deferred-inspection descriptive window`. No manifest, report, summary, chart annotation or
export filename may describe it as a genuine forward holdout or as out-of-sample. Its guard
conditions remain in force: it may be inspected only after TV-2 parity acceptance, no
threshold may change after it is inspected, and a provider with later history does not justify
silently shortening the sample — affected bars carry a data-availability flag.

## Friction

Commission and slippage are declared in the script at the `PARITY` values and are overridden
in the strategy Properties tab. Pine cannot read them back, so they are `OPERATOR` fields.
All three scenarios run. Friction is recorded, never chosen or optimized.

| Field | Value |
|---|---|
| Scenario | `PARITY` / `BASE` / `STRESS` |
| Commission type | |
| Commission value | |
| Slippage (ticks) | |
| Initial capital | |
| Order size | one directional unit |
| Pyramiding | `0` |

Scenario definitions (frozen): `PARITY` zero/zero; `BASE` 0.01% per transaction and one
minimum tick per fill; `STRESS` 0.03% per transaction and three minimum ticks per fill.

## Thresholds in force

Every threshold is fixed in the Pine source and identical across variants. Record the block
verbatim from § 2 of the script, or state `unchanged from
pine/cuttingboard_direct_proxy_v0.1.pine § 2` and give the Pine SHA-256 above. **No threshold
may differ between variants or between runs.** A run that changed one is not a variant — it is
a different study.

## Missing-data counts

| Field | Value | Source |
|---|---|---|
| Bars with at least one missing symbol | | AUTO |
| Missing symbols on the final bar (of 20) | | AUTO |
| Missing-vote distribution (0–8) | | OPERATOR (from the exported ledger) |
| Bars where breadth denominator symbols were absent | | OPERATOR |

A missing requested value stays missing. Breadth counts an absent tradable symbol as **not
advancing**, matching the pinned engine. A missing value never becomes a neutral vote.

## Gate results

| Gate | Class | Rejections | Notes |
|---|---|---|---|
| V0 no regime direction | — | | |
| Gate 1 REGIME | AVAILABLE | | |
| Posture rejections (R-05, counted separately) | AVAILABLE | | |
| Gate 2 CONFIDENCE | INERT | | |
| Gate 3 DIRECTION | INERT | | |
| Gate 4 STRUCTURE | AVAILABLE | | |
| Gate 5 STOP_DEFINED | INERT | | |
| Gate 6 STOP_DISTANCE | AVAILABLE | | |
| Gate 7 RR_RATIO | INERT | | |
| Gate 8 MAX_RISK | INERT / UNAVAILABLE_LITERAL | | |
| Gate 9 EARNINGS | INERT (`SKIPPED_FAIL_OPEN`) | n/a | |
| Gate 10 EXTENSION | AVAILABLE | | |
| Gate 11 TIME | **UNAVAILABLE** | n/a | Excluded from the soft arithmetic; record the bar count it was unavailable on |
| Q-12 soft aggregation | AVAILABLE (Gate 6, Gate 10 only) | | |
| K-01 kill switch | AVAILABLE | | |
| E-04 macro conflict | AVAILABLE | | |
| T-01 / I-01 / E-05 | INERT diagnostics | | |

Unavailable is not the same as passing. An excluded gate is reported separately and never
enters the arithmetic (`docs/conventions.md` §h).

## Results

| Field | Value |
|---|---|
| Trades | |
| Long / short split | |
| Exposure | |
| Win rate | |
| Average trade | |
| Profit factor | |
| Maximum drawdown | |
| Gross return | |
| Friction-adjusted return | |
| `AMBIGUOUS_INTRABAR` trades | |
| Results by regime | |
| Results by posture | |
| Results by structure | |
| Incremental delta from the prior variant | |

`AMBIGUOUS_INTRABAR` trades use the conservative stop-first result in the headline metrics.
The flag is exported so offline intraday data can resolve them later; the headline is never
quietly restated as the favourable outcome.

## Raw exports

| File | SHA-256 | Contents |
|---|---|---|
| | | List of trades |
| | | Per-bar gate state |
| | | Performance summary |

The ledger must carry: signal date and next-open fill date; direction, variant, entry, stop,
target and signal ATR; every gate boolean; first rejection gate and all rejection gates;
regime, posture, confidence, net score and vote coverage; structure label and derived inputs;
the missing-data mask; exit reason and the ambiguous-intrabar flag; gross and
friction-adjusted return; MFE/MAE where available; and cumulative gate rejection counts.

Screenshots and summary tables are supplementary. When a screenshot, an export and the
manifest disagree, the manifest and ledger are authoritative.

## Known parity exceptions

Carry forward every open item from
[`../spec/PARITY_CASES.md`](../spec/PARITY_CASES.md) § *Known parity exceptions*, and add any
new one this run surfaced. An exception that is not written down is not disclosed.

| # | Exception | Status |
|---|---|---|
| 1 | Pinned source not resolved during TV-1 | |
| 2 | Declared interpretations DI-4 … DI-6 unresolved (DI-1 … DI-3 quoted from `../spec/TV-1-LITERAL-RECOVERY-AMENDMENT.md`; still unverified until TV-2) | |
| 3 | EMA warm-up divergence (D-01) | |
| 4 | ATR initialization divergence (D-02) | |
| 5 | Provider / session mapping `PROXY` | |
| 6 | End-of-day percent-change proxy | |
| 7 | Tick quantization of protective distances | |
| 8 | Same-bar stop-and-target ambiguity | |

## Declaration

- [ ] No threshold was changed for this run.
- [ ] No CuttingBoard file, ref, branch, PR, issue, workflow, setting or remote was mutated.
- [ ] No parameter, threshold or conclusion from this run was fed back into CuttingBoard.
- [ ] No unavailable gate was recorded as passing.
- [ ] The 2022–2026 window is described only as a deferred-inspection descriptive window.
- [ ] The Pine SHA-256 above is the hash of the exact source that produced this ledger.
