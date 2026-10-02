# Market Model — rates, credit and liquidity (MARKET_MODEL.md)

**This file answers: "What do we currently think is happening, why, and what would prove us wrong?"** It is current understanding, not the historical archive. Today it covers the rates/credit/liquidity complex, the area that currently looks most central. Other market hypotheses join §6 when they arise, because the learning process does not freeze.

**How to read it.** It has two kinds of section.

**Current — changes with the market; read these first:**

| What | Where |
|---|---|
| Active hypotheses and their states | §6 |
| Contradictions and research notes | §7 |
| Base case, competing explanations, discriminating observations | §8 |
| Predictions and falsification conditions (with a status tracker) | §8 |

**Structural reference — changes rarely:**

| What | Where |
|---|---|
| Mechanisms: the transmission map and its links | §1–§2 |
| Causality classes | §3 |
| Instrument classes: gauge or vehicle | §4 |
| Why each gauge is kept | §5 |

Claims carry the evidence labels (OBSERVED · DERIVED · MODEL ESTIMATE · INTERPRETATION · PREDICTION · UNMEASURED). Relationships carry the causality labels.

**Created:** Round 11 — Claude (Opus 5.5) · 2026-10-01 · values are the Oct 1 close unless dated otherwise. The daily page is `WATCHLIST.md` (Market Roster); it carries the compact **DAILY STATE**, which cites this file by section, thesis name and contradiction ID.

**Edit rule (revised Round 12): this file is current understanding only.** It must stay readable; history must stay recoverable. Those are different goals with different homes: history lives in `ROUNDS.md` and git.

| Section | Rule |
|---|---|
| §1–§5 (map, links, causality, instruments, missing cogs) | Updated in place, with a one-line note in `ROUNDS.md` |
| §6 Thesis register | Shows each thesis's **current** state and its **last** change (date + evidence). Older changes move to `ROUNDS.md` at the weekly review |
| §7 Contradictions | Shows **OPEN** entries and those resolved since the last weekly review. Resolved entries move to `ROUNDS.md`, with their resolution, at the weekly review. **Nothing leaves without a written status and the evidence for it** |
| §8 Adversarial challenge | Redone whenever the base case changes; earlier versions stay in `ROUNDS.md` |

*Round 11 had made §6 and §7 append-only. Round 12 replaced that rule (ChatGPT Round 12 §7): git already guarantees recoverability, and a log that only grows stops being read.*

**Two label axes.**
- **Claims** carry evidence labels (pillar P1, `RESEARCH_MAP.md`): OBSERVED · DERIVED · MODEL ESTIMATE · INTERPRETATION · PREDICTION · UNMEASURED.
- **Relationships** carry the causality labels below. The causality label OBSERVED means *seen in the current data over a stated window*, which is still not causation.

**Causality labels used throughout (ChatGPT Round 11 §3).** We do not write "X causes Y" when all we know is that X and Y are moving together.
- **MECHANICAL:** an identity or a contractual or rule-based link, such as nominal = real + breakeven, a mortgage priced off Treasuries, or a vol-target fund's sizing rule.
- **PLAUSIBLE:** a sound economic mechanism exists; strength and timing are not guaranteed.
- **HISTORICAL:** the two have moved together in past samples. Say which samples, and whether the link has broken before.
- **OBSERVED:** seen in the current data, over a stated window.
- **HYPOTHESIS:** proposed, not yet shown.

---

## 1. The transmission map

The chain is not linear. Shocks enter at several points, and some links feed back.

```
UPSTREAM      oil / geopolitics      fiscal supply      foreign long ends       funding plumbing
SHOCKS              │                     │                   │                (reserves, repo, RRP)
                    ▼                     │                   │                      ┆ silent until
POLICY      [1] Fed reaction → priced path│                   │                      ┆ it breaks
                    ▼                     ▼                   ▼                      ┆
SOVEREIGN   [2] 2Y ──► [3] curve ──► [4] 10Y / 30Y  =  expected policy path + term premium ◄┄┄┘
                                                    =  real yield + breakeven
                    ┌──────────────┬────────────┼──────────────┬──────────────┐
                    ▼              ▼            ▼              ▼              ▼
PRIVATE     [5] mortgage      [7] IG credit  [8] HY / CCC   [9] dollar    [11] equity discount
RATES           rate =            (rates +       / loans         │            rate, set against
                10Y + spread      spread)        (floating        ▼            earnings revisions
                    ▼                            interest)   [10] gold /           ▼
REAL        [6] housing,                                     commodities    [12] breadth: rate-
ECONOMY         bank lending                                                 sensitive sectors
                                                                             move first
                                                                                   ▼
RISK        [13] equity vol ◄──── [14] systematic exposure ◄──── realised vol ◄────┘
APPETITE          └───────────────────────► (amplifier loop) ─────────────┘
```

**Feedback loops (sign and speed matter more than the arrows):**

| Loop | Path | Sign · speed | Why it matters now |
|---|---|---|---|
| **LOOP-1 · Oil self-limiting** | Oil ↑ → headline CPI ↑ → Fed hikes → real yields ↑, dollar firm, demand ↓ → oil ↓ → hikes priced out → duration turns | Negative · weeks to months | The most likely route to a duration turn under the base case. The oil curve is steeply backwardated: the market already prices the shock as temporary |
| **LOOP-2 · Fiscal term premium** | Yields ↑ → federal interest cost ↑ → deficits and supply ↑ → term premium ↑ → yields ↑ | Positive · quarters | Tested at the Nov 4 refunding; Treasury guides coupon sizes unchanged "for at least the next several quarters" |
| **LOOP-3 · Vol control** | Equities ↓ → realised vol ↑ → vol-target and CTA de-grossing → equities ↓ | Positive · days | Fuel present (exposure at the 98th–100th percentile); trigger absent (VIX 16.4) |
| **LOOP-4 · Liquidation** | Margin or redemption stress → sell what is liquid and profitable (gold, Treasuries) → safe havens fall with equities | Positive · days | Why gold and bonds can fall *in* a crash. Not active |
| **LOOP-5 · Housing/banks → growth** | Mortgage rates ↑ → housing and loan demand ↓ → growth ↓ → policy path ↓ → yields ↓ | Negative · months | The slow brake; SLOOS shows residential demand weakening, business lending not |
| **LOOP-6 · Common cause** | A Middle East supply shock lifts oil **and** gold at the same time | No causal link between them | Explains days when oil and gold rise together despite higher yields |

## 2. Links — mechanism, failure mode, confirmation, contradiction

"Since Jun 30" means Jun 30 → Sep 30, 2026, from FRED unless marked otherwise.

