# TV-0 Gate Translation Matrix

Status: FROZEN FOR TV-1

Source: `dwats250/cuttingboard`
`59f8279d796335149afdec4aa507b6f927233518`

## Classification vocabulary

- `EXACT_FORMULA`: the decision rule can be translated literally from the
  pinned source.
- `FORMULA_EXACT_DATA_PROXY`: the formula is literal, but historical
  provider, session, symbol, or warm-up differences prevent full runtime
  parity.
- `CURRENTLY_INERT`: present in the engine but cannot change the SPY direct
  path under the pinned construction.
- `EXECUTION_PROXY`: requires declared simulated timing/fill behavior.
- `EXCLUDED_EXTERNAL`: needs data TradingView does not provide with an honest
  historical contract.
- `EXCLUDED_OPERATIONAL`: validates runtime operations rather than market
  setup quality.
- `DEFERRED_PATH`: real engine behavior intentionally outside direct-mode v0.

## Temporal warning

CuttingBoard consumes fresh quotes at its actual run time and combines them
with completed daily history. TV-0 evaluates confirmed daily bars and acts at
the next daily open. Therefore, TV-0 audits the gate relationships under an
end-of-day historical proxy; it does not claim time-of-day parity with a live
premarket or hourly CuttingBoard run.

## Gate inventory

