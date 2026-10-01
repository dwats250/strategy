# PAPER_TRADES — prospective setups and decision-quality ledger

**Canonical location:** `dwats250/strategy/exploratory/portfolio-strategy-collab-2026/PAPER_TRADES.md`
**Opened:** Round 5 — Claude (Fable 5.1) · 2026-10-01 14:10 ET (11:10 PT)
**Purpose:** learn whether we form good observations, theses, setups, triggers, invalidations,
instrument choices and exits. Not a simulated brokerage. Results are reported in R (planned
risk = entry − invalidation), never in simulated dollars.

## Rules (binding)

1. **No hindsight.** A setup becomes a paper trade only if its plan below was written before the trigger fired. Every entry carries a timestamp. After activation the thesis, entry, invalidation, setup family and target logic are frozen; new information closes the record and opens a new one.
2. **Realism.** Every setup is one we could have taken with real capital in a Questrade TFSA with Level-2 options (long calls/puts only; no spreads).
3. **Option gate.** Premium ≤ C$150 (3%); ≥ 60 DTE at entry and ≥ 45 DTE after the expected holding period; bid–ask ≤ 10% of mid; OI ≥ 500 at the strike. Otherwise the vehicle is shares, or NO TRADE. Cheap far-OTM premium is not a loophole.
4. **Ladder:** OBSERVATION → WATCH → FULLY SPECIFIED → PAPER TRIGGER → PAPER TRADE → REPEATED OBSERVATIONS → MICRO-LIVE CANDIDATE → larger capital only after evidence. Paper results show executability, not edge.
5. **Grades:** A good decision/good result · B good decision/bad result · C bad decision/good result (a warning) · D bad/bad. Optimise for A + B.
6. **Market Brief** is read-only evidence; decisions live here.

## Ledger

| ID | Written | Symbol | Setup | Dir | Vehicle | Status | Thesis result | Grade |
|---|---|---|---|---|---|---|---|---|
| PT-001 | 2026-10-01 14:10 ET | ACN | A gap continuation | Long | Shares | WATCH | — | — |
| PT-002 | 2026-10-01 14:10 ET | VRT | E base breakout | Long | Shares | WATCH | — | — |
| PT-003 | 2026-10-01 14:10 ET | MU | B pullback continuation | Long | Shares (1) | WATCH | — | — |
| PT-004 | 2026-10-01 14:10 ET | FICO | C post-shock reversal | Long | Shares | WATCH | — | — |
| PT-005 | 2026-10-01 14:10 ET | SPY | D macro downside | Short | SH shares (paper: short SPY ref.) | WATCH | — | — |
| PT-006 | 2026-10-01 14:10 ET | TLT | Duration turn (Stage A) | Long | Shares, or Jan-27 82 call if gate passes | WATCH | — | — |
| PT-007 | 2026-10-01 14:10 ET | CBOE | E reclaim / tactical | Long | Shares | WATCH | — | — |
| PT-008 | 2026-10-01 14:10 ET | HWM | E base breakout | Long | Shares | WATCH | — | — |
| PT-009 | 2026-10-01 14:10 ET | ITB | Rates-turn equity (new) | Long | Shares | WATCH | — | — |
| PT-010 | 2026-10-01 14:10 ET | CLS | B pullback continuation (new) | Long | Shares (TSX) | WATCH | — | — |

Setup families: A post-earnings gap continuation · B pullback continuation in a leader ·
C post-shock mean reversion · D macro downside · E base breakout after a momentum break ·
F durable-hold dislocation entry (strategic; not paper-traded here). Definitions: `ROUNDS.md` Round 4 §B.

Regime/context common to all records (Oct 1, 2026): 10Y 5.29% (24-yr high); Fed 3.75–4.00%
after a Sep 16 hike; MOVE ~102–107 (record) vs VIX ~16.5; 21% of S&P 500 above 50-day, 40% above
200-day; XLK the only sector up in September; WTI ~$90; gold −25% from January record.

---

## Detailed records

