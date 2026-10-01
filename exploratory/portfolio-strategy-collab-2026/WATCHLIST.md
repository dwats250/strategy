# Market Roster (WATCHLIST.md)

**What this file is:** the page to open on an ordinary trading day. It answers:
- what markets matter, and what each one is telling us;
- what businesses we care about;
- what setups are developing;
- what has gone stale;
- what would actually cause capital to move.

Research detail lives in `RESEARCH_MAP.md`, trade plans in `PAPER_TRADES.md`, history in `ROUNDS.md`.

**Version:** Round 10 — Claude (Opus 5.5) · values as of the **Oct 1, 2026 close** unless marked. This file replaced the Round 1–6 watchlist; that version's still-useful parts are in the archive at the bottom, and the full text is in git history (commit `f4757b7` and earlier).

**Reading order (≈ 5 minutes):**
1. Narrative — has anything below changed it?
2. Gauges.
3. Decision points due this week.
4. Tactical roster status.

---

## 1. Working narrative (update only when something meaningful changes)

*Last changed: 2026-10-01.*

- **Rates are the shock.** The 10Y closed at 5.29% on Sep 30, a 24-year high, and eased to 5.24% on Oct 1. The 30Y is at 5.60%. About 73 of the 10Y's 85 bp Q3 rise was real yield, not breakevens. The pressure is global: JGB 10Y 3.10%, French OATs at 2002 highs. Rate volatility is extreme (MOVE 108; +65% in 3 months).
- **The rate shock is transmitting through every price-sensitive channel except equity volatility:**
  - the dollar is at a 52-week high (DXY 102.0);
  - gold is −4% over a month and below both averages;
  - long-duration assets closed at 52-week lows on Oct 1 (TLT, IEF, LQD, HYG), and ITB printed a new 52-week low intraday;
  - high-yield spreads are widening from tight levels (HY OAS 3.12% on Sep 30, from 2.73% on Sep 23).
- **The headline index is held up by a narrow set of leaders and by mechanical positioning.**
  - SPY sits on its 50-day average, 1.8% from its high; QQQ is near its high.
  - Only **23% of S&P 500 members are above their 50-day** and 41% above their 200-day (thetrading.tools, Oct 1). RSP and IWM are 4–5% below their 50-day averages.
  - Volatility-control funds hold equities at the **98th percentile of exposure since 2010** (Deutsche Bank data via Reuters, Oct 1), bought because realised volatility is low.
  - Barclays estimates a bearish volatility shock could force **more than $100B** of selling; UBS estimates the downside selling would be roughly 5× the upside buying.
- **Energy is a separate geopolitical story.** WTI is at $93 and Brent at $102.5, up 35–43% in three months. US–Iran talks have stalled and Hormuz traffic is disrupted. Copper is firm ($6.57, above both averages), so industrial demand is not cracking.
- **The single transmission to watch: does rate volatility reach equity volatility?**
  - **If it does** (VIX above 20 with realised volatility rising), the vol-control deleveraging, the weak breadth and the narrow leadership all point the same way (Program G).
  - **If the long end turns first** (a 10Y weekly close below its 10-week average with breakevens contained), the duration and rate-sensitive watches activate instead (Program C).
  - **HY OAS ≥ 4%** would mean rate pressure has become credit stress. That triggers a review of every core thesis.

## 2. Market gauges (permanent; no expiry, no entry price)

Values are Oct 1 closes from Yahoo daily history. Yields are Cboe yield indices. The Treasury par curve shown is Sep 30, the latest official print.