| ID | Engine surface | Pinned behavior | Class | TV-1 treatment |
|---|---|---|---|---|
| O-01 | `validation.py` freshness, type, bounds | Required halt symbols must be fresh, valid, and inside configured sanity bounds | `EXCLUDED_OPERATIONAL` | Record as unavailable; do not turn data-delivery checks into signals |
| K-01 | `runtime._kill_switch` | Halt when VIX level `>35`, VIX daily change `>15%`, or absolute SPY daily change `>3%` | `FORMULA_EXACT_DATA_PROXY` | Implement as a visible market-stress exclusion using confirmed daily values |
| R-01 | `regime.detect_expansion_regime` | SPY and QQQ positive; VIX change `<=-1%`; at least 70% of the configured tradable universe advancing; at least two leaders up `>=1.5%` | `FORMULA_EXACT_DATA_PROXY` | Implement with configurable TradingView symbol IDs; missing symbols count as not advancing, matching source |
| R-02 | `regime.compute_regime` | Eight votes from SPY, QQQ, IWM, VIX level/change, DXY, TNX, and BTC | `FORMULA_EXACT_DATA_PROXY` | Translate thresholds literally; expose every vote and missing-data flag |
| R-03 | Missing-vote bounding | Missing votes shrink the surviving leader toward zero; confidence uses an eight-vote denominator | `EXACT_FORMULA` | Implement literally |
| R-04 | Regime classification | VIX change `>15%` forces CHAOTIC; bounded net `>=2` gives RISK_ON, `<=-2` gives RISK_OFF, otherwise NEUTRAL | `EXACT_FORMULA` | Implement literally |
| R-05 | Posture | Low confidence, CHAOTIC, and most NEUTRAL states become STAY_FLAT; RISK_ON/RISK_OFF require their posture thresholds | `EXACT_FORMULA` | Implement literally and count posture rejections separately |
| D-01 | EMA9/21/50 | Pandas recursive EMA with `adjust=False` over the engine's acquired history | `FORMULA_EXACT_DATA_PROXY` | Use Pine EMA for v0; record warm-up/window divergence and require tolerance tests |
| D-02 | ATR14 | Pandas `ewm(alpha=1/14, adjust=False)` on true range | `FORMULA_EXACT_DATA_PROXY` | Do not call Pine ATR “exact” until initialization parity is demonstrated; implement a documented approximation or custom equivalent |
| D-03 | Momentum | `(close - close[5]) / close[5]` | `EXACT_FORMULA` | Implement literally |
| D-04 | Volume ratio | Current volume divided by the prior 20 completed sessions' average | `EXACT_FORMULA` | Implement literally; exclude current volume from the denominator |
| S-01 | BREAKOUT label | Absolute five-day momentum `>2%`, volume ratio `>1.3`, and price beyond EMA9 in the same direction | `EXACT_FORMULA` | Implement literally; do not add a recent-high/low breakout requirement |
| S-02 | REVERSAL label | Absolute EMA9/21 spread `<0.2%` plus absolute five-day momentum `>0.3%` | `EXACT_FORMULA` | Implement literally; do not add an actual crossover test |
| S-03 | TREND/PULLBACK | Determined from EMA alignment and price relative to EMA9/21 | `EXACT_FORMULA` | Implement literal priority order |
| S-04 | CHOP | Missing history/metrics, degraded aligned structure, or fallthrough | `EXACT_FORMULA` | Hard exclusion in the structure variant |
| C-01 | Direct direction | Direction is manufactured from regime: RISK_ON/EXPANSION long, RISK_OFF short, NEUTRAL from net sign | `CURRENTLY_INERT` | Preserve as the candidate direction; count Gate 3 but do not claim independent information |
| C-02 | Direct geometry | Reference entry is current price; stop is one ATR away; target is two ATR away | `EXECUTION_PROXY` | Qualify using signal-close reference geometry; simulate the fill at next open using the protocol |
| Q-01 | Gate 1 REGIME | STAY_FLAT hard-rejects | `EXACT_FORMULA` | Incremental posture gate |
| Q-02 | Gate 2 CONFIDENCE | Confidence below `0.50` hard-rejects | `CURRENTLY_INERT` | Preserve and count; posture normally blocks the same candidate first |
| Q-03 | Gate 3 DIRECTION | Candidate direction must match regime | `CURRENTLY_INERT` | Preserve and count; direct candidate direction is generated from regime |
| Q-04 | Gate 4 STRUCTURE | CHOP hard-rejects | `EXACT_FORMULA` | Implement |
| Q-05 | Gate 5 STOP_DEFINED | Stop must be positive and differ from entry | `CURRENTLY_INERT` | Preserve as an invariant; direct one-ATR geometry normally guarantees it |
| Q-06 | Gate 6 STOP_DISTANCE | Risk must be at least 1% of entry and at least one ATR | `EXACT_FORMULA` | Implement; the ATR leg is equality by construction, leaving ATR/price `>=1%` as the meaningful direct-path test |
| Q-07 | Gate 7 RR_RATIO | Minimum 2R, except 3R in NEUTRAL | `CURRENTLY_INERT` | Preserve and count; direct geometry manufactures exactly 2R and reachable directional postures are not NEUTRAL |
| Q-08 | Gate 8 MAX_RISK | Fixed SPY option proxy must fit the risk budget after regime multiplier | `CURRENTLY_INERT` | Calculate for audit display only; on the pinned reachable SPY direct path, the fixed debit/credit proxies fit the $400 budget |
| Q-09 | Gate 9 EARNINGS | `None` is fail-open; generated candidates always use `None` | `CURRENTLY_INERT` | Mark `SKIPPED_FAIL_OPEN`; never source earnings data in v0 |
| Q-10 | Gate 10 EXTENSION | Entry must be within `1.5×ATR14` of EMA21 | `EXACT_FORMULA` | Implement |
| Q-11 | Gate 11 TIME | No new entry at or after 15:30 ET | `EXCLUDED_OPERATIONAL` | Daily proxy cannot honestly reproduce live run time; label unavailable and remove from soft-failure arithmetic |
| Q-12 | Soft-gate aggregation | Zero misses qualifies; one miss watchlists; two or more reject | `EXACT_FORMULA` | Apply only to the declared available soft gates; report excluded gates separately |
| P-01 | FVG pullback mode | A qualified direct result may switch to imbalance-pullback geometry | `DEFERRED_PATH` | Disabled in v0 |
| P-02 | EXPANSION continuation | Separate long-only breakout/hold/momentum/extension/stop/RR/time path | `DEFERRED_PATH` | Disabled in v0; inventory retained for a later experiment |
| X-01 | Options flow alignment | External print-level options flow can downgrade PASS to WATCHLIST | `EXCLUDED_EXTERNAL` | Unavailable; no pass assumption and no fabricated flow |
| X-02 | Chain validation | Live expiration, bid/ask, OI, and spread checks determine initial ALLOW/BLOCK | `EXCLUDED_EXTERNAL` | Unavailable; no option-return or full-engine qualification claim |
| X-03 | Correlation policy | GLD/DXY direction changes sizing modifier only | `FORMULA_EXACT_DATA_PROXY` | Calculate as diagnostic only; it does not create an entry in v0 |
| E-01 | Execution confidence sizing | Confidence below `0.60` blocks; higher confidence maps to size multipliers | `EXCLUDED_OPERATIONAL` | Gate effect may be counted, but simulated quantity stays one directional unit |
| E-02 | Trade-count/loss/cooldown | Two trades/day, two-loss lockout, and 15-minute cooldown | `EXCLUDED_OPERATIONAL` | Exclude from daily gate-quality study |
| E-03 | ORB constraint | Intraday price must clear ORB unless continuation; unavailable ORB fails open | `EXCLUDED_OPERATIONAL` | Exclude from daily v0 |
| E-04 | Macro pressure | VIX, DXY, TNX, and BTC form RISK_ON/OFF/MIXED/NEUTRAL/UNKNOWN; opposing direction blocks | `FORMULA_EXACT_DATA_PROXY` | Implement as the final optional market-context variant |
| T-01 | Thesis gate | Builds catalyst/confirmation/invalidation from existing outputs and blocks incomplete/conflicted theses | `CURRENTLY_INERT` | Reproduce status counters; normal direct candidates passing macro pressure should remain valid |
| I-01 | Invalidation gate | Re-expresses adverse thesis status | `CURRENTLY_INERT` | Diagnostic only; do not invent price-action invalidation beyond the fixed stop |
| E-05 | Entry-quality gate | Blocks missing/stale/conflicted/unconfirmed entries | `CURRENTLY_INERT` | Diagnostic only; normal direct candidates with structure confirmation should be CLEAN |

