# Proxy run manifest — template v0.1

Status: `TEMPLATE — COPY PER RUN, FILL BEFORE EXPORT, NEVER EDIT AFTER`

Created: 2026-07-28 UTC

Copy to `manifests/RUN_<run_id>.md`, **fill every field before capturing anything**, then
record the same run as one row in `../LEDGER.csv`. A field that cannot be established is written
`UNRECOVERABLE` — never left blank and never guessed.

> **Fill this before the export, not after.** UV02's friction scenario is permanently
> `UNRECOVERABLE` because Properties were never captured before export; seven otherwise-clean
> captures cannot support a friction-adjusted claim. The cost was not the missing field — it was
> that the field could not be recovered later at any price.

---

## Identity

| Field | Value |
|---|---|
| `run_id` | |
| `run_date` (UTC) | |
| `operator` | |

## Source and script binding

| Field | Value |
|---|---|
| `cuttingboard_source_pin` | `59f8279d796335149afdec4aa507b6f927233518` |
| `script_file` | `scripts/cuttingboard_asis_proxy_v0_1.pine` |
| `script_sha256` | `048f5c66eefa3fdb8df9cec882006b1d8cf5fc9772d8694614559ba0a1bce3b5` |
| `rule_mapping_version` | `RULE_MAPPING_v0.1.md` |
| Script edited before this run? | must be **no** — an edit means a new file and a new hash (§c, §e) |

## Chart and data convention

| Field | Value |
|---|---|
| `symbol` (exact TradingView ticker) | |
| `timeframe` | |
| `session` (regular / extended) | |
| `timezone` (chart setting) | |
| `chart_data_convention` (standard candles? adjusted? dividends?) | |
| `data_provider / exchange feed` | |
| `bar_timestamp_convention` (bar labels open or close) | |
| `date_window_start`, `date_window_end` | |
| Bars available at capture | |

> Bar-timestamp convention and adjustment semantics are recorded explicitly. An off-by-one
> convention mismatch is indistinguishable from look-ahead in results.

## Macro series actually resolved

The 8-vote model requires all of these. Record which resolved and which returned `na`, because a
missing vote changes `bounded_net` and therefore the regime.

| Series | Ticker used | Resolved? |
|---|---|---|
| SPY | `AMEX:SPY` | |
| QQQ | `NASDAQ:QQQ` | |
| IWM | `AMEX:IWM` | |
| VIX | `CBOE:VIX` | |
| DXY | `TVC:DXY` | |
| TNX | `TVC:TNX` | |
| BTC | `BITSTAMP:BTCUSD` | |

## TradingView capture details

| Field | Value |
|---|---|
| `tv_account` | |
| `tv_plan` (affects bar limits) | |
| `tv_capture_method` (Export chart data / screenshot / manual) | |
| Any non-default chart setting | |
| Export file name | |
| Export `sha256` | |

## Declared limitations in force for this run

Restated per run so no reader has to reconstruct them:

- Gate 8 (MAX_RISK) and Gate 11 (TIME) are **NOT REPRESENTABLE** and are excluded from the soft
  count — never counted as passing.
- `EXPANSION` regime, CONTINUATION and PULLBACK_IMBALANCE entry modes are **not represented**.
- Chain validation and the five-step decision chain are **not represented**; the accepted path is
  therefore unobservable here, exactly as it was in the closed audit (EA-6-006).
- `volume_ratio` and `ema_spread_pct` are **approximations** — mapping §3.2.

## Result summary

| Field | Value |
|---|---|
| Bars evaluated | |
| Hard-gate pass | |
| Qualified | |
| Watchlist | |
| Kill-switch bars | |
| First-rejection distribution | |

## Amendment rule

Pre-registered per run and never edited after capture. A correction is a dated amendment file or
a new versioned manifest (`docs/conventions.md` §b).
