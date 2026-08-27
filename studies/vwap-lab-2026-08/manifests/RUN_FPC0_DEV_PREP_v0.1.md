# PREP — FPC-0 first development run · v0.1 · 2026-08-26 · NOT RUN

Pre-run manifest for the **first FPC development configuration (FPC-0)**. This is a
**PREP** record: the run is **not executed** and **no FPC outcome is inspected** in
this packet (owner/HELM charge 2026-08-26). When separately authorized, the run is
frozen to a `RUN_FPC0_DEV_v1.0.md` first, then executed. Frozen on commit;
corrections are dated amendments (§b/§c). Governing family charter:
`FPC_CHARTER_v0.1.md`.

## What this run WILL do (when authorized)

- Simulate **FPC-0 symmetric** (`fastalpha_engine.simulate(..., signal_mode="fpc")`,
  `enable_longs=True, enable_shorts=True`, `atr_stop_mult=1.0`, EMA 9/20) over the
  **development** window **2024-09-03 → 2025-12-31**.
- Corpus view: **screened** (frozen `CORPUS_MASK_v1.0`) **primary**, **raw**
  sensitivity — the established dual-report basis.
- Produce the standard experiment tear sheet (`tearsheet.py`): trades, cumulative R,
  **mean expectancy R (primary metric)**, net $, PF, win rate, max-DD R, long/short
  decomposition, fixed-seed bootstrap CI, outlier concentration, monthly consistency.
- Report FPC-0 **against the VDC symmetric benchmark** (control) via `ab_dual` — VDC
  is now retained only as a research control (`VDC_TERMINAL_DISPOSITION_v1.0.md`).
- Descriptive diagnostics specific to FPC: entries per fresh regime (must be ≤ 1),
  count of fresh regimes that produced no entry (armed-but-expired), and the
  FPC-vs-VDC entry-set difference (how many VDC opposing-candle entries FPC drops).

## Primary question (frozen)

Does restricting entry to the **first** pullback per fresh regime change
risk-normalized expectancy (mean R) versus naked VDC's repeated opposing-candle
entries, on development data? Development is **not** confirmation; a favorable
development result earns at most a later, separately pre-registered FPC validation on
a **fresh** window (charter §8) — never the consumed VDC validation window.

## Firewall (binding)

Development window only (2024-09-03 → 2025-12-31). No inspection of: the VDC
validation window (2026-01-06 → 2026-04-30, consumed), the embargo, the unused
historical buffer, the late-May..Aug hypothesis-source outcomes, or the
frozen-forward holdout. No EMA/stop/window/exit/sizing/cost change from V0 (FPC-0
changes **only** the entry rule). No EMA50/55, PVAE, expansion/persistence,
ShockRatio, volume, RSI, ADX, gap, time-of-day, or ATR-regime structure (charter §6).
No TradingView dependency, no CuttingBoard contact, no merge.

## Code (pinned; frozen already, run pending)

| File | SHA256 |
|---|---|
| `analysis/fastalpha_engine.py` | `26e1fb07641b35deb8461cf7d3af45d25eefcf45462e66448a4c390cba5f5b0e` |
| `analysis/tearsheet.py` | `c950bc6f55cfe1c7493db8ceaf38d529309e67ccd84c435b7fe60b588d0a8fb6` |
| `analysis/test_fpc_signals.py` | `074e73fcb78b9c992e4e17b8f4607e242fd106a88adb7d7f60a7bc5d67a715d5` |

Corpus sha256 `a4afaa704e6ded54f62f1670c52ff74070338ccb943eebcc2f73fe9c170ed97a`.
`signal_mode="fpc"` is verified by `test_fpc_signals.py` (8 cases); the driver
script (`fpc0_dev.py`) is authored in the run packet, not here.

## Budget (§9/§f)

Executing this run spends **FPC configuration 1 of ≤ 12** (FPC-dev **0 → 1/12**),
recorded as a new `family=FPC, budget_class=development` ledger row **at execution**.
**No draw in this PREP packet.** VDC interpreted-development remains **15/18**
(untouched; the 3 unused VDC slots stay intentionally unused).

## Completion criteria (for the future run, not this packet)

Determinism (byte-identical re-simulation); tear sheet emitted for screened + raw;
FPC-vs-VDC benchmark delta reported; per-regime entry-count invariant (≤ 1) asserted
from the trade set; disposition stated **without** selecting a production
configuration and **without** opening any confirmation/holdout work.

## Exact next development-run charge (proposed, not executed)

> "STRATEGY LAB — FPC-0 FIRST DEVELOPMENT RUN. Freeze `RUN_FPC0_DEV_v1.0.md`, then
> run FPC-0 symmetric (`signal_mode='fpc'`, EMA 9/20, stop 1.0) over 2024-09-03 →
> 2025-12-31, screened primary + raw. Emit the standard tear sheet and an `ab_dual`
> vs VDC symmetric (benchmark/control). Report mean expectancy R (primary),
> long/short decomposition, bootstrap CI, outlier concentration, monthly consistency,
> FPC-specific per-regime entry counts (≤ 1) and FPC-vs-VDC dropped-entry count.
> Classify the development effect (BETTER / NEUTRAL / WORSE vs VDC) without selecting a
> production config. Spend FPC config 1/12. Development only — no validation, no
> holdout, no fresh-window confirmation. Commit and push. No merge."

## Amendments

*(append dated amendments here; never edit the text above in place)*