### PT-001 — ACN · post-earnings gap continuation (A) · Long
- **Timestamp:** 2026-10-01 14:10 ET. ACN $217.12 (+18.4%), day range 214.50–227.63, volume 20.65M by 13:44 ET (~4× the September daily average of ~5.0M).
- **Observation:** Q4 FY26 beat (rev $18.7B vs $18.0B; EPS $3.29 vs $3.18), record $84.5B bookings, FY27 guide +3–6% LC. Stock had fallen 59% from its high to $118 and gapped +18% from $183.37.
- **Thesis:** institutions re-rate a 12.5x forward P/E, 10% FCF-yield business after a de-risking print; follow-through over 2–6 weeks toward the 200-day (196 → already above) and the pre-June gap zone ~$250–260.
- **Catalyst:** none further; the print is the catalyst. Baird $245 / Evercore $250 targets.
- **Confirmation required:** (1) day-1 (Oct 1) close ≥ 221.07 (upper half of the range); (2) no close below day-1 VWAP for two consecutive sessions through Oct 8.
- **Exact entry trigger:** first daily close > 227.63 on volume ≥ 1.5× the 20-day average, by Oct 15 (10 sessions). If (1) fails, the setup is **void**, not postponed.
- **Invalidation:** daily close < 214.50 (gap-day low).
- **Expected holding:** 20–40 sessions.
- **Exit logic:** half at 2R; trail the rest under the 20-day average on a close. R ≈ entry − 214.50 (≈ $13–14 at a $228 entry → 2R ≈ $255).
- **Time stop:** 40 sessions after entry.
- **Alternative explanation:** a one-day short-covering repricing in a business guiding +3–6%; consulting spend still soft; the Jun 18 −18% gap was on the same company.
- **Market Brief evidence:** none (single-name).
- **Vehicle:** shares (3 at ~$228 ≈ C$975; risk ≈ C$57). Options rejected: Dec 240 call 8.80/10.40 = C$1,370; Nov 240 call 5.00/6.20 = C$800 — both above the C$150 gate.

### PT-002 — VRT · base breakout after momentum break (E) · Long
- **Timestamp:** 2026-10-01 14:10 ET. VRT $247.41. 50-day 261.73, 200-day 264.14. Base: Sep 14 low 234.61 to Sep 25 high 253.46 (closes), 3 weeks.
- **Observation:** −35% from the $379.94 high; Sep 9 gap −9.6% on a valuation reset; FY26 guide raised across all metrics (sales $13.8–14.2B, EPS $6.65–6.75); UIG acquisition; forward P/E 30.8 for +36% FY27 EPS.
- **Thesis:** fundamentals intact + completed base → a reclaim of the 50-day resumes the primary uptrend toward the 61.8% retrace (~$324).
- **Catalyst:** Q3 earnings Oct 21 (inside the hold if triggered before).
- **Confirmation required:** weekly close > 257 (base high) **and** > the 50-day, on weekly volume ≥ 1.5× the 10-week average.
- **Exact entry trigger:** the Monday open after the qualifying weekly close. If not triggered by Oct 20, the setup is **suspended** through earnings and re-armed only on a new post-earnings base.
- **Invalidation:** daily close < 232.
- **Expected holding:** 4–12 weeks.
- **Exit logic:** half at 2R (R ≈ $30 → ~$322), trail the rest under the 20-day.
- **Time stop:** 60 sessions.
- **Alternative explanation:** AI-capex de-rating continues; the base is a pause before a lower leg (VST/CEG/GEV peers also below their averages).
- **Market Brief evidence:** none.
- **Vehicle:** shares (3–4; risk C$128–171 at 4 — use 3 to stay ≤ C$150). Options rejected: Dec 260 call 21.65/22.25 = C$3,170.

