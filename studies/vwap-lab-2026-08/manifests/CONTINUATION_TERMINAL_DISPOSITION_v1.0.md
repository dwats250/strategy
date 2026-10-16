# VWAP CONTINUATION LANE — TERMINAL DISPOSITION · v1.0 · 2026-08-27

Owner/HELM ruling recorded at HEAD `49038cb` (FPC-0 first development run). This
concludes the **entire VWAP continuation research lane**. It is a disposition record,
not a governance program. Frozen on commit; corrections are dated amendments (§b/§c).
It extends `VDC_TERMINAL_DISPOSITION_v1.0.md` (which retired naked VDC) to the whole
continuation lane including FPC.

## Ruling

The VWAP continuation lane is concluded: **NO EDGE FOUND.**

Scope of this terminal disposition:

- naked **VDC**
- VDC **EMA variants** (3×3 surface)
- VDC **ATR-stop variants** (5-arm surface)
- **PVAE** stratification
- VDC **long-only** (development + the one validation look)
- **FPC** / first-pullback continuation (FPC-0)

**VDC symmetric V0 is retained only as a benchmark / research control.**

## Evidence base (committed; not re-opened)

| Probe | Result |
|---|---|
| naked VDC (development, all diagnostics) | risk-neutral-to-negative in R |
| EMA 10/22 A/B | DEVELOPMENT NEUTRAL |
| ATR-stop surface {0.75…1.75} | FLAT / no material R sensitivity (sizing artifact in $) |
| 3×3 EMA surface | PARAMETER-INSENSITIVE (all cells within 0.0096 R) |
| symmetric PVAE | PARKED (long/short contrasts disagree) |
| long-only development | MODEST / UNCERTAIN (CI straddles 0, outlier-dependent) |
| long-only single-look VALIDATION | FAILS VALIDATION (A: long-only expR > 0 fails) |
| FPC-0 first development run | FPC DEVELOPMENT WORSE (screened ΔR −0.032, raw agrees) |

Every entry-timing lever on the VWAP/EMA continuation regime has now been probed;
the one durable structural fact (a long-positive / short-negative asymmetry) is about
*side*, not entry geometry, and its long side is not reliably positive on its own.

## Consequences (binding)

- **Both continuation budgets are CLOSED as intentionally unused.** VDC
  interpreted-development final **15/18** — the 3 unused slots are **not** to be
  spent. FPC interpreted-development final **1/12** — the remaining FPC budget is
  **closed**, not to be spent.
- **Do not create another continuation-entry variant** (no further EMA/ATR/long-short/
  PVAE/first-pullback or any other continuation-entry rule).
- VDC symmetric V0 remains available **only** as a benchmark/control in comparisons,
  never as a candidate to be tuned.

## Firewall (unchanged)

No inspection of the embargo (2026-01-02 / 2026-01-05), the unused historical buffer,
the late-May..Aug hypothesis-source outcomes, or the frozen-forward holdout. The
2026-01-06 → 2026-04-30 validation window is consumed. No TradingView dependency, no
CuttingBoard contact, no merge.

## Next lane

A distinct, structurally different family — **VMR (VWAP Mean Reversion)** — is opened
by the same charge as an independent research lane (not a continuation repair). See
`VMR_CHARTER_v0.1.md` and `RUN_VMR0_DEV_PREP_v0.1.md`. No VMR outcome is inspected in
that packet.

## Amendments

*(append dated amendments here; never edit the text above in place)*