| Group | Gauge | Oct 1 | vs 50d / 200d | 1m / 3m | What it tells us | Today's reading |
|---|---|---|---|---|---|---|
| **Equity regime** | SPY | 763.99 | 763.1 / 720.0 | +0.3% / +2.6% | Headline trend | At its 50-day, 1.8% off its high — resilient |
| | QQQ | 742.03 | 715.7 / 667.9 | +4.9% / +4.1% | Growth leadership | Leading, near its high |
| | RSP | 209.00 | 216.7 / 205.7 | −3.9% / −2.7% | The average stock | Below its 50-day: participation weak |
| | IWM | 279.02 | 292.8 / 276.2 | −4.0% / −6.2% | Liquidity and growth breadth | Below its 50-day, on its 200-day: small caps not confirming |
| | S&P % above 50d / 200d | 23.0% / 40.9% | — | — | Breadth under the index | WEAK (thetrading.tools, Oct 1) |
| **Rates** | US 2Y | 4.88% (Sep 30) | — | +74 bp in Q3 | Policy expectations | Pricing more hikes (Fed 3.75–4.00% after the Sep 16 hike) |
| | US 10Y | 5.24% | 4.82% / 4.44% | — | Discount rate, real yield | 24-year-high zone; real yield 2.93% (Sep 30) |
| | US 30Y | 5.60% | 5.29% / 5.00% | — | Term premium / fiscal | Mid-5s |
| | 2s10s / 5s30s | 41 bp (Sep 30) / ~59 bp (Oct 1) | — | — | Curve shape | Bear-steepening |
| | TLT / IEF | 77.71 / 89.30 | 81.8 / 85.5 · 92.1 / 94.5 | −5.1% / −9.1% · −3.0% / −5.1% | Duration trend | Both closed at **52-week lows**: downtrend intact |
| **Credit** | HYG / LQD | 76.90 / 102.03 | 79.1 / 79.9 · 105.4 / 108.5 | −2.8% · −3.0% | Spread plus duration | Both at 52-week lows; LQD's drop is mostly duration |
| | HY OAS | 3.12% (Sep 30) | 1-yr low 2.80% | +39 bp in a week | Is rate pressure becoming credit stress? | Widening from tight levels; not yet stress |
| **Volatility** | VIX | 16.39 | 15.9 / 18.1 | — | Equity uncertainty | Calm |
| | MOVE | 108.1 | 80.0 / 73.7 | +39% / +65% | Rates uncertainty | Extreme — uncertainty is in **rates, not equities** |
| **Dollar** | DXY | 102.04 | 100.0 / 99.3 | +2.4% / +1.2% | Global financial conditions | **52-week high**: yields tightening conditions through the dollar |
| **Metals** | Gold (front future) | 4,203 | 4,364 / 4,554 | −4.4% / +1.9% | Real yields, the dollar, hedge demand | Below both averages, −21% from its high: real-yield/dollar pressure |
| | Silver | 61.26 | 63.9 / 72.6 | −5.2% / +1.0% | High-beta precious | −47% from its high |
| | Copper | 6.57 | 6.55 / 6.11 | +1.0% / +7.4% | Global industrial demand | Above both averages: no growth scare |
| **Energy** | WTI / Brent | 93.01 / 102.50 | 88.6 / 82.2 · 94.8 / 87.5 | +3.1% / +35% · +8.3% / +43% | Supply shock vs demand | Geopolitical supply premium |
| | XLE | 62.70 | 62.1 / 56.5 | −3.2% / +17.8% | Energy equities | Back above its 50-day |

**Market Brief / market-review** stays read-only evidence. Hypotheses H1–H5 (Sep 30) map onto these rows: H1 rates restrictive, H2 rates vol > equity vol, H3 weak participation, H4 calm equity vol, H5 narrow leadership. All five are consistent with the Oct 1 readings.

## 3. Investable roster — long-horizon businesses (worth understanding continuously; **not** "approved to buy")

Roles describe each business's place in Dustin's **whole investment program**, not its weight inside the C$5,000 sleeve (Round 10).

| Business | Program | Role (program level) | Oct 1 | vs 50d / 200d · off high | Status | Last reviewed | Next review event | What would change it |
|---|---|---|---|---|---|---|---|---|
| **CBOE** (sleeve: held) | D | CORE candidate, with a named dependency (SPX × retail short-dated × regulation) | 277.19 | 288.0 / 287.0 · −24% | Thesis intact | 2026-10-01 (R6/R8) | Q3, Oct 30; monthly volume (~Oct 2–5) | Options volume negative y/y for two quarters; a fee or 0DTE rule; loss of exclusivity |
| **CME** | D | CORE candidate (not held) | 265.10 | 270.3 / 278.5 · −19% | Approved candidate; Strategy F trigger ≤ ~$220 or clearing growth ≥ ADV growth | 2026-10-01 | **Q3, Oct 21**; September volume release | FMX share gains; a volume regime pinned at zero rates |
| **ICE** | D | CORE candidate (second choice) | 151.47 | 155.2 / 155.1 · −14% | Understand; no trigger defined | 2026-10-01 (R4) | Q3, Oct 29 | Mortgage-tech trend, which is the rates-turn kicker |
| **SPGI** | D | CORE candidate (damaged) | 388.16 | 417.8 / 424.5 · −25% | Cohort E-08 (Setup A pre-registration if still ≥ 25% below its high) | 2026-10-01 | **Q3, Oct 27** | Ratings issuance; Indices growth |
| **LNG** (sleeve: held) | E | CORE (existing asset) + embedded growth option | 272.40 | 272.1 / 246.5 · −8% | Thesis intact (LNG-A / LNG-B) | 2026-10-01 (R6) | **Q3, Oct 29**; FERC on the expansion (late 2026) | LNG-A: contracted share < ~85% or tenor < ~12 years. LNG-B: permit denial, or FID slipping past 2027 |
| **WMB** | E | Understand only — **not attractive at price** | 69.22 | 72.2 / 71.1 · −13% | 28x forward with negative FCF (Round 4) | 2026-10-01 (R4) | Q3, Nov 2 | Valuation reset, or FCF turning positive |
| **TSM** (sleeve: held, 26% of the sleeve) | H | **SATELLITE** (geopolitical tail) | 459.20 | 423.8 / 386.2 · −4% | Thesis intact; tranche 2 conditional on Oct 15 | 2026-10-01 (R8/R9) | **Q3, Oct 15**; monthly revenue (~10th) | Two hyperscalers cutting capex; N2 failure; a cross-strait event (handled by size) |
| **MU** | H / B | TACTICAL (cyclical economics) | 1,097.39 | 954.4 / 677.4 · −10% | PT-003 WATCH; requires a larger account to hold live | 2026-10-01 | Dec earnings; TrendForce pricing | Memory contract prices flat quarter-on-quarter |
| **VRT** | H / B | SATELLITE or TACTICAL | 246.12 | 261.8 / 264.2 · −35% | PT-002 WATCH; cohort E-04 | 2026-10-01 | **Q3, Oct 21 (est.)** | Orders/backlog; the UIG close |
| **CLS** | H / B | TACTICAL (customer concentration) | 373.09 (NYSE) | 329.1 / 330.3 · −21% | PT-010 WATCH | 2026-10-01 | **Q3, Oct 26; Investor Day Oct 27** | Hyperscaler order changes |

