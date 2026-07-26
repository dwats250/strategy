# TV-1 Parity Cases — CuttingBoard Direct-Path Proxy v0.1

Status: `DOCUMENTED — OBSERVED RESULTS PENDING A TRADINGVIEW RUN`

Created: 2026-07-26

Implementation under test:
[`../pine/cuttingboard_direct_proxy_v0.1.pine`](../pine/cuttingboard_direct_proxy_v0.1.pine)

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`.
Mutation permission: **NONE**. Nothing here proposes a CuttingBoard change.

## What this document is

The twelve discriminating cases `charges/TV-1-PINE-IMPLEMENTATION.md` requires, each stated
as a fixture with the **expected** result derived from the frozen literals and the TV-0R
literal-rule appendix, plus an **observed** slot for the TradingView run.

**Performance is not a test oracle.** A change that improves results but breaks a fixture is
wrong.

## Honest status of the `Observed` column

Every `Observed` cell reads `PENDING`. TV-1 was implemented in a headless container with no
TradingView access, so the script has **not been compiled, loaded, or run**. Under
`docs/conventions.md` §h, unavailable is not the same as passing: no case below is claimed to
have been verified, and the charge's validation items 1–5 remain open. The expected values
are arithmetic over cited literals and are checkable by inspection; they are not run results.

---

## Declared interpretations — resolve these first

Where the frozen matrix classifies a gate `EXACT_FORMULA` but does not supply the literal a
Pine translation needs, the implementation makes a declared choice rather than inventing a
threshold. Each is marked in the Pine source and listed here. **TV-2 must resolve every one
against the pinned source.** None is called exact, and none may be treated as verified.

| ID | Where | Frozen text | Declared choice | Risk if wrong |
|---|---|---|---|---|
| DI-1 | S-02 REVERSAL | "absolute EMA9/21 spread `<0.2%`" — denominator unstated | spread taken as `abs(ema9 - ema21) / ema21` | Denominator `close` instead of `ema21` shifts the REVERSAL boundary by roughly the price/EMA21 gap — small, but it changes label counts |
| DI-2 | S-03 / S-04 | "Determined from EMA alignment and price relative to EMA9/21"; CHOP is "degraded aligned structure, or fallthrough" | Bull aligned: `close > ema9` TREND_UP, `ema21 <= close <= ema9` PULLBACK_UP, `close < ema21` degraded → CHOP. Bear mirrored | Wrong band boundaries move mass between PULLBACK and CHOP, which changes Gate 4 rejection counts directly |
| DI-3 | D-02 ATR14 | "Pandas `ewm(alpha=1/14, adjust=False)` on true range" — true range and seed unstated | Standard TR (`max(h-l, abs(h-c1), abs(l-c1))`), first bar seeded `h-l`, recursion seeded on the first TR to match `adjust=False` | A different seed changes early-history ATR, therefore stop distance, Gate 6 and Gate 10 in the warm-up window |
| DI-4 | C-01 | "NEUTRAL from net sign" — raw or bounded unstated | RAW `net_score`, the field the `RegimeState` actually reports | Only affects computed NEUTRAL, which is unreachable for entries (Case 4); diagnostic impact only |
| DI-5 | Q-08 | "fixed SPY option proxy must fit the risk budget after regime multiplier" — multiplier given only for directional regimes | Budget `400` for RISK_ON / RISK_OFF / EXPANSION; elsewhere the gate is `UNAVAILABLE_LITERAL` and never passes | None on reachable paths; the gate is INERT there. Never silently treated as satisfied |
| DI-6 | Execution | "protective levels are anchored to the actual `t+1` fill" | Distances submitted in ticks from the fill (`strategy.exit` `loss`/`profit`), so the stop is live on the fill bar | One-tick quantization of the stop and target; on SPY that is $0.01 |

---

## Case 1 — strict versus inclusive threshold operators

All six R-02 vote comparisons are **strict**; a value exactly equal to a cutoff votes
`NEUTRAL`. The posture, R-01 VIX, macro-component, Gate 6 and Gate 10 comparisons are
**inclusive**.

| Fixture | Input | Expected | Observed |
|---|---|---|---|
| 1a | SPY `pct = 0.003000` | `vote_spy = NEUTRAL` (needs `> 0.003`) | PENDING |
| 1b | SPY `pct = 0.003001` | `vote_spy = RISK_ON` | PENDING |
| 1c | VIX level `= 18.0` | `vote_vix_level = NEUTRAL` (needs `< 18`) | PENDING |
| 1d | VIX level `= 25.0` | `vote_vix_level = NEUTRAL` (needs `> 25`) | PENDING |
| 1e | R-01 VIX `pct = -0.010000` | Condition 2 **passes** (`<= -0.01`) | PENDING |
| 1f | RISK_ON, `confidence = 0.75` | `AGGRESSIVE_LONG` (inclusive `>=`) | PENDING |
| 1g | NEUTRAL, VIX level `= 18.0` | `NEUTRAL_PREMIUM` (inclusive `>=`) — but see Case 4 | PENDING |
| 1h | NEUTRAL, VIX level `= 25.0` | `NEUTRAL_PREMIUM`, not STAY_FLAT (`> 25` is strict) | PENDING |
| 1i | Gate 6, `risk / entry = 0.010000` | `PASS` (inclusive `>=`) | PENDING |
| 1j | Gate 10, `abs(entry - ema21) = 1.5 * ATR` exactly | `PASS` (inclusive `<=`) | PENDING |
| 1k | Macro volatility `change_pct = -0.010000` | component `RISK_ON` (inclusive `<=`) | PENDING |

## Case 2 — missing-vote bounding

`bounded_net = max(0, net - missing)` when `net > 0`, otherwise `min(0, net + missing)`.
`confidence = abs(bounded_net) / 8` — the **structural** eight-vote denominator, never
`total_votes`. Bounding is clamped at zero and never crosses sign. `net == 0` takes the
second branch.

| Fixture | Votes | Expected | Observed |
|---|---|---|---|
| 2a | 4 ON, 0 OFF, 1 NEUTRAL, 3 missing | `net = 4`, `missing = 3`, `bounded = 1`, `conf = 0.125`, regime `NEUTRAL`, posture `STAY_FLAT` | PENDING |
| 2b | 0 ON, 6 OFF, 0 NEUTRAL, 2 missing | `net = -6`, `bounded = -4`, `conf = 0.500`, regime `RISK_OFF` (via the `<= -2` branch, since `conf < 0.60`), posture `STAY_FLAT` (needs `>= 0.55`) | PENDING |
| 2c | 1 ON, 0 OFF, 4 NEUTRAL, 3 missing | `net = 1`, `bounded = max(0, -2) = 0`, `conf = 0`, regime `NEUTRAL` — clamp holds, sign never crosses | PENDING |
| 2d | 2 ON, 2 OFF, 2 NEUTRAL, 2 missing | `net = 0` → second branch → `bounded = min(0, 2) = 0`, `conf = 0` | PENDING |
| 2e | 6 ON, 0 OFF, 2 NEUTRAL, 0 missing | `net = 6`, `bounded = 6`, `conf = 0.750`, regime `RISK_ON`, posture `AGGRESSIVE_LONG` | PENDING |
| 2f | All 8 missing | `total = 0`, `net = 0`, `bounded = 0`, `conf = 0`, regime `NEUTRAL`, posture `STAY_FLAT`; `missing_symbol_count > 0` flagged | PENDING |

Missing votes are **skipped**: they enter no counter and no breakdown. A missing symbol can
never become a neutral vote — protocol TV-2 acceptance item 8.

## Case 3 — RISK_ON, RISK_OFF, CHAOTIC, EXPANSION and computed NEUTRAL

| Fixture | Setup | Expected | Observed |
|---|---|---|---|
| 3a | `bounded = +5`, `conf = 0.625` | `RISK_ON` (via `>= 4 and conf >= 0.60`), posture `CONTROLLED_LONG`, direction LONG | PENDING |
| 3b | `bounded = +6`, `conf = 0.750` | `RISK_ON`, posture `AGGRESSIVE_LONG` | PENDING |
| 3c | `bounded = +2`, `conf = 0.250` | `RISK_ON` (via the plain `>= 2` branch), posture `STAY_FLAT` (`conf < 0.50`) — RISK_ON does **not** imply a tradable posture | PENDING |
| 3d | `bounded = -5`, `conf = 0.625` | `RISK_OFF`, posture `DEFENSIVE_SHORT`, direction SHORT | PENDING |
| 3e | VIX `pct = 0.16`, any votes | `CHAOTIC` first — the check precedes every net branch. Posture `STAY_FLAT`. K-01 also halts (`> 0.15`), so V4+ rejects on the kill switch before the regime is consulted | PENDING |
| 3f | R-01 all four conditions true | `EXPANSION`, posture `EXPANSION_LONG`, `confidence = 1.0`, `net = 0`, all vote counters `0`, `vote_coverage = 0`. The eight-vote model never runs and the posture function is never called | PENDING |
| 3g | `bounded ∈ {-1, 0, 1}` | `NEUTRAL`, `conf <= 0.125`, posture `STAY_FLAT` via the global floor | PENDING |

## Case 4 — the apparent NEUTRAL reachability issue

Arithmetic over the cited literals, stated so the fixture is checkable rather than asserted:
`confidence = abs(bounded_net) / 8` and `bounded_net` is an integer, so the only attainable
confidences on the computed branch are `0, 0.125, …, 1.0`. `NEUTRAL` requires
`abs(bounded_net) <= 1`, hence `confidence <= 0.125`, hence `confidence < 0.50`, hence the
global posture floor fires first.

| Fixture | Expected | Observed |
|---|---|---|
| 4a | `NEUTRAL_PREMIUM` count over the full sample = **0** in every variant | PENDING |
| 4b | Every `NEUTRAL` bar is a Gate 1 rejection in V1+ | PENDING |
| 4c | `TRANSITION` never appears — `_classify_regime` cannot emit it | PENDING |
| 4d | The `0.50 <= confidence < 0.55` interval is never observed on the computed branch | PENDING |

This is the fixture for semantic finding 1. **TV-1 does not adjudicate it.** Confirming,
narrowing or falsifying the hypothesis remains TV-2's task under the frozen contract.

## Case 5 — BREAKOUT / REVERSAL priority

Priority order implemented: missing metrics → CHOP; BREAKOUT; REVERSAL; TREND/PULLBACK from
alignment; degraded or fallthrough → CHOP.

| Fixture | Setup | Expected | Observed |
|---|---|---|---|
| 5a | `mom5 = +0.025`, `vol_ratio = 1.4`, `close > ema9`, and EMA9/21 spread `= 0.001` | `BREAKOUT_UP` — breakout is evaluated before reversal | PENDING |
| 5b | Spread `= 0.001`, `mom5 = +0.005`, `vol_ratio = 1.0`, EMA9 > EMA21 > EMA50, `close > ema9` | `REVERSAL` — reversal is evaluated before TREND/PULLBACK | PENDING |
| 5c | `mom5 = +0.025`, `vol_ratio = 1.4`, `close < ema9` | **not** BREAKOUT_UP — direction must agree with price versus EMA9 | PENDING |
| 5d | `mom5 = +0.03`, `vol_ratio = 1.25` | **not** BREAKOUT — volume ratio must exceed 1.3 | PENDING |
| 5e | Price makes a new 52-week high with `mom5 = 0.005`, `vol_ratio = 1.0` | **not** BREAKOUT — no recent-high test exists. Names must not be silently upgraded (semantic finding 7) | PENDING |
| 5f | EMA9 crosses EMA21 with spread `= 0.004` | **not** REVERSAL — there is no crossover test, only a current-spread approximation | PENDING |

## Case 6 — direct 2R construction

`entry = close`, `stop = close ∓ ATR`, `target = close ± 2 ATR`, so `risk = ATR`,
`reward = 2 ATR`, `rr = 2.000` **before Gate 7 evaluates it**.

| Fixture | Expected | Observed |
|---|---|---|
| 6a | `ref_rr = 2.000` on every candidate bar, long and short | PENDING |
| 6b | Gate 7 passes on every reachable directional candidate (`>= 2.0`) | PENDING |
| 6c | Gate 7's `3.0` NEUTRAL requirement is never exercised on an entry, because NEUTRAL cannot produce one (Case 4) | PENDING |
| 6d | Gate 7 cumulative rejections attributable to reachable direct candidates = **0** | PENDING |

Fixture for semantic finding 2. The R:R gate is constructed, not discovered.

## Case 7 — stop ATR-floor equality and the independent 1% floor

Gate 6 has two legs: risk `>= 1%` of entry **and** risk `>= 1 ATR`. Direct geometry sets
risk `= ATR` exactly, so the ATR leg passes by equality and Gate 6 reduces to `ATR / price >= 1%`.

| Fixture | Setup | Expected | Observed |
|---|---|---|---|
| 7a | any bar | `g6_leg_atr = PASS` by equality on every candidate | PENDING |
| 7b | `close = 500.00`, `ATR = 4.00` → `0.0080` | `g6_leg_pct = FAIL`, Gate 6 `FAIL` | PENDING |
| 7c | `close = 500.00`, `ATR = 5.00` → `0.0100` | `g6_leg_pct = PASS` (inclusive), Gate 6 `PASS` | PENDING |
| 7d | `close = 500.00`, `ATR = 6.00` → `0.0120` | Gate 6 `PASS` | PENDING |

Fixture for semantic finding 3. Expect Gate 6 to reject most low-volatility SPY bars: a 1%
daily ATR is a high bar for SPY in calm regimes, and that selectivity is the gate's real
content.

## Case 8 — zero, one and two available soft failures

Aggregation runs over the **declared available** soft gates only — Gate 6 and Gate 10. Gate
11 is excluded and reported separately.

| Fixture | Setup | Expected | Observed |
|---|---|---|---|
| 8a | Gate 6 PASS, Gate 10 PASS | `soft_fail_count = 0` → `QUALIFIED` → V3+ may enter | PENDING |
| 8b | Gate 6 FAIL, Gate 10 PASS | `= 1` → `WATCHLIST` → **no entry** | PENDING |
| 8c | Gate 6 PASS, Gate 10 FAIL | `= 1` → `WATCHLIST` → no entry | PENDING |
| 8d | Both FAIL | `= 2` → `REJECT` | PENDING |
| 8e | Any of the above | `excluded_soft_gates = 1` displayed; Gate 11 never contributes a miss **and never contributes a pass** | PENDING |

## Case 9 — kill-switch strict comparisons

| Fixture | Input | Expected | Observed |
|---|---|---|---|
| 9a | VIX level `= 35.00` | no halt (`> 35` is strict) | PENDING |
| 9b | VIX level `= 35.01` | halt | PENDING |
| 9c | VIX `pct = 0.150000` | no halt — and no CHAOTIC either, since that is also `> 0.15` | PENDING |
| 9d | VIX `pct = 0.150001` | halt **and** CHAOTIC; in V4+ the kill switch is the first rejection | PENDING |
| 9e | SPY `pct = -0.030000` | no halt | PENDING |
| 9f | SPY `pct = -0.030001` | halt (absolute value) | PENDING |
| 9g | VIX missing | no halt from the VIX legs — a missing value is not a breach | PENDING |

## Case 10 — macro-pressure conflict

Components are built in the pinned units: `change_pct = pct_change_decimal * 100`
(**percentage points**), `change_bps = pct_change_decimal * price * 100` (rates only). The
cutoffs are in those units and are reproduced exactly, not rescaled.

| Fixture | Components | Expected | Observed |
|---|---|---|---|
| 10a | VIX `-0.50` pp, DXY `-0.30` pp, TNX `-42` bps, BTC `+2.0` pp | all four `RISK_ON` → overall `RISK_ON`; LONG candidate allowed, SHORT candidate **BLOCKED** `macro_pressure_conflict` | PENDING |
| 10b | Mirror of 10a | overall `RISK_OFF`; SHORT allowed, LONG **BLOCKED** | PENDING |
| 10c | VIX `RISK_ON`, DXY `RISK_OFF`, TNX/BTC missing | `on >= 1 and off >= 1` → `MIXED` → allowed in both directions | PENDING |
| 10d | VIX `RISK_ON`, other three missing | `known = 1`; falls through every branch to the terminal `MIXED` — **not** RISK_ON | PENDING |
| 10e | All four exactly `0.0` | all `NEUTRAL` → overall `NEUTRAL` → allowed, size unchanged | PENDING |
| 10f | All four missing | `UNKNOWN` → allowed, size unchanged | PENDING |
| 10g | VIX `pct_change_decimal = -0.0002` (a 0.02% move) | `change_pct = -0.02 <= -0.01` → `RISK_ON`. **Recorded as found:** the percentage-point cutoffs are one basis point wide, so almost any non-zero move classifies and `MIXED` should dominate the sample | PENDING |
| 10h | BTC `+0.02` pp with VIX `RISK_OFF` | bitcoin's direction is inverted relative to the other three; expect `MIXED` | PENDING |

Pressure **blocks only on direct directional conflict**. Its size multipliers (`0.75`, `0.5`)
belong to E-01, which the frozen matrix classifies `EXCLUDED_OPERATIONAL`: they are displayed
and recorded, never applied. Simulated quantity stays one directional unit.

## Case 11 — unavailable gates do not silently report PASS

| Gate | Class | Expected surface | Observed |
|---|---|---|---|
| Q-11 Gate 11 TIME | `EXCLUDED_OPERATIONAL` | No boolean at all. Data-window export is `na`, table reads `UNAVAILABLE`, excluded from the soft arithmetic, and a separate counter records the bars it was unavailable on | PENDING |
| Q-09 Gate 9 EARNINGS | `CURRENTLY_INERT` | `SKIPPED_FAIL_OPEN` — fail-open **by pinned construction**, not by an implementation choice; no earnings data is sourced | PENDING |
| Q-08 Gate 8 outside RISK_ON/RISK_OFF/EXPANSION | multiplier not supplied by TV-0 | `UNAVAILABLE_LITERAL`, `g8_pass = false`. Never a silent pass (DI-5) | PENDING |
| O-01, Q-11, E-01, E-02, E-03 | `EXCLUDED_OPERATIONAL` | Not implemented, not counted as satisfied, and excluded from every aggregate | PENDING |
| X-01, X-02 | `EXCLUDED_EXTERNAL` | Not implemented. No flow is fabricated and no full-engine qualification is claimed | PENDING |
| P-01, P-02 | `DEFERRED_PATH` | Disabled in v0; no continuation or FVG path exists in the source | PENDING |

## Case 12 — no repainting after confirmation

| Fixture | Expected | Observed |
|---|---|---|
| 12a | Every `request.security` uses `"D"` with `barmerge.lookahead_off` | PENDING |
| 12b | Signals are gated on `barstate.isconfirmed`; no order is submitted from a forming bar | PENDING |
| 12c | Entry fills at the open of `t+1`; no value from `t+1` enters the bar-`t` decision | PENDING |
| 12d | `signal_pass` recorded live on bar `t` is unchanged after bar `t` closes | PENDING |
| 12e | A fresh chart reload reproduces the historical trade list exactly | PENDING |
| 12f | Protective distances use the ATR known at the close of `t` and never a later ATR | PENDING |

---

## Known parity exceptions carried forward to TV-2

1. **Pinned source not resolved during TV-1.** Preflight item 6 could not be satisfied: the
   TV-1 container had no CuttingBoard checkout and no read access to the pinned commit. The
   implementation consumes the hash-verified literal-rule appendix, not the source. TV-2 must
   resolve `59f8279d796335149afdec4aa507b6f927233518` and re-check every literal against it.
2. **The script has not been compiled or run.** Charge validation items 1–5 are open.
3. **EMA warm-up divergence (D-01).** `ta.ema` seeds with an SMA; the engine's
   `ewm(adjust=False)` seeds on the first observation. Both are computed and the difference
   is exported as `ema9_div_vs_pandas` / `ema21_div_vs_pandas` for a tolerance test.
4. **ATR initialization (D-02).** The custom recursion is the gate input; `ta.atr` is
   computed only as a divergence diagnostic. Pine ATR is **not** called exact.
5. **Provider and session mapping is `PROXY`.** Formula parity and data parity are separate.
   Every cross-symbol ID is an input with a visible default and is recorded per run.
6. **Percent-change proxy.** The engine consumes a live quote's `pct_change_decimal`; this
   proxy uses `(close - close[1]) / close[1]` on confirmed daily bars, per the matrix's
   temporal warning. This is an end-of-day historical proxy, not time-of-day parity.
7. **Tick quantization (DI-6).** Protective distances are submitted in ticks from the fill.
8. **Same-bar stop-and-target bars** rely on TradingView's conservative stop-first assumption
   for the headline result; the ambiguity flag and counter are exported so intraday data can
   resolve them later.
