# VWR0-EXP findings — seam 2 (2026-10-16)

**Runs:** `VWR0-EXP__20261016T211249Z` and `VWR0-RAW__20261016T211405Z`, each run once from the frozen
v1.1 configs, at commit `1f4af3a` with a clean tree. The code-tree hash `393e0ab9…` matches the pin.
**Data:** `a4afaa70…`, mask v1.0 (the raw run unmasked). **The data ends 2026-08-21.** Every statement below
describes SPY history up to that date and is **exploratory**: this corpus was explored for VWAP/EMA ideas
in August, and nothing here is a holdout.

**Reconciliation:** `reconcile_run.py` passed 56/56 configuration-window checks:
- equity equals trades to the cent;
- every trade paid exactly 2 × shares × $0.0135;
- every trade satisfies shares = floor(0.999 × equity ÷ (fill + cost));
- nothing was held overnight, and every exit came at or before the flatten minute;
- the calendar halves partition the full window exactly;
- the variant diffs and ledger rows reconcile.

**Determinism:** a non-exported rerun of the frozen config (no ledger row; it is not a second scored run)
matched all 99 output files byte for byte (`DETERMINISM_CHECK_VWR0-EXP_2026-10-16.txt`).

## Suspicious prints found after the run — unresolved (read first; amended 2026-10-16, see addendum)

On **2025-04-23**, from about 11:28 ET onward, over a hundred RTH minutes carry highs at **$544–545**
while their bodies trade at $534–539 and the vendor per-minute VWAP stays at the body. The pattern is
consistent with late-reported prints at the morning's price level. Whether a resting stop could have
filled there is **unknown**: an independent hourly source lacks these prints, but no condition-coded tick
data is available (`docs/lab/DATA_QUALITY_2026-10-16.md`). The frozen mask v1.0 is an isolated-spike rule and does not catch a cluster.
A trade-blind scan (`diagnose_offmarket_wicks.py`) flags 122 such minutes in the corpus: 111 on
2025-04-23 and 11 spread over 9 other sessions.

Shorts entered that afternoon were stopped repeatedly at those prices. The signal-bar stops were also
widened by the same wicks. Exposure by configuration, from the run's own trade files, with nothing
re-run (`DIAGNOSTIC_offmarket_wicks_VWR0-EXP_2026-10-16.txt`):

| Configuration | Total net | P&L on 2025-04-23 | Total excluding that session | Mean R excluding it |
|---|---|---|---|---|
| VWR0 | −$25,320 | −$13,998 | −$11,322 | −0.032 (t −0.92) |
| VWR1 | −$27,748 | −$13,367 | −$14,381 | −0.039 (t −1.42) |
| VWR2 | −$6,126 | −$496 | −$5,630 | −0.011 (t −0.17) |
| VWR3 | −$27,961 | −$8,125 | −$19,836 | −0.066 (t −2.00) |
| VWR4 | −$18,506 | −$1,838 | −$16,667 | −0.037 (t −0.80) |
| IG-AUSTIN-P0 | −$4,934 | −$798 | −$4,135 | −0.017 (t −0.30) |
| Session-hold benchmark | +$13,399 | −$626 | +$14,025 | — |

**What it changes:** the **size** of the VWR0, VWR1 and VWR3 losses, which are roughly doubled, or
inflated by about 40% for VWR3, by one suspect session. **What it does not change:** every
configuration's **sign**, and its standing below the benchmark. The frozen results stand as recorded.
Excluding a session is a diagnostic here, not a replacement result. Any corrected treatment needs your
decision; see the end.

## Headline (full scored window 2024-09-10 → 2026-08-21, 489 sessions, $100k, 1× notional, as frozen)

| Configuration | Trades | Total return | Sharpe (daily, ann.) | Max DD (session close) | Expectancy R (net) | t (mean R) | Win rate | Gross before costs | Costs |
|---|---|---|---|---|---|---|---|---|---|
| **VWR0** baseline | 2,428 | −25.3% | −1.01 | −28.2% | −0.038 | −1.10 | 28.7% | −$16,532 | $8,788 |
| VWR1 no EMA9 confirm | 3,318 | −27.7% | −1.14 | −30.9% | −0.044 | −1.59 | 31.7% | −$15,818 | $11,930 |
| VWR2 EMA/VWAP cross | 932 | −6.1% | −0.69 | −8.1% | −0.013 | −0.20 | 29.8% | −$2,308 | $3,817 |
| VWR3 signal-close 2R | 1,746 | −28.0% | −1.21 | −32.4% | −0.071 | −2.16 | 33.3% | −$21,721 | $6,240 |
| VWR4 morning only | 1,380 | −18.5% | −1.46 | −20.2% | −0.041 | −0.88 | 28.0% | −$13,362 | $5,144 |
| VWR0-RAW (no mask) | 2,432 | −26.6% | −1.07 | −29.5% | −0.045 | −1.33 | 28.7% | −$17,906 | $8,690 |
| IG-AUSTIN-P0 (independent) | 1,274 | −4.9% | −0.53 | −7.4% | −0.020 | −0.36 | 29.4% | +$355 | $5,289 |
| SPY session-hold (benchmark) | 489 | **+13.4%** | **+0.54** | −9.2% | — | — | 53.8% | +$15,619 | $2,219 |