## Load-bearing semantic findings to test

These are source-derived hypotheses. TV-2 must prove or narrow each one.

1. **Computed NEUTRAL is effectively non-tradable.** Regime classification
   permits NEUTRAL only near zero bounded net, while posture requires
   confidence at least `0.50`; confidence is absolute bounded net divided by
   eight. The computed branch therefore appears unable to reach
   `NEUTRAL_PREMIUM`.
2. **The direct R:R gate is constructed, not discovered.** Direct candidates
   are built with a one-ATR stop and two-ATR target, so the result is exactly
   2R before Gate 7 evaluates it.
3. **The direct ATR stop-floor leg is constructed to pass.** Candidate risk is
   one ATR and the gate requires at least one ATR. The independent 1%-of-price
   floor remains meaningful.
4. **Direction alignment is constructed to pass.** The same regime function
   creates the candidate direction and checks it.
5. **SPY max-risk is probably inert on reachable direct paths.** Current fixed
   max-loss proxies are $150 for debit and $350 for credit against a $400
   RISK_ON/RISK_OFF/EXPANSION budget.
6. **Several late decision gates re-state upstream facts.** Thesis,
   invalidation, and entry-quality are expected to add little or no rejection
   power on a fully formed direct candidate that already survived macro
   pressure.
7. **Structure names must not be silently upgraded.** BREAKOUT is a
   momentum/volume/EMA condition, not a recent-high break; REVERSAL is a
   current EMA-spread approximation, not an observed crossover.

## TV-1 implementation rule

The Pine source must expose each available gate as a named boolean and emit a
rejection counter for each gate. A composite expression without named
intermediate states fails TV-1 because it prevents incremental attribution.

