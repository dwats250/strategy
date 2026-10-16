# V0 (EMA 9/20) tear sheet — EMA 9/20

Primary view **screened** (frozen CORPUS_MASK_v1.0); raw is sensitivity. Local development window; corpus/mask unaltered. Not TV-equivalent (split-only vs ADJ feed seam).

## Headline (screened | raw | Δ screened−raw)
| metric | screened | raw | Δ |
|---|---|---|---|
| n | 1354 | 1363 | -9 |
| net_pnl | -86.6386 | -111.6136 | 24.9750 |
| expectancy | -0.0640 | -0.0819 | 0.0179 |
| median_pnl | -0.4200 | -0.4300 | 0.0100 |
| win_rate_pct | 21.7134 | 21.3500 | 0.3634 |
| profit_factor | 0.8855 | 0.8551 | 0.0303 |
| payoff_ratio | 3.1865 | 3.1443 | 0.0422 |
| avg_bars_held | 12.6152 | 12.5018 | 0.1134 |
| max_drawdown | 131.9844 | 143.9365 | -11.9521 |

long/short (screened): long n=701 net=31.0515 PF=1.092522 | short n=653 net=-117.6901 PF=0.720403

## R-normalized (screened; 1R = frozen initial stop distance)
total_r=12.1866 mean_r=0.009 median_r=-0.841052 avg_winner_r=2.986633 avg_loser_r=-0.818415 stdev_r=2.001935

## Outlier concentration (screened) — robustness diagnostic only
(% of gross profit 669.9) best 1: 44.81 (6.6891%) · best 5: 102.935 (15.3657%) · best 10: 147.0618 (21.9528%) · top 1%: 175.2126 (26.155%)
net excl best 1/5/10: -131.4486 / -189.5736 / -233.7004

## Uncertainty (screened) — bootstrap CI of mean expectancy
mean=-0.063987 · IID 95% CI [-0.176498, 0.056218] (**PROVISIONAL — IID resampling ignores possible serial dependence in trade outcomes**) · block(L=11) 95% CI [-0.210546, 0.071518]

## Portfolio (screened) — trade-based
Sharpe/trade=-0.029938 Sortino/trade=-0.066307 · annualized -0.956984/-2.119538 (tpy=1021.79, assumption-dependent)
CAGR / Calmar: **DEFERRED** (account-construction-dependent).

## Consistency (screened)
months=16 · profitable months 5/16 (31.25%) · max win streak 5 · max loss streak 28
