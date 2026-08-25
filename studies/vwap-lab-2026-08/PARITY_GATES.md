# PARITY GATES — VDC Fast Alpha v0 local reproduction · status record

Created 2026-08-25 (dated status entries only; append, don't rewrite). Three gates
separate what the local foundation can and cannot claim. **No gate being open blocks
TradingView R0 capture; every gate being closed is required before any local backtest
result could ever substitute for TradingView evidence.**

## Gate 1 — DATA / BAR PARITY: `PENDING`

Do the locally reconstructed Massive 5-minute OHLCV bars match the actual TradingView
chart bars used for R0? **Not assumed.** The recent authoritative TradingView experiment
was identified as `BATS:SPY`; Massive/Polygon stock aggregates may represent a
different/consolidated feed, so exact OHLC — and especially **VOLUME** — may differ.
Because VDC session VWAP is volume-sensitive, feed mismatch can produce legitimate
signal differences. **Never classify such differences as code defects before bar parity
is checked.** Open sub-item: shortened-session 211-bar behavior and the terminal partial
5-minute bucket vs TradingView early-close bars.

## Gate 2 — SEMANTIC / FEATURE PARITY: `LOCALLY VERIFIED / TV CONFIRMATION PENDING`

Given identical 5-minute OHLCV input bars, does local code reproduce session VWAP, EMA9,
EMA20, ATR14, state, and trigger per Pine semantics? Local status (2026-08-25):
`analysis/parity_foundation.py` implements the exact source mechanics (manual 5m-hlc3
session VWAP with per-session reset; continuous cross-session EMA/ATR over the RTH-only
sequence; entry-window/bar-color/doji rules), verified by the deterministic tests in
`analysis/test_parity_foundation.py` (9/9 pass). EMA/RMA/ATR recurrences and SMA seeding
follow the published Pine reference pseudocode; **exact TradingView initialization /
warm-up / float behavior remains unconfirmed against TV output — this gate does not
reach full PARITY until compared with TradingView evidence.**

## Gate 3 — EXECUTION / BROKER-EMULATOR PARITY: `PENDING R0 TRADE-LIST EXPORT`

Entry fills, slippage, ATR-stop placement/fills, same-bar stop behavior, thesis-exit
order/fill timing, EOD immediate fill, early-close session handling (no 15:50 bar
exists on shortened sessions, so the source's EOD flatten never fires there), pending-
order interactions with `flat`, trade sequence, and P/L. **No emulator is implemented
and none may be built under the current charge.** Nothing local claims execution parity.
