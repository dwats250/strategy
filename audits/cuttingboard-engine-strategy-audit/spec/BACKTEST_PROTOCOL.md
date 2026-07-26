# TV-0 Frozen Backtest Protocol

Status: FROZEN FOR TV-1

## Objective

Measure the incremental historical effect of reproducible CuttingBoard gate
families on a directional SPY proxy. The study measures gate selectivity and
the distribution of simulated underlying returns. It does not estimate
options-spread profitability or recommend live trading.

## Frozen instrument and timeframe

- Chart instrument: SPY
- Candle type: standard OHLC
- Timeframe: one day
- Signal state: completed bar only
- Position limit: one open simulated position
- Pyramiding: disabled
- Direction: long and short
- Continuation and FVG paths: disabled

The script must reject non-daily charts at runtime. It must not support
Heikin-Ashi, Renko, Range, Kagi, Line Break, or Point & Figure testing.

## Frozen timing model

1. Compute all gate states after daily bar `t` is confirmed.
2. Submit the simulated market entry for the open of bar `t+1`.
3. Use ATR known at the close of `t`; no value from `t+1` may affect the
   signal.
4. The simulated protective levels are anchored to the actual `t+1` fill:
   - long stop: fill minus signal ATR;
   - long target: fill plus two signal ATR;
   - short stop: fill plus signal ATR;
   - short target: fill minus two signal ATR.
5. Exit at the first modeled stop or target touch.
6. If both stop and target are touched within the same daily candle, mark the
   trade `AMBIGUOUS_INTRABAR` and use the conservative stop-first result in
   the headline metrics. Export the ambiguity flag so offline intraday data
   can resolve it later.
7. No same-bar reversal. A new signal may enter only after the prior position
   is closed and a later bar confirms.

This is an execution proxy. CuttingBoard's candidate reference entry is the
current quote; using the next open and re-anchoring fixed ATR geometry avoids
future knowledge but is not exact runtime parity.

## Cross-symbol data contract

Every external symbol is an explicit Pine input with a visible default. TV-1
must not bury provider-specific ticker IDs inside gate functions.

Required contexts:

- SPY, QQQ, IWM
- VIX
- DXY
- US 10-year yield proxy
- BTC/USD proxy
- configured breadth universe
- configured expansion-leadership universe

Formula parity and data parity are separate. A formula can pass while a
provider/session mapping remains `PROXY`.

Rules:

- `request.security()` uses the daily timeframe.
- `barmerge.lookahead_off` for same-timeframe cross-symbol requests.
- Signals consume confirmed values only.
- No future offset or lookahead construction may expose an unconfirmed value
  to a historical bar.
- Missing requested values remain missing. Expansion breadth counts missing
  tradable symbols as not advancing, matching the pinned engine.
- The run manifest records every symbol ID used.

## Incremental variants

Thresholds and formulas are identical in every variant. Only gate-family
activation changes.

| Variant | Required state |
|---|---|
| V0 | Regime class supplies LONG for RISK_ON/EXPANSION and SHORT for RISK_OFF; ignore posture |
| V1 | V0 plus computed posture/confidence permission |
| V2 | V1 plus SPY structure and CHOP exclusion |
| V3 | V2 plus available direct soft gates: stop-distance and extension; preserve inert-gate counters |
| V4 | V3 plus market-stress kill switch |
| V5 | V4 plus macro-pressure directional conflict |
| V6 | Full reproducible direct proxy, including diagnostic thesis/invalidation/entry-quality states but excluding unavailable gates |

Every variant runs from the same code and produces a `variant_id`. Separate
scripts with drifting formulas are forbidden.

## Predetermined study windows

- Warm-up/data-availability observation: 2015-01-01 through 2015-12-31
- In-sample descriptive window: 2016-01-01 through 2021-12-31
- Untouched out-of-sample window: 2022-01-01 through 2026-07-24
- Combined descriptive window: 2016-01-01 through 2026-07-24

The out-of-sample window may be inspected only after TV-2 parity acceptance.
No threshold may change after it is inspected. A provider with later history
does not justify silently shortening the sample; affected bars must carry a
data-availability flag.

## Friction scenarios

Underlying-share friction is a sensitivity input, not an options-cost proxy.

Run and record:

1. `PARITY`: zero commission, zero slippage.
2. `BASE`: 0.01% commission per transaction and one minimum tick of slippage
   per fill.
3. `STRESS`: 0.03% commission per transaction and three minimum ticks of
   slippage per fill.

Do not optimize these values. Headline gate comparisons must show both
frictionless signal behavior and the base-friction result.

## Required exports

Each run must preserve:

- full simulated trade ledger;
- signal date and next-open fill date;
- direction, variant, entry, stop, target, and signal ATR;
- every gate boolean;
- first rejection gate and all rejection gates;
- regime, posture, confidence, net score, and vote coverage;
- structure label and derived inputs;
- missing-data mask;
- exit reason and ambiguous-intrabar flag;
- gross and friction-adjusted return;
- maximum favorable and adverse excursion when available;
- cumulative gate rejection counts;
- trade count, exposure, win rate, average trade, profit factor, and maximum
  drawdown;
- long/short split;
- results by regime, posture, and structure;
- incremental deltas from each prior variant.

Screenshots and summary tables are supplementary. They never replace the raw
trade ledger and run manifest.

## Required run manifest

Every run records:

- CuttingBoard source SHA;
- Pine source SHA-256;
- Pine version;
- run timestamp;
- SPY chart symbol, timeframe, timezone, and session setting;
- all cross-symbol IDs;
- variant;
- date window;
- every threshold;
- commission and slippage;
- missing-data counts;
- known parity exceptions;
- raw export filenames.

## TV-2 parity acceptance

TV-2 passes only when:

1. All literal thresholds match the pinned source.
2. Momentum and volume-ratio fixture cases match exactly.
3. EMA and ATR differences are measured, bounded, and disclosed.
4. Regime vote, missing-vote bounding, classification, and posture fixtures
   match.
5. Structure priority fixtures match, including BREAKOUT before EMA alignment
   and REVERSAL before TREND/PULLBACK.
6. Direct soft-gate aggregation matches for available gates.
7. No signal changes after its bar closes.
8. Cross-symbol missing data cannot become neutral silently.
9. The seven semantic findings in the gate matrix are confirmed, narrowed, or
   falsified with evidence.

## Stop conditions

Stop TV-1 or TV-2 if:

- Pine cannot represent a rule without changing its meaning;
- a required symbol has no viable historical mapping;
- request limits force the universe to be silently reduced;
- a missing gate must be assumed to pass for the script to trade;
- the strategy repaints;
- standard-candle fills cannot be established;
- an implementation choice would optimize performance;
- the code begins modeling options returns; or
- any work would modify CuttingBoard.

The proper outcome is a narrower honest proxy, not an invented full-engine
replica.

