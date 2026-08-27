# VDC — TERMINAL DISPOSITION · v1.0 · 2026-08-26

Owner/HELM ruling recorded at HEAD `d8a20dd` (long-only single-look validation).
This is a disposition record, not a governance program. Frozen on commit;
corrections are dated amendments (§b/§c).

## Ruling

The current naked **VWAP Drift Continuation (VDC)** family is:

- **RETIRED as a strategy candidate.**
- **RETAINED as a benchmark / research control.**

## Evidence base (already committed; not re-opened)

| Probe | Result |
|---|---|
| R0 reference (TradingView) | PF 1.0401, net +25.69 — REFERENCE-ONLY |
| Symmetric PVAE stratification | PARKED (long/short contrasts disagree, rule C) |
| Local engine calibration | RESEARCH-READY (residual = feed seam + corpus bad-ticks) |
| EMA 10/22 (V1) A/B | DEVELOPMENT NEUTRAL |
| Fixed-risk re-expression | +12.19 R but −$86.64 fixed-share = sizing artifact |
| ATR-stop surface {0.75…1.75} | FLAT / NO MATERIAL R SENSITIVITY |
| Compact 3×3 EMA surface | PARAMETER-INSENSITIVE (all cells within 0.0096 R) |
| Long-only development A/B | MODEST / UNCERTAIN (CI straddles 0, outlier-dependent) |
| **Long-only single-look VALIDATION** | **FAILS VALIDATION** — A (long-only expectancy R > 0) fails at −0.01872; B, C hold |

Across every development probe the naked VDC family is risk-neutral-to-negative;
its one coherent feature (a persistent long-positive / short-negative asymmetry)
directionally replicated out-of-sample (B, C) but did **not** yield a positive
standalone edge (A). The one authorized validation look is consumed.

## Consequences (binding)

- **Do not spend the remaining VDC development configurations.** Final VDC
  interpreted-development accounting stands at **15 / 18**; the unused **3 slots
  are intentionally unused** and are not to be consumed.
- **No further VDC work of any kind**, specifically: no new EMA variant, no ATR-stop
  variant, no long/short variant, no PVAE rescue, no time-of-day filter, no
  volatility filter, no alternate validation slice. The 2026-01-06 → 2026-04-30
  validation window is **consumed** and may not be re-used.
- VDC (symmetric V0) remains available **only** as a control/benchmark in
  comparisons (e.g., the FPC family measures itself against it), never as a
  candidate to be tuned.

## Firewall (unchanged)

No inspection of the embargo (2026-01-02 / 2026-01-05), the unused historical
buffer, the late-May..Aug hypothesis-source outcomes, or the frozen-forward
holdout. No TradingView dependency, no CuttingBoard contact, no merge.

## Amendments

*(append dated amendments here; never edit the text above in place)*