| # | Link | Mechanism | Class | Breaks when | Confirms | Contradicts | Reading (Oct 1) |
|---|---|---|---|---|---|---|---|
| 1 | Oil → headline CPI → Fed reaction | Energy reaches headline CPI within weeks; the Fed reacts if it fears expectations will follow | PLAUSIBLE · OBSERVED as co-movement — **the Fed's own rationale does not name oil** | The Fed "looks through" a supply shock; the oil curve signals transience | Strip adds hikes after an oil rise | Oil rises, strip unchanged | The Fed hiked Sep 16 (12–0), saying only "Inflation remains elevated"; energy is not mentioned. Headline CPI 3.4% vs core 2.4% (August) makes energy the likely source; the link is our inference. WTI +34% since Jun 30 |
| 2 | Fed path → 2Y | 2Y ≈ the average expected policy rate over two years, plus a small premium | MECHANICAL | Flight to quality can pull the 2Y below the path | 2Y and fed funds strip move together | 2Y falls while strip rises | 2Y 4.88% vs effective funds 3.88%. Strip: Dec 4.08%, Jan 4.15%, May '27 4.50% → about 2½ more 25 bp hikes priced |
| 3 | 2Y → 10Y via the curve | 10Y = expected short rates over ten years + term premium | MECHANICAL identity; the split is model-dependent | Term premium moves on its own (supply, foreign demand, rate vol) | 10Y ≈ 2Y moves with term premium stable | 10Y rises with the 2Y flat | Jun 30 → Sep 30: 10Y +85 bp, 2Y +74 bp, 2s10s +11 bp (+16 to Oct 1). Kim–Wright term premium +32 bp (0.70 → 1.02) over the matched window Jun 30 → Sep 25, when the 10Y rose +73 bp → **roughly 55% policy path, 45% term premium** (model-dependent; the ACM model is the cross-check, not read this round) |
| 4 | 10Y = real + breakeven | Fisher identity | MECHANICAL | — | — | — | 10Y real **+73 bp** (2.20 → 2.93), breakeven **+12 bp** (2.24 → 2.36), 5y5y 2.36%. A real-rate shock, not an inflation-expectations shock |
| 5 | 10Y → mortgage rate | Mortgage = Treasury benchmark + primary/secondary spread | MECHANICAL + spread | The spread moves: MBS demand, rate vol, bank or Fed buying | Mortgage moves 1:1 with the 10Y | Spread widens (amplifies) or narrows (cushions) | Freddie Mac 30Y **7.28%** (+79 bp; Oct 1); MND 7.60% (Sep 30). Spread to the 10Y ≈ **2.0 pp, unchanged since Jun 30**. MBB OAS 38.5 bp (Sep 30) |
| 6 | Mortgage → housing and refinancing | Payment affordability. Lock-in: the MBS universe's average coupon is 3.63% against 7.3% today, which freezes resale and refinancing | PLAUSIBLE + HISTORICAL; lags 3–12 months | Builder rate buydowns; income growth | Applications, sales and starts fall | Activity firm at 7%+ | SLOOS (July): weaker demand across all residential categories. ITB −14% in 3 months (a price, not activity) |
| 7 | Rates and curve → bank lending | Net interest margin (10Y−3M), deposit costs, securities losses, loan demand | PLAUSIBLE; **sign ambiguous** | Steeper curve and strong loan demand offset it | SLOOS tightening; KRE breaks; deposit outflows | — | **Not transmitting.** SLOOS: C&I standards unchanged, large-firm demand stronger, CRE standards eased. KRE −6% in 3 months, near its 200-day. 10Y−3M 107 bp (+50) |
| 8 | Rates → IG credit | Price = Treasury duration + spread; spread = default + liquidity premium | MECHANICAL for price · PLAUSIBLE for spread | Demand for all-in yield (~6%) absorbs supply | IG OAS > ~100 bp; BBB widening | IG flat while equities fall | LQD −5.3% total return in 3 months, ~90% of it duration. IG OAS 0.84% (+8 bp); BBB 1.03% (+8) |
| 9 | Short rates → HY, CCC, loans | Floating-rate interest costs rise with the policy rate; the weakest borrowers' coverage fails first | MECHANICAL (interest cost) → PLAUSIBLE (defaults, lagged) | Earnings growth outruns interest cost; refinancing windows stay open | CCC widening spreads to B/BB; loan prices fall | CCC widens while loans rise | **CCC 11.79% (+209 bp; wider than in March's stress)**. HY 3.12% (+37 bp; +44 bp in the week to Sep 30). BKLN price flat (20.37 → 20.46, just below its 50- and 200-day), +2.2% total return in 3 months |
| 10 | US yields → dollar | Rate differentials draw capital | PLAUSIBLE · HISTORICAL · OBSERVED in September only | Foreign yields rise too; a US-specific risk premium sends yields up and the dollar down | Broad dollar rises with US−foreign spreads | Dollar falls while US yields rise | Broad dollar **−0.5%** Jun 30 → Sep 25 (but +1.5% in September). DXY's 52-week high is euro-led (EUR −1.4%); the **yen rose 3%**; USD/CAD flat (1.4205 → 1.4222) |
| 11 | Real yields and dollar → gold | Opportunity cost (real yield) and currency of denomination | HISTORICAL — strong 2006–21; weakened 2022–25, coinciding with record central-bank buying | Official-sector buying; geopolitical hedge demand | Gold falls as real yields rise for > 1 month | Gold rises with real yields | 3 months: real +73 bp, **gold +4%**. Month by month (Jun–Sep), gold moved opposite the broad dollar in 4 of 4 months and clearly opposite 5Y real yields in 2 of 4 (footnote ¹) |
| 12 | Rates → equity discount rate | Higher real rates lower the value of distant cash flows, most for long-duration growth | PLAUSIBLE — valuation arithmetic that holds earnings and the risk premium fixed, which they are not | Earnings revisions outrun rates; the risk premium compresses | P/E falls as yields rise | P/E holds while estimates rise | Forward P/E **19.2** (10-year avg 19.0). Q3 EPS est. +29.1%, **raised 1.3% during the quarter** (5-year norm −2.2%). Forward earnings yield 5.21% ≈ the 10Y (FactSet, Sep 25) |
| 13 | Rates → breadth | Rate-sensitive sectors reprice first (housing, banks, small caps carrying floating debt); the index is held by sectors with earnings momentum | PLAUSIBLE · OBSERVED | Rates fall; earnings broaden | Breadth weakens further as the 10Y rises | Breadth recovers with the 10Y > 5% | 23% of S&P above the 50-day. 3 months: ITB −14%, IWM −6%, KRE −6%, versus QQQ +4% and SPY +3%. (XLU −13% and VNQ −8% fell too, but are screened out as rate gauges because their drivers are mixed — §4) |
| 14 | Rate vol → equity vol | Discount-rate uncertainty; cross-asset risk managers cut risk when portfolio vol rises | HISTORICAL — March 2026: both spiked | Low realised equity vol and strong earnings | VIX climbs toward the MOVE | MOVE > 100 with VIX < 18 for weeks | MOVE 108 (March peak 115); VIX 16.4 (March peak 31.1) |
| 15 | Realised vol → systematic flows | Vol-target funds set exposure = target vol ÷ realised vol; CTAs follow trend | MECHANICAL rule · size is a HYPOTHESIS | Realised vol stays low | VIX ↑, index ↓, reported de-grossing | — | Exposure at the 98th (Deutsche Bank via Reuters) to 100th (BofA, secondary) percentile. Estimated selling up to ~$163B vs ~$9B of buying room (BofA via secondary source). US equities trade ~$1.29T a day (June) |
| 16 | Funding → Treasury market | Dealers and basis trades finance Treasuries in repo; funding stress forces selling | MECHANICAL | Standing repo facility backstop; ample reserves | SOFR > IORB by ≥ 5 bp outside month-ends; SRF use > $10B | — | **Quiet.** SOFR 3.90% = IORB 3.90% at quarter-end; SRF $1.2B (Sep 30); ON RRP ≈ $0.35B (the buffer is gone); reserves $2.95T |
| 17 | Foreign long ends → US term premium | Substitution (JGB, Bund) and repatriation (Japanese banks) | PLAUSIBLE · HISTORICAL (weak) | — | US moves with JGB/Bund | US moves alone | 1 month: US +46 bp vs Bund +15, JGB +8, Gilt +21, Canada +13. France +65 and Italy +47 are a separate euro-spread story. **Mostly US-specific** |

¹ Month-end pairs: gold front future (Yahoo), broad dollar (FRED DTWEXBGS; September to Sep 25), 5Y real yield (FRED DFII5).
- June: gold −12.1% · dollar +1.7% · 5Y real +32 bp.
- July: gold +1.7% · dollar −1.0% · 5Y real +26 bp.
- August: gold +9.1% · dollar −0.9% · 5Y real −1 bp.
- September: gold −6.6% · dollar +1.5% · 5Y real +55 bp.

Gold moved opposite the dollar in all four months. It moved clearly opposite real yields in June and September, with them in July, and against a flat reading in August.

## 3. Cause vs correlation — the relationships most at risk of over-reading

