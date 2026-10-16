# VMR-L — VWAP mean reversion (lab) · proposal v0.1 · 2026-10-16

**Status: PROPOSED — awaiting the strategy-definition review. No real-data run has been made.** The
machine form, [`VMRL_EXPERIMENT_v0.1.toml`](VMRL_EXPERIMENT_v0.1.toml), refuses real data until it is
frozen. Code: `src/stratlab/strategies/vwap_mean_reversion.py` and `src/stratlab/volatility.py`. Tests:
`tests/test_mean_reversion.py` (synthetic).

## Research card

| Field | Content |
|---|---|
| **Family** | VWAP mean reversion: displacement from VWAP, then failed extension, then movement back toward VWAP |
| **Source / date** | Lab hypothesis group (roadmap 2026-10-16). Reference: the parked August VMR design (`studies/vwap-lab-2026-08/manifests/VMR_CHARTER_v0.1.md`). Its displacement metric is reused as a definition; its threshold, reversal candle, ATR stop and fixed-share sizing are **not** revived. |
| **Stated rules vs assumptions** | No external source. Every rule below is a lab choice, declared before any outcome. |
| **Observation** | On many sessions SPY stretches far from session VWAP, stalls, and drifts back. The same picture also appears on trend days, where price never comes back. |
| **Proposed mechanism** | A large, fast displacement from the day's volume-weighted fair price exhausts the order flow that caused it. Liquidity providers and value buyers or sellers lean against it. Once a bar fails to extend further, the imbalance has stopped growing, and price reverts part or all of the way to VWAP. |
| **Competing explanation** | (1) **Trend days:** VWAP lags a persistent move, so a large displacement *is* the trend. A failed-extension bar is an ordinary pause, and "reversion" happens because VWAP catches up over time, not because price returns. (2) **Volatility scaling:** E divides by a 5-minute ATR, so quiet sessions produce large E from modest moves. (3) **Shock versus structure:** a brief news fan-out may revert while sustained directional structure does not. MR3 tests this split directly. |
| **Measurable hypothesis** | MR0's per-trade expectancy, in R net of costs, is positive. Also, MR0 does not trail the session-hold benchmark on daily-equity Sharpe over the same window and costs. |
| **Primary comparison** | Expectancy R (net) with t-stat. Δ expectancy R for each variant against MR0. Daily-equity Sharpe as the portfolio view, reported separately. |
| **Status** | PROPOSED |
| **Linked results** | none |
| **Conclusion / next question** | (after the run) |

### Distinguishing terms used here

| Term | Meaning in this family |
|---|---|
| **Distance from VWAP** | `E = (close − VWAP) / ATR14`, in units of the current 5-minute ATR. Price-scale free. |
| **EMA separation / expansion** | Not used by VMR-L. Measuring EMA fan-out is a separate question (continuation and reversal families). VMR-L is deliberately defined without EMAs, so its results cannot be confused with EMA effects. |
| **Persistence** | How long the displacement has lasted. MR3 measures it as the minimum \|E\| over the up-to-6 in-session bars before the extended bar (fewer early in the session). |
| **Shock versus sustained structure** | A shock arrives quickly from near VWAP: some bar among the up-to-6 in-session bars before the extended bar had \|E\| < 1. Sustained structure has been far from VWAP the whole time. |

## Baseline MR0 (5-minute signal bars, 1-minute execution; shorts mirror longs)

Decided on completed bar *t*:

1. **Extension:** E_{t−1} ≤ −K. The previous bar closed at least K ATRs below VWAP. **K = 4.0.**
2. **Failed extension:** low_t > low_{t−1} **and** close_t > close_{t−1}. The bar made no new low and
   closed back toward VWAP.
3. **Entry window:** the bar ends between 10:00 and 15:00 ET. This avoids the unstable first 30 minutes
   (VWAP has little history) and the last hour.
4. **Stop:** min(low_{t−1}, low_t) − $0.01, at least 5 bps below close_t. A new extreme refutes the
   failed-extension thesis.
5. **Exit:** the first later signal bar (complete or not) that closes at or through VWAP, filled at the
   next minute's open; or the stop; or the session flatten (5 minutes before the calendar close).
6. Fills at the next 1-minute open. One position at a time, with **no cooldown**: after any exit, a new
   entry may be taken on the next qualifying bar, including on the same displacement. No new entry on a
   signal bar with missing minutes. Stops and targets are rounded to $0.01.

