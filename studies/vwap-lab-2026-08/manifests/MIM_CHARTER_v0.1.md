# MIM — MARKET INTRADAY MOMENTUM · family charter / preregistration · v0.1 · 2026-08-27

A new independent research family, opened by owner/HELM charge 2026-08-27 (Codex
reconnaissance rank #1). Worked under `docs/research/FAMILY_AUTONOMY_PROTOCOL_v1.0.md`.
MIM-0 is a **literature-faithful exact replication baseline** — no fitted strategy
parameter. This charter is the frozen pre-registration; results (when unblocked) are
recorded by dated amendment. **Status: BLOCKED — DATA/SEMANTIC (see §Blocker).**

## 1. Family & literature

**MIM — Market Intraday Momentum.** Literature baseline: **Gao, Han, Li & Zhou,
*Market Intraday Momentum.*** Core hypothesis: the SPY return from the previous RTH
close through the end of the first 30 minutes **positively predicts** the return during
the final 30 minutes.

## 2. MIM-0 — one exact baseline (frozen; no fitted parameter)

### Clock semantics (ET; 1-minute bar-START timestamps)

- `previous_close` = previous RTH session's final regular-session close.
- `price_10_00` = the **09:59 bar close** (price observed at 10:00).
- `late_open` = the **15:30 bar open** (executable late-window-start proxy).
- `late_close` = the **15:59 bar close** — a **CONTINUOUS-session close proxy**, **not**
  an official closing-auction fill.
- A session yields an observation only if it has all three standard-clock bars
  (09:59 / 15:30 / 15:59). Sessions missing any — including **early closes** — produce
  **no observation and no trade**.

`early_return = price_10_00 / previous_close − 1` ·
`late_return = late_close / late_open − 1`.

### Sign strategy

`early_return > 0` → **LONG** the final half hour; `< 0` → **SHORT**; `== 0` → **no
trade**. One trade maximum per day. **No** stop, target, VWAP, EMA, ATR, magnitude
threshold, volatility/volume/macro filter, or side rescue.

### Statistical primary (frozen before outcomes)

OLS `late_return_t = α + β·early_return_t + ε_t`; **primary association condition
β > 0**. Report β, intercept, standard error, t-stat, 95% CI, R², N. **Robust
standard-error convention = HC1** (White heteroskedasticity-consistent, small-sample
corrected) as **PRIMARY**; classical OLS SE secondary; 95% CI via the normal 1.96
multiplier. **Frozen — no covariance-estimator shopping.**

### Economic translation (sign strategy)

Mean bps/trade, median bps, cumulative bps, long/short separately, PF, win rate, max
drawdown under a **fixed-notional** convention (1 unit notional per trade → the
realized fractional return is the per-trade P/L), bootstrap CI (fixed seed),
monthly consistency, outlier concentration.

### Costs (frozen before outcomes; not optimized)

Gross association is reported **separately** from executable economics. Three frozen
cost views: (1) **zero-cost**; (2) the existing lab **adverse-slippage** convention
(1 tick per fill, 2 fills → ~`2·0.01/price` in bps); (3) **one conservative round-trip
stress = 5 bps**. No cost assumption is optimized, and **no auction-executable alpha is
claimed from OHLCV** (the 15:59 close is a continuous-session proxy).

## 3. Kill / advance gates (frozen)

MIM-0 receives **one** exact replication baseline. **FAMILY DEAD** if any of:
`β ≤ 0`; **or** gross sign-strategy expectancy `≤ 0`; **or** a positive gross
expectancy does **not** survive the frozen conservative cost stress. **No rescue** —
do not then test alternative early/late windows, high-vol/high-vol subsets, macro
days, long-only, or a rest-of-day predictor. If **all** gates pass →
**EDGE CANDIDATE — VALIDATION DECISION REQUIRED** (validation is **not** run
autonomously).

## 4. Data & firewall

Development **2024-09-03 → 2025-12-31** only. The consumed VDC validation window
(2026-01-06 → 2026-04-30) is **not** MIM validation. No embargo / buffer /
hypothesis-source / forward-holdout inspection. Fresh confirmation, if ever earned,
must be a genuinely fresh window frozen later. No TradingView dependency, no
CuttingBoard contact, no merge.

## Blocker — DATA/SEMANTIC (status C), before outcome access

**Resolved before touching outcomes, per the charge.** MIM-0's `early_return` crosses
the **previous RTH close**, so it spans the overnight. The local corpus is
**split-adjusted but DIVIDEND-UNADJUSTED** (Polygon `adjusted=true` = splits only;
`data/CORPUS_SPY_1m_2024-09-01_2026-08-22.md`; R0 ledger "split-only … NOT ADJ"). On
SPY ex-dividend sessions the previous-close→open gap therefore contains an unadjusted
dividend drop (~30–40 bps) that is **not** momentum.

Trade-blind evidence (`analysis/mim_overnight_diagnostic.py` →
`MIM_OVERNIGHT_DIAGNOSTIC_2026-08-27.json`): over 333 dev overnight gaps the median
`|gap|` is **27.6 bps**, and the twelve largest moves are all **genuine macro/news
gaps** (e.g., the April 2025 tariff sequence −346/−323/−260 bps; 2025-01-27 −216 bps).
A ~30–40 bps dividend drop is **buried at the median of the overnight distribution** —
**no OHLCV threshold can separate ex-dividend drops from ordinary overnight moves**
without also discarding the genuine momentum gaps the hypothesis depends on.

Therefore a clean dividend-adjustment convention for the previous-close return
**cannot be established from the corpus alone**, and guessing ex-dividend dates or a
gap-threshold heuristic is prohibited. **STOP at DATA/SEMANTIC BLOCKER (C).** MIM-0 is
**pre-registered, implemented (`analysis/mim.py`), and unit-tested
(`analysis/test_mim.py`, 6/6 on synthetic data)** — the development regression and
economics are **not** run.

**To unblock (a new-provider decision for HELM), either:** (a) supply a **SPY
ex-dividend calendar** for the development window (then exclude or dividend-adjust the
~5–6 ex-dividend sessions precisely, by a convention frozen before outcomes), or
(b) supply a **dividend-adjusted (total-return) SPY previous-close** series. Either is
a new corporate-action data source not present in the repository and not fetched here.

## Budget (§9/§f)

MIM interpreted-development budget **≤ 4** (default new-family allowance; the family
charter may not exceed it). VMR/VDC/FPC budgets are not inherited. **0 spent** — MIM-0
is blocked before execution; a `family=MIM` ledger row is written only at the first
actual run.

## Amendments

*(append the dated result amendment once the blocker is resolved and MIM-0 is run;
never edit the pre-registration above in place)*
