# exports/ — immutable, self-describing (per `docs/conventions.md` §e)

Empty until source ingest. No run has produced an export.

## Immutability

Once written, an export is **never modified**. A new run producing new numbers gets a **new file**,
not an edit to an old one. The `LEDGER.csv` row, not the export, is the authoritative record (§f).

## Naming convention

Export filenames encode what produced them so the name tells you most of what you need before
opening it:

```
VWAP_<family>_<symbol>_<tf>_<session>_<class>_<start>_<end>_<scriptver>.csv
```

Example (illustrative only — no such run exists):
`VWAP_VDC_SPY_5m_RTH_dev_2024-01-02_2026-06-30_v0.1.0.csv`

- `<family>` — `VDC | VMR | VREV`
- `<class>` — `dev | val | holdout`
- `<start>_<end>` — first and last **accepted fill** dates in the export (state this explicitly in
  the run manifest; for filtered runs these differ from the scored window)
- `<scriptver>` — the strategy script version that produced it (§c)

## TradingView capture requirements

Every interpreted run captures, and records in its frozen run manifest and the ledger:

1. **List-of-Trades export** — the raw TradingView CSV, saved here under the naming convention
   above, with its **sha256** recorded in the ledger (`export_sha256`).
2. **Performance Summary screenshot** — the TradingView strategy-tester summary panel.
3. **Chart screenshot with fingerprint** — showing the on-chart parameter fingerprint and the
   symbol/timeframe/session/timezone/extended-hours state.
4. **Loaded-bar range** — the actual first/last bar available at capture (`date_window_*`).
5. **Chart context** — symbol/feed, timeframe, session, timezone, extended-hours toggle, candle
   type, and broker-emulator commission/slippage.
6. **Script identity** — script file, version, and sha256 (`script_file`, `script_sha256`).

An export whose provenance cannot be tied back to a frozen run manifest and a ledger row is not
admissible evidence for this study.
