# Engine behaviour — Backtesting.py 0.6.6 as used by the lab

Every statement below is pinned by a hand-checkable test in `tests/test_engine_behavior.py`
(25 tests, plus the seam-2 amendment tests in `tests/test_seam2_amendments.py`) and re-run in CI. Default test setup: price 100.00 everywhere except the minutes a test
overrides; cash 10,000; zero costs unless stated. If a version bump breaks any of these tests, it is
a behaviour change to understand. Do not edit the test to match.

| # | Behaviour | Demonstrated result | Test |
|---|---|---|---|
| 1 | Completed-bar signal, next-bar execution | A decision on the 09:40 minute fills at the 09:41 **open** (101), not the 09:40 close (100) | `test_market_entry_fills_at_next_minute_open` |
| 2 | Higher-timeframe signals | A 5m bar 09:30–09:34 is published on the 09:34 minute (values NaN before that) and fills at the 09:35 open | `test_five_minute_signal_published_on_last_minute_and_filled_next_bucket` |
| 3 | Missing minute in a bucket | If 09:39 is missing, the 09:35 bucket publishes on 09:38. The fill is still at 09:40, after the bucket ends, so nothing leaks. | `test_missing_last_minute_publishes_early_but_fills_after_bucket_end` |
| 4 | Initial stop on the entry bar | A stop at 99 hit inside the entry minute exits in that same minute at 99 (R = −1) | `test_initial_stop_can_trigger_in_the_entry_minute` |
| 5 | Gap through stop | A minute opening at 97 under a 99 stop fills at **97** (R = −3) | `test_gap_through_stop_fills_at_the_worse_open` |
| 6 | Stop and target in the same minute | Resolved as the **stop**, for longs and shorts (pessimistic). The lab counts these as `ambiguous_exit`. | `test_stop_and_target_in_same_minute_resolves_to_stop` |
| 7 | Target gapped through | Fills at the better open (103 against a 101 target), **provided the minute does not also trade through the stop**. If it does, the stop wins even though the open was beyond the target (see row 23). | `test_target_gapped_through_fills_at_the_better_open` |
| 8 | Discretionary exit against a later stop touch | The exit fills at the minute's open, before the stop. The library already does this; I tested my contrary hypothesis and it was wrong. | `test_discretionary_exit_precedes…`, `test_raw_library_close_with_live_stop_also_fills_at_open` |
| 9 | Costs | Per-share cost charged as cash on entry and exit; fills unadjusted. 99 shares × $0.01 × 2 = $1.98. Relative sizing includes the cost (floor(9990 / 100.01) = 99). | `test_per_share_costs_charged_on_both_sides` |
| 10 | Equity reconciliation | Final equity = cash + Σ trade P&L | `test_equity_reconciles_to_trade_pnl` |
| 11 | Insufficient capital, explicit size | 200 shares × $100 > $10,000: the order is **cancelled with a warning**, no trade | `test_order_larger_than_capital_is_cancelled_with_warning` |
| 12 | Insufficient capital, relative size | Equity below one share: cancelled with a warning | `test_relative_size_with_equity_below_one_share_is_cancelled` |
| 13 | Sizing at the fill price | A gap up after the decision is still affordable: size is computed at the fill (floor(9990/110) = 90) | `test_relative_size_uses_the_fill_price_not_the_decision_close` |
| 14 | Session flatten | Normal day: closed at the 15:55 open | `test_session_flatten_normal_day_fills_at_1555_open` |
| 15 | Early close from the calendar | 2024-12-24: 210 minutes, last minute 12:59, flatten at 12:55. The 13:00 auction print is outside the session. | `test_early_close_uses_calendar_not_fixed_clock` |
| 16 | DST | 2025-03-07 (EST) opens 14:30 UTC, 2025-03-10 (EDT) opens 13:30 UTC; both enter at 10:01 ET and exit at 15:55 ET | `test_dst_transition_keeps_eastern_clock_rules` |
| 17 | No entries after the flatten decision; no overnight carry | A 15:56 entry is ignored; the position is closed at 15:55 | `test_no_entries_after_flatten_decision_and_no_overnight_carry` |
| 18 | Interior session missing its close | Flattened at the last available minute and flagged (`flatten_fallback`) | `test_interior_session_missing_close_flattens…` |
| 19 | Open position when the data ends | Reported as `open_at_end`, marked to the final **close**; the equity curve carries the unrealized P&L | `test_open_position_at_data_end_is_marked_not_closed` |
| 20 | Why not `finalize_trades=True` | The library would close at the last bar's **open** (105) rather than mark at the close (105.5) | `test_library_finalize_would_close_at_last_open_documented` |
| 22 | Entry minute opens beyond the stop | Long, stop 99, the fill minute opens at 98: entry and exit both at 98. No risk was ever defined, so R is NaN and exit_reason is `stop_beyond_fill` (counted as "Trades with undefined R"). | `test_entry_minute_opening_beyond_stop_has_no_defined_risk` |
| 23 | Open beyond the target, same minute touches the stop | The library fills the **stop** (99), although the open (103) shows the target was reached first. This is a pessimistic bias, not merely an unknown path. Flagged `ambiguous_exit`. | `test_open_beyond_target_with_stop_touch_still_resolves_to_stop_pessimistic` |
| 24 | First bar of a backtest | Backtesting.py never calls `next()` on bar 0, so a run's first minute is never a decision point. The session-hold benchmark therefore fills at 09:32 (not 09:31) on the first session of each run only. | `test_session_hold_benchmark_enters_0931_exits_flatten_including_early_close` |
| 25 | Actual reward/risk with a signal-close target | Stop 99 and target 101 set at a 100 signal close; the fill gaps to 100.5, so the actual reward/risk is 0.5/1.5 = 0.33, reported per trade | `test_signal_close_target_reports_actual_reward_risk_after_gap` |
| 21 | Determinism | Identical trades and equity on rerun | `test_reruns_are_identical`, plus `tests/test_experiment_pipeline.py::test_reruns_are_deterministic` (byte-identical metrics and trade files) |