The illustrative chance-maximum Sharpe (about 1.00 for 7 independent zero-skill trials) does not come into
play, because every trial's Sharpe is negative.

## Findings

- **Suspicious prints, unresolved (amended 2026-10-16):** on 2025-04-23, over a hundred minutes carry
  highs at $544–545 above $534–539 bodies. An independent hourly source does not show them, and mask v1.0
  does not catch them. Their executability is unknown. That session booked −$14.0k of VWR0's −$25.3k,
  −$13.4k of VWR1's and −$8.1k of VWR3's. Stop fills not supported by the independent source total −$13.2k
  for VWR0 (`docs/lab/DATA_QUALITY_2026-10-16.md`). Session P&L is not a corrected result; excluding the
  session changes loss sizes, not signs. The frozen numbers stand; the data treatment is your decision.
- None of the seven trials (the VWR family, the raw rerun, IG-AUSTIN-P0) made money on SPY from 2024-09-10
  to 2026-08-21 after costs. All of them finished below the SPY session-hold benchmark (+13.4%, Sharpe
  0.54) under identical capital, costs and session hours. This holds as frozen, and it also holds with the
  suspect session 2025-04-23 excluded. The results are negative and exploratory, and no rescue variant
  has been run.
- **VWR0** (hypothesis: a same-bar VWAP touch-proxy reclaim with EMA9 confirmation precedes continuation)
  is **not supported**: −0.038R per trade (t −1.10; −0.032R, t −0.92, excluding 2025-04-23), −25.3% account
  return and Sharpe −1.01. Gross P&L was negative even before $8.8k of costs. The gate is met (2,428 trades,
  at least 200 required), so this is an informative negative.
- **VWR1** (hypothesis: EMA9 confirmation adds nothing). The gate is met: 1,402 trades differ (1,146 added,
  256 removed, 0 altered), and the t-stats are −1.10 and −1.59, so the "both below 1" clause does not
  apply. Δ expectancy is −0.006R, with the added trades averaging −0.064R. **The evidence cannot separate
  the arms.** Confirmation was not shown to add or subtract meaningful value, and both arms lose.
- **VWR2** (hypothesis: the touch proxy is a better entry event than the EMA/VWAP cross). The gate is met
  (932 and 2,428 trades). **Not supported:** the cross lost less, −0.013R against −0.038R and −6.1% against
  −25.3%. Most of the dollar difference comes from trading less (15% of minutes in the market against 38%).
  Its own expectancy is indistinguishable from zero (t −0.20) and negative after costs. Only 135 trades are
  shared with VWR0.
- **VWR3** (hypothesis: with the same stop, the EMA9 exit beats a fixed signal-close 2R target). The gate is
  met: 1 same-minute stop/target exit in 1,746 (0.06%), and 5.3% exited at the flatten. The result is
  **directionally consistent** with the hypothesis: the 2R arm was worse at −0.071R (t −2.16) against
  −0.038R, and on the 1,601 shared entries the 2R exit averaged 0.069R worse (paired t −1.91, not
  conventionally significant). The target raises the win rate (33.3% against 28.7%), but 1,127 stop exits
  against 526 target exits leave expectancy lower. Actual reward/risk at the fill was close to nominal (p10
  1.91, median 2.00, p90 2.09). This says the target exit is no improvement; it does not say the EMA exit
  has an edge.
- **VWR4** (hypothesis: any effect is concentrated in the morning). The gate is met (1,380 trades). **Not
  supported:** Δ expectancy is −0.003R, the Sharpe was −1.46 against −1.01, and the account return was −18.5%.
- **IG-AUSTIN-P0** (hypothesis: the stated setup, executed mechanically on SPY shares, is positive after
  costs). The gate is met (1,274 trades). **Not supported:** −0.020R per trade (t −0.36), −4.9% (Sharpe
  −0.53). Gross P&L before costs was about flat (+$355), and $5.3k of costs made it a loss. This is evidence
  about the provisional, underlying-only, completed-bar reading of the setup on SPY. It says nothing about
  the creator's options results.
- **VWR0-RAW** (mask sensitivity, descriptive only): −26.6% (−0.045R) against −25.3% (−0.038R) masked. Raw
  has 2,432 trades against 2,428 (+4) and 892 stop exits against 890 (+2). The differences sit in the
  2024H2, 2025H1 and 2025H2 windows, where the masked prints were (one extra raw trade in 2025H2, +$1.16).
  2026H1, 2026H2 and the recent window are identical. Mask v1.0 is therefore not material. The bigger data
  issue is the unmasked cluster on 2025-04-23 described above.
