# CuttingBoard → TradingView proxy — rule mapping v0.1

Status: `PRE-REGISTERED — FROZEN BEFORE ANY RUN. NEVER EDITED IN PLACE.`

Created: 2026-07-28 UTC

**Source pin:** `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`
All line references below are at that pin, read commit-addressed.

**Claim boundary.** This is a *proxy*. It is **not** a CuttingBoard replay, not a parity
artifact, and not an empirical verdict on strategy profitability. It reproduces the gate
semantics that a daily TradingView chart can faithfully express, and it names — in §3 — every
semantic it cannot.

**No tuning.** Every literal below is transcribed from the pinned source. No threshold is
loosened, no gate removed, no filter added, no variant created, and no parameter searched.

---

## 1. Regime layer — the 8-vote model

`cuttingboard/regime.py:167–175`. Votes are cast per input; a missing input is skipped, not
neutralised.

| # | Vote | RISK_ON when | RISK_OFF when | Proxy source |
|---|---|---|---|---|
| 1 | SPY pct_change | `> 0.003` | `< -0.003` | `AMEX:SPY` daily % change |
| 2 | QQQ pct_change | `> 0.003` | `< -0.003` | `NASDAQ:QQQ` |
| 3 | IWM pct_change | `> 0.004` | `< -0.004` | `AMEX:IWM` |
| 4 | VIX level | `< 18` | `> 25` | `CBOE:VIX` close |
| 5 | VIX pct_change | `< -0.03` | `> 0.05` | `CBOE:VIX` % change |
| 6 | DXY pct_change | `< -0.002` | `> 0.003` | `TVC:DXY` |
| 7 | TNX pct_change | `< -0.005` | `> 0.008` | `TVC:TNX` |
| 8 | BTC pct_change | `> 0.015` | `< -0.020` | `BITSTAMP:BTCUSD` |

**Worst-case bounding** (`regime.py:199–205`): `missing = 8 − votes_cast`;
`bounded_net = max(0, net − missing)` when `net > 0`, else `min(0, net + missing)`;
`confidence = |bounded_net| / 8`.

**Classification** (`_classify_regime`, `regime.py`):

```
vix_pct > 0.15                       -> CHAOTIC        (VIX_CHAOTIC_SPIKE)
net >= 4 and confidence >= 0.60      -> RISK_ON
net >= 2                             -> RISK_ON
net <= -4 and confidence >= 0.60     -> RISK_OFF
net <= -2                            -> RISK_OFF
otherwise                            -> NEUTRAL
```

**Posture** (`_determine_posture`): `CHAOTIC` or `confidence < 0.50` → `STAY_FLAT`.
`STAY_FLAT` short-circuits all per-symbol qualification (`qualification.py:803–820`; the
short-circuit is in `qualify_all`, confirmed by EA-4).

**Direction** (`direction_for_regime`): `RISK_ON → LONG`, `RISK_OFF → SHORT`,
`EXPANSION → LONG`, `NEUTRAL → sign(net_score)` with `net == 0 → no candidate`,
`CHAOTIC → none`.

## 2. Per-symbol layer

### 2.1 Derived metrics (`config.py:109–112`)

`EMA_FAST 9` · `EMA_SLOW 21` · `EMA_TREND 50` · `ATR_PERIOD 14` (Wilder RMA) ·
`OHLCV_MIN_BARS 21`.

### 2.2 Structure (`structure.py:146–212`, priority order preserved)

```
1. no history / no EMA                                        -> CHOP
2. momentum_5d >  0.02 and vol_ratio > 1.3 and price > ema9   -> BREAKOUT
   momentum_5d < -0.02 and vol_ratio > 1.3 and price < ema9   -> BREAKOUT
3. |ema_spread_pct| < 0.002 and |momentum_5d| > 0.003         -> REVERSAL
4. bull-aligned: price >= ema9 -> TREND; price >= ema21 -> PULLBACK; else CHOP
   bear-aligned: price <= ema9 -> TREND; price <= ema21 -> PULLBACK; else CHOP
5. fallthrough                                                -> CHOP
```

`CHOP` is disqualifying and is never promoted.

### 2.3 Candidate geometry (`options.py:_build_candidate`) — deterministic

```
risk_distance = ATR14                 (fallback: 2% of entry when ATR unavailable)
LONG :  stop = entry − ATR14,  target = entry + 2 × ATR14
SHORT:  stop = entry + ATR14,  target = entry − 2 × ATR14
```

**Consequence, recorded because it drives §2.4:** reward/risk is **2.0 by construction on every
candidate**. It is not an outcome of the setup; it is fixed by the geometry.

### 2.4 The eleven gates (`qualification.py:42–56`, `368–540`)

Gates 1–4 hard (immediate reject); 5–11 soft (exactly one miss → WATCHLIST, two or more →
REJECT). No partial credit.