**Where K = 4.0 comes from (trade-blind):** \|E\| over in-window 5-minute bars has a P90 of 3.93 (August
corpus, masked) and 3.94 (fresh capture), and a P95 of 4.83 on both. About 9.5% of bars reach \|E\| ≥ 4.0
(`analysis/EXCURSION_QUANTILES_2026-10-16.json.txt`; no strategy, no P&L). K is a round number near P90,
fixed before any outcome. The quantiles were computed on the **same scored population** that the run
will score, so K is trade-blind but not out-of-sample. The August design's K = 4.09 was a P90 on its development window; it is noted
for reference, not adopted.

## Variants — one factor each, entry/context and exit kept separate

| ID | Group | Rule difference from MR0 | Question | Uninformative if |
|---|---|---|---|---|
| **MR1** | entry | Enter on the extended bar itself (E_t ≤ −K); no failed-extension confirmation. Stop beyond that bar's extreme. | Does waiting for a failed extension improve outcomes, or does it just enter later? | Fewer than 100 trades differ from MR0 |
| **MR2** | entry | **K = 5.0** (about P96) instead of 4.0 | Does a more extreme displacement revert more reliably? | MR2 has fewer than 100 closed trades |
| **MR3** | context | Shock filter: some bar among the up-to-6 in-session bars before the extended bar had \|E\| < 1.0 | Does reversion work after a quick shock but not after sustained structure? (the competing explanation) | MR3 has fewer than 100 closed trades, or fewer than 100 trades differ from MR0 |
| **MR4** | exit | Fixed target halfway from close_t to VWAP_t, placed at entry; no VWAP-close exit | Is a partial-reversion target better than waiting for a full return to VWAP? | Same-minute stop/target exits exceed 5% of MR4 trades |
| **BENCH** | benchmark | SPY session-hold (`stratlab.strategies.benchmarks:SessionHold`) | Reference only, not a trial | — |

**What this batch cannot test.** Competing explanation (3), shock versus sustained structure, is tested
by MR3. Explanation (1), trend days, is touched only indirectly by MR3. Explanation (2), ATR-denominator
scaling, has **no variant**. The trade files do not store ATR or E at the signal, and adding them would
mean an engine change, so (1) and (2) are **not tested** by this experiment. A post-run diagnostic
(expectancy R by ATR-at-signal tercile, with features recomputed from each trade's signal bar) may be
added after the run as **description only**, never as a rule change.

No combinations, no threshold search, no time-of-day or long/short selection, and no rescue variants after
the results. Trials planned: 5 (MR0–MR4).

## Data, execution, costs, sizing (to be confirmed at review)

| Item | Proposal |
|---|---|
| Data | **Review decision.** (a) The fresh capture `spy-1m-polygon-20241016-20261015-cap20261016-729dc4e9`, 2024-10-16 → 2026-10-15 (scored from 2024-10-23 after 5 warm-up sessions), unmasked. It is the most recent, and its bars are byte-identical to the August corpus over the overlap. Mask v1.0 is bound to the August file, and its prints are only partly corroborated by an independent source (`docs/lab/DATA_QUALITY_2026-10-16.md`). (b) The August corpus with mask v1.0, for consistency with VWR. **Recommended: (a).** The independent-hourly diagnostic would be pre-committed as a post-run check, and its affected-trade count reported. |
| Prior exposure | No mean-reversion configuration has ever been run on either dataset. The data was explored for VWAP/EMA continuation (August, and VWR in October), and the August VMR study profiled the \|E\| distribution trade-blind. So results are exploratory, and nothing here is a holdout. |
| Execution | Backtesting.py 0.6.6 on 1-minute RTH bars, XNYS calendar, as for VWR (`docs/lab/ENGINE_BEHAVIOR.md`) |
| Costs | $0.0035 commission + $0.01 slippage per share per side ($0.0135/share/side) |
| Sizing | $100,000; 99.9% of equity notional per trade; one position |
| Windows | Full scored history, calendar halves, latest 6 months (exploratory); fresh capital per window; warm-up 5 sessions |
| Primary metric | Expectancy R (net) with t-stat; daily-equity Sharpe and return as the portfolio view; trade R and portfolio results are reported separately |

## Reuse note

VMR-L needed a strategy module, one new indicator module (`volatility.py`: Wilder ATR, which matches the
August implementation to 1e-9 on the original corpus) and a config. There were **no changes** to the
engine, runner, metrics, windows or report. The synthetic end-to-end test
(`tests/test_mean_reversion.py::test_runs_through_existing_runner_and_report`) runs it through the
unchanged runner and report.
