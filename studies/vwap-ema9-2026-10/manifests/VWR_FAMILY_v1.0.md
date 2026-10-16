# VWR family v1.0 — VWAP touch-and-reclaim baseline, four variants, raw-data rerun, benchmark

**Status: FROZEN** in the commit that adds this file, before any real-data run. This version supersedes
`VWR_FAMILY_PROPOSAL_v0.1.md`, which stays as the proposal record. The machine-readable twins are
[`VWR0_EXPERIMENT_v1.0.toml`](VWR0_EXPERIMENT_v1.0.toml) and
[`VWR0_RAW_ROBUSTNESS_v1.0.toml`](VWR0_RAW_ROBUSTNESS_v1.0.toml). Where wording differs, the TOMLs govern,
because they are what the runs record. Each is run **once**.

Owner decisions applied (2026-10-16, seam-1 review): VWR0 stays the simple same-bar baseline; the
variant batch, 1× notional sizing, $0.0135/share/side costs and mask v1.0 (primary, with the raw
rerun) are approved; and amendments 1–6 below. **No trend filter has been added.**

VWR is a **lab-defined research strategy**. It is not the Instagram creator's strategy.
IG-AUSTIN-P0 (`SOURCE_RULES_IG_AUSTIN_v1.0.md`) runs alongside it as an **independent** strategy, and
SPY-SESSION-HOLD runs as a **benchmark**. Neither is diffed as a VWR variant.

## Common to every configuration

| Item | Definition |
|---|---|
| Data | `spy-1m-polygon-20240901-20260822-a4afaa70` (SHA-256 `a4afaa70…ed97a`, 422,657 rows), RTH only via the XNYS calendar. Integrity mask v1.0 (9 one-minute bars) for every configuration except the raw rerun. **The data ends 2026-08-21.** No result is current to the run date. |
| Execution bars | 1-minute. Signals use **completed** bars of the strategy's timeframe, anchored at the session open. A signal bar missing any constituent minute produces no new entry, though exits are still evaluated on it. No EMA/VWAP cross is evaluated on a session's first signal bar. Backtesting.py never decides on a run's very first bar. |
| Fills | Market orders fill at the next 1-minute open. Stops and targets are checked on 1-minute OHLC from the entry minute onward. A minute that opens beyond the stop fills at that open. A stop and a target inside one minute resolve as the stop, even when the minute opened beyond the target (pessimistic); these exits are counted. |
| Session | Flat 5 minutes before the calendar close (15:55, or 12:55 on early closes). Nothing is held overnight. |
| Capital / sizing | $100,000. Every entry uses 99.9% of current equity as notional, with no leverage and one position at a time. Money at risk to the stop therefore varies trade by trade; the initial risk distribution is reported (amendment 3). |
| Costs | $0.0035 commission plus a $0.01 slippage allowance per share per side, charged as cash: $0.0135/share/side. |
| Warm-up | The first 5 sessions (2024-09-03 → 2024-09-09) are never scored. EMA runs continuously across sessions; VWAP resets daily. |
| Windows | Full scored history 2024-09-10 → 2026-08-21 (489 sessions); calendar halves 2024H2 (partial) through 2026H2 (partial); latest six months 2026-02-23 → 2026-08-21, **exploratory**. Every window is a separate fresh-capital run with identical settings. |
| Trials | **7** configurations: VWR0–VWR4, IG-AUSTIN-P0, and the VWR0 raw rerun. The benchmark is not a trial; nothing is selected from it. |
| Chance-max Sharpe (amendment 5) | About 1.00 annualized: the expected maximum Sharpe of **7 independent zero-skill trials** over 489 sessions. This is an **illustrative null approximation**. It is not a significance threshold and not a complete deflated Sharpe ratio. The configurations are strongly correlated (shared rules, overlapping trades), and this corpus was already explored for VWAP/EMA ideas in August, so the true selection effect is not captured by this number. |

## VWR0 — baseline (5-minute bars)

Signal on completed 5m bar *t*; shorts mirror longs exactly. **VWR0 does not require prior trend
establishment.** Price need not have been above VWAP, and EMA9 need not have been above VWAP, before
bar *t*. Everything is decided from bar *t* alone (amendment 1).

1. **Context:** close_t > VWAP_t. VWAP is session-anchored (hlc3), valued at the close of bar *t*.
2. **Touch proxy:** low_t ≤ VWAP_t. This is a **bar-level proxy**: it compares the bar's extreme with
   VWAP as of the bar's close, and does not prove that price met VWAP inside the bar, because VWAP moves
   during the bar.
3. **EMA9 confirmation:** close_t > EMA9_t.
4. **Entry window:** the bar ends between 09:45 and 15:30 ET, inclusive.
5. **Initial stop:** min(low_t − $0.01, close_t × (1 − 5 bps)).
6. **Exit:** the first later completed 5m bar that closes below EMA9 (long), or the stop, or the
   session flatten.

## Variants — one factor each

"Uninformative if" gates decide whether a comparison can say anything. **Winner-removal checks
(net P&L excluding the largest 1/5/10 trades, top-5 share of gross profit) are fragility diagnostics.**
They are reported for every configuration and are never used to invalidate a result (amendment 4).

