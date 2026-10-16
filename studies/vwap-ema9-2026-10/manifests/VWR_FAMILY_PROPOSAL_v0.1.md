# VWR family proposal v0.1 — VWAP touch-and-reclaim baseline and four variants

**Status: PROPOSED.** Written 2026-10-16. **No real-data run of any configuration below has been
made.** After seam-1 review this is frozen as `VWR_FAMILY_v1.0.md`, with
[`VWR0_EXPERIMENT_v0.1.toml`](VWR0_EXPERIMENT_v0.1.toml) frozen as v1.0. Only then is the
experiment run, and it is run once.

VWR is a **lab-defined research strategy**. It is not the Instagram creator's strategy. The provisional
creator interpretation (IG-AUSTIN-P0, `SOURCE_RULES_IG_AUSTIN_v0.1.md`) runs alongside it as an
**independent** strategy under the same data, capital, costs and windows, and is never diffed as a VWR
variant.

## Common to every configuration

| Item | Definition |
|---|---|
| Data | `spy-1m-polygon-20240901-20260822-a4afaa70` (SHA-256 `a4afaa70…ed97a`, 422,657 rows), RTH only via the XNYS calendar. Integrity mask v1.0 applied (9 bars); see the data note below. |
| Execution bars | 1-minute. Signals use **completed** bars of the strategy's timeframe, anchored at the session open. |
| Fills | Market orders at the next 1-minute open. Stops and targets are evaluated on 1-minute OHLC from the entry minute onward. A minute opening beyond the stop fills at that open. Stop and target inside the same minute counts as the stop (pessimistic), and these exits are counted. |
| Session | Flat 5 minutes before the calendar close (15:55, or 12:55 on early closes). Nothing is held overnight. |
| Capital / sizing | $100,000. Each entry uses 99.9% of current equity as notional (no leverage). One position at a time. |
| Costs | $0.0035 commission + $0.01 slippage allowance per share per side, charged as cash ($0.0135/share/side). |
| Warm-up | The first 5 sessions (2024-09-03 → 2024-09-09) are never scored. EMA is continuous across sessions; VWAP resets daily. |
| Windows | Full scored history: 2024-09-10 → 2026-08-21 (489 sessions). Calendar halves 2024H2 (partial) → 2026H2 (partial). Latest six months: 2026-02-23 → 2026-08-21, exploratory. Every window is a separate fresh-capital run with identical settings. |
| Trials planned | 6 (VWR0–VWR4 plus IG-AUSTIN-P0). Implied chance-maximum Sharpe at N=6 and T=489 sessions is about 0.93 annualized (`metrics.expected_max_sharpe`). |

## VWR0 — baseline (5-minute bars)

Signal on completed 5m bar *t*. Shorts mirror longs exactly.

1. **Context:** close_t > VWAP_t. VWAP is session-anchored and uses the hlc3 source.
2. **Trigger (touch-and-reclaim):** low_t ≤ VWAP_t. The bar traded at or through VWAP and closed back above it.
3. **EMA9 confirmation:** close_t > EMA9_t.
4. **Entry window:** the bar ends between 09:45 and 15:30 ET, both inclusive.
5. **Initial stop:** min(low_t − $0.01, close_t × (1 − 5 bps)).
6. **Exit:** the first later completed 5m bar that closes below EMA9 (long), or the stop, or the session flatten.

## Variants — one factor each