### PT-003 — MU · pullback continuation in a leader (B) · Long
- **Timestamp:** 2026-10-01 14:10 ET. MU $1,089 (+2.3% post-earnings). 50-day 953; 200-day 677; RSI 56; 52w range 165.50–1,255.
- **Observation:** FQ4 rev $54.2B vs $51.1B; FQ1 guide $61.5B vs $57B; GM ~86% "floor"; forward P/E 6.0. TrendForce: 4Q26 DRAM contract prices +10–15% q/q, moderating.
- **Thesis:** memory cycle still accelerating in HBM/enterprise; a controlled pullback to the 20/50-day is bought by institutions and the uptrend resumes toward the $1,255 high and beyond.
- **Catalyst:** none until December earnings; TrendForce monthly pricing.
- **Confirmation required:** pullback of ≥ 8% from the post-earnings high that touches the 20-day or 50-day on declining volume; no close below the 50-day.
- **Exact entry trigger:** first daily close above the prior day's high after the touch, with RSI(14) > 50.
- **Invalidation:** daily close below the pullback low.
- **Expected holding:** 3–8 weeks.
- **Exit logic:** half at 2R, trail under the 20-day.
- **Time stop:** 40 sessions.
- **Alternative explanation:** the print marked the cycle peak (pricing growth is decelerating); −14% from high already reflects distribution.
- **Vehicle:** 1 share reference (paper R-normalised; live would be C$1,550 = 31% notional with ~C$150 risk at a 10% stop). Options impossible (Dec 1100 call 94.85/99.40 = C$14,000).

### PT-004 — FICO · post-shock mean reversion (C) · Long
- **Timestamp:** 2026-10-01 14:10 ET. FICO $647.50 (+9.3%); Sep 29 −27% (worst day ever) to a $586.05 low; 50-day 1,039; 200-day 1,224; RSI 23.5.
- **Observation:** FHFA single pricing grid with VantageScore (Sep 28); Rocket switching Q4; BofA $700 / Barclays $935 / BMO $1,150 targets; Scores ≈ 68% of revenue, mortgage ≈ 42% of Scores (≈ 29% of revenue); Jefferies: EBITDA may fall ~20%.
- **Thesis:** the market has priced more than a 20–30% earnings impairment (−67% from high, ~15x stale EPS, ~20x impaired EPS vs a 40–60x history); once selling exhausts, a base forms and retraces part of the shock.
- **Catalyst:** Nov 4 earnings; any grid implementation date.
- **Confirmation required (all):** ≥ 10 consecutive sessions without a close below 586.05 (count from Sep 30); a close above the 20-day; a defined base high.
- **Exact entry trigger:** first daily close above the base high after the three conditions are met.
- **Invalidation:** daily close below the base low.
- **Expected holding:** 4–10 weeks.
- **Exit logic:** target the 50% retrace of the Sep 28–29 shock leg; half there, trail the rest under the 20-day.
- **Time stop:** 50 sessions.
- **Alternative explanation:** the regulatory erosion is just starting (implementation date, more lenders switching, $0.99 competitor pricing); negative equity and $5.6B debt amplify any earnings decline. A break of 586 is the downside-continuation signal — observe, do not trade (option markets $5–18 wide, OI < 50).
- **Vehicle:** shares (1 ≈ C$920; risk ≈ C$90 at a 10% stop).

### PT-005 — SPY · macro downside (D) · Short
- **Timestamp:** 2026-10-01 14:10 ET. SPY 763.45; 50-day ≈ 763; VIX 16.5; 10Y 5.29%.
- **Observation:** index ~2% from its high while 21% of members are above their 50-day (a configuration a breadth site says has appeared three times since 1927); 75% of S&P stocks fell in September; rates at 24-year highs; MOVE at records; leadership confined to tech.
- **Thesis:** when the index loses its 50-day with breadth this weak and rates this high, the following 2–6 weeks see a 5–8% decline as the few leaders catch down.
- **Catalyst:** FOMC Oct 27–28; earnings season from mid-October; Treasury refunding.
- **Confirmation required (≥ 3 of 5):** (1) daily close < 750 [mandatory]; (2) breadth < 25% above 50-day [met]; (3) 10Y at a weekly cycle high [met]; (4) VIX > 18; (5) RSP and IWM below their 200-day.
- **Exact entry trigger:** the first daily close < 750 while ≥ 3 conditions hold.
- **Invalidation:** daily close back above the 50-day average.
- **Expected holding:** 2–6 weeks.
- **Exit logic:** half at 2R (R ≈ 13 → ~724), rest at 3R or on the first weekly close above the 10-day.
- **Time stop:** 20 sessions.
- **Alternative explanation:** narrow leadership can persist for months (2023–24); a soft CPI or dovish FOMC squeezes a crowded under-positioning.
- **Market Brief evidence:** Sep 30 daily — "a 10Y at 24-year highs, a weak average stock, and little hedging demand" (market-review, truth-today read).
- **Vehicle:** paper reference = short SPY; live expression = SH shares (ProShares Short S&P 500, $32.30), ~30 shares ≈ C$1,380, risk ≈ C$60 at a 4.3% stop. **Options: NO TRADE** — Dec 740 put 11.89/11.93 = C$1,697; Dec 700 put = C$862; nothing under C$150 inside 10% of spot. The Round 4 720/700 spread is deleted (no Level 3).

