# RUN MANIFEST PREP — R1 (VDC instrumented development) · v0.1 · 2026-08-25

**Status: PREP — NOT FROZEN. This is not a run authorization.** Prepared from
`RUN_MANIFEST_TEMPLATE_v0.1.md` so the R1 manifest can be frozen quickly before capture.
Freeze (new version per template convention, fill remaining OWNER-OBSERVE fields, commit)
**before** the TradingView capture. Authority for building this PREP and the R1 source:
owner charge of 2026-08-25 (Dustin), "STRATEGY LAB — BUILD R1 INSTRUMENTED VDC"; Fable 5
as lane 1 for this charge only, per the owner's standing in-session per-charge
disposition (§j table unchanged).

## Identity & authorization

- Run id: `VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0R1`
- Family: `VDC` · Budget class: `development` · Role: **A1.8 R1 — instrumented VDC
  development; instrumentation must not alter strategy behavior**
- Charter governing: `STUDY_CHARTER_v0.1.md` + Amendments A1, A2, A3;
  `PVAE_ANALYSIS_PREREG_v0.1.md` (frozen covariate definitions)
- R0 reference: frozen at repo commit `a824eb5841941025220092a2ea9325c91a1e6dd7`
  (manifest `RUN_VDC_SPY_5m_dev_R0_v1.0.md`; trade-list export sha256
  `8d2db8dc78bec56594dd26d8a3020eb3c73c2a9dc976cdd421191f8827751241`)
- Capture authorization: **UNRESOLVED — requires an explicit Dustin charge naming the R1
  capture.** Nothing in this PREP runs anything.

## R1 source identity

- Script: `../scripts/VWAP_Continuation_FastAlpha_v0_R1_instrumented_v1.0.pine`
  sha256 `32aaaa4d2148186774921c8529c5ab3600bfe4110ffff2fd0213a6631ff72bc4`
- Base: `../scripts/VWAP_Continuation_FastAlpha_v0.pine`
  sha256 `c476429225c2ba4abb7c91d370f3abde893d9e4afe83a41ac8a0069e342c6c9e`
- Differences from v0, exhaustively: (1) strategy title/shorttitle renamed
  `... v0 R1` — presentation only, all execution properties byte-identical; (2) an R1
  header comment; (3) appended section 13 instrumentation. **v0 lines 19–349 are
  byte-identical to R1 lines 41–371** (verified by `diff`; the single insertion is the
  blank separator line opening the appended region).

## Instrumentation containment — verified before any capture

Static (on the committed R1 source):

- Every executable `strategy.*` reference lies inside the byte-identical v0 copy; the
  instrumentation region contains **zero** executable `strategy.*` references (the one
  textual hit is a comment).
- Every assignment in the instrumentation region targets a new instrumentation-only
  variable (`rthBarsCompleted`, `acceptLongVotes`, `acceptShortVotes`,
  `alignedExpCount`); no v0 variable is written below the v0 copy, and no code above
  section 13 reads an instrumentation variable (instrumentation identifiers do not exist
  before line 371).
- Instrumentation plots use `display = display.data_window`: nothing is drawn on the
  chart; v0 visuals (3 plots, 2 plotshapes) are unchanged.

Local mirror (`../analysis/instrumentation_r1.py`, deterministic tests in
`../analysis/test_instrumentation_r1.py`):

- 19/19 tests pass (10 instrumentation + 9 foundation).
- Containment assertion: all 24 foundation columns — including
  `long_candidate`/`short_candidate` — pass through **byte-identical across all 38,357
  local rows**; the mirror mutates nothing. R1 local semantic candidates are exactly
  the R0 foundation candidates.
- Dev-window availability (counts only; no outcomes, no terciles): 25,877 rows;
  acceptance state available 24,875 (unavailable exactly 334 sessions × 3 warm-up
  bars); expansion available 25,826 (EMA50 seed + 2); RecentShock available 25,860
  (ATR seed + window). Availability arithmetic reconciles exactly.

## Exported instrumentation fields (plot titles = export column names)