| ID | Rule difference from VWR0 | Question | Expected mechanism | Primary comparison metric | Evidence is uninformative if… |
|---|---|---|---|---|---|
| **VWR1** | Drop rule 3 (no EMA9 confirmation) | Does EMA9 confirmation add anything beyond VWAP context plus touch? | More entries, many below EMA9, which then often exit on the next bar. If confirmation filters failed reclaims, VWR0's expectancy in R beats VWR1's. | Δ expectancy R (net) on matched dates, with the added-trade expectancy from the diff table | Fewer than 100 trades differ; or \|ΔR\| < 0.03 with t-stats under 1 for both |
| **VWR2** | Replace rule 2 with an **EMA9/VWAP cross** on bar *t*. Context, confirmation and exit are unchanged. | Is a precisely defined VWAP touch a better entry event than the EMA/VWAP cross (the event the creator uses)? | The cross fires later in a move and less often. A trend-continuation edge would favour the earlier touch; a confirmation edge would favour the cross. | Δ expectancy R; trade count; concentration (top-5 share) | Either arm has fewer than 100 trades; or the result reverses sign when the top 5 trades are removed |
| **VWR3** | Replace rule 6 with a **fixed 2R target**: target = close_t + 2 × (close_t − stop). No EMA exit. Same initial stop. | With the same initial risk, does an EMA9-managed exit beat a fixed 2R target? | The EMA exit cuts losers early and can ride trends. 2R caps winners and lets losers reach the full stop. | Δ expectancy R; win rate; average R of winners and losers; Sharpe | Same-minute stop/target ambiguity affects more than 5% of VWR3 exits; or the session flatten closes most 2R trades (target rarely reachable) |
| **VWR4** | Entry window **09:45–11:30** ET (bar end), instead of 09:45–15:30 | Is any VWAP-reclaim effect concentrated in the morning, when VWAP has the least history? | Morning sessions carry more range and volume. A morning-only arm removes the midday chop. | Δ expectancy R; Sharpe on the same capital (the time-restricted arm is idle more of the day) | The morning arm has fewer than 100 trades; or VWR0's morning subset (from the diff) is statistically indistinguishable from its afternoon subset |

**Independent reference: IG-AUSTIN-P0.** 3m bars, VWAP(ohlc4), completed EMA9/VWAP cross entry,
close-through-EMA9 exit and a signal-bar stop, as defined in `SOURCE_RULES_IG_AUSTIN_v0.1.md`. It is
reported alongside VWR under identical conditions and is not compared to VWR as a variant.

## Not run, by design

- No threshold tuning: the 5 bps stop floor, 2R, 09:45/15:30/11:30 and EMA length 9 are fixed up front.
- No combinations of variants, and no long-only or short-only arms. The August study already showed a
  long/short asymmetry on this corpus, so choosing a side now would be data-snooped. Direction splits
  are **reported** but not selected.
- No regime classifier.

## Prior exposure of this data (read before interpreting anything)

- The same SPY corpus was used in August for VWAP/EMA-based continuation research (VDC, FastAlpha
  EMA 9/20, and others): 18 development configurations and one validation look. The validation window
  (2026-01-06 → 2026-04-30) is consumed, and late-May → Aug 2026 sessions were inspected visually as a
  hypothesis source. **Nothing on this corpus is a holdout for VWAP/EMA ideas** (conventions §g).
  Every VWR result is exploratory.
- The latest-six-months window (2026-02-23 → 2026-08-21) overlaps the consumed validation window and
  the visually inspected sessions. It describes recent behaviour and is not an out-of-sample test.
- The data ends 2026-08-21, 56 days before this proposal. The creator's examples (Sep 28 and Oct 1,
  2026) are outside it. An October-current six-month window needs a new download, which is blocked on a
  credential (see `docs/lab/HANDOFF.md`).

## Data note — integrity mask

Mask v1.0 drops 9 RTH minutes whose high or low sits 0.6–2.2% away from an unchanged body: isolated
wick prints. On 1-minute stop evaluation, such prints would trigger stops that a resting order on a lit
venue probably would not have hit. Mask v1.0 is therefore applied. Two caveats:

- One masked bar (2024-12-20 11:10) carries 56× median volume with a vendor VWAP at the wick. It may be
  a real late-reported block.
- At least one similar unmasked wick exists (2025-05-27 13:14, low 585.39 against a body around 590,
  about 0.8%).

**Proposed robustness check, not a variant:** rerun VWR0 on the raw corpus and report the difference.
