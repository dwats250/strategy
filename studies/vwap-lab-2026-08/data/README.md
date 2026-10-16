# data/ — offline SPY market-data seam

Status (2026-08-25, corpus captured and verified): **DATA CORPUS PASS — OFFLINE SPY CORPUS
READY FOR PARITY WORK.** A SPY 1m corpus (2024-09-03 → 2026-08-21, 422,657 rows) was
captured owner-side and mechanically verified; its durable, commit-addressed provenance and
health record is
[`CORPUS_SPY_1m_2024-09-01_2026-08-22.md`](CORPUS_SPY_1m_2024-09-01_2026-08-22.md). The
dataset itself remains local and gitignored under `cache/` and is never committed. All
TradingView parity questions remain open (see that record and the parity list below).

Historical status (2026-08-25, earlier, accurate for its moment — retained, not rewritten):
**DATA CREDENTIAL / ENTITLEMENT UNAVAILABLE.** No Massive/Polygon (or
other market-data) credential exists in this environment; no account was created, no data
was purchased, and **no live API call has been made**. The seam below is committed so the
first laptop session with a credential can prove entitlement in minutes; its normalization
and 1-minute→5-minute reconstruction logic is verified offline by `selftest` against a
**synthetic** fixture. Entitlement facts (history depth, fields, limits) remain
**unverified by behavior** until a real `probe` runs.

**This directory is market-data infrastructure, not strategy evidence.** Nothing here
computes a strategy, a PVAE outcome, or a backtest, and nothing here is admissible for any
study claim.

## Provider choice

Massive / Polygon-compatible Stocks Aggregates API. Rationale: consolidated U.S. stock
aggregate bars are preferable for a VWAP study to a single-exchange feed. Public docs
suggest the aggregates endpoint serves historical 1-minute stock OHLCV with bounded free
history — **verify by API behavior, never assume the docs match the account.**

## Usage

```
export MASSIVE_API_KEY=...            # or POLYGON_API_KEY; never echoed or stored
python3 fetch_spy_aggs.py probe   --date 2026-08-04
python3 fetch_spy_aggs.py capture --start 2024-09-01 --end 2026-08-22
python3 fetch_spy_aggs.py selftest    # offline, no credential needed
```

- `probe` — one completed RTH day of SPY 1-minute aggregates; reports row count, first/last
  timestamps, fields present (including vendor `vw` and transaction count `n`), and the
  reported `adjusted` flag. This is the entitlement test.
- `capture` — paginated download into `cache/` (gitignored): raw provider pages under
  `cache/raw/` (sha256-recorded), a deterministic canonical `CSV.gz` under
  `cache/canonical/`, and a JSON metadata manifest under `cache/manifests/` recording the
  exact query, range, row count, page checksums, and semantics. Rate-limited to stay under
  the free tier's 5 requests/min. After a real capture, lane 1 commits the small metadata
  manifest (not the dataset) alongside this README.
- `selftest` — deterministic offline test against `fixtures/sample_aggs_response.json`
  (**synthetic data**, labeled as such in its `request_id`; not provider output).

## Canonical format and semantics

`t_ms, utc_iso, et_iso, session, o, h, l, c, v, vw, n` — one row per 1-minute bar.

- `t_ms` is the provider's bar-**start** timestamp (epoch ms, UTC), preserved unmodified;
  `utc_iso` / `et_iso` are derived, never substituted.
- `session` is `RTH` iff the ET bar start is in `[09:30, 16:00)`, else `EXT`.
  **Extended-hours bars are flagged, never deleted, during acquisition.**
- Captures request `adjusted=true` and record the flag the provider reports. The
  split/dividend adjustment convention vs TradingView's chart setting is an open parity
  item (below).
- CSV.gz is used (stdlib, deterministic `mtime=0`, matches this repo's CSV-export habit);
  Parquet would add a dependency with no current consumer.
- Do **not** commit raw datasets from `cache/`; the deterministic downloader + committed
  metadata/checksum manifest is the record. A tiny fixture is committed only for
  deterministic testing.

## Vendor VWAP warning

The provider's per-bar `vw` field is a vendor aggregate-bar VWAP. It is **not** TradingView's
session-anchored VWAP and must never be substituted for it. Local session VWAP must be
recomputed from bars under the exact TV convention once parity requirements are known.

## Local-parity requirements (open until the exact Pine source is ingested)

Local reproduction of the TradingView strategy context will eventually require, exactly:

- the exact TradingView VWAP source expression (anchor, price input, reset behavior);
- the EMA implementation (seeding/warm-up included);
- the ATR implementation and smoothing (RMA/Wilder vs SMA);
- session reset behavior across RTH boundaries;
- chart timezone;
- RTH filtering convention (which bars exist on the TV chart);
- order timing (bar close vs next open, calc-on settings);
- broker-emulator assumptions (commission, slippage, fill model);
- the data adjustment convention (splits/dividends) on both sides.

**Parity is never declared because charts look similar** — it is proven mechanically, per
the R0/R1 identity-gate style in `../manifests/STUDY_CHARTER_v0.1.md` Amendment A1.8.