### PT-006 — TLT · duration turn, Stage A (regime) · Long
- **Timestamp:** 2026-10-01 14:10 ET. TLT 77.99 (52w low 76.76); 20-day 81.70; 50-day 82.44; 200-day 85.52. 10Y 5.29%, 30Y 5.64%, 10Y real 2.93%, 10Y breakeven 2.36%, MOVE ~102–107.
- **Observation:** Q3's +85 bp in the 10Y was ~73 bp real yield; auctions mixed; Fed hiking; TLT IV rank ~96–100. Long duration is cheap on valuation but in a confirmed downtrend.
- **Thesis:** the first durable reversal in the 10Y trend, with breakevens stable, marks a tradable duration rally of 6–10% in TLT over 1–3 months as term premium compresses.
- **Catalyst:** FOMC Oct 27–28; Q4 refunding (early Nov); CPI Oct 14.
- **Confirmation required (all three):** (M1) 10Y weekly close below its 10-week average with that average no longer rising; (M2) TLT weekly close above its 50-day; (M3) 10Y breakeven ≤ 2.45% and not rising over four weeks. Plus one of: 30Y real yield ≥ 20 bp off its cycle high; MOVE < 95; 2Y ≥ 25 bp off its cycle high.
- **Exact entry trigger:** the Monday open after the qualifying weekly close.
- **Invalidation:** 10Y weekly close ≥ 40 bp above the trigger-week yield, or TLT daily close below the trigger-week low.
- **Expected holding:** 4–12 weeks.
- **Exit logic:** half at 2R; rest on a weekly close below the 20-day, or at the 200-day (85.5).
- **Time stop:** 60 sessions (shares) / 30 days before expiry (call).
- **Alternative explanation:** the move is fiscal/term-premium driven and continues after the Fed stops; Japan/Europe long ends keep selling; a bear-steepener regime (`WATCHLIST.md` §6).
- **Market Brief evidence:** rates block / Treasury par curve (market-review Sep 30).
- **Vehicle — two expressions, chosen at trigger:**
  - Shares: 10 TLT ≈ C$1,110; stop per invalidation (≈ 3–4% → risk ≈ C$40).
  - Long call, only if ≥ 90 DTE remain at trigger: **TLT Jan 15 2027 82 call** — read live Oct 1 ~14:00 ET: bid 1.05 / ask 1.07 / mid 1.06, IV 15.7%, OI 28,594, vol 827, 106 DTE, premium US$107 = **C$152**, thesis expiry Dec 15 (30 DTE). Delta not shown (est. ~0.25 from moneyness). Also read: Jan 80 call 1.70/1.71 (OI 67,473, C$243 — over budget); Jan 83 call 0.82/0.83 (OI 32,044, C$118); Dec 80 call 1.40/1.44 (C$205). Breakeven 83.06 (+6.5%); at TLT 86 (+10%) intrinsic 4.00 = 3.8× premium. Theta: ~1% of premium per day at 60 DTE. **Versus shares:** the call pays ~4× on a 10% move where 10 shares pay +US$78; it loses 100% on a correct-but-late thesis. Rule: the call only if the trigger fires by Oct 17 (≥ 90 DTE); after that, shares.