## 4. Tactical roster (each keeps thesis, setup, activation, invalidation and horizon — or goes stale)

Watch types and lifecycle rules are in §6. Full plans and annotations are in `PAPER_TRADES.md`.

| Record | Family | Watch type | Activation (frozen) | Invalidation | Expires / reviewed | Oct 1 status |
|---|---|---|---|---|---|---|
| PT-001 ACN | Earnings › RECOVERY | Event | — | — | **EXPIRED — NO TRIGGER** (Oct 1); SHADOW to Dec 11 | Day 1: +15.8%, close location 0.08 |
| PT-002 VRT | Broken-leader reclaim | Tactical setup | Weekly close > 262 on ≥ 1.5× volume | Close < 232 | **Expires at the Oct 20 close** if not triggered (earnings Oct 21 changes the structure; any post-earnings base is a fresh record) | 246.12 |
| PT-003 MU | Trend pullback | Tactical setup | Pullback ≥ 8% touching the 20/50-day, then a close above the prior high | Close below the pullback low | **Expires on the first close below the 50-day without a qualifying pullback**, or at Dec earnings | 1,097 — extended |
| PT-004 FICO | Post-shock reversal | Tactical setup | 10 sessions without a close < 586.05 + reclaim of the 20-day + close above the base high | Close below the base low | **Expires at its next earnings (est. Nov 4)** if not triggered, or on a close < 586.05 | 661.75 — session 2 of 10 |
| PT-005 SPY | Index downside (G) | Regime-linked tactical | Close < 750 with ≥ 3 of 5 conditions | Close above the 50-day | **Reviewed monthly (next Nov 2) and after FOMC (Oct 28).** Expires at a review if fewer than 3 of its 5 conditions remain possible | 763.99 |
| PT-006 TLT | Duration turn (C) | **ACTIVE REGIME WATCH — LAST REVIEWED 2026-10-01** | M1–M3 + 1 optional (weekly) | 10Y +40 bp / trigger-week low | Reconfirm monthly and after CPI (Oct 14), FOMC (Oct 28) and the refunding (early Nov) | 77.71 — new 52-week-low close |
| PT-007 CBOE | Tactical compounder entry | Tactical setup | Close > 288 on ≥ 1.5× volume | Close < 262 | **Expires at the Oct 29 close** (earnings Oct 30) | 277.19 |
| PT-008 HWM | Broken-leader reclaim | Tactical setup | Close > 248 on ≥ 1.5× volume, then a weekly close > 260 | Close < 222 | **Expires at the Oct 28 close** (earnings Oct 29) | 228.38 |
| PT-009 ITB | Duration turn (C) | **ACTIVE REGIME WATCH — LAST REVIEWED 2026-10-01** | M1 + MND ≤ 7.35% + close above the 20-day | Close < 84.00 | Reviewed with PT-006 | 87.37 |
| PT-010 CLS | Trend pullback | Tactical setup | 8–12% pullback holding the 20-day, then a close above the prior high | Pullback low / 50-day | **Expires at the Oct 26 close** (earnings after the close); re-arming needs a fresh record | 373.09 — extended |
| Cohort E-01…E-10 | Earnings (A) | Event | Setup A / A-M per the mechanical rule | Completed day-1 RTH low | Each closes at its D+20 | First: UNH, Oct 13 |

