# ODR — OVERNIGHT / OPENING DISLOCATION REVERSAL · family charter / preregistration · v0.1 · 2026-08-27

A new independent research family, authorized by owner/HELM charge 2026-08-27 and worked
under `docs/research/FAMILY_AUTONOMY_PROTOCOL_v1.0.md`. ODR-0 is one smallest falsifiable
baseline (no fitted strategy parameter). This is the frozen pre-registration; the result
is recorded by dated amendment. Frozen on commit (§b/§c).

## 1. Provenance (verified independently)

Literature anchor: **Liu, Qingfu & Tse, Yiuman (2017), "Overnight returns of stock
indexes: Evidence from ETFs and futures," *International Review of Economics & Finance*
48(C):440–451** (SSRN 2921758; ScienceDirect S1059056016301563; RePEc
reveco:v48:y:2017:i:c:p:440-451). Verified by independent search: the paper documents
that **US ETF overnight returns are significantly positive while intraday returns are
negative** — an intraday reversal of the overnight move. That is the antecedent for ODR's
`β < 0` reversal hypothesis. (The exact PDF is paywalled; the citation, venue, authors,
and central finding were confirmed from multiple indexing sources.)

## 2. ODR-0 — smallest baseline hypothesis (frozen)

*SPY's dividend-neutral previous-RTH-close → 09:30 opening return **negatively predicts**
its 09:30 → 10:00 first-half-hour return.*

### Clock semantics (ET; 1-minute bar-START timestamps)

- `previous_close` = previous RTH session final close.
- `open_0930` = the **09:30 bar open** (opening print; the signal is observed here).
- `open_0931` = the **09:31 bar open** (causal entry — one bar after the signal print).
- `close_0959` = the **09:59 bar close** (the 10:00 price; exit).
- A session is used only if it is a **NORMAL FULL session** with bars 09:30 / 09:31 /
  09:59 / 15:59; early closes and sessions missing any produce no observation/trade.

`overnight_return = (open_0930 + cash_distribution − previous_close) / previous_close`
(**dividend-neutral**, cash added only on SPY ex-dividend sessions via the frozen State
Street sidecar `data/SPY_EX_DIVIDENDS_v1.0.json` — the SAME convention as MIM). ·
`first_half_hour_return = close_0959 / open_0930 − 1` (09:30→10:00; intraday, clean) ·
`trade_return = close_0959 / open_0931 − 1` (09:31→09:59; executable).

### Association test (frozen)

`first_half_hour_return = α + β·overnight_return + ε`; **preregistered sign β < 0.**
Robust SE convention = **HC1** (White heteroskedasticity-consistent, small-sample
corrected) PRIMARY; classical OLS SE secondary; 95% CI via normal 1.96. Frozen before
outcomes; no covariance-estimator shopping.

### Causal sign strategy

`overnight_return > 0` → **SHORT**; `< 0` → **LONG**; `== 0` → **no trade**. Signal
observed from the 09:30 opening print; **enter using the 09:31 bar open**; **exit using
the 09:59 bar close**; one trade maximum per normal full session.
`realized = −sign(overnight_return) · trade_return`. **No** threshold, VWAP, EMA, ATR,
stop, target, volume/volatility/macro filter, side rescue, or alternate opening/exit
window.

### Costs (frozen before outcomes; not optimized)

Three views, gross reported separately from executable economics: (1) **zero-cost**;
(2) existing lab **one-tick execution stress** (1 tick per fill, 2 fills → `2·0.01/price`
bps); (3) one conservative **fixed 5 bps round-trip stress**.

## 3. Kill / advance gates (frozen)

One baseline. **FAMILY DEAD** if any of: `β ≥ 0` (reversal requires β < 0); **or** gross
causal sign-strategy expectancy `≤ 0`; **or** a positive gross expectancy fails the frozen
conservative cost stress. If baseline dies → FAMILY DEAD, stop. If **all** gates pass →
**EDGE CANDIDATE — VALIDATION DECISION REQUIRED**, stop (validation **not** run
autonomously). No rescue; no alternate window after failure.

## 4. Data & firewall

