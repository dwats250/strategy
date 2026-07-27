# CuttingBoard Gate Lab

Status: TV-0 COMMISSIONED — CONTRACT FROZEN FOR FIRST IMPLEMENTATION

Prepared: 2026-07-26 UTC

## Authority and boundary

This is a separate historical-research project. It is not part of
`dwats250/cuttingboard`, does not allocate a CuttingBoard PRD, and may not
modify or feed parameters into CuttingBoard.

The immutable source snapshot for the first study is:

- Repository: `dwats250/cuttingboard`
- Branch: `main`
- Commit: `59f8279d796335149afdec4aa507b6f927233518`
- Commit date: 2026-07-26 UTC

CuttingBoard is read-only evidence. Any possible refactoring suggested by the
study requires a later independent review and an explicit CuttingBoard
decision. Backtest performance alone cannot authorize an engine change.

## Research question

> When translated honestly to completed daily OHLCV data, which reproducible
> CuttingBoard gate families change the historical distribution of
> directional SPY proxy setups, and which gates are redundant, inert,
> unavailable, or dependent on operational/external data?

This study does not reproduce options returns, option-chain liquidity, live
fills, implied volatility, spread pricing, execution quality, or a live
CuttingBoard run. It does not make an alpha or future-performance claim.

## Work packets

1. **TV-0 — Gate contract and experiment design**
   - Source snapshot pinned.
   - Gate translation matrix frozen.
   - Temporal and execution proxies declared.
   - Incremental experiment variants frozen.
   - No Pine code.

2. **TV-1 — Pine v6 implementation**
   - One SPY daily strategy.
   - Gate-family variants and rejection counters.
   - Completed-bar calculations and next-bar-open fills.
   - No threshold tuning.

3. **TV-2 — Parity and semantic verification**
   - Formula fixtures and selected historical cases.
   - Fix translation defects only.
   - Record provider/session mismatches instead of hiding them.

4. **TV-3 — Frozen evaluation**
   - Run the predetermined variants and date windows.
   - Export the full trade list and gate counts.
   - Preserve every run through a manifest.

5. **TV-4 — Offline reproduction**
   - Rebuild the frozen contract in Python.
   - Establish bounded trade-by-trade parity with the Pine output.
   - Continue research without depending on TradingView.

## Current documents

- `spec/GATE_TRANSLATION_MATRIX.md`
- `spec/BACKTEST_PROTOCOL.md`
- `charges/TV-1-PINE-IMPLEMENTATION.md`

## TV-1 script

- [`pine/cuttingboard_direct_proxy_v0.1.pine`](pine/cuttingboard_direct_proxy_v0.1.pine) —
  status: written, **not yet validated**. Compile, chart load, non-daily refusal, variant
  selection, and parity observation are all still outstanding. No parity is claimed.

## Non-negotiable safeguards

- Historical simulation only.
- No broker connection, alerts-to-orders, or automated execution.
- Standard SPY candles only.
- No future-data access or repainting.
- No parameter optimization in TV-0 through TV-3.
- Every result carries the pinned CuttingBoard SHA and Pine source hash.
- Unavailable gates are labeled unavailable; they are never silently treated
  as validated.
- A result may audit CuttingBoard, but cannot mutate CuttingBoard.