- **Portfolio and per-trade views, under 1× notional sizing.** Money at risk to the stop ranged from 0.05%
  (p10) to 0.26% (p90) of equity per trade (VWR0). As frozen, VWR0's dollar-weighted R (−0.083) was about
  twice its per-trade mean (−0.038). **Most of that gap comes from the suspect 2025-04-23 session**: wick-widened stops put
  more money at risk on exactly the trades that were stopped. Excluding that session, they are −0.039 and
  −0.032. The gap persists for VWR3 (−0.089 against −0.066) and VWR4 (−0.092 against −0.037). There, the
  widest-stop quartile of trades carries most of the dollar loss. This is a diagnostic of the approved
  sizing, not a reason to change it here.
- **Time stability.** VWR0 was roughly flat to slightly positive in 2024H2 (+0.9%), 2025H2 (+0.4%) and
  the partial 2026H2 (+1.2%). It lost 20.2% in 2025H1, of which −17.5% came in April 2025: the tariff shock
  plus the suspect 2025-04-23 session. It lost 8.8% in 2026H1. The latest six months (2026-02-23 → 2026-08-21;
  exploratory, overlapping) were negative at −5.6%, Sharpe −1.73, −0.029R. **No evidence that recent
  behaviour favours this family.** VWR4's positive recent expectancy (+0.059R, t 0.53) is a noise-level
  subset result and is not a finding.
- **Direction asymmetry repeats.** VWR0 longs averaged +0.030R and shorts −0.108R, while SPY rose 39.6%
  from the first scored open to the last close. This is the same asymmetry the August study saw. It is
  reported, not selected; a long-only arm was not pre-registered and has not been run.
- **Fragility (diagnostic only).** Because results are negative throughout, winner removal only deepens
  the losses. VWR0's top 5 trades made about 10% of its gross profit, and removing them takes net P&L to
  −$38.6k.

## What this does not show

- It does not show whether VWAP/EMA9 ideas work on other instruments, timeframes, sizing schemes or
  periods. It does not show results after 2026-08-21, and it says nothing about the creator's options
  trading.
- It is not a holdout test. Nothing on this corpus can be one for VWAP/EMA ideas.
- Unregistered rules (long-only, risk-based sizing, trend filters, other targets) have not been run.
  Proposing them now would be post-hoc and would need a new, authorized, frozen design.

## Decision for Dustin (not acted on)

Whether to adopt a **trade-blind integrity mask v2**: for example, the rule in
`diagnose_offmarket_wicks.py`, which drops or caps minutes whose wick goes beyond the body while the vendor
VWAP stays at the body. It would be frozen as a new versioned data treatment, and VWR0-EXP would be re-run
under it as a new, separately ledgered experiment counted as additional trials. The rule is trade-blind,
but it was written after seeing that one session hurt these strategies, so any rerun is exploratory data
hygiene, not a rescue. The frozen results above stand either way.

## Outstanding (non-blocking)

- A fresh-data download. It needs `MASSIVE_API_KEY` and would get a new dataset id.
- An off-device backup of `~/.local/share/stratlab/`.

## Addendum — 2026-10-16 (closeout review)

An independent review found that this note stated as fact what `docs/lab/DATA_QUALITY_2026-10-16.md`
leaves unresolved. The wording above was corrected in place; no number changed. The original wording, kept
for the record:

> ## Data-integrity defect found after the run (read first)
>
> On **2025-04-23**, from about 11:28 ET onward, over a hundred RTH minutes carry highs at **$544–545** while their bodies trade at $534–539 and the vendor per-minute VWAP stays at the body. The pattern is most consistent with late-reported prints at the morning's price level. A resting stop could not have filled there at midday. The frozen mask v1.0 is an isolated-spike rule and does not catch a cluster. A trade-blind scan (`diagnose_offmarket_wicks.py`) flags 122 such minutes in the corpus: 111 on

> - **Data defect, found after the run:** on 2025-04-23, over a hundred minutes carry off-market highs at $544–545 above $534–539 bodies, which mask v1.0 does not catch. Shorts were stopped at those prints. The defect accounts for −$14.0k of VWR0's −$25.3k, −$13.4k of VWR1's and −$8.1k of VWR3's. Excluding that session changes loss sizes, not signs. The frozen numbers stand; a corrected mask is your decision.

Further evidence since this note was written:
- Yahoo Finance hourly bars (an independent source) do not show the midday $545 prints. Their morning
  highs match Massive's.
- Tick condition codes are not available on the current plan.
- Mask v1.0's own prints are only partly corroborated.
- Stop fills outside Yahoo's hourly range by more than $0.50 number 15 for VWR0 (recorded net P&L
  −$13,186) and 1–15 for the other configurations.

None of this makes the prints provably unexecutable, and subtracting their P&L is not equivalent to a
compounded rerun.

