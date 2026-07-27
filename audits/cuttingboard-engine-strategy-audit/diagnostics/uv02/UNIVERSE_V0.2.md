# Universe note — CuttingBoard Direct-Path Proxy v0.2

Status: `NEW UNIVERSE EXPERIMENT — NOT TV-1 EVIDENCE`

Created: 2026-07-26

## What this is, and what it is not

`diagnostics/uv02/cuttingboard_direct_proxy_v0.2.pine` is a **separate universe experiment**. It is not a
continuation of TV-1, not a correction to TV-1, and not TV-1 evidence.

`pine/cuttingboard_direct_proxy_v0.1.pine` is **frozen and untouched**. It remains the
historical diagnostic artifact for TV-1 and the subject of TV-1R. Nothing in this note or in
v0.2 edits, supersedes, or re-opens it, and no v0.2 result may be reported as a v0.1 result.

The reason for the split is substantive, not cosmetic. v0.1 reproduces the pinned
CuttingBoard membership verbatim — `config.ALL_SYMBOLS` minus `config.NON_TRADABLE_SYMBOLS`
for breadth, and `config.EXPANSION_LEADERSHIP_SYMBOLS` for leadership — because the TV-0R
literal-rule appendix requires TV-1 to reproduce those lists without substituting, dropping,
or supplementing a member. **v0.2 deliberately departs from that membership.** It therefore
cannot be used for TV-1 or TV-2 parity: its R-01 breadth and leadership outputs are not
comparable to the pinned engine, by construction and on purpose.

This note replaces a manually patched TradingView copy. Nothing was cherry-picked.

## The 16 breadth members

`TRADABLE_UNIVERSE_SIZE` remains `16.0`, so the breadth arithmetic is unchanged: `>= 0.70` of
16 still requires at least 12 advancing symbols, and 11 advancing (`0.6875`) still fails.

**Broad (3)**

- `AMEX:SPY`
- `NASDAQ:QQQ`
- `AMEX:IWM`

**Metals / miners (5)**

- `AMEX:GLD`
- `AMEX:SLV`
- `AMEX:GDX`
- `AMEX:SIL`
- `AMEX:GDXJ`

**Energy (2)**

- `AMEX:USO`
- `AMEX:XLE`

**Semis / high beta (6)**

- `NASDAQ:NVDA`
- `NASDAQ:AVGO`
- `NASDAQ:AMD`
- `NASDAQ:MU`
- `NASDAQ:TSLA`
- `NASDAQ:SOXX`

This membership is used consistently in the input declarations, cross-symbol acquisition, the
missing-data flags and missing-data count, the advancing-breadth sum, the leadership
calculation, the last-bar state table, and every diagnostic string.

## The 5 leadership members

- `NVDA`
- `AVGO`
- `AMD`
- `MU`
- `SOXX`

Every leadership member is also a breadth member, so unlike v0.1 no leadership member is
structurally ineligible and none contributes a forced zero. The leadership threshold
(`EXPANSION_LEADERSHIP_MIN_PCT = 0.015`) and the minimum count
(`EXPANSION_LEADERSHIP_MIN_COUNT = 2`) are **unchanged**.

## Macro context — unchanged, and not breadth members

`VIX`, `DXY`, `TNX` and `BTC/USD` remain contextual inputs feeding the R-02 vote model, the
kill switch, and macro pressure. They are **excluded from the breadth denominator**, exactly
as the non-tradable macro drivers were in v0.1. Their symbol IDs are unchanged.

## Excluded symbols, and why

**Removed from the v0.1 universe**

- `PAAS` — removed entirely, not merely re-pointed to a different exchange. It was one of the
  two known v0.2 compile defects.
- `AAPL`, `META`, `AMZN`, `COIN`, `MSTR` — replaced as part of the deliberate universe change.
- `SMCI` — removed entirely. It existed in v0.1 only because the pinned leadership list names
  it while `ALL_SYMBOLS` does not, making it structurally ineligible; v0.2 does not reproduce
  the pinned list, so the member and its forced-zero term have no purpose here.

**Discretionary dashboard-only, deliberately kept out of the historical breadth universe**

- `SNDK`
- `UCO`
- `HYMC`
- `DRAM`

These belong to an active discretionary dashboard, not to a historical breadth study. Mixing
them in would let present-day watchlist composition drive historical breadth counts, which is
a selection effect, not a measurement.

**Also not added**

- `SMH` — not added.
- `PAAS` — not re-added under any exchange prefix.

## What was not changed

No threshold, gate order, variant logic, timing model, or friction model was altered. All
seven variants `V0`–`V6` remain in this one source file, selected by the same `Variant` input
and reported through the same `variant_id`; there is no per-variant script. The R-02 vote
cutoffs, R-04 classification bands, R-05 posture cutoffs, structure literals, Gate 6 and Gate
10 comparisons, macro-pressure cutoffs and aggregation, the confirmed-bar/next-open timing
model, and the PARITY/BASE/STRESS friction scenarios are all identical to v0.1.

Only three things differ: universe membership, the two compile defects, and the script
identity (`CuttingBoard Direct-Path Proxy v0.2 (Universe)` / `CB-DIRECT-v0.2`).

## Compile defects corrected in v0.2 only

1. `input.time()` defaults now use the const-foldable date-string form —
   `timestamp("1 Jan 2022 00:00 +0000")` and `timestamp("24 Jul 2026 00:00 +0000")`. The
   `(timezone, y, m, d, h, m)` form is not a constant expression and is rejected as an
   `input.time()` default.
2. `PAAS` removed entirely.

Neither correction is applied to v0.1, which stays frozen.

## Status

This file has **not** been compiled, loaded, or run. No parity, performance, or correctness
claim is made for it. Compile and chart-load results are to be reported from TradingView.
