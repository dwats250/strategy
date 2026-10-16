# SOURCE PROVENANCE + MECHANICAL CHARACTERIZATION — VWAP Continuation "Fast Alpha v0"

Dated record, 2026-08-25. Owner-charged lane-1 source ingest.

## Provenance

| Field | Value |
|---|---|
| Original title | `VWAP Continuation - Fast Alpha v0` |
| Short title | `VWAP FastAlpha v0` |
| Pine version | 6 (`//@version=6`) |
| Ingest date | 2026-08-25 |
| Immutable source path | `scripts/VWAP_Continuation_FastAlpha_v0.pine` |
| Source SHA256 | `c476429225c2ba4abb7c91d370f3abde893d9e4afe83a41ac8a0069e342c6c9e` |
| Supplied by | Owner (Dustin), directly from TradingView, verbatim payload in the ingest charge |
| Source status | **SOURCE INGESTED / PARITY PENDING** |

The `.pine` file is immutable source evidence (`docs/conventions.md` §c): never cleaned,
reformatted, or "improved." Any behavioral change is a new version file.

## Mechanical characterization (derived from the code only)

Where code and comments could differ, the code governs; comments are recorded as the
source's stated contract, not proof of emulator behavior.

### Strategy declaration

Pine v6 · initial capital 50,000 USD · sizing `strategy.fixed`, 1 unit · pyramiding 0 ·
commission `percent` 0.0 · slippage 1 tick · `calc_on_order_fills=false` ·
`calc_on_every_tick=false` · `process_orders_on_close=false`.

### Chart / session contract

Requires a 5-minute chart (runtime error otherwise) and RTH-only data (runtime error if
`session.ispremarket or session.ispostmarket` is ever true). Documented benchmark: SPY,
standard candles. Timezone logic: `America/New_York` via `hour(time, TZ)*100 +
minute(time, TZ)` — all HM comparisons use **bar-start** timestamps. `inRTH =
session.ismarket`; `newRTH = session.isfirstbar_regular`.

### Entry window

`inEntryWindow = inRTH and currentHM >= 935 and currentHM < 1530`, on bar-start times.
On the intended 5m chart: **first eligible signal-bar start 09:35**, **last eligible
signal-bar start 15:25** ET. Signal-bar time is distinct from entry-fill time (below).

### Session VWAP (load-bearing: NOT `ta.vwap()`)

Manual accumulation, reset each RTH session: on `newRTH`, `cumulativePV := hlc3*volume;
cumulativeV := volume`; on each subsequent `inRTH` bar, `+=` the same; else both `na`.
`sessionVWAP = cumulativePV/cumulativeV` when `inRTH` and `cumulativeV > 0`, else `na`.

**Local-parity rule:** reconstruct the RTH 5-minute OHLCV bar FIRST, then accumulate
`((high_5m+low_5m+close_5m)/3) * volume_5m`. Provider vendor `vw`, 1-minute `vw`
aggregation, tick-level VWAP, and 1-minute session VWAP sampled at 5 minutes are all
**different quantities** and are not used.

### EMA / ATR

`ema9 = ta.ema(close, 9)`, `ema20 = ta.ema(close, 20)`, `atr14 = ta.atr(14)`. **No session
reset** — on the required RTH-only chart these run over the continuous sequence of RTH
5-minute bars across session boundaries; extended-hours bars must never enter the input
sequence. Implication preserved: the first true range of a new session references the
previous session's final RTH close, so the overnight gap can affect ATR14.

Recurrences implemented locally per the published Pine reference pseudocode (EMA:
`alpha=2/(len+1)`, SMA seed; ATR: RMA of true range, `alpha=1/len`, SMA seed; first-bar
TR = high−low when no previous close). **Exact TradingView initialization/warm-up and
floating-point behavior: PARITY PENDING — not guessed silently** (see `../PARITY_GATES.md`
Gate 2).

### Directional state / trigger

`bullishState = close > sessionVWAP and ema9 > ema20`; `bearishState` mirrored. No EMA50
exists in naked VDC v0 (EMA50 belongs only to future observational PVAE instrumentation).
`redBar = close < open`; `greenBar = close > open`; a doji (`close == open`) is neither.
`flat = strategy.position_size == 0`. `longSignal = inEntryWindow and flat and
bullishState and redBar`; `shortSignal = inEntryWindow and flat and bearishState and
greenBar`.

### ATR stop

Computed on the **signal bar**: `atrStopTicks = max(1, int(round((atr14 * 1.0) /
syminfo.mintick)))`; `strategy.exit(loss=atrStopTicks)` is issued alongside the entry.
The ATR distance is frozen from the signal bar — not recalculated later. `syminfo.mintick`
is **not hardcoded locally** until the TradingView symbol contract is captured or otherwise
mechanically established. Entries are gated by `not na(atr14)`.

### Entry order timing

`strategy.entry` is a market order with `process_orders_on_close=false`.
**SOURCE SEMANTIC:** next available emulator tick — historically, normally the next
5-minute bar's open. **EXECUTION PARITY: PENDING TradingView R0 evidence.** No exact
emulator-parity claim is made.

### Thesis exit

`strategy.close("Long"/"Short", comment="VWAP Failure")` when `position_size > 0 and
close < sessionVWAP` (long) or `position_size < 0 and close > sessionVWAP` (short). With
`process_orders_on_close=false`, fill timing is a broker-emulator question — PENDING R0;
no local fill price is assumed.

### End-of-day flatten

`eodFlatten = inRTH and currentHM == 1550` (bar-START time); if a position exists,
`strategy.close_all(comment="EOD", immediately=true)`. Source contract as commented: on
the 5m chart the 15:50 bar closes at 15:55 and `immediately=true` exits on that closing
tick. Recorded as the source contract; actual fills verified against R0.

### Mechanical observations (recorded, not interpreted)

- On shortened sessions (early close ~13:00 ET) no 15:50 bar exists, so the EOD flatten
  never fires; end-of-session position handling there is an open execution-parity item.
- The VWAP `else` branch (non-RTH reset to `na`) is unreachable on a compliant RTH-only
  chart; recorded as written.
- Order interactions on the same bar (pending stop vs thesis close vs EOD `close_all`,
  and `flat` evaluation while exit orders are pending) are emulator questions — PENDING R0.
- Plots/plotshapes are visual only; no behavioral effect.
