# RUN MANIFEST PREP — R0 (VDC naked development reference) · v0.1 · 2026-08-25

**Status: PREP — NOT FROZEN. This is not a run authorization.** Prepared from
`RUN_MANIFEST_TEMPLATE_v0.1.md` so the R0 manifest can be frozen quickly at the laptop.
Fields marked `MECHANICAL(source)` are established by the ingested Pine
(`scripts/VWAP_Continuation_FastAlpha_v0.pine`, sha256 `c4764292…e342c6c9e`). Fields
marked `OWNER-OBSERVE` must be filled from the actual TradingView UI — **Pine defaults
and observed TradingView state are separate evidence; nothing below invents UI state.**
Freeze (rename per template convention, fill remaining fields, commit) **before** capture.

## Identity & authorization

- Run id: `VWAP_VDC_SPY_5m_RTH_dev_<daterange>_v0` — daterange pending window freeze
- Family: `VDC` · Budget class: `development`
- Charter governing: `STUDY_CHARTER_v0.1.md` + Amendments A1, A2
- Source status at run time: `INGESTED@scripts/VWAP_Continuation_FastAlpha_v0.pine
  sha256 c476429225c2ba4abb7c91d370f3abde893d9e4afe83a41ac8a0069e342c6c9e`
- Authorization: **UNRESOLVED — requires an explicit Dustin charge naming R0**

## Pre-registered trial accounting (§b amendment)

- `trials_planned`: UNRESOLVED — commit before the first development run
- `dsr_threshold_implied`: UNRESOLVED — compute here once the window/sample length is frozen
- Budget draw: R0 = 1 of VDC ≤ 18 when interpreted (sealed-capture ruling A1.7 applies)

## Execution context

| Field | Value | Evidence class |
|---|---|---|
| Strategy title | `VWAP Continuation - Fast Alpha v0` | MECHANICAL(source) |
| Pine version | 6 | MECHANICAL(source) |
| Initial capital | 50,000 USD | MECHANICAL(source declaration) — confirm Properties panel shows it |
| Sizing | fixed, 1 unit | MECHANICAL(source declaration) — confirm in UI |
| Pyramiding | 0 | MECHANICAL(source declaration) — confirm in UI |
| Commission | percent, 0.0 | MECHANICAL(source declaration) — confirm in UI |
| Slippage | 1 tick | MECHANICAL(source declaration) — confirm in UI |
| calc_on_order_fills / calc_on_every_tick / process_orders_on_close | false / false / false | MECHANICAL(source declaration) — confirm if surfaced |
| Exact symbol/exchange as TradingView shows it | __ (prior authoritative context: `BATS:SPY` — must be re-observed, not assumed) | OWNER-OBSERVE |
| `syminfo.mintick` / tick size | __ (NOT hardcoded anywhere locally) | OWNER-OBSERVE |
| Timeframe | 5m (source errors otherwise) | MECHANICAL(source) — confirm chart |
| Candles | standard | OWNER-OBSERVE (source documents standard) |
| Session | RTH only (source errors on EXT bars) | MECHANICAL(source) — confirm chart toggle |
| Chart timezone | __ | OWNER-OBSERVE |
| Data adjustment setting (splits/dividends) | __ | OWNER-OBSERVE |
| Deep Backtesting available history | __ | OWNER-OBSERVE |
| Exact selected date window | __ (pending window freeze) | OWNER-OBSERVE |
| Recalculation settings as surfaced | __ | OWNER-OBSERVE |
| Bar Magnifier setting if surfaced | __ | OWNER-OBSERVE |
| Any other property that can alter emulator fills | __ | OWNER-OBSERVE |
| Strategy Properties screenshot | __ | OWNER-OBSERVE (required capture) |
| Loaded-bar range at capture | start __ / end __ | OWNER-OBSERVE |

## Windows & firewall (§g, A1.6)

- Development window: **UNRESOLVED — WINDOW FREEZE REQUIRED BEFORE R0** (see charter
  §12 and Amendment A2). Constraints already frozen: hypothesis-source contamination
  late May–Aug 2026; local corpus begins 2024-09-03; validation/deferred-inspection
  protected; holdout is frozen-forward only.
- Embargo: length __ (≥ longest indicator lookback; A1-reviewed recommendation:
  ≥ 2 full sessions) ; boundary __
- Deferred-inspection window: __ (never "out of sample")
- Holdout: not applicable to R0.

## Strategy specification (from ingested source — never from lineage)

- Script: `VWAP_Continuation_FastAlpha_v0.pine` sha256 `c4764292…e342c6c9e`
- Trigger: opposing 5m candle inside directional state (long: red bar while
  `close>sessionVWAP` and `EMA9>EMA20`; short mirrored; doji is neither), flat only,
  signal-bar start ∈ [09:35, 15:30) ET
- Entry: market order; source semantic = next available emulator tick (normally next
  5m bar open historically); execution parity PENDING R0
- Stop: `strategy.exit(loss = max(1, round(ATR14×1.0 / mintick)))`, frozen at signal bar
- Exit hierarchy: ATR stop; thesis exit `strategy.close` on close beyond session VWAP
  against position; EOD `close_all(immediately=true)` on the 15:50 bar
- VWAP acceptance state used: none in naked VDC v0 (A1.2 vocabulary is PVAE covariate
  work, not a VDC input)
- Excursion metric params: not computed in R0 (naked reference run)

## Capture & export

Per `../exports/README.md`: List-of-Trades export + sha256; Performance Summary
screenshot; chart fingerprint screenshot; loaded-bar range; chart context; script
identity. Naming: `VWAP_VDC_SPY_5m_RTH_dev_<start>_<end>_v0.csv`.

## Post-run

- Ledger row appended (sealed or interpreted status marked per A1.7): __
- Notes / anomalies: __