### PT-007 — CBOE · 50-day reclaim after a shakeout (E) · Long (tactical, separate from the strategic hold)
- **Timestamp:** 2026-10-01 14:10 ET. CBOE $279.35; fell 307.62 (Sep 1) → 253.26 (Sep 28) → 279 with no identified cause; 50-day 288.06; 200-day 286.85; earnings Oct 30.
- **Observation:** Q2 revenue +25%, EPS +45%, guidance raised; Aug index options ADV +29%; S&P/VIX licence to 2051 signed ~Sep 29; forward P/E 19.
- **Thesis:** the September slide was positioning, not fundamentals; a reclaim of the 50/200-day confirms the shakeout and sets up a run back to the 52w high ($371) area over 1–3 months.
- **Catalyst:** Oct 30 earnings; monthly volume releases (early each month).
- **Confirmation required:** daily close > 288 (50-day and 200-day) on volume ≥ 1.5× the 20-day average.
- **Exact entry trigger:** the next open after the qualifying close.
- **Invalidation:** daily close < 262 (below the Sep 30 close and the midpoint of the shakeout).
- **Expected holding:** 4–12 weeks.
- **Exit logic:** half at 2R (R ≈ 26 → ~$340), trail under the 20-day.
- **Time stop:** 60 sessions.
- **Alternative explanation:** the slide reflects something not yet public (a volume air-pocket, a competitive or regulatory item); exchanges de-rating with financials (XLF −1.1% on Sep 30).
- **Vehicle:** shares (3 ≈ C$1,230; risk ≈ C$110 at a $262 stop). Options rejected: Jan 2027 300 call 14.70/15.40, IV 39.6% = C$2,140.

### PT-008 — HWM · base breakout (E) · Long
- **Timestamp:** 2026-10-01 14:10 ET. HWM $227.84; range 224–233 since the Sep 1 drop from 254.89; 50-day 260.35; 200-day 248.16; forward P/E 38.8, FY27 EPS +21%; guidance raised Aug 6; earnings Oct 29.
- **Observation:** record aerospace backlogs, +28% commercial aero revenue, EBITDA margin 32%; stock −26% from high with no identified reason for the September drop.
- **Thesis:** quality aero-cycle leader in a tight base; a reclaim of the 200-day then the 50-day resumes the uptrend.
- **Confirmation required:** daily close > 248 (200-day) on ≥ 1.5× volume, then a weekly close > 260 (50-day).
- **Exact entry trigger:** the open after the daily close > 248; add nothing until the weekly close > 260.
- **Invalidation:** daily close < 222.
- **Expected holding:** 4–12 weeks.
- **Exit logic:** half at 2R (R ≈ 26 → ~$300), trail under the 20-day.
- **Time stop:** 60 sessions.
- **Alternative explanation:** 39x forward is the problem — the de-rating of expensive industrials (GE −20% from high on 37x) continues regardless of backlog.
- **Vehicle:** shares (4 ≈ C$1,300; risk ≈ C$148 at a $222 stop from a $248 entry).