| Gate | Rule at the pin | Proxy status |
|---|---|---|
| 1 REGIME | posture `STAY_FLAT` → reject | **mapped** |
| 2 CONFIDENCE | `confidence < 0.50` → reject | **mapped** |
| 3 DIRECTION | candidate direction must match regime direction | **mapped** |
| 4 STRUCTURE | `CHOP` → reject | **mapped** |
| 5 STOP_DEFINED | stop > 0 and distance > 0 | **mapped** (always true given §2.3) |
| 6 STOP_DISTANCE | `stop_pct < 0.01` fails; else `risk < 1.0 × ATR14` fails | **mapped** — reduces to `ATR14 / price >= 0.01`, since risk **is** ATR14 |
| 7 RR_RATIO | `rr < min_rr` fails; `min_rr` = 3.0 in NEUTRAL, else 2.0 | **mapped** — with §2.3, `rr = 2.0`, so this **always fails in NEUTRAL** and otherwise sits exactly on the boundary. See §3.2 |
| 8 MAX_RISK | contracts and dollar risk vs `ACCOUNT_EQUITY 15000` × `MAX_RISK_PCT_PER_TRADE 0.026667`, using option spread width | **NOT REPRESENTABLE** — §3.1 |
| 9 EARNINGS | earnings within 5 days; unknown → **PASS** (fail-open) | **mapped as PASS** — the engine itself sets `has_earnings_soon = None` in `_build_candidate`, so this gate is fail-open in the engine too |
| 10 EXTENSION | `abs(entry − ema21) / ATR14 > 1.5` fails | **mapped** |
| 11 TIME | no new entries after 15:30 ET | **NOT REPRESENTABLE on daily bars** — §3.1 |

### 2.5 Kill switch (`runtime/__init__.py:2185–2204`)

`vix_level > 35` **or** `vix_pct > 0.15` **or** `|spy_pct| > 0.03` → terminal HALT.
Comparisons are strict `>`; EA-5 verified this on all three legs at and just above threshold.
**mapped.**

---

## 3. Semantics this proxy cannot represent

Declared before any run, so no result silently assumes them.

### 3.1 Structurally unrepresentable

| Semantic | Why |
|---|---|
| **Gate 8 MAX_RISK** | Depends on option spread width, estimated debit, strategy selection, and contract sizing. No option-chain data on a TradingView price chart |
| **Gate 11 TIME** | A 15:30 ET intraday cutoff has no meaning on a daily bar |
| **Chain validation** | `chain_validation.py` requires a live option chain. This is the same boundary that made the accepted path unobservable in EA-6 (finding EA-6-006) |
| **The five-step decision chain** | `create_trade_decision` → execution policy → thesis → invalidation → entry quality. These consume session state, ORB state, and prior-run context that a chart does not carry |
| **Validation / freshness / clock-skew halts** | `FRESHNESS_SECONDS 300` and `MAX_CLOCK_SKEW_SECONDS 5` describe live quote acquisition. Chart history has no quote age |
| **EXPANSION regime** | Requires breadth over `config.ALL_SYMBOLS` plus leadership over `EXPANSION_LEADERSHIP_SYMBOLS`. Representable in principle but needs ~20 additional `request.security` calls; **excluded from v0.1 and declared, not silently omitted**. The proxy therefore cannot emit `EXPANSION` and its `LONG` bias |
| **CONTINUATION and PULLBACK_IMBALANCE entry modes** | A separate nine-step sequence and an FVG post-hoc upgrade (`qualification.py:687`, `:823`). v0.1 covers the **DIRECT** path only |

### 3.2 Uncertain — mapped, but with a recorded doubt

| Semantic | Doubt |
|---|---|
| **Gate 7 at the boundary** | Geometry gives `rr = 2.0` and the test is `rr < min_rr`, so the gate should pass at 2.0. EA-2/EA-6 traces nonetheless recorded rejections reading `"R:R 2.00 below 2.0 minimum"`, which implies the computed ratio fell fractionally below 2.0 in floating point. The proxy reproduces the comparison as written; **any run must report Gate 7 pass/fail counts separately rather than assuming the boundary resolves one way** |
| **Gate 6 at the boundary** | `risk` *is* `ATR14`, so `risk < 1.0 × ATR14` is an equality comparison in floating point. Same caution |
| **`volume_ratio` definition** | Used by the BREAKOUT branch. The proxy uses volume ÷ its own 20-bar SMA; the engine's exact denominator was not transcribed for v0.1 and is recorded here as an approximation, not a match |
| **`ema_spread_pct` definition** | Proxy uses `(ema9 − ema21) / price`. Sign and denominator convention not verified against source for v0.1 |
| **Session / timezone** | The engine reasons in ET on live quotes; the proxy reasons on whatever session the chart declares. Recorded per run in the run manifest |

---

## 4. What a run of this proxy may and may not claim

**May:** signal/opportunity frequency; the evaluated → qualified → emitted funnel *where
representable*; which mapped gates appear decisive, inert, or overlapping; a chronology of
representative signals; and the unrecoverable gaps above.

**May not:** any statement of profitability, edge, expectancy, or future performance; any claim
of equivalence to a live CuttingBoard run; any statement about the accepted path, which is
unobservable here for the same reason it was unobservable in EA-6; or any conclusion carried
back into the closed audit.

## 5. Amendment rule

Pre-registered and frozen. Corrections are a dated amendment appended here or a new versioned
file with the version in the filename (`docs/conventions.md` §b). A change to any threshold or
gate is a **new study**, not an amendment to this one.