Development **2024-09-03 → 2025-12-31** only. The consumed VDC validation window
(2026-01-06 → 2026-04-30) is **not** ODR confirmation. No embargo / buffer /
hypothesis-source / forward-holdout inspection. Fresh confirmation, if ever earned, is a
genuinely fresh window frozen later. No new market-price/intraday provider (the State
Street distributions seam is reused for corporate-action normalization only). No
TradingView dependency, no CuttingBoard contact, no merge.

## 5. Budget (§9/§f)

ODR interpreted-development **≤ 4** (default new-family allowance). ODR-0 = config 1. A
`family=ODR, budget_class=development` ledger row is written at the run.

## Code (frozen)

| File | SHA256 |
|---|---|
| `analysis/odr.py` | `31ee6ab3c86420cb5d478dd3f8dd09e6448b364a1e9f276ed5e8275b1a12fd63` |
| `analysis/test_odr.py` | `1eaaa7ddf6196be4bb337d437342f829473e1241af6b1f35651a505d889f920b` |
| `analysis/mim.py` (reused: OLS/HC1, sidecar, bootstrap, cost constants) | `f80474fdfb38cf948c9dd86c9f32f3dc0e9fe81ec536dbf62b64c7ad1a80f222` |
| `data/SPY_EX_DIVIDENDS_v1.0.json` | `40b09763d7dc844f9f0d65714411f0173c5b3531601ba1eb601d0cf3d6394622` |

Corpus sha256 `a4afaa704e6ded54f62f1670c52ff74070338ccb943eebcc2f73fe9c170ed97a`. Screened
(frozen `CORPUS_MASK_v1.0`) primary, raw sensitivity. Tests 4/4 synthetic. No engine
change; ODR is a standalone module.

## Reproduction

```
cd studies/vwap-lab-2026-08/analysis
python3 odr.py               # -> ODR0_DEV_2026-08-27.json
python3 test_odr.py          # 4/4 synthetic
```

## Amendments

### Amendment 1 — result (2026-08-27) — **ODR FAMILY DEAD**

Run under the frozen pre-registration; `odr.py` unchanged since the freeze commit
`dcd0d84`. Evidence `analysis/ODR0_DEV_2026-08-27.json` sha256
`9fb70af1f5fc6004fc3bb8cfe0bd479717a47231b1b0dd6742c87ac5d2c9dd54`; byte-identical across
reruns. **N = 328** observations (screened primary; dividend-neutral overnight).

**Association (screened; `first_half_hour = α + β·overnight`):**

| quantity | value |
|---|---:|
| **β** | **−0.03571** |
| HC1 SE (primary) | 0.04031 |
| t (HC1) | −0.886 |
| 95% CI (HC1) | [−0.11472, +0.04331] |
| R² | 0.00697 |
| N | 328 |

The preregistered sign **β < 0 holds directionally** (a reversal tendency, consistent
with Liu & Tse), **but it is statistically insignificant** (t −0.89; CI straddles zero).

**Causal sign strategy (enter 09:31 open, exit 09:59 close):** gross mean **−0.6255
bps**/trade (cum −204.5 bps, PF 0.938, win 49.8%, max-DD 475 bps); long −0.975 bps
(n=131), short −0.392 bps (n=196); bootstrap mean CI95 [−3.34, +2.39] bps (straddles
zero). Costs: zero −0.63, lab-slippage −0.95, 5 bps-stress −5.63. **Robustness:** raw ==
screened (β −0.03571, gross −0.6255; the masked bad-tick bars are not ODR clock bars).

**Verdict — FAMILY DEAD** by the frozen gate: although β < 0, the **gross causal
sign-strategy expectancy is ≤ 0** (−0.6255 bps), and it would also fail the cost stress.
The overnight→first-half-hour reversal is directionally present but too weak to be
statistically significant or to yield a positive executable edge on SPY in the
development window. Per the frozen no-rescue rule: **report and stop** — no alternate
opening/exit window, no threshold, no subset. Autonomous STOP at **A — ODR FAMILY DEAD**.

ODR interpreted-development **0 → 1/4** (config 1; the remaining ≤3 are **not** earned by
a failed baseline). Ledger row `ODR0_DEV_2024-09-03_2025-12-31`.
