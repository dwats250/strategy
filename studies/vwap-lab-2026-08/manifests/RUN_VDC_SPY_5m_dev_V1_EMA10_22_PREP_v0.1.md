# RUN MANIFEST — V1 EMA 10/22 controlled perturbation (VDC development) · PREP v0.1

**PREP, not frozen, not a run authorization.** Pre-capture preparation for the V1 controlled
variant, per `docs/conventions.md` §b/§c. It is frozen (renamed to a v1.0 run manifest) only if
and when the owner authorizes a V1 TradingView capture. Nothing here interprets performance; no
outcome analysis was run locally (charge constraint).

## Identity & authorization

- Run id (planned): `VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_V1_EMA10_22`
- Family: `VDC` · Budget class: `development` · Role: **controlled single-factor perturbation** of
  the naked VDC v0 strategy — the FastAlpha trading EMA pair only, 9/20 → 10/22.
- Authorization: **owner charge of 2026-08-26 (Dustin), "V1 EMA 10/22 CONTROLLED PERTURBATION."**
  Scope: create the versioned V1 Pine source, this PREP manifest, a static diff proof, and a local
  semantic (candidate-level) sanity comparison; **no outcome analysis before TradingView capture;
  no merge.** Capture disposition (sealed vs interpreted) is set by a later capture charge, not
  presumed here.

## Source pin (exact artifact — controlled variant)

- Variant script: `../scripts/VWAP_Continuation_FastAlpha_V1_EMA10_22.pine`
  sha256 `bca7f7eaf8fd7c93e3400dd72a8661f3d8f9d99219509a2f0fedf3cc03b32519`
  · strategy short-title **`VWAP FastAlpha v1`**
- Base (source of record): `../scripts/VWAP_Continuation_FastAlpha_v0.pine`
  sha256 `c476429225c2ba4abb7c91d370f3abde893d9e4afe83a41ac8a0069e342c6c9e`

## The controlled change — exact semantic diff (proof: `../analysis/v1_ema1022_diff_proof.py`)

V1 is **byte-identical to v0 except four lines**; only two are strategy-semantic:

```
line 79 (SEMANTIC):  int EMA_FAST_LEN = 9   ->   int EMA_FAST_LEN = 10
line 80 (SEMANTIC):  int EMA_SLOW_LEN = 20  ->   int EMA_SLOW_LEN = 22
line  3 (identity):  "VWAP Continuation - Fast Alpha v0"  ->  "... v1 (EMA 10/22)"
line  4 (identity):  shorttitle "VWAP FastAlpha v0"       ->  "VWAP FastAlpha v1"
```

Proof method (deterministic, reproducible): (1) raw line diff = exactly lines {3,4,79,80}; (2)
after neutralizing all comments and double-quoted string literals, the only residual difference is
lines 79–80 (the two EMA length constants). Both source SHA256s are asserted. The two length
constants feed `ta.ema(close, EMA_FAST_LEN)` / `ta.ema(close, EMA_SLOW_LEN)` at section 5 and drive
`bullishState` / `bearishState` (section 6) and the long/short triggers (section 7) — the single
factor under test.

**Everything else is identical, verbatim (deliberate, to keep the perturbation minimal):** session
VWAP, ATR(14), the 1×ATR stop and its tick conversion, the entry window (0935–1530), the
opposing-candle trigger, long/short logic structure, the VWAP-failure thesis exit, EOD flatten at
1550/15:55, sizing (fixed 1), commission 0%, slippage 1 tick, and all broker-emulator /
`strategy()` properties. **No EMA55, no PVAE filter, no slope/volume/shock/gap/RSI/ADX/TOD or any
other filter was added.**

**Retained-verbatim labels (recorded so nothing is misread):** to maximize the byte-identical
region, the internal identifiers `ema9`/`ema20`, the plot titles `"EMA 9"`/`"EMA 20"`, the header
comments, and the timeframe/session guard messages are left exactly as in v0. Under V1 these denote
the **fast (length 10)** and **slow (length 22)** EMAs by definition of this controlled variant. If
a V1 chart-data CSV is ever exported, its `EMA 9` / `EMA 20` columns therefore carry the fast(10) /
slow(22) series. If V1 is later promoted or instrumented, correct these labels in that future
versioned step.

## Execution context — required, exact R0 context (owner confirms at capture)