| Relationship | Strongest honest class today | Current evidence | We may write | We may not write |
|---|---|---|---|---|
| **Yields ↔ gold** | HISTORICAL (weakened since 2022) · OBSERVED month to month only *via the dollar* | Gold +4% while 10Y real +73 bp (Jun 30 → Oct 1). June (−12%) and September (−7%) falls coincided with the dollar and front-end real yields rising | "Gold fell in September as the dollar and 5Y real yields rose" | "Rising yields are pushing gold down" |
| **Yields ↔ dollar** | PLAUSIBLE · OBSERVED in September only | Broad dollar −0.5% over the episode, +1.5% in September; euro-led; yen stronger | "September's dollar rise coincided with the 2Y repricing" | "The rate shock is strengthening the dollar" |
| **Yields ↔ equities** | PLAUSIBLE · OBSERVED for rate-sensitive sectors · **not observed at the index** | P/E 19.2 with rising estimates; ITB, IWM and KRE down | "Rate-sensitive sectors are repricing with yields" | "Rates are pressuring equities" |
| **Credit ↔ equities** | PLAUSIBLE (equity is the junior claim on the same cash flows) · HISTORICAL | CCC wider than March while SPY sits 1.8% below its August high | "The CCC tail and the index are diverging" | "Credit is warning equities" |
| **Vol ↔ systematic flows** | MECHANICAL rule · magnitude a HYPOTHESIS | Exposure 98th–100th percentile; flow estimates from secondary reports | "Vol-target exposure is high and would fall if realised vol rose" | "Systematic funds will sell $X" |
| Oil ↔ breakevens | PLAUSIBLE · OBSERVED weakly | 10Y breakeven +12 bp while oil rose 34%; 5y5y 2.36% | "The oil shock has not reached long-run inflation expectations" | "Oil is driving yields higher through inflation expectations" |
| Fed path ↔ 2Y | MECHANICAL | 2Y +74 bp; strip adds ~2½ hikes | "The 2Y is pricing more hikes" | — |
| 10Y ↔ mortgage rate | MECHANICAL + spread | Spread stable at ~2.0 pp | "Mortgage rates rose with the 10Y" | — |
| Rate vol ↔ MBS spreads | PLAUSIBLE (negative-convexity hedging) · **not observed** | MOVE +65% in 3 months; MBS OAS still tight (MBB 38.5 bp) | "MBS spreads have not reacted to rate vol" | "Rate vol is stressing mortgages" |
| US ↔ foreign yields | HISTORICAL · weak now | US +46 bp vs Bund +15 / JGB +8 in a month | "The US long end is moving more than core peers" | "This is a global bond rout" |

## 4. Instrument map — gauge, vehicle, both, or remove

The screen asks one question per instrument: **does it carry information or an expression we cannot get more cleanly elsewhere?** Durations and yields are from issuer pages as of Sep 30; returns are 3-month total returns to Oct 1 (Yahoo adjusted closes).

| Instrument | What it is | Class | Why |
|---|---|---|---|
| **SGOV** | 0–3-month T-bills | **VEHICLE** (cash) | The risk-free rate in a share; the hurdle every trade must beat. Carries no information |
| USFR · SHV · BIL | Floating 2Y notes · 0–1Y bills · 1–3-month bills | **REMOVE** | Same job as SGOV with no additional signal |
| **IEF** | 7–10Y Treasuries, duration 6.84 | **BOTH** | The 10Y in price form and the denominator that strips duration out of LQD and MBB. As a vehicle: a lower-convexity duration turn |
| VGIT · SHY · GOVT | 3–10Y · 1–3Y · all-maturity Treasuries | **REMOVE** | Redundant with IEF and the 2Y yield itself |
| **TLT** | 20Y+ Treasuries, duration 14.6 | **BOTH** | The duration-turn vehicle with liquid, cheap options (IV ~16%) |
| EDV · ZROZ | 20–30Y STRIPS, duration ~24–27 | **REMOVE** | More leverage, no new signal; long calls on TLT already deliver convexity at a defined loss |
| TIP · SCHP · STIP · VTIP | TIPS: broad and 0–5Y | **REMOVE as instruments** | The information is the real yield and the breakeven, read directly from FRED (DFII10, T10YIE). As a vehicle, "real yields fall" is a subset of the duration-turn thesis |
| **MBB** | Agency MBS, duration 5.92, OAS 38.5 bp | **GAUGE** | Mortgage-spread health. A poor vehicle: negative convexity caps the gain in a rally once refinancing revives |
| VMBS | Agency MBS | **REMOVE** | Duplicate of MBB |
| **LQD** | IG corporates, duration 7.53 | **GAUGE** (secondary) | The intraday price proxy for IG. IG OAS from FRED is the primary gauge |
| VCSH · IGSB | Short IG | **REMOVE** | Mostly carry; little information |
| **HYG** | HY corporates, duration 3.30, BB 58% / B 33% / CCC 7% | **BOTH** (vehicle conditional) | The risk-transmission sensor. Puts are a vehicle only if CREDIT STRESS becomes ACTIVE; the Round 1–3 HYG put was rejected on price (EV ≈ 0.73× premium) |
| JNK | HY corporates | **REMOVE** | Duplicate; HYG's options are deeper |
| **BKLN** | Senior floating-rate loans | **GAUGE** (new) | Floating coupons leave almost no rate duration, so its price is nearly pure credit. It is also the direct channel from Fed hikes to leveraged borrowers' interest costs |
| SRLN · FLOT | Loans · IG floaters | **REMOVE** | SRLN duplicates BKLN; FLOT is cash-like |
| **ITB** | Homebuilders; top DHI, PHM, LEN | **BOTH** | The housing leg of the transmission and a duration-turn equity expression (shares only; its options are illiquid) |
| XHB | Broader home-related equities | **REMOVE** | Duplicate of ITB, diluted |
| **KRE** | Regional banks | **GAUGE** | Bank-channel stress (the 2023 template): margins, deposits, securities losses, CRE |
| XLU · VNQ · IYR | Utilities · REITs | **REMOVE as rate gauges** | Mixed drivers: AI-power demand for utilities; data centres and commercial property for REITs. XLU −13% in 3 months is larger than IEF's loss and is not a clean rates signal. Utility businesses belong to Program E if ever studied |

**What each surviving instrument actually gives us**

- **SGOV.** Three-month bills in a share. It tracks the policy rate with about a one-month lag and has no duration. It is the place idle cash earns the risk-free rate, and the benchmark a trade must beat. *Not* a gauge: it says nothing the fed funds rate does not.
- **IEF.** The 10-year Treasury in price form (duration 6.84; a 1 bp yield change ≈ 0.07% price). Its main job is as a denominator: LQD ÷ IEF isolates the IG spread, and MBB ÷ IEF isolates mortgage spread behaviour. As a vehicle it expresses a duration turn with less convexity and a smaller drawdown than TLT.
- **TLT.** Very long Treasury duration (14.6; WAM 26 years; SEC yield 5.49%). Highly sensitive to the long end: 1 bp ≈ 0.15%. It is affected by real yields, inflation expectations, term premium and supply. Since June the move has been almost all real yield (breakevens +12 bp); split the other way, roughly 55% expected policy path and 45% term premium, which is where supply shows up. It is the duration-turn vehicle (PT-006) because its options are liquid and cheap. Not a cash substitute: −8.4% in three months.
- **MBB.** Agency mortgage exposure: Treasury duration (5.92) plus mortgage-spread behaviour plus prepayment optionality. **Round 11 nuance:** the universe's average coupon is 3.63% against ~7.3% mortgage rates, so most borrowers are deep out of the money to refinance. MBB therefore behaves more like a Treasury with a spread than it did in 2020–22. That is the leading explanation — C-010 (a), still open — for why mortgage spreads have not widened with rate vol. Signal: MBB underperforming IEF duration-adjusted means housing finance is under stress. So far only marginally: MBB −4.2% in 3 months against about −3.9% for an IEF position scaled to MBB's duration — consistent with ordinary extension, not spread stress.
- **LQD.** IG corporates: duration 7.53, SEC yield 5.95%. About 90% of its 3-month loss was Treasury duration. It tells us whether the rate shock is becoming a corporate-funding problem for strong borrowers; today it is not (IG OAS +8 bp).
- **HYG.** Rate exposure plus credit-spread exposure plus a 7% coupon: duration 3.30, SEC yield 6.96%, BB 58% / B 33% / CCC 7%. Its price moves with both Treasury yields and spreads. Over 3 months about two-thirds of its price loss was rates; in the last week spreads dominated. It is the sensor for sovereign-rate pressure becoming corporate stress, and a hedge vehicle only under an ACTIVE credit thesis.
- **BKLN.** Senior secured floating-rate loans. Coupons reset with short rates, so its price is close to pure credit risk. A hiking cycle *raises* its income while *raising* borrowers' interest burden: if loan prices fall while short rates rise, the hiking channel is breaking borrowers. Today its price is flat (20.46, just below its 50- and 200-day averages) and its 3-month total return +2.2%: flat-to-soft, not stressed.
- **ITB.** Homebuilder equity (P/E 14.7 trailing on Oct 1). It is hit through the mortgage rate (demand) and the discount rate. Lock-in gives builders a larger share of a frozen resale market. It is where a rate turn shows up early in equities, and a shares-only vehicle.
- **KRE.** Regional banks: margin (curve), deposit costs, unrealised securities losses and CRE in one price. A gauge of whether the rate shock reaches bank balance sheets (2023). Today it does not.

