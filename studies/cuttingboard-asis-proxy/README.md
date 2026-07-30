# cuttingboard-asis-proxy

Status: `BASELINE EXECUTED — RUN_SPY_1D_2015-01-01 REGISTERED 2026-07-30 UTC. SINGLE DECLARED BASELINE; NO FURTHER RUNS OR VARIANTS.`

Created: 2026-07-28 UTC

**Source pin:** `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`

---

## What this study is

A reproducible baseline for **what the present CuttingBoard gate semantics would surface on
declared TradingView chart history**, with every threshold transcribed as-is from the pinned
source.

## What it is not

- **Not a CuttingBoard replay.** It reproduces the gate semantics a daily chart can express, not
  the engine.
- **Not a parity artifact.** No comparison against a live run is made or implied.
- **Not an empirical verdict on profitability.** It reports counts and sequences. It makes no
  claim about edge, expectancy, or future performance, and gives no trading recommendation.
- **Not part of the closed engine audit.** The audit is closed at EA-8
  ([`../../audits/cuttingboard-engine-strategy-audit/EA-AUDIT-CLOSEOUT.md`](../../audits/cuttingboard-engine-strategy-audit/EA-AUDIT-CLOSEOUT.md)).
  This study neither amends it nor executes EA-9. Proxy conclusions stay here.

## No tuning — by construction

Every literal comes from the pinned source. **No threshold is loosened, no gate removed, no
filter added, no variant created, no parameter searched, and no trade count targeted.** The Pine
script deliberately exposes **no inputs**, because an input is a tuning surface.

## Contents

| Path | Role |
|---|---|
| [`manifests/RULE_MAPPING_v0.1.md`](manifests/RULE_MAPPING_v0.1.md) | Source-pinned mapping from CuttingBoard semantics to proxy rules, **and** the explicit list of unrepresentable and uncertain semantics (§3) |
| [`manifests/RUN_MANIFEST_TEMPLATE_v0.1.md`](manifests/RUN_MANIFEST_TEMPLATE_v0.1.md) | Provenance/run manifest — fill **before** capture |
| [`manifests/FINDINGS_TEMPLATE_v0.1.md`](manifests/FINDINGS_TEMPLATE_v0.1.md) | Findings template that separates proxy behaviour from live-engine evidence |
| [`scripts/cuttingboard_asis_proxy_v0_1.pine`](scripts/cuttingboard_asis_proxy_v0_1.pine) | The proxy — Pine v6 indicator, SHA-256 `048f5c66eefa3fdb8df9cec882006b1d8cf5fc9772d8694614559ba0a1bce3b5` |
| [`manifests/RUN_SPY_1D_2015-01-01.md`](manifests/RUN_SPY_1D_2015-01-01.md) | The executed baseline's run manifest — FROZEN at capture 2026-07-30 UTC |
| `LEDGER.csv` | Authoritative run record (§f). One row: `RUN_SPY_1D_2015-01-01` |
| [`exports/CBASIS_v0_1_AMEX_SPY_1D_RTH_20150101-20260729_048f5c66.csv`](exports/CBASIS_v0_1_AMEX_SPY_1D_RTH_20150101-20260729_048f5c66.csv) | Registered immutable export (3,619 rows, SHA-256 `d1b53750…`), with capture screenshot alongside |
| [`analysis/FINDINGS_RUN_SPY_1D_2015-01-01.md`](analysis/FINDINGS_RUN_SPY_1D_2015-01-01.md) | Published findings, including the row-level v0.5 comparison |

## Why an indicator, not a strategy

A TradingView *List of Trades* contains only trades that were taken; rejections never become
trades. That limitation cost the earlier UV02 work its rejection evidence. This proxy is an
**indicator** that emits per-bar series for every gate, the soft-fail count, and the
first-rejection code — so every evaluation opportunity is observable, not only the passing ones.
It also makes no P&L claim, which matches the study's boundary.

## Coverage

**Covered:** the 8-vote regime model with worst-case bounding, regime classification, the
STAY_FLAT floor, direction selection, the structure classifier, the deterministic ATR geometry,
the kill switch, and Gates 1–7, 9, 10.

**Not covered — declared, never silently omitted** (mapping §3.1): Gate 8 (MAX_RISK, needs an
option chain), Gate 11 (TIME, meaningless on daily bars), chain validation, the five-step
decision chain, validation/freshness halts, the `EXPANSION` regime, and the CONTINUATION and
PULLBACK_IMBALANCE entry modes. **v0.1 is the DIRECT path only.**

Unavailable gates are reported as `NOT REPRESENTABLE` and excluded from the soft-fail
arithmetic. An unavailable gate is never counted as passing (`docs/conventions.md` §h).

## One structural note worth reading before any run

`options.py:_build_candidate` sets `stop = 1 × ATR14` and `target = 2 × ATR14`, so **reward/risk
is 2.0 by construction on every candidate**. Consequences: Gate 7's minimum is 2.0 outside
NEUTRAL, so it sits exactly on the boundary; in NEUTRAL the minimum is 3.0, so **Gate 7 always
fails in NEUTRAL**. Gate 6's ATR floor is likewise an equality comparison. Boundary behaviour
must be *reported as observed*, not assumed — see mapping §3.2.

## The declared baseline — executed

**TradingView execution was not available to the agent that built this package.** The single
declared baseline has since been run by the operator (dwats250) and registered:
[`manifests/RUN_SPY_1D_2015-01-01.md`](manifests/RUN_SPY_1D_2015-01-01.md) (frozen),
`LEDGER.csv` row 1, and
[`analysis/FINDINGS_RUN_SPY_1D_2015-01-01.md`](analysis/FINDINGS_RUN_SPY_1D_2015-01-01.md).
The procedure, kept as the record of how it was produced:

1. Open a chart at the symbol/timeframe you want to declare as the baseline.
2. Add `scripts/cuttingboard_asis_proxy_v0_1.pine` **unmodified** — verify the SHA-256 above
   first. Editing it means a new file and a new hash (§c, §e).
3. Copy `manifests/RUN_MANIFEST_TEMPLATE_v0.1.md` to `manifests/RUN_<run_id>.md` and **fill every
   field before capturing anything**, including chart timezone, session, adjustment convention,
   data provider, and which of the seven macro series actually resolved.
4. Capture via *Export chart data* (the per-bar series are `display.data_window`) and/or the
   last-bar summary table.
5. Save the export to `exports/` with a self-describing name, record its SHA-256, and add one
   row to `LEDGER.csv`.
6. Write findings from `manifests/FINDINGS_TEMPLATE_v0.1.md`.

**Run only the single declared baseline.** No variant sweep, no threshold change, no second
configuration — those would be a different study.

> Whether TradingView's *Export chart data* emits `display.data_window` series was never
> established in prior work and was untested when this package was built. **Resolved at capture
> (RUN_SPY_1D_2015-01-01): the export does include all `display.data_window` series.** The
> fallback (last-bar summary table) was not needed and is recorded in the run manifest.

## Conventions

`docs/conventions.md` applies in full: §a layout, §b pre-registered manifests never edited in
place, §c versioned scripts, §d analysis code as part of the experiment, §e immutable
self-describing exports, §f the ledger is authoritative, §h unavailable is not the same as
passing.
