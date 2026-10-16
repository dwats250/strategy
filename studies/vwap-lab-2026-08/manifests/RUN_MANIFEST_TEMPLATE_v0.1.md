# RUN MANIFEST TEMPLATE v0.1 — VWAP Strategy Lab

Copy this file to `RUN_<family>_<tf>_<class>_<date>.md`, fill **before** capture, and **freeze**
(never edit in place afterward — `docs/conventions.md` §b). One frozen run manifest per interpreted
run. A run without a frozen manifest is not a study run.

> **Blocked until source ingest.** No run manifest may be frozen while `VDC_SOURCE_STATUS =
> SOURCE_REQUIRED` for a VDC run, and no VMR/VREV run is authorized this sprint. This template
> exists so the schema is pre-registered, not so a run can start.

---

## Identity & authorization

- Run id: `VWAP_<family>_<symbol>_<tf>_<session>_<class>_<daterange>_<scriptver>`
- Family: `VDC | VMR | VREV`
- Budget class: `development | validation | holdout`
- Charter version governing this run: `STUDY_CHARTER_v0.1.md` (or later)
- Source status at run time: `SOURCE_REQUIRED | INGESTED@<pin> | VDC-0_COMMISSIONED@<ref>`
- Authorization: (the explicit Dustin charge that permits this run)

## Pre-registered trial accounting (`docs/conventions.md` §b amendment)

- `trials_planned`: (independent configs committed before the first run of this class)
- `dsr_threshold_implied`: (observed performance needed at this N and sample length — compute here)
- Budget draw: this run consumes 1 of the class ceiling in `STUDY_CHARTER §9`; running total: `__ / __`

## Execution context (confirm, do not inherit provisionals blindly)

- Symbol / feed: (e.g. `AMEX:SPY`)
- Timeframe: (e.g. `5m`)
- Session: (e.g. `RTH 09:30–16:00 ET`)
- Chart timezone: 
- Extended hours: `OFF`(confirm) 
- Candles: (standard / heikin / …)
- Broker emulator: commission = __ ; slippage = __
- Loaded-bar range at capture: start __ / end __

## Windows & firewall (`docs/conventions.md` §g)

- Development window: start __ / end __
- Embargo: length __ (≥ longest lookback) ; boundary __
- Deferred-inspection window (if any): __ (label as deferred-inspection, never "out of sample")
- Holdout window (holdout runs only): pre-registered on __ ; frozen-forward from __

## Strategy specification (fill from ingested source — never from lineage)

- Script file + version: 
- Script sha256: 
- Trigger: 
- Entry: 
- Stop construction: 
- Exit hierarchy: 
- Position timing: 
- VWAP acceptance state used (`ESTABLISHED | MIXED` per §4) and its frozen thresholds: 
- Excursion metric params (price_ref, ATR length/smoothing per §5): 

## Capture & export (see `../exports/README.md`)

- Export file (immutable, self-describing name): 
- Export sha256: 
- Screenshots (chart fingerprint + Performance Summary): 
- Capture method: 

## Post-run (into `../LEDGER.csv` — ledger is authoritative, §f)

- Ledger row appended: `yes/no`
- Notes / anomalies: 