### PT-009 — ITB · rates-turn equity expression (new, independent) · Long
- **Timestamp:** 2026-10-01 14:10 ET. ITB $85.59 (−1.6%); 52w range 84.83–115.26; trailing P/E 14.7; top holdings DHI 17.9%, PHM 11.2%, LEN 8.1%; 30-yr fixed mortgage 7.60% (MND, Sep 30); mortgage–Treasury spread ~231 bp.
- **Observation:** homebuilders sit 1% above a 52-week low at 14.7x trailing, −15% in three months, as mortgage rates made new cycle highs. Builders historically lead TLT out of a rates peak because the equity discount rate and the demand channel both turn at once.
- **Thesis:** when the 10Y trend turns (PT-006's M1) and mortgage rates roll over, ITB rallies 15–25% in 2–4 months from a washed-out base, with more beta than TLT and without duration's term-premium problem.
- **Catalyst:** FOMC Oct 27–28; builder earnings (LEN mid-Dec; DHI late Oct).
- **Confirmation required:** (1) PT-006's M1 condition met (10Y weekly close below its 10-week average); (2) 30-yr mortgage rate ≥ 25 bp below its cycle high (≤ 7.35% on MND); (3) ITB daily close above its 20-day average.
- **Exact entry trigger:** the open after all three hold.
- **Invalidation:** daily close < 84.00 (below the 52-week low).
- **Expected holding:** 6–16 weeks.
- **Exit logic:** half at 2R, trail under the 20-day; hard target the 200-day.
- **Time stop:** 80 sessions.
- **Alternative explanation:** affordability is broken at any plausible mortgage rate; builders' margins compress from incentives; a recession hits demand before rates help.
- **Market Brief evidence:** rates block (Treasury par curve); mortgage rate not covered by the brief — a candidate gap.
- **Vehicle:** shares (12 ≈ C$1,460; risk ≈ C$55 at an $84 stop from an $87 entry). **Options: NO TRADE** — the Jan 2027 chain carries non-standard strikes (84.51, 88.47, 90.46 …) from a distribution adjustment, OI mostly < 500, quotes inconsistent (read live Oct 1).

### PT-010 — CLS · pullback continuation in a leader (B, new independent) · Long
- **Timestamp:** 2026-10-01 14:10 ET. CLS US$376.47 (+4.2%) / TSX ~C$510; 50-day 328.40; 200-day 329.94; ATR ≈ 5.6%/day; earnings + Investor Day Oct 26.
- **Observation:** +27% in a month; Q2 revenue +62%, FY26 guide raised to $20.5B; FY27 consensus EPS +75%; AI-rack customers (Google, OpenAI); Bernstein/FBN initiations at Outperform; forward P/E 24.
- **Thesis:** the strongest Canadian-listed AI-infrastructure leader; the next orderly 8–12% pullback into the 20-day is bought and the trend resumes into the Investor Day.
- **Confirmation required:** a pullback of 8–12% from the swing high on declining volume that holds the 20-day; no close below the 50-day.
- **Exact entry trigger:** first daily close above the prior day's high after the pullback low, RSI(14) > 50. If the pullback coincides with the Oct 26 print, re-arm after it.
- **Invalidation:** daily close below the pullback low (or below the 50-day, whichever is nearer).
- **Expected holding:** 3–8 weeks.
- **Exit logic:** half at 2R, trail under the 20-day.
- **Time stop:** 40 sessions.
- **Alternative explanation:** customer concentration (two hyperscaler-class customers) and 5–10% daily swings make a "pullback" indistinguishable from the start of a 30% correction; CLS fell 50% in early 2025 on similar fundamentals.
- **Vehicle:** 2 TSX shares (≈ C$1,020; risk ≈ C$112 at a 2×ATR stop). CAD listing — no FX. Options not inspected (TSX options are C$0.99/contract; liquidity unverified).

---

## Observations not advanced to setups (recorded so they are not re-invented)

- **EWZ post-election** (Round 3): regime position; re-specify after Oct 4 / Oct 25 if desired.
- **QQQ downside:** correlated with PT-005; one index short at a time.
- **UNH Oct 13 reaction:** eligible for a Strategy A record if it gaps ≥ 8% on a beat/raise; write the record **before** the print, not after.
- **CME ≤ ~$225 (≈ 18x forward):** a Strategy F durable-hold trigger, not a paper trade (see `ROUNDS.md` Round 5).
- **U.UN / uranium:** SPUT discount < 5% trigger (`WATCHLIST.md` §5b).

## After-entry template (copy under the record when a trigger fires)

```
Entry timestamp: | Entry reference price: | Planned R (entry − invalidation):
MFE: | MAE: | Exit timestamp: | Exit reference price: | Exit reason:
Underlying directional result: | Option behaviour (if any):
Thesis: confirmed / invalidated / unresolved | Timing: good / early / late
Instrument choice: appropriate / poor | Risk plan: useful / inadequate
Process violation: yes / no | Grade: A / B / C / D | Primary lesson (one sentence):
```
