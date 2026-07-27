# UV02 capture log — Universe Relevance Study, v0.2

Status: `DIAGNOSTIC RAW EVIDENCE — NOT A TV-3 PACKAGE, NOT TV-1 PARITY`

Captured: 2026-07-26 · Logged: 2026-07-26

## What these captures are

Seven TradingView **List of Trades** exports, one per variant `V0`–`V6`, produced by
[`cuttingboard_direct_proxy_v0.2.pine`](cuttingboard_direct_proxy_v0.2.pine) on a SPY 1D
standard-candle chart.

They are **diagnostic raw evidence only**. They are not a TV-3 run package, they do not
satisfy `../../spec/BACKTEST_PROTOCOL.md` § *Required exports*, and they carry no parity claim
against `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`. See
[`UNIVERSE_V0.2.md`](UNIVERSE_V0.2.md) for why v0.2 is not comparable to the pinned engine.

No profitability, alpha, live-execution, or options-return claim is made or supported here.

## Script binding

| Field | Value |
|---|---|
| Source file | `diagnostics/uv02/cuttingboard_direct_proxy_v0.2.pine` |
| SHA-256 | `d2420bc398d3e23f477d71edbd5e6f1cdb51e377380c2e000f1a0bc63eba53ce` |
| Pine version | v6 |
| Script identity | `CuttingBoard Direct-Path Proxy v0.2 (Universe)` / `CB-DIRECT-v0.2` |

Every export filename embeds `d2420bc3`, the first eight hex digits of that SHA-256, so each
capture is bound to the exact bytes that produced it. **The Pine file must never be edited in
place**: doing so would break that binding and silently orphan all seven captures. A change
gets a new file and a new hash, per `docs/conventions.md` §e.

## Export inventory

Chart symbol `SPY`, timeframe `1D`, candle type standard OHLC, window `FULL` chart history,
as-of `2026-07-24`.

| Variant | File | SHA-256 | Rows | Captured |
|---|---|---|---|---|
| V0 | `exports/UV02-d2420bc3-SPY-1D-STD-FULL-V0-ASOF-2026-07-24.csv` | `067d0f0b0c1107bbe0e63823ace1c38d641087c603b12305a8c1ab90e45f631d` | 1835 | 18:56 |
| V1 | `exports/UV02-d2420bc3-SPY-1D-STD-FULL-V1-ASOF-2026-07-24.csv` | `549cc56aeeb57954de88f3c0f862f09a52ef45509a5b21b119ab23059d0b1e33` | 815 | 19:57 |
| V2 | `exports/UV02-d2420bc3-SPY-1D-STD-FULL-V2-ASOF-2026-07-24.csv` | `eff9cb62d56cc89608da2eeb48607e9bef1701150fa51128a6a911dfda7f395e` | 675 | 19:58 |
| V3 | `exports/UV02-d2420bc3-SPY-1D-STD-FULL-V3-ASOF-2026-07-24.csv` | `17e596fea0e3b570dea07f6a9edf48b200abcbc41a4f2ccb8a815ba5ac602e23` | 277 | 19:59 |
| V4 | `exports/UV02-d2420bc3-SPY-1D-STD-FULL-V4-ASOF-2026-07-24.csv` | `3eee1582fd64aee560a3bbfe395439fd7534089d11e13655a772b2722b4b4eb8` | 253 | 19:59 |
| V5 | `exports/UV02-d2420bc3-SPY-1D-STD-FULL-V5-ASOF-2026-07-24.csv` | `163e4ad617985ef7cdfe24aec5f67de130310924c98be802a6faa524e4edf592` | 251 | 19:59 |
| V6 | `exports/UV02-d2420bc3-SPY-1D-STD-FULL-V6-ASOF-2026-07-24.csv` | `68f27234797cef3f28db58ea261d6829299edeb7970a5c9eb0f7ce43f7925736` | 185 | 18:53 |

Rows are trade **legs**, not trades, and exclude the header. They are structural counts
recorded for integrity checking. **They are not a result and must not be read as one.**

Exports are immutable (`docs/conventions.md` §e). A re-capture produces new files, never an
edit to these.

## Runtime refusal observed

Running the script on a 15-minute chart produced the intended runtime refusal. This confirms
the frozen-timeframe guard fires. The refusal is diagnostic evidence of the guard, not a
validation pass for the script as a whole.

## Provenance gaps — recorded, not inferred

1. **Friction scenario: `UNRECOVERABLE`.** The v0.2 declaration defaults to the `PARITY`
   scenario (zero commission, zero slippage), but TradingView's Properties tab overrides
   declaration values, and no saved Properties screenshot exists for this capture session.
   Which of `PARITY` / `BASE` / `STRESS` was in force therefore **cannot be established from
   the surviving artifacts and has not been guessed.** Any analysis of these files must treat
   the friction setting as unknown. Future captures must record it before export.
2. **Chart timezone, session setting, extended-hours flag, and data provider / exchange feed
   are unrecorded** for this session.
3. **Window is `FULL` chart history, not a predetermined study window.** The earliest observed
   trade row is `2001-04-10`, well before the protocol's 2015 warm-up and 2016 in-sample
   windows. These captures do not map onto the protocol's window structure.
4. **The 2022-01-01 – 2026-07-24 period has been inspected** as part of this full-history
   capture. Per `../../spec/TV-0R-BACKTEST-INTERPRETATION-AMENDMENT.md` it is a
   `deferred-inspection descriptive window`; it was never a forward holdout, and **its
   pre-inspection status cannot be restored.** No artifact in this project may describe it as
   untouched or out-of-sample.

## What these exports structurally cannot supply

The TradingView List of Trades carries: trade number, type, date, exit signal, price, size,
net PnL, return %, commission, favorable/adverse excursion, cumulative PnL, and duration.

Against `../../spec/BACKTEST_PROTOCOL.md` § *Required exports* it does **not** carry: any gate
boolean; the first rejection gate or the full rejection set; regime, posture, confidence, net
score, or vote coverage; the structure label or its derived inputs; the missing-data mask; the
ambiguous-intrabar flag; cumulative gate rejection counts; results grouped by regime, posture,
or structure; or a `variant` field in the rows — the variant is encoded only in the filename.

This limitation is structural, not a capture error: **a List of Trades contains only trades
that were taken, and rejections never become trades.** Closing this gap is the subject of the
next research gate, `UV02-E1`.

The script already instruments 49 `display.data_window` plot series covering regime, posture,
structure, all eight R-02 votes, breadth and leadership counts, derived-metric divergences,
and per-gate booleans. Whether TradingView's *Export chart data* emits `data_window`-only
series is an open empirical question and is the first item of `UV02-E1`. It has **not** been
tested, and nothing here assumes it works.

## Ledger

`docs/conventions.md` §f makes `LEDGER.csv` — one row per run — the authoritative record, and
it wins over any export or screenshot that disagrees with it. No `LEDGER.csv` exists for UV02
yet. Creating one is the convention-correct next custody step and is recommended, but it is
deliberately **not** created here: its friction column would have to be written
`UNRECOVERABLE` for all seven rows, and that decision belongs to Dustin rather than to this
log. There is no `docs/WORK_LEDGER.md` convention in this repository and none was created.