## Library facts that shaped the design

- **Leading-NaN warm-up skip.** `Backtest.run` skips every bar before all `self.I()` indicators are
  non-NaN. The lab therefore passes features as data columns and controls warm-up explicitly
  (`warmup_sessions`), so scored windows are never silently shortened.
- **Sharpe.** The library's "Sharpe Ratio" divides a geometric annualized return by a non-standard
  annualized volatility. The lab computes its own from session-close equity (mean/sd × √252) and stores
  the library's figure in `metrics.json` only.
- **Spread.** The library's `spread` is charged once, at entry. The lab uses a per-share commission
  hook instead, so both sides are charged symmetrically.
- **Integer shares.** Fractional shares are unsupported. At $100k on SPY that is fine (the rounding cost
  is under 0.6% of notional).

## Unavoidable bar-resolution ambiguity

Execution is on 1-minute OHLC. Inside a minute the path is unknown, so:

1. A stop and a target touched in the same minute resolve as the stop, even when the minute opens beyond the target (row 23), so the bias is pessimistic. The count is reported per run ("Stop/target same-minute exits").
2. A stop is assumed fillable at its price unless the minute opens beyond it. Real fills in fast
   markets can be worse. The per-share slippage allowance is the only proxy.
3. Isolated bad prints in the 1-minute data can trigger stops (see the integrity mask note in
   `studies/vwap-ema9-2026-10/manifests/VWR_FAMILY_PROPOSAL_v0.1.md`).

## NautilusTrader fallback — not triggered

Nothing required by the current studies is impossible or inaccurate in Backtesting.py. Known limits,
which matter only for later work:

- One instrument per `Backtest`, and no shared capital pool across strategies. Multi-strategy portfolios
  (explicitly out of scope for the first release) would need a portfolio layer or NautilusTrader.
- No bid/ask or tick data and no order latency model. Quote-level realism would need NautilusTrader
  plus quote data.
- No native partial fills or order-book liquidity.

Migration should be proposed only after one of these blocks a specific, authorized experiment, and
the limitation should be demonstrated with a failing test first.