AMEX:SPY (NYSE Arca) · 5m · RTH · exchange timezone America/New_York · ADJ (dividend-adjusted,
same feed convention as R0/R1) · all R0 strategy Properties unchanged (capital $50,000, fixed qty
1, pyramiding 0, commission 0%, slippage 1 tick, on bar close, order execution delay one tick) ·
development range **2024-09-03 → 2025-12-31 inclusive**. Any deviation from the R0 context
confounds the single-factor comparison and is a STOP.

## No identity gate (this is a deliberate perturbation)

Unlike R1 (instrumentation that must NOT change trades, gated by the R0/R1 identity gate), **V1 is
expected to produce a different trade set than R0.** There is no identity gate. The eventual V1
capture supports a controlled A/B (V1 vs R0) expectancy comparison under a **separate** future
analysis charge; no such comparison is run now.

## Windows & firewall (A3 — unchanged)

Development 2024-09-03 → 2025-12-31 inclusive. Embargo (2026-01-02 / 2026-01-05), validation
(2026-01-06 → 2026-04-30, SEALED), unused buffer, hypothesis-source, and holdout are untouched. If
a chart-data export physically contains post-development rows, they are dropped before any value
column is read.

## Trial accounting (§b) — context, no draw now

- VDC development interpreted runs to date: **2 of ≤ 18** (R0 = 1; R1 first-unseal = 2).
- This PREP draws **nothing**. A future interpreted V1 development run would draw one further
  VDC-development slot; `dsr_threshold_implied` is recomputed in the frozen V1 run manifest before
  that capture, per the §b amendment.

## Local semantic candidate sanity (flat-agnostic — NO OUTCOMES)

From `../analysis/v1_ema1022_diff_proof.py` over the development window (2024-09-03 → 2025-12-31),
comparing LOCAL SEMANTIC CANDIDATES (the flat-agnostic objects `parity_foundation` already
computes; same corpus for both, so the split-only/ADJ feed seam cancels in the differential):

```
dev 5m bars: 25877
long_candidate   v0(9/20)=4489   V1(10/22)=4532   bars differing=115
short_candidate  v0(9/20)=3472   V1(10/22)=3472   bars differing=108
```

Candidate state only — no fills, trades, P/L, or expectancy. This confirms the perturbation is live
and bounded; it is **not** a performance result and pre-judges nothing.

## Capture requirements (owner) and custody (this repo)

1. **V1 List of Trades CSV** (the primary artifact for the future V1-vs-R0 comparison).
2. Chart-data CSV optional (see retained-labels note above if exported).
3. Loaded-bar range, exact Properties, and a fingerprint screenshot.
4. On supply: preserve byte-identical under `../exports/` with sha256; freeze this manifest to
   v1.0; and record per the capture charge's disposition (sealed vs interpreted). No interpretation
   occurs before that charge.

## Minimal TradingView capture procedure (exact)

1. Chart: **AMEX:SPY**, **5-minute**, **Regular Trading Hours**, chart timezone **America/New_York
   (Exchange)**, price/adjustment **ADJ (dividend-adjusted)** as in R0, extended hours **OFF**.
2. Pine Editor → paste the exact V1 source
   (`VWAP_Continuation_FastAlpha_V1_EMA10_22.pine`, sha256 `bca7f7ea…`); confirm the strategy
   short-title reads **`VWAP FastAlpha v1`**; **Add to chart**.
3. Confirm Strategy **Properties** equal R0 exactly (they are baked into the `strategy()` header):
   initial capital 50000, currency USD, order size **fixed 1**, pyramiding 0, commission **0%**,
   slippage **1 tick**, recalculate after order fills OFF, on every tick OFF, process orders on
   close OFF.
4. Strategy Tester → set the backtest / Deep Backtesting range to **2024-09-03 → 2025-12-31
   inclusive**; run; confirm the List of Trades begins on the 2024-09-03 session and ends on the
   2025-12-31 session before exporting.
5. **Export List of Trades** CSV (chart-data CSV optional). Keep Volume on the chart if exporting
   chart data.
6. Record the loaded-bar range and Properties, capture the fingerprint screenshot, and supply the
   file(s). The V1-vs-R0 comparison is a separate authorized analysis — **do not interpret before
   capture.**

## Amendments

*(append dated amendments here; never edit the text above in place)*