## 5. What would actually cause capital to move (decision points, dated)

| Date | Decision | Rule already written | Where |
|---|---|---|---|
| Oct 15 | TSM tranche 2 (sleeve) | Buy only if Q4 guidance ≥ consensus **and** 2026 capex is held or raised **and** the > 40% growth outlook is intact | PROPOSAL §1; ROUNDS R5 |
| Oct 21 | CME — candidate to enter | Strategy F: ≤ ~$220 **or** clearing/transaction revenue growing at least as fast as ADV. Entering would also need the capital-unlock comparison (PROPOSAL §7) | ROUNDS R5–R6 |
| Oct 29 | LNG tranche 2 (sleeve) | After the print, unless LNG-A is invalidated | PROPOSAL §1 |
| Oct 30 | CBOE third share (sleeve) | After the print, unless options volume is negative y/y, a fee/0DTE rule appears, or exclusivity is lost | PROPOSAL §1 |
| Any day | A regime break | HY OAS ≥ 4%, or VIX > 20 with rising realised volatility → review every core thesis | §1 |
| Not yet | Tactical capital | **None.** No family has completed paper evidence; live capital needs PAPER TRADE + REPEATED OBSERVATIONS | PAPER_TRADES rule 4 |
| Any day | Speculation | Only with the loss accepted in writing beforehand | PROPOSAL §6 |

## 6. Watch lifecycle (Round 10)

| Type | Examples | Expiry |
|---|---|---|
| **Permanent gauge** | SPY, 10Y, VIX, gold | None |
| **Event watch** | Earnings cohort | When the pre-specified event window closes; untriggered → EXPIRED — NO TRIGGER (+ SHADOW where specified) |
| **Tactical setup** | MU pullback, CBOE reclaim | When its stated horizon passes, the price structure defining it materially changes, or the thesis changes. Old entry levels are never moved behind the market; a fresh setup needs a fresh record |
| **Regime watch** | Duration turn, breadth/downside | Stays active for months with periodic reconfirmation: "ACTIVE REGIME WATCH — LAST REVIEWED <date>" |
| **Long-horizon business thesis** | CBOE, LNG, TSM | Reviewed after major information events (earnings, acquisitions, regulation, capital allocation, structural change); active until the thesis evidence changes |

The expiries in §4 were added on Round 10 as dated lifecycle annotations. No frozen trigger, invalidation or exit rule was changed.

## 7. Stale / archived (Round 10 review)

Archived ideas are not refuted. They are no longer described by a live thesis, setup and horizon. Reviving one needs a fresh record.

| Item (old watchlist §) | Why archived |
|---|---|
| Round 4 tactical board (§0) | Superseded by `PAPER_TRADES.md` |
| MBB → TLT duration ladder (§1) | Superseded by the frozen PT-006/PT-009 records; MBB as a vehicle can return at a trigger |
| Gold/metals entry rules (§2) | Gold is now a **gauge**. Any metals decision belongs to the exposure map and the capital-unlock comparison, not a sleeve entry rule |
| Power and electrification (§3: GEV, ETN, BE, GRID, VST, CEG) | No live record; the AI-power exposure is studied through VRT, CLS and HWM |
| Energy tactical rules (§4: XLE, XEG) | Energy is a **gauge**; no live energy thesis |
| Semiconductors/SMH (§5) | Covered by TSM and MU |
| Brazil/EWZ (§5a) | Dropped from the sleeve in Round 4; no record written for the Oct 4 election |
| Uranium (§5b: U.UN, URNM, CCO) | No program; the SPUT-discount trigger is preserved in git history |
| Parked list (§5c, §7: tankers, Japan banks, munis, mREITs, coal/aluminium/lithium, Canadian telecoms, Poland/Greece, ZPR, TLT calls, TBT, UVXY, Ackman-style instruments) | Rejected or unstudied; no live thesis |
| Chaos-regime map (§6) | Absorbed into the gauges (§2) and the narrative (§1) |

## 8. Research questions that deserve time now

The full queue is in `RESEARCH_MAP.md`. The three nearest to changing decisions:
1. **The cohort analysis.** Frozen before UNH (Oct 13) in `RESEARCH_MAP.md` Program A; the first readout comes after the last cohort event's D+20 (~Nov 30).
2. **An exposure map of Dustin's whole program** (LIRA, TFSA, margin, metals, cash, other) answering "what economic risks do we already own before deploying another dollar?" Future work; not full accounting.
3. **What preceded past long-end tops** (Oct 2023, 2006–07, 1994–95). This sharpens the duration regime watch before it is needed.