| Field | Frozen definition |
|---|---|
| `ACCEPT_STATE_DIR` | A1.2 directional VWAP acceptance state: 1 ESTABLISHED LONG / −1 ESTABLISHED SHORT / 0 MIXED / na unavailable (fewer than 4 completed current-session bars) |
| `EMA50` | `ta.ema(close, 50)` — executed-family slow EMA |
| `S_9_20_50` | A1.4 dispersion `abs(EMA9 − EMA50) / ATR14` |
| `ORDERED_9_20_50` | 1 if EMA9>EMA20>EMA50; −1 mirrored; 0 otherwise; na in warm-up |
| `EXPANDING_9_20_50` | A1.4 `S_t > S_(t−2)` strict → 1/0; na in warm-up |
| `ALIGNED_EXP_COUNT_9_20_50` | consecutive completed bars of direction-consistent aligned-expansion (ordered ≠ 0 and expanding); 0 when not aligned-expanding |
| `SHOCK_RATIO` | A1.4 `TrueRange_t / ATR14_(t−1)` (prior completed bar's ATR) |
| `RECENT_SHOCK` | max `SHOCK_RATIO` over current + previous 3 completed bars; na unless all four exist |
| `S_10_22_55` | observational-only alternate family dispersion `abs(EMA10 − EMA55)/ATR14` |
| `ORDERED_10_22_55` | observational-only alternate ordering, coded like `ORDERED_9_20_50` |

Entry-stamp note (A1.8): `direction` comes from the trade list itself; per-entry stamps
are recovered offline by joining entry fills (fill bar − 5 min = signal bar) against
these exported series. No filtered or gated strategy exists; none is authorized.

## Recorded interpretations & Pine uncertainties (report-before-capture record)

1. **A1.2 "that bar's session VWAP"** — implemented as each of the four completed
   current-session closes vs **its own bar's** session VWAP (ties count toward neither;
   na until four current-session bars). The alternative reading (all four closes vs the
   current bar's VWAP) was NOT implemented; flag at freeze if the owner intends it.
2. **`ALIGNED_EXP_COUNT` direction flips** — a single-bar flip between full opposite
   orderings while expanding starts a new run at 1 (direction-consistent runs). Rare on
   5m; `ORDERED_9_20_50` is exported so any other convention is reconstructable offline.
3. **`RECENT_SHOCK` na guard** — explicit na check (na unless all four window values
   exist) rather than relying on `math.max` na propagation; local mirror matches.
4. **`display.data_window` export inclusion** — believed included in TradingView
   "Export chart data"; **verify at capture**. If the columns are missing from the
   export, the identity-safe fallback is changing `display =` on the instrumentation
   plots (presentation-only); record that as a dated script version bump per §c.
5. **Title rename** — export filenames will carry the R1 title; presentation-only.

## Pre-registered trial accounting (§b amendment) — to resolve at freeze

- `trials_planned`: charter §9 VDC development ceiling **18** (unchanged; R1 introduces
  no new configuration — same trading spec as R0).
- `dsr_threshold_implied`: same basis as R0 (N=18, T=334 dev sessions → daily SR 0.1014,
  annualized ≈ 1.61) unless the freeze changes the sample basis.
- Budget draw: **owner decision at freeze.** Options per A1.7: capture SEALED
  (performance panel not inspected; no draw until first unsealing) — note that the
  **R0/R1 trade-list identity comparison is a mechanical admissibility check, not
  performance interpretation**, and can run on a sealed capture; or capture INTERPRETED
  (draw 2/18 recorded at capture). Record the choice in the frozen manifest and ledger.

## Execution context — must match R0 exactly (re-observe at capture, do not inherit)

Same chart and properties as `RUN_VDC_SPY_5m_dev_R0_v1.0.md`: AMEX:SPY (NYSE Arca), 5m,
RTH, exchange timezone America/New_York, ADJ enabled, capital $50,000, fixed qty 1,
pyramiding 0, commission 0%, slippage 1 tick, on bar close, bar detalization Default
(4 ticks/bar), order execution delay one tick, limit at requested price. Deviations are
a STOP for the identity gate.

## Windows & firewall (A3 — unchanged)

- Development: **2024-09-03 → 2025-12-31 inclusive** (R1 capture range).
- Embargo 2026-01-02/2026-01-05 and validation 2026-01-06 → 2026-04-30: untouched;
  validation is captured only by the separate, sealed R2 (not authorized here).
- Holdout: frozen-forward only; not applicable.

## R0/R1 identity gate (A1.8 — admissibility, pre-registered mechanics)

Before any R1 evidence is admissible: mechanical comparison of the R1 List-of-Trades
export against the preserved R0 export
(`../exports/VWAP_VDC_SPY_5m_RTH_dev_2024-09-03_2025-12-31_v0.csv`) — exact trade
count (1,331), side sequence, entry/exit timestamps, entry/exit prices, per-trade and
cumulative P/L, allowing only explicitly documented export precision differences.
**If the trade set differs: STOP; PVAE is not analyzed; the discrepancy is reported,
not repaired silently.**

## Capture & export — minimal owner procedure (when a capture charge exists)

1. Open the exact R0 chart: AMEX:SPY, 5m, RTH, exchange timezone, ADJ on.
2. Add the R1 script verbatim from
   `scripts/VWAP_Continuation_FastAlpha_v0_R1_instrumented_v1.0.pine` (no edits; all
   properties come from the source; confirm the Properties panel matches R0).
3. Confirm the strategy tester covers 2024-09-03 → 2025-12-31 (same loaded range /
   Deep Backtesting state as R0).
4. Export the List of Trades CSV.
5. Export chart data CSV — **verify the ten instrumentation columns are present**
   (uncertainty 4 above); keep a volume pane on the chart so volume is included
   (also closes the R0 Gate-1 volume gap on the same feed).
6. Screenshot the Properties panel and chart fingerprint.
7. Deliver the files; preservation, hashing, ledger row, and the identity gate run
   here. If SEALED was chosen, do not open the performance summary.

## Post-run (deferred to the frozen R1 manifest)

- Ledger row: pending capture.
- Notes / anomalies: pending.