**Gauges that are series, not instruments (added Round 11; see §5):** 10Y real yield and breakeven; fed funds futures strip; IG / HY / CCC OAS; broad trade-weighted dollar; USD/JPY and USD/CAD; WTI front vs 12-month; mortgage rate − 10Y; SOFR − IORB (alarm); NFCI, foreign 10Ys and Kim–Wright term premium (weekly); auction results (event).

## 5. Missing cogs — the smallest set that changed the reading

Tested against one question: **did adding it change our interpretation of Oct 1?**

| Candidate | Changed the reading? | Verdict |
|---|---|---|
| **Real yields vs breakevens** | **Yes.** The shock is real-rate (+73 bp), not inflation (+12 bp). This killed the "oil → inflation expectations → yields" chain as the main path | **ADD — daily** |
| **Priced Fed path** (fed funds futures; 2Y) | **Yes.** Roughly 55% of the 10Y move is the expected policy path (Kim–Wright, matched window), and that share moves with the strip. PT-006's stated mechanism, term premium, is the large minority | **ADD — daily** |
| **Credit quality split** (IG / HY / CCC OAS + BKLN) | **Yes.** The stress is in the CCC tail only, and CCC is already wider than in March | **ADD — daily** |
| **Broad dollar** (vs DXY) | **Yes.** It is flat over the episode; DXY's high is a euro move | **ADD — daily** (with USD/JPY and USD/CAD, Dustin's own currency risk) |
| **Oil curve slope** (front vs 12-month) | **Yes.** Steep backwardation (WTI −19% Nov '26 → Dec '27; dated Brent $114 vs Dec Brent $102) says the market treats the shock as temporary, which is LOOP-1's premise | **ADD — daily** |
| Mortgage spread (mortgage rate − 10Y; MBB vs IEF) | Yes: transmission is one-for-one, not amplified | **ADD — weekly** |
| Treasury auctions | Partly: stop-throughs in the 10Y/30Y argue against a buyers' strike | **ADD — event** (10Y Oct 7, 30Y Oct 8, refunding Nov 4) |
| Funding (SOFR − IORB, SRF use, ON RRP) | No (quiet). But the ON RRP buffer is gone, so reserves now absorb every drain | **ADD — alarm, two tiers:** *watch* (move to daily) when SOFR − IORB > +5 bp outside month-ends; *regime-break alarm* when > +10 bp outside quarter-ends |
| Financial conditions index (NFCI) | Yes: looser than in June, which contradicted "tightening" | **ADD — weekly** (lags; a cross-check, not a signal) |
| Global sovereigns (Bund, JGB, Canada 10Y) | Yes: refuted "the pressure is global" | **ADD — weekly** |
| Term premium model (Kim–Wright) | Helpful for decomposition; model-dependent and lagged | Weekly context only |
| Bank reserves | No — ample ($2.95T); matters near scarcity | Folded into the funding alarm |
| Cross-currency basis | Not observable reliably for free | **NOT NOW** |
| Dealer positioning | Weekly, lagged; its meaning changed with the 2026 eSLR rule | **NOT NOW** |
| Other commodity curves | Copper flat, gold in normal carry: no signal | **NOT NOW** |

**The five that matter:** the real/breakeven split, the priced Fed path, the credit-quality split, the broad dollar, and the oil curve slope. Auctions are the event gauge; funding is the alarm.

## 6. Thesis register — regime hypotheses and their states

States: **FORMING · ACTIVE · STRENGTHENING · WEAKENING · INVALIDATED · DORMANT.** No numeric scores. A state changes only with a written evidence note, and not on one noisy print unless the thesis explicitly depends on it. Three OPEN contradictions (§7) against the same thesis force a state review at the next DAILY STATE; they do not change the state automatically.