| ID | Rule difference from VWR0 | Question | Expected mechanism | Primary comparison | Uninformative if |
|---|---|---|---|---|---|
| **VWR0** | — | Does a same-bar touch-proxy reclaim with EMA9 confirmation precede continuation? | Participants defend VWAP; a reclaim with momentum marks the defended side | Expectancy R (net) with t-stat; daily-equity Sharpe | Fewer than 200 closed trades in the full window |
| **VWR1** | Drop rule 3 (no EMA9 confirmation) | Does EMA9 confirmation add anything beyond context plus touch? | More entries, many below EMA9, which often exit on the next bar | Δ expectancy R vs VWR0; expectancy of added trades | Fewer than 100 trades differ from VWR0 (added + removed + altered); or \|Δ expectancy R\| < 0.03 and both \|t-stat\| < 1 |
| **VWR2** | Replace rule 2 with an EMA9/VWAP cross on bar *t* (EMA_{t−1} ≤ VWAP_{t−1}, EMA_t > VWAP_t); rules 1, 3–6 unchanged | Is the touch proxy a better entry event than the EMA/VWAP cross (the creator's event)? | The cross fires later in a move and less often | Δ expectancy R; trade count | Either arm has fewer than 100 closed trades |
| **VWR3** | Replace rule 6: exit at a **2R target placed from the signal close**, target = close_t + 2 × (close_t − stop), or at the stop or flatten; no EMA exit (amendment 2) | With the same stop, does an EMA9-managed exit beat a fixed signal-close 2R target? | The EMA exit cuts losers early and can ride trends; the target caps winners | Δ expectancy R; win rate; **actual** reward/risk at fill | Same-minute stop/target exits exceed 5% of VWR3 trades; or more than 50% of VWR3 trades exit at the session flatten |
| **VWR4** | Entry window 09:45–11:30 ET (bar end) | Is any effect concentrated in the morning? | Morning range and volume; midday chop removed | Δ expectancy R; Sharpe on the same capital | Fewer than 100 closed trades |
| **VWR0-RAW** | VWR0 on the corpus **without** mask v1.0 (separate TOML) | How much do the 9 masked wick prints matter at 1-minute stop resolution? | Masked wicks would trigger some stops | Δ expectancy R and Δ stop-exit count vs VWR0 | Descriptive only; never used to choose between masked and raw |

**Amendment 2: why the target is signal-close-based.** The order carries its stop and target when it
is placed, so Backtesting.py checks both from the entry minute onward (entry at the open, then the
rest of that minute). A target recomputed from the actual fill would have to be attached after the
fill. It would then miss entry-minute target hits while still catching entry-minute stops, a hidden
pessimistic bias. The lab therefore keeps the signal-close target, names it as such, and reports each
trade's **actual** initial reward/risk = side × (target − fill) / |fill − stop|. It differs from 2.0 by
the gap between the signal close and the fill.

## Independent strategy and benchmark

- **IG-AUSTIN-P0**: as frozen in `SOURCE_RULES_IG_AUSTIN_v1.0.md`. Uninformative if it has fewer than
  100 closed trades. It is always uninformative about the creator's options P&L (underlying-only
  proxy, later entry).
- **SPY-SESSION-HOLD** (amendment 6): every session, buy 99.9% of equity notional at the 09:31 open
  (09:32 on a run's first session; see the engine note) after the first completed minute, with no stop
  and no target. Sell at the calendar flatten (15:55 open; 12:55 on early closes). Same capital, same
  per-share costs, same windows. It shows what being long SPY during the same regular-session hours
  earned net of the same costs. It has no R multiple.

## Reporting (amendment 3)

Portfolio results use account equity sampled at each session close. Per-trade conclusions use R
multiples from the initial stop. The two are reported separately and never mixed. Initial account
risk per trade (shares × |fill − stop| ÷ equity before entry) is reported as a distribution for every
configuration, together with notional exposure and, for VWR3, actual reward/risk.

## Not run, by design

No threshold tuning, no combinations of variants, no long-only or short-only arms, no trend filter, no
regime classifier, and **no rescue variants after the results**.

## Prior exposure of this data

The August study used this corpus for VWAP/EMA continuation research. Its ledger has 19 development
rows; one (R1) is sealed and uninterpreted, so there were 18 interpreted development draws over 17
distinct configurations, plus one validation look on 2026-01-06 → 2026-04-30. Sessions from late May
to August 2026 were inspected visually. **Nothing on this corpus is a holdout for VWAP/EMA ideas**
(conventions §g), and every result here is exploratory. The latest-six-months window overlaps the
consumed validation window and the inspected sessions.

## Data note — integrity mask

Mask v1.0 drops 9 RTH minutes whose high or low sits about 0.6–2.3% from an unchanged body. Two caveats:
2024-12-20 11:10 may be a real late-reported block (56× median volume), and at least one similar
unmasked wick exists (2025-05-27 13:14). The raw rerun shows how much the choice matters.

---

### Amendment 2026-10-16 (before any real-data run) — runnable configs, rounding, exit evaluation

1. **Runnable configs are v1.1.** The v1.0 TOMLs were committed with `code_tree_sha256 = "PENDING"`, so
   they cannot run, and §b forbids editing them. `VWR0_EXPERIMENT_v1.1.toml` and
   `VWR0_RAW_ROBUSTNESS_v1.1.toml` are identical to v1.0 except for their headers and
   `code_tree_sha256 = 393e0ab99ff62733b1b50b2033a2368211bfb24a18ec1478cb767de9023f0550` (src/stratlab at
   commit 6d25dd1, after the pre-freeze review corrections). Only v1.1 is run.
2. **Rounding.** Initial stops are rounded to $0.01 after the formula is applied. The VWR3 target is
   computed from the rounded stop and then rounded to $0.01. A hand check against the unrounded formula
   can differ by up to half a cent.
3. **Exit evaluation.** "A later completed bar closes back through EMA9" means any later signal bar,
   **complete or not**. Only new entries skip bars with missing minutes; exits are still evaluated on them.