| Thesis | State (Oct 1) | Evidence note | Moves up if | Moves down if |
|---|---|---|---|---|
| **OIL SUPPLY SHOCK → FED REACTION** (upstream) | **FORMING** | The oil shock is real (WTI +34% since Jun 30) and the Fed hiked Sep 16, but its statement says only "Inflation remains elevated" and does not name energy. Headline 3.4% vs core 2.4% makes energy the likely source; the link is inferred | The Oct 28 statement or press conference cites energy/headline inflation; the 2Y moves with oil day to day (P8) | Oil falls and the strip does not move; or the Fed cites growth or a higher neutral rate (→ benign alternative) |
| **POLICY-LED REAL-RATE REPRICING** (base case; replaces Round 10's loose "rates are the shock") | **ACTIVE** | 2Y +74 bp; 10Y real +73 / breakeven +12; roughly 55% path / 45% term premium (Kim–Wright, Jun 30 → Sep 25) | 10Y keeps tracking the strip; real yields lead | 10Y rises with the strip flat (→ term premium story); or breakevens lead |
| **LONG-RATE STRESS TRANSMISSION** (term premium, buyers' strike, funding) | **FORMING** (not ACTIVE) | For: term premium +32 bp, a large minority (~45%) of the move; mild bear-steepening (2s10s +11 bp, 10Y−3M +50 bp); MOVE 108; private foreign selling of notes and bonds (−$29B, July); 20Y and 5Y tails. Against: 10Y/30Y stop-throughs; SOFR ≤ IORB | Long-end tails ≥ 2 bp with indirect < 65%; 10Y up while the strip is flat; funding alarm | Strong Oct 7/8 auctions; term premium flat for a month |
| **DURATION TURN** (PT-006, PT-009) | **DORMANT** | No M1/M2; strip still adding hikes; TLT at a 52-week-low close | Oil rolls over and the strip removes ≥ 1 hike; M1 met | — (already dormant) |
| **HOUSING TRANSMISSION** | **ACTIVE** | Mortgage 7.28–7.60%, spread stable; SLOOS residential demand weaker; ITB −14% in 3 months | Builder orders and margins fall in Q3 reports | Mortgage < 7% with the 10Y < 5% |
| **CCC TAIL REPRICING** | **ACTIVE** | CCC +209 bp since Jun 30; wider than March | B/BB widen; BKLN falls below its 52-week low (20.21) | CCC back under ~10.5% |
| **CREDIT STRESS (broad)** | **DORMANT** | IG +8 bp; loan prices flat; SLOOS unchanged; NFCI looser than June | IG OAS ≥ 1.00% and HY ≥ 3.75% together | — |
| **DOLLAR AS A TRANSMISSION CHANNEL** | **FORMING** | Broad dollar flat over the episode; +1.5% in September only | Broad dollar > 2% above its Jun 30 level with US−foreign spreads widening | Dollar falls while US yields rise (→ US risk-premium story) |
| **GOLD AS A RATE CASUALTY** | **WEAKENING** (Round 10 implied ACTIVE) | Gold +4% while real +73 bp; monthly moves track the dollar; central banks 289t in Q2 (+62% y/y) | Gold falls with real yields for a month with the dollar flat | Gold rises for a month with real yields rising → **INVALIDATED** |
| **BREADTH / RATE-SENSITIVE ROTATION** | **ACTIVE** | 23% above the 50-day; rate-sensitive sectors −6% to −14% in 3 months; QQQ +4% | Breadth < 20% with the index falling | > 50% above the 50-day while the 10Y holds ≥ 5% |
| **INDEX EARNINGS OFFSET** (the benign counterweight) | **ACTIVE** | Q3 EPS +29% est., raised during the quarter; P/E at its 10-year average; 62% positive guidance | Q3 beats and Q4 guidance broaden beyond tech and energy | Estimates cut in the season; P/E compresses with yields |
| **SYSTEMATIC DELEVERAGING** | **FORMING** (fuel without trigger) | Exposure at the 98th (Deutsche Bank) to 100th (BofA, secondary) percentile; VIX 16.4; realised vol low | VIX > 20 with realised vol rising and the index below its 50-day | Exposure normalises without a drawdown |
| **FUNDING / PLUMBING STRESS** | **DORMANT** | SOFR = IORB at quarter-end; SRF $1.2B; reserves $2.95T; RRP ≈ 0 | SOFR − IORB > +5 bp outside month-ends (watch) or > +10 bp outside quarter-ends (alarm); SRF > $10B | — |

**Last state changes (since the last weekly review; moved to `ROUNDS.md` at the weekly review)**
- None since the 2026-10-02 weekly review. The register-opening changes of 2026-10-01 were moved to `ROUNDS.md` (Weekly review — week ending 2026-10-02).

## 7. Contradictions (current: open and recently resolved)

A contradiction is not an error. It is an observation that differs from what our working explanation would normally imply. We record it, accumulate it, and do not rewrite the thesis on one. Repeated contradiction against the same thesis is evidence the model is weak.

**Lifecycle (revised Round 12):**
- **OPEN** — recorded; waiting for its discriminating evidence.
- **EXPLAINED** — the discriminating evidence named in the entry arrived and favoured an explanation compatible with the current model. **A new story without that evidence does not count:** the entry stays OPEN. This is the guard against explaining contradictions away.
- **MODEL UPDATED** — the evidence favoured an explanation the current model did not hold, and §1–§6 were changed. The entry names what changed.
- **INCONCLUSIVE** — the window closed (default six weeks unless the entry says otherwise) without discriminating evidence.

**Admission rule (Round 12).** A new contradiction must be against a **written** expectation that predates the observation: a link's confirmation or contradiction cell in §2, a prediction P1–P10 or condition W1–W5, or a thesis's up/down condition in §6. A divergence noticed by scanning many series is a *research note*, not a contradiction. This protects against noticing only the interesting variables.

*Round 11's vocabulary (OPEN · RESOLVED-FOR · RESOLVED-AGAINST · STALE) maps to OPEN · EXPLAINED · MODEL UPDATED · INCONCLUSIVE.*

*Round 12 re-screen (prompted by the lane-2 review).* Round 11 admitted all ten entries, but only five had an expectation written before the observation, in the committed Round 10 roster (`792fce3`): C-001, C-002, C-003, C-005, C-009. The other five (C-004, C-006, C-007, C-008, C-010) were expectations written beside the data. They are kept, because each names a discriminating test, but they are graded **RESEARCH NOTE** and do not count toward any thesis's three-contradiction review. **Half of Round 11's log was post-hoc — a concrete instance of the forking-paths risk.**

**C-001 · 2026-10-01 · Dollar · OPEN** (against DOLLAR AS A TRANSMISSION CHANNEL)
- *Grade (Round 12 re-screen):* **CONTRADICTION** — written beforehand in `792fce3` WATCHLIST §1: "the dollar is at a 52-week high", listed as a channel the rate shock was transmitting through.
- *Observed:* 10Y +85 bp since Jun 30, but the broad dollar is −0.5% (to Sep 25). DXY's 52-week high comes from euro weakness; the yen rose 3%.
- *Expected under the Oct 1 narrative:* a broad dollar rally.
- *Possible explanations:* (a) foreign yields rose too, keeping differentials stable; (b) the dollar is pricing a US-specific risk premium (fiscal) that offsets rate carry; (c) the dollar response is lagged — September's +1.5% is the start.
- *Discriminating evidence:* broad dollar vs the US−Bund and US−JGB 2Y spreads over October. (c) predicts a further broad rise; (b) predicts yields up and the dollar down on supply news (the refunding, Nov 4).

**C-002 · 2026-10-01 · Gold · OPEN** (against GOLD AS A RATE CASUALTY)
- *Grade:* **CONTRADICTION** — `792fce3` WATCHLIST: "gold is −4% over a month" listed as a transmission channel; gauge reading "real-yield/dollar pressure".
- *Observed:* 10Y real +73 bp since Jun 30, yet gold (front future) +4% (4,038 → 4,212). June's −12% came with the 10Y flat (but 5Y real +32 bp and the broad dollar +1.7%).
- *Expected:* gold falling with real yields.
- *Possible explanations:* (a) official-sector buying sets a floor (Q2 289t, +62% y/y; PBoC 22 months running); (b) gold trades the dollar month to month, not real yields; (c) a geopolitical hedge (LOOP-6) offsets opportunity cost.
- *Discriminating evidence:* the next month in which real yields and the dollar move in *opposite* directions. Gold following the dollar → (b). Gold flat through both → (a).

**C-003 · 2026-10-01 · Financial conditions · OPEN** (against "rate shock → tightening")
- *Grade:* **CONTRADICTION** — `792fce3` WATCHLIST gauge reading: "yields tightening conditions through the dollar".
- *Observed:* NFCI −0.548 (Sep 25) and STLFSI −0.81 are both looser than on Jun 30 (−0.514; −0.64).
- *Expected:* conditions tightening.
- *Possible explanations:* (a) equity strength and tight IG spreads outweigh rates in the index; (b) the index lags; the last week's HY widening is not in it; (c) the rate shock is being absorbed (benign alternative).
- *Discriminating evidence:* the NFCI for the weeks ending Oct 2 and Oct 9 (published Oct 7 and Oct 14). (b) predicts a jump; (c) predicts no change.

**C-004 · 2026-10-01 · Credit dispersion · OPEN** (against CCC TAIL REPRICING as a hiking-channel story)
- *Grade:* **RESEARCH NOTE** — the "floating-rate borrowers hurt first" expectation was written in Round 11 beside the observation. It does not count toward a thesis tally.
- *Observed:* CCC OAS +209 bp since Jun 30 (wider than in March's stress), while floating-rate loan prices (BKLN) are flat (total return +2.2%) and IG is +8 bp.
- *Expected under the hiking channel:* floating-rate borrowers (loans) hurt first.
- *Possible explanations:* (a) the CCC widening is sector-specific (not rate-driven); (b) loans lag because coupons reset upward and defaults come later; (c) the fixed-rate CCC tail faces a refinancing wall at much higher rates.
- *Discriminating evidence:* loan prices and default headlines over the next 4–6 weeks. BKLN below 20.21 supports (b). Stable loans with continued CCC widening supports (a) or (c).

**C-005 · 2026-10-01 · Earnings vs discount rate · OPEN** (against INDEX_DOWNSIDE, PT-005, and "rates pressure equities")
- *Grade:* **CONTRADICTION** — against the explanation written in `792fce3` WATCHLIST §1: "The headline index is held up by a narrow set of leaders and by mechanical positioning."
- *Observed:* the 10Y is at 5.24%, yet the S&P forward P/E is 19.2 (10-year average 19.0) and Q3 estimates *rose* 1.3% during the quarter (5-year norm −2.2%). The forward earnings yield (5.21%) ≈ the 10Y yield.
- *Expected:* multiple compression.
- *Possible explanations:* (a) earnings growth (+29% Q3, +32% CY26) is outrunning the discount-rate effect; (b) concentration: a few megacaps and energy carry the aggregate; (c) the equity risk premium is compressed and fragile.
- *Discriminating evidence:* the Q3 season (from mid-October). Broadening beats and guidance → (a). Beats confined to tech and energy with misses elsewhere → (b). P/E falling on in-line results → (c).

**C-006 · 2026-10-01 · Volatility split · OPEN** (against link 14)
- *Grade:* **RESEARCH NOTE** — Round 10 posed rate-vol → equity-vol as a *question*, not a prediction. The "within weeks" expectation was written in Round 11. (Round 10's "Calm" reading is corrected in §8; that is a description, not a failed prediction.)
- *Observed:* MOVE 108, near its March peak (115), while VIX is 16.4, half its March peak (31.1). VIX is ordinary (200-day 18.1), not "unusually calm". The anomaly is the gap.
- *Expected:* rate vol of this size reaches equity vol within weeks, as it did in March.
- *Possible explanations:* (a) earnings strength anchors equity vol; (b) systematic and short-vol positioning suppresses realised vol until it breaks (LOOP-3); (c) March was a joint oil-and-growth shock, while today is a policy-path shock that equities consider benign.
- *Discriminating evidence:* VIX on CPI (Oct 14) and FOMC (Oct 28) days. VIX > 20 with realised vol rising → (b). VIX steady while the MOVE falls → (c).

**C-007 · 2026-10-01 · Yen · OPEN**
- *Grade:* **RESEARCH NOTE** — no prior written expectation about the yen.
- *Observed:* the US−JGB 10Y spread widened (US +85 bp since Jun 30; JGB +27 bp since Jul 6), yet the yen rose 3% against the dollar.
- *Expected:* a wider differential weakens the yen.
- *Possible explanations:* (a) the BoJ hike (Sep 18, to 1.25%) narrowed *front-end* differentials; (b) repatriation (Japanese banks sold ~$70B of foreign bonds this year, per Reuters); (c) intervention risk above 160.
- *Discriminating evidence:* USD/JPY on US data surprises in October. If it stops responding to US yields, (b) gains.

**C-008 · 2026-10-01 · Oil vs breakevens · OPEN** (against "oil → inflation expectations → long yields")
- *Grade:* **RESEARCH NOTE** — the chain appeared only as an illustrative loop in ChatGPT's Round 11 prompt. Round 10 had already recorded that the move was mostly real yield.
- *Observed:* WTI +34% since Jun 30 and headline CPI 3.4%, but the 10Y breakeven rose only +12 bp; 5y5y is 2.36%.
- *Expected under the prompt's example chain:* breakevens leading yields higher.
- *Possible explanations:* (a) the steeply backwardated curve tells markets the shock is temporary; (b) the Fed's hike anchored expectations, so the transmission ran through real yields instead.
- *Discriminating evidence:* if breakevens rise > 2.5% while oil holds, the inflation-expectations channel is opening and the base case is re-specified ("the Fed is behind").

**C-009 · 2026-10-01 · Our own Round 10 narrative · OPEN**
- *Grade:* **CONTRADICTION** — `792fce3` WATCHLIST §1: "The pressure is global: JGB 10Y 3.10%, French OATs at 2002 highs."
- *Observed:* in the last month US 10Y +46 bp, Bund +15, JGB +8, Gilt +21, Canada +13. Only France (+65) and Italy (+47) kept pace.
- *Expected (Round 10 §1):* "the pressure is global".
- *Possible explanations:* (a) a US-specific policy shock; (b) global term premium plus a euro-periphery fiscal story.
- *Discriminating evidence:* on the next long-end selloff day, check whether Bund and JGB move ≥ half as much as the US.

**C-010 · 2026-10-01 · Rate vol vs mortgage spreads · OPEN**
- *Grade:* **RESEARCH NOTE** — no prior written expectation about MBS spreads.
- *Observed:* MOVE +65% in 3 months, while the mortgage–Treasury spread (~2.0 pp) and MBS OAS (MBB 38.5 bp, Sep 30; current coupon ~36 bp per Goldman, Sep 17) are unchanged.
- *Expected:* high rate vol widens MBS spreads through negative-convexity hedging.
- *Possible explanations:* (a) the deep-discount MBS universe (WAC 3.63%) has little prepayment optionality left; (b) bank and overseas MBS demand at these yields.
- *Discriminating evidence:* MBB underperforming IEF duration-adjusted by > 1% over a month while the MOVE stays > 100 → spread transmission returns.

**C-011 · 2026-10-02 · Route of the front-end repricing · OPEN**
- *Grade:* **RESEARCH NOTE.** No expectation written beforehand covered a labour-data repricing. The base case names oil → Fed (LOOP-1) as the most likely route to a duration turn. The benign alternative assumes a strong economy. It does not count toward any thesis tally.
- *Observed:* September payrolls +29k (consensus ~85–90k); July and August revised −60k; unemployment 4.2%; AHE +0.1% m/m (BLS, Oct 2). October-hike odds fell to 12–14% from ~70% early in the week (Reuters; CME FedWatch via Schwab). The 2Y fell 7 bp intraday (Reuters). **Causality is unclear:** WTI was already −3.9% at 06:00 ET (Yahoo), before the 08:30 ET release, and the G7 reserve release came the same day. The sources attribute the hike repricing to payrolls (INTERPRETATION by the sources). Oil and labour cannot be separated for this session.
- *Expected:* under the base case, hikes come out when oil rolls over. Under the benign case, real rates are held up by strong growth. Neither model has a node for a labour-market shock removing hikes.
- *Possible explanations:* (a) a growth/labour route to the duration turn exists alongside LOOP-1 (LOOP-5's "growth ↓ → policy path ↓" leg, reached through labour rather than housing); (b) a one-day repricing that reverses if CPI (Oct 14) runs hot; (c) the Fed's reaction function is energy-led (P10), so labour softness only delays hikes and does not remove them.
- *Discriminating evidence:* the strip after CPI (Oct 14) and the Oct 28 rationale (P10). If hikes stay out with oil > $80, (a) gains and the base-case route needs re-specifying. If hikes return on a hot CPI, (b) or (c). Window: to Nov 4.
- *Unresolved companion observation:* the long end's Oct 2 close is UNMEASURED. TLT was −0.36% at 15:36 ET after +0.8% intraday, so the long end may not have followed the front end (bear-steepening). Read FRED DGS2, DGS10 and DGS30 for Oct 2 before drawing any inference.

**Tally (Oct 2):** 11 OPEN — 5 CONTRADICTIONS (C-001 dollar channel, C-002 gold, C-003 tightening, C-005 index support, C-009 "global") and 6 RESEARCH NOTES (C-004, C-006, C-007, C-008, C-010, C-011). No thesis has three contradictions.

## 8. Adversarial challenge to the Oct 1 narrative (mandatory, Round 11 §14)

**The narrative under test:** "rate shock → stronger dollar / weaker duration / weaker gold / deteriorating breadth / rising credit pressure, while equity volatility remains unusually calm."

| Component | Verdict | Evidence |
|---|---|---|
| Rate shock | **CONFIRMED, renamed** | A policy-led real-rate repricing: 2Y +74 bp, real +73 bp, breakeven +12 bp; term premium a large minority (~45%, model-dependent) |
| Stronger dollar | **DOWNGRADED** | September only; broad dollar flat over the episode; euro-led; yen stronger (C-001, C-007) |
| Weaker duration | **CONFIRMED** (mechanical) | TLT −8.4%, IEF −4.5% in 3 months; 52-week-low closes |
| Weaker gold | **DOWNGRADED** | September only; gold's level ignored +73 bp of real yield (C-002) |
| Deteriorating breadth | **CONFIRMED, reinterpreted** | The transmission showing up in rate-sensitive sectors, not on its own an index signal (C-005) |
| Rising credit pressure | **NARROWED** | CCC tail and the last week's HY; not IG, loans, bank lending or FCIs (C-003, C-004) |
| Equity vol "unusually calm" | **CORRECTED** | VIX is ordinary; the anomaly is MOVE near March's peak with VIX at half its March level (C-006) |
| "The pressure is global" (Round 10 §1) | **DOWNGRADED** | US-centred; France and Italy are a separate story (C-009) |

**The seven questions**
1. **Are Treasury buyers stepping in aggressively?** No, but they are not on strike either.
   - For a strike: the 20Y (Sep 15) tailed 2.0 bp and the 5Y (Sep 23) 3.1 bp. Private foreign investors sold $29B of notes and bonds in July. China's holdings ($618B) are the lowest since 2008. Japanese banks sold ~$70B of foreign bonds this year. Leveraged basis books are down ~20% (Morgan Stanley via Reuters).
   - Against a strike: the 10Y and 30Y stopped through on Sep 9–10 with 79.2% and 79.5% indirect. The 2Y and 7Y tailed only 0.2 and 0.7 bp. Foreign official buyers added $44B in July. Dealers have balance-sheet room after the eSLR change.
   - Demand is price-sensitive and clears at higher yields. Next tests: Oct 7 (10Y), Oct 8 (30Y), Oct 16 (TIC for August), Nov 4 (refunding).
2. **What is the long end pricing?** Mostly the policy path in real terms: roughly 55% path / 45% term premium (Kim–Wright, matched window Jun 30 → Sep 25; model-dependent); real +73 bp vs breakeven +12 bp. Supply and foreign flows live inside the term-premium share, which is a large minority, not a rounding error. Inflation expectations contribute little. The move is US-centred.
3. **Is gold weakness rate-driven?** Partly, at best. September fits. But over three months gold rose against +73 bp of real yield, its monthly moves track the dollar, and central-bank buying (Q2 289t) is a non-rate bid. Dustin's metals are not a clean rates bet in either direction.
4. **Is credit deteriorating or repricing?** Repricing, with a deteriorating tail. IG +8 bp and LQD's loss ~90% duration; loan prices flat; bank standards unchanged; NFCI looser. The CCC tail (+209 bp, wider than in March) is the real deterioration. The last week's HY move *may* be the first sign of it spreading — a hypothesis that C-004 will test.
5. **Does weak breadth matter if megacap earnings are strong?** Less for the index than the narrative implied. Q3 estimates are rising, positive guidance is far above its five-year average (72 companies vs an average of 43; 44 negative), and the P/E sits at its 10-year average. Breadth weakness is concentrated where rates bite. It matters as the transmission's footprint and as PT-005's evidence, but it needs the leaders to stumble to become an index signal.
6. **Are vol-control flows large enough to matter?** As a trigger, no; as an amplifier, yes.
   - The sizing rule is mechanical, and exposure is at the 98th (Deutsche Bank) to 100th (BofA, secondary) percentile.
   - The largest estimate seen (~$163B, BofA via a secondary source) is about 13% of one day's US equity value traded ($1.29T/day in June). Spread over a week, that is a few percent of daily volume.
   - It can deepen a fall that something else starts; it is unlikely to start one, because it needs realised vol to rise first.
7. **What would the benign interpretation look like?** Below.

**BASE CASE — policy-led real-rate repricing, most likely triggered by the oil supply shock.**
- OBSERVED: WTI +34% since June; Brent above $100; headline CPI 3.4%. INTERPRETATION: an oil supply shock (Hormuz and Middle East shut-ins, per secondary reports) pushed headline inflation up.
- OBSERVED: the Fed hiked with core CPI at 2.4%. Its statement says only "Inflation remains elevated" and does not name energy, so the oil → Fed link is our inference (OIL → FED REACTION — FORMING).
- DERIVED: futures price ~2½ more hikes by mid-2027; the 10Y rose ~85 bp, almost all real. MODEL ESTIMATE: roughly 55% expected policy path, 45% term premium.
- INTERPRETATION: the shock shows where the link is mechanical, or plausible and observed: mortgages, homebuilders, small caps, the CCC tail.
- It has *not* reached IG credit, bank lending, funding markets or aggregate financial conditions. At the index, earnings growth (+29% Q3 est.) has so far offset the discount-rate effect (C-005, open).
- The dollar and gold readings were over-stated.
- The system is fragile in two places, the CCC tail and record systematic equity exposure, but neither has a trigger yet.
- PREDICTION (tested by P6, P8): the shock is **self-limiting through LOOP-1**: if oil rolls over, the strip unwinds and duration turns.

**BEST ALTERNATIVE EXPLANATION — growth-led normalisation (benign).**
- Real yields are rising because the economy and profits are strong (CY26 EPS +32%, estimates rising, positive guidance far above its five-year average), and the market is pricing a higher neutral rate.
- The Fed is normalising, not squeezing. The market absorbs it: long-end auctions clear, funding is calm, IG is tight, FCIs are loose, VIX is ordinary.
- Weak breadth is rotation toward earnings winners. CCC widening is the normal cost of higher rates for the weakest borrowers. Gold's drop is positioning after a parabolic run (January's 5,318 high), not rates.
- On this view nothing cascades. The "shock" is a level shift that persists **even if oil falls**, because growth, not oil, sets the real rate.

**Second alternative — fiscal/term-premium stress (bearish), kept for completeness.**
- The long end reprices for supply: deficits, a bills share of 22%, private foreign selling, Japanese repatriation and the basis trade shrinking. The Fed hike is a sideshow.
- It ends in a funding or market-function accident.
- It is less supported than the base case, but not by a wide margin. For it: term premium is a large minority (~45%), and the curve has bear-steepened mildly (2s10s +11 bp, 10Y−3M +50 bp). Against it: the long-end auctions cleared and SOFR sits at IORB.

**WHAT WOULD DISTINGUISH THEM**

| Observation (next 4–6 weeks) | Base case predicts | Benign predicts | Stress predicts | When |
|---|---|---|---|---|
| WTI front-month below $80 (≈ −14%) | Strip removes ≥ 1 hike, 10Y −25 bp or more | Yields stay high (growth sets them) | Long end stays high or rises; curve steepens | Any time |
| **Daily oil vs 2Y co-movement through October** (unconditional) | 2Y moves with oil on big oil days | 2Y ignores oil; responds to growth data (payrolls, retail sales) | 10Y moves without the 2Y | End of October |
| **Oct 28 FOMC statement and press conference** | Rationale cites energy or headline inflation | Rationale cites growth strength or a higher neutral rate | Cites market functioning or Treasury liquidity | Oct 28 |
| Strip-repricing days (CPI Oct 14, FOMC Oct 28) | 10Y moves ≥ 0.6× the 2Y, same direction | Same | 10Y moves independently of the 2Y | Event dates |
| Q3 earnings and Q4 guidance | Cuts in rate-sensitive and consumer sectors | Beats broaden beyond tech and energy | Irrelevant to the long end | Mid-Oct → mid-Nov |
| CCC and HY OAS | CCC keeps widening; HY drifts toward 3.5% | CCC stabilises; HY back under 3% | IG > 1.0–1.1% joins | Weekly |
| Breadth (% above 50-day) | Stays weak while the 10Y > 5% | Recovers > 50% with the 10Y ≥ 5% | Collapses with the index | Daily |
| Long-end auctions (Oct 7–8) and refunding (Nov 4) | Normal | Normal or strong | Tails ≥ 2 bp, indirect < 65%; coupon sizes raised | Event dates |
| Dollar | Firm with front-end spreads | Firm | Falls while US yields rise | Daily |
| Gold | Tracks the dollar | Tracks the dollar | Rises with yields (fiscal hedge) | Monthly |
| Funding | Quiet | Quiet | SOFR − IORB > +10 bp outside quarter-end (alarm tier) | Weekly |
| Breakevens | 2.2–2.5% | 2.2–2.5% | Rising with term premium | Daily |

**Falsifiable predictions if the base case is right (to the Nov 4 refunding):**
- **P1.** 2s10s stays between 25 and 65 bp while yields stay elevated: the long end follows the front end.
- **P2.** The 10Y breakeven stays 2.20–2.50%.
- **P3.** IG OAS stays < 1.00%; HY OAS stays between 2.90% and 4.00%.
- **P4.** The mortgage–Treasury spread (Freddie Mac − 10Y) stays 1.8–2.3 pp.
- **P5.** ITB and IWM underperform SPY while the 10Y ≥ 5.0%.
- **P6 (LOOP-1 test).** If WTI front-month closes below $80 with its 12-month backwardation narrowing, the strip removes ≥ 1 hike and the 10Y falls ≥ 25 bp within two weeks.
- **P7.** Funding stays quiet: SOFR ≤ IORB + 5 bp outside month-ends.
- **P8.** On at least 60% of the October sessions when the WTI front month moves ≥ 2%, the 2Y moves in the same direction.
- **P9.** On CPI (Oct 14) and FOMC (Oct 28) days, the 10Y moves at least 0.6× the 2Y, in the same direction.
- **P10.** The Oct 28 statement or press conference attributes "elevated" inflation to energy or headline pressures rather than to strong growth or a higher neutral rate.

*Which predictions separate which explanations:* P1–P4, P7 and P9 are shared with the benign alternative; they test the base case only against the stress alternative. **P5, P6, P8 and P10 are the ones that separate the base case from the benign alternative.** P8 and P10 do not depend on oil falling, so the base case cannot go untested through the window.

**What would make us admit the base case is wrong:**
- **W1.** WTI front-month falls below $80 and the 10Y does not fall (or rises) → term premium/supply, not the policy path, is driving. The stress alternative gains; the benign one gains if credit and breadth also improve.
- **W2.** IG OAS > 1.10%, or SOFR − IORB > +10 bp outside quarter-end (the alarm tier) → the stress alternative.
- **W3.** Breadth recovers to > 50% above the 50-day while the 10Y holds ≥ 5.0% and CCC tightens → the benign alternative.
- **W4.** Breakevens > 2.60% with oil up → the inflation-expectations channel has opened (2.50–2.60% is a watch zone between P2 and W4). The base case is re-specified as "the Fed is behind", which is a different regime.
- **W5.** P8 fails (the 2Y ignores oil through October) **and** the Oct 28 rationale cites growth or a higher neutral rate → the benign alternative replaces the base case.

**Prediction tracker (Round 13).** Updated by the daily cycle whenever a prediction resolves. Statuses: PENDING · HIT · MISS · VOID (its condition never arose).

| ID | Prediction (short) | Separates base case from | Resolves by | Status |
|---|---|---|---|---|
| P1 | 2s10s stays 25–65 bp | Stress | Nov 4 | PENDING |
| P2 | 10Y breakeven 2.20–2.50% | Stress | Nov 4 | PENDING |
| P3 | IG OAS < 1.00%; HY 2.90–4.00% | Stress | Nov 4 | PENDING |
| P4 | Mortgage − 10Y spread 1.8–2.3 pp | Stress | Nov 4 | PENDING |
| P5 | ITB and IWM underperform SPY while the 10Y ≥ 5.0% | **Benign** | Nov 4 | PENDING |
| P6 | WTI < $80 → strip −1 hike and 10Y −25 bp within 2 weeks | **Benign** | Conditional | PENDING (condition not met; WTI intraday low 88.06 on Oct 2) |
| P7 | SOFR ≤ IORB + 5 bp outside month-ends | Stress | Nov 4 | PENDING |
| P8 | ≥ 60% of October's ±2% WTI days see the 2Y move the same way | **Benign** | Oct 30 | PENDING. Qualifying days so far: **0 of 1 same direction**. Oct 1: WTI +2.7% (settlement 92.87, fxstreet), 2Y −10 bp (4.88 → 4.78) — opposite. Oct 2: qualification UNMEASURED (WTI −1.6% to −4% intraday; settlement unread); if it qualifies, the 2Y moved the same way, with oil and payrolls confounded (C-011) |
| P9 | On CPI and FOMC days the 10Y moves ≥ 0.6× the 2Y, same direction | Stress | Oct 28 | PENDING |
| P10 | The Oct 28 rationale cites energy or headline inflation | **Benign** | Oct 28 | PENDING |

| Condition | Status |
|---|---|
| W1–W5 (admit the base case is wrong) | None triggered (Oct 2). W2 and W4 could not be read on Oct 2 (IG OAS and breakeven UNMEASURED); last read not triggered on Oct 1 |

**Review:** on the DAILY STATE each session; a full re-run of this section after the FOMC (Oct 28) and the refunding (Nov 4), or earlier if W1–W5 fires.

---

## Sources (Round 11, read 2026-10-01)

- **FRED series:**
  - yields: DGS2/10/30, DFII5/10/30, T5YIE, T10YIE, T5YIFR, T10Y2Y, T10Y3M;
  - credit spreads: BAMLH0A0HYM2, BAMLC0A0CM, BAMLC0A4CBBB, BAMLH0A3HYC;
  - term premium and conditions: THREEFYTP10, NFCI, ANFCI, STLFSI4;
  - mortgage: MORTGAGE30US;
  - funding: SOFR, IORB, DFF, WRESBAL, RRPONTSYD, WTREGEN;
  - dollar and FX: DTWEXBGS, DEXJPUS, DEXUSEU;
  - oil: DCOILWTICO, DCOILBRENTEU.
  - Links: https://fred.stlouisfed.org
- **Yahoo Finance daily history:**
  - ETFs and indices;
  - futures curves: CL, BZ, GC, NG, HG, ZQ;
  - FX.
  - Read live in the browser, Oct 1.
- **iShares fund pages (Sep 30):** [TLT](https://www.ishares.com/us/products/239454/), [IEF](https://www.ishares.com/us/products/239456/), [HYG](https://www.ishares.com/us/products/239565/), [LQD](https://www.ishares.com/us/products/239566/), [MBB](https://www.ishares.com/us/products/239465/).
- [FactSet Earnings Insight, Sep 25, 2026](https://advantage.factset.com/hubfs/Website/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_092526.pdf).
- [Edward Jones weekly, Sep 11 (August CPI)](https://www.edwardjones.com/us-en/market-news-insights/stock-market-news/stock-market-weekly-update-9-11-2026).
- [Fed SLOOS, July 2026](https://www.federalreserve.gov/data/sloos/sloos-202607.htm).
- [Fed statement, Sep 16](https://federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm).
- [Fed Monetary Policy Report, July](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm).
- **Treasury:**
  - [TIC release](https://home.treasury.gov/news/press-releases/sb0631);
  - [August refunding statement](https://home.treasury.gov/news/press-releases/sb0590);
  - [TBAC deck Q3](https://home.treasury.gov/system/files/221/TreasuryPresentationToTBACQ32026.pdf).
- [NY Fed SOFR](https://markets.newyorkfed.org/api/rates/secured/sofr/last/6.json) and [repo operations](https://markets.newyorkfed.org/api/rp/repo/all/results/last/10.json).
- [TradingEconomics bond yields](https://tradingeconomics.com/bonds) (page read Oct 1, 2026; its header misprints the year).
- **Fed-decision odds:** [Kalshi/Polymarket via DeFi Rate](https://defirate.com/prediction-markets/fed-decision-odds/snapshot/2026-09-27T1313/) (snapshot Oct 1, 08:17 ET; prediction markets, not CME FedWatch).
- **Further sources:**
  - [TIC table 5, China/Japan holdings](https://ticdata.treasury.gov/resource-center/data-chart-center/tic/Documents/slt_table5.html).
  - JGB 10Y on Jul 6 ([adnkronos](https://english.adnkronos.com/2026/07/06/key-10-year-jgb-yield-hits-29-year-high-of-2-830-pct/)).
  - BoJ hike to 1.25% on Sep 18 ([Nation Thailand](https://www.nationthailand.com/news/world/40071184)).
  - Fed reserve-management purchases paused ([The Star, Sep 16](https://www.thestar.com.my/business/business-news/2026/09/16/fed-extends-pause-on-reserve-management-purchases-to-october)).
- **Carried forward from Round 10** (see `ROUNDS.md` Rounds 5–10):
  - vol-control exposure at the 98th percentile since 2010 (Deutsche Bank data via Reuters, Oct 1);
  - S&P breadth (thetrading.tools, Oct 1);
  - the MND daily mortgage rate;
  - ITB trailing P/E and TLT implied volatility (option chains read live Oct 1).
- **Secondary reports:**
  - Treasury demand: [Reuters via wtvbam, basis trade, Sep 24](https://wtvbam.com/2026/09/24/analysis-hedge-funds-sour-on-basis-trade-as-treasury-selloff-continues/); [Reuters via devdiscourse, Japan repatriation, Sep 25](https://www.devdiscourse.com/article/international/3982589-analysis-japans-bond-falling-knife-stalls-repatriation-rush).
  - Auctions: [Newsquawk 2Y](https://www.newsquawk.com/headlines/us-sells-usd-69bln-of-2yr-notes-tail-02bps) and [7Y](https://www.newsquawk.com/headlines/us-sells-usd-44bln-of-7-year-notes-tail-07bps); [Vault Report September auctions](https://thevaultreport.com/treasury-auctions/2026-09).
  - Gold: [gold June decline](https://profit.pakistantoday.com.pk/2026/06/30/gold-heads-for-worst-monthly-fall-since-2008-as-rate-hike-bets-strengthen); [central-bank buying Q2](https://www.cruxinvestor.com/posts/66-rate-hike-odds-push-gold-lower-central-banks-bought-289-tonnes) (its "July record $5,589" conflicts with Yahoo's front-future high of 5,318 on Jan 29 and is not used).
  - Oil: [oil supply drivers, Sep 12](https://www.psuconnect.in/market/crude-oil-price-today-12-september-2026-brent-holds-near-104-wti-at-100).
  - Systematic flows: [BofA systematic-selling estimate via CryptoBriefing](https://cryptobriefing.com/bank-of-america-163b-stock-risk/).
  - Market depth: [Rosenblatt, June 2026 volumes](https://www.rblt.com/market-structure-reports/us-securities-volumes-june-2026).
  - Bank capital: [BNP on eSLR, Jun 10](https://economic-research.bnpparibas.com/html/en-US/US-regulatory-easing-offers-limited-support-Treasuries-market-6/10/2026,53537).
