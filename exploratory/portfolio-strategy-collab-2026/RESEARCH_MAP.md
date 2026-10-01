# Research Map

**Current understanding, not history.** `ROUNDS.md` is the record of how we got here; this file
is what matters now. Both Claude and ChatGPT should be able to read it cold and recover the state
of every idea. Update it in place; record material changes in one line in `ROUNDS.md`.

**Last updated:** 2026-10-01 (Round 7 — Claude, Opus 5.5)

---

## What are we becoming experts in? (provisional)

Working answer after seven rounds: **how prices behave when information or regimes change** —
- **discrete events:** earnings repricings and event shocks (Programs A, F);
- **trend structure in a few genuine secular leaders:** pullbacks and reclaims (Program B);
- **slow macro transitions:** rates/duration (Program C) and breadth/index regime (Program G, candidate);
- **long-horizon investing core:** businesses that monetise activity or contracted demand rather than requiring a forecast of direction (Programs D, E).

The first three produce evidence quickly; the last is where capital compounds. The Round 10
checkpoint tests whether this answer still holds.

---

## Research universe vs deployment universe

| | Research universe | Deployment universe |
|---|---|---|
| Scope | Broad: any liquid listed instrument, any price, any option premium | Narrow: what the capital, permissions, liquidity, tax, risk budget and execution allow today |
| Constraints exist to | Protect evidence quality (timestamps, liquidity, no hindsight) | Protect capital |
| Valid outcomes | Thesis confirmed / invalidated / unresolved | Trade · NO TRADE · **GOOD OPPORTUNITY / CURRENTLY CAPITAL CONSTRAINED** · **GOOD STRATEGY / REQUIRES LARGER ACCOUNT** |

A strategy is never distorted to fit today's account. MU (PT-003) is the current example of
"requires larger account". Funding a constrained opportunity by selling something else is a
separate decision (`PROPOSAL.md` §6, capital unlocking).

---

## Active research programs

Families (`PAPER_TRADES.md` §5) map to programs; one program can hold several families.

| Program | Families | Frequency | Typical hold | Plausible edge | Data needed | Capital scalability | Major failure mode |
|---|---|---|---|---|---|---|---|
| A · Earnings repricing | EARNINGS_CONTINUATION | High — dozens of large gaps each quarter | 2–8 weeks | Slow institutional repositioning after a de-risking print (post-earnings drift) | Earnings calendar, consensus, implied move, day-1 OHLCV + VWAP, 20-session follow-through | Medium–high (liquid large caps) | Confusing short-covering spikes with repricing; small samples; a documented anomaly that may already be arbitraged in large caps |
| B · Secular-leader pullbacks and reclaims | TREND_PULLBACK, BROKEN_LEADER_RECLAIM | Medium — a few per month across 10–20 leaders | 3–12 weeks; can become investments | Trend persistence in names with rising estimates | Daily OHLCV, moving averages, relative strength, estimate revisions | High | Catching broken momentum; leaders correlated with each other (AI hardware) |
| C · Rates / duration regime | MACRO_DURATION_TURN | Rare — one or two regime turns a cycle | 1–6 months | Convexity at a genuine long-end turn; cheap liquid options (TLT IV ~16%) | Treasury par/real curves, term premium, MOVE, auctions, Fed path, mortgage rates, Market Brief rates block | High | Buying "high yields" before the trend turns; fiscal/term-premium drivers that outlast the Fed |
| D · Market infrastructure (tollbooths) | TACTICAL_COMPOUNDER_ENTRY (+ strategic holds) | Monthly data; quarterly decisions | Years | Monetising activity without predicting direction; operating leverage; proprietary products | Monthly ADV/RPC releases, segment revenue, data revenue, capital returns | High | Paying peak multiples at peak volumes; competition or regulation of a franchise product |
| E · Contracted energy and power infrastructure | (strategic holds) | Quarterly | Years | Long-dated contracted cash flows plus permitted growth, bought at a toll-road multiple | Filings (contract %, tenor, fee structure), permits, financing, global supply schedule | High | Mistaking commodity or merchant exposure for contracted cash flow; financing costs; supply waves |
| F · Post-shock / special situations (exploratory) | POST_SHOCK_REVERSAL | Low–medium | 4–10 weeks | Overshoot after forced selling | Event detail, estimate cuts, positioning, post-event price structure | Low–medium | High information cost per trade; "down a lot" mistaken for "cheap"; contaminated indicators |
| G · Breadth and index regime (candidate, new Round 7) | INDEX_DOWNSIDE | Rare | 2–6 weeks | Index catching down to weak breadth when rates are restrictive | Breadth series (% above 50/200-day), RSP vs SPY, VIX term structure, rates; market-review hypotheses H1–H5 | Medium | Narrow leadership can persist for years (2023–24); short-side path dependence |

### A · Earnings repricing
**Question:** when an earnings report causes a large repricing, what distinguishes institutional continuation from a one-day reaction?
**State:** active. PT-001 ACN is pending its day-1 close (Oct 1). Its likely expiry on a gap-and-fade day becomes the first shadow observation. The Oct–Nov cohort below is the forward sample.
**Two layers, deliberately separated:**
- **Event layer — every cohort event, both directions, whether or not anything triggers.** This prevents conclusions being drawn only from trades that fired (selection bias).
- **Trade layer — Setup A records, long only as frozen.** Pre-registered mechanically: **every cohort name ≥ 25% below its 52-week high at the close before its report** gets a Setup A record written that evening. UNH is pre-registered regardless (owner instruction) and its frozen qualifier decides the outcome.

**Event-layer capture (fixed before the first event):**
- **Pre-event (prior close):** % from 52-week high; position vs 50/200-day; consensus EPS and revenue; implied move from the nearest-expiry at-the-money straddle.
- **Event:** gap % at the open; result vs consensus; guidance change; day-1 volume ÷ 3-month average; day-1 close location in the range (0 = low, 1 = high); close vs day-1 VWAP if available; day-1 return minus SPY.
- **Follow-through:** returns at +5, +10 and +20 sessions from the day-1 close; whether days 2–5 held the completed day-1 low; whether a close beyond the day-1 high (low, for gap-downs) occurred within 10 sessions.

**Outcome labels (frozen):**
- **CONTINUATION** — the +20-session close is beyond the day-1 close in the gap's direction.
- **REVERSAL** — the gap is fully filled (the prior close is crossed) within 20 sessions.
- **NEUTRAL** — anything else.

**Key open questions:**
- Does day-1 close location predict the 20-session outcome?
- Does a gap larger than the implied move behave differently?
- Do damaged names (≥ 25% below their high) continue more than leaders?
- Do gap-downs mirror gap-ups?

**Worth deeper study if:** after ~20 event-layer observations, one or two day-1 variables separate CONTINUATION from REVERSAL with a clear margin. That triggers a pre-registered retrospective study under `docs/conventions.md`.

### B · Secular-leader pullbacks and reclaims
**Question:** can we enter genuinely powerful long-term trends during temporary weakness without catching broken momentum?
**State:** active, four WATCH records:
- TREND_PULLBACK: MU (PT-003), CLS (PT-010) — both extended, no pullback yet.
- BROKEN_LEADER_RECLAIM: VRT (PT-002), HWM (PT-008) — basing below their averages.

**Key open questions:**
- Do broken-leader reclaims behave like trend pullbacks, or like new and weaker trends?
- How much does sector context matter? MU, CLS and TSM are one AI-hardware factor.
- What should rank candidates in a large universe: estimate revisions or relative strength?

**Worth deeper study if:** both families produce completed observations with clean timing records. Then a retrospective study on a defined leader universe becomes worth running, because this is the most capital-scalable program.

### C · Rates / duration regime
**Question:** can we recognise the transition from a rising-rate regime to a duration-positive regime early enough to act, without catching falling bonds?
**State:** WATCH (PT-006 TLT, PT-009 ITB — one family, one shared condition M1).

**Evidence as of Oct 1:**
- 10Y 5.29% on Sep 30 (a 24-year high) and 5.24% intraday Oct 1.
- About 73 of the 85 bp Q3 rise in the 10Y was real yield.
- MOVE at records; the Fed hiked on Sep 16.
- TLT and ITB both printed new 52-week lows Oct 1, then recovered.

**Market Brief / market-review inputs (read-only):** the daily Treasury par-curve table and hypotheses H1 (the long end is restrictive) and H2 (rates vol is elevated relative to equity vol).
**CME** sits in this program as a business counterweight: it is paid while the rate path stays active, and duration pays when it turns.
**Key open questions:**
- What preceded past long-end tops (Oct 2023, 2006–07, 1994–95)?
- Do homebuilders or mortgage spreads lead TLT?
- How much of the move is foreign long-end pressure (JGB 10Y 3.10%, OAT at 2002 highs)?
**Worth deeper study if:** always — rare but high-convexity. The study of past tops is the next step regardless of triggers.

### F · Post-shock / special situations (exploratory — must earn attention)
**Question:** can severe event-driven repricings produce repeatable opportunities after the first forced move?
**State:** PT-004 FICO WATCH (session 2 of 10 on Oct 1). FICO reports around Nov 4 (vendor estimate), so this program overlaps Program A's cohort.
**Earn-or-retire test at Round 10:** at least one completed observation with a clean timing record **and** the indicator study (below) scoped with a data source. Otherwise the program moves to the research queue.

### G · Breadth and index regime (candidate — added Round 7)
**Why added:** PT-005 (INDEX_DOWNSIDE) had no program, and market-review hypotheses H3–H5 are its live evidence:
- 21% of S&P members above their 50-day while the index sits ~2% from its high;
- about 75% of members fell in September;
- VIX ~16 against a record MOVE.

**Question:** does extreme narrow breadth with restrictive rates and calm equity vol precede index drawdowns often enough to trade with defined risk?
**Status:** candidate. It becomes a program at Round 10 only if the breadth statistic is verified and a historical sample exists.

---

## Long-horizon theses

### D · Market infrastructure (tollbooths)
**Claim:** exchanges, index/data and clearing businesses are attractive long-horizon holdings because they monetise financial activity rather than requiring a forecast of its direction.

**Evidence:**
- Adjusted EPS 2018–2025 (company releases): of the seven year-on-year changes, CBOE rose in 6 and CME in 4. Both run ~65% operating margins.
- Cboe's index options ADV grew from ~1.9M (2019) to 4.9M (2025), a structural rise driven by 0DTE (~60% of SPX volume) and retail.
- CME's rates ADV grew 9,951k → 14,200k (2018–2025).
- Proprietary franchises: SPX/VIX licensed to Cboe through 2051; CME's Treasury and SOFR complex.

**Counterevidence:**
- CME's EPS was flat 2019–2021, including a VIX-29 year, so these businesses are not "volatility = profit".
- Q2 2026 showed CME clearing fees −2.6% y/y while market data rose 20%; revenue does not track ADV one-for-one because of rate per contract (RPC), mix and tiering.
- The 2018–2025 history is eight observations of several entangled variables (policy, rate level, retail growth, pricing actions) and supports no causal claim.

**Business engines to study, not regime labels:**
- volume (secular vs cyclical);
- pricing and RPC;
- proprietary vs multi-listed products;
- recurring data revenue (CME ~14% of revenue, Cboe Data Vantage ~24% of net revenue);
- clearing economics;
- operating leverage;
- capital returns (CME ~4% total yield including its variable dividend; Cboe a smaller dividend plus net cash).

**Candidates:**
- **CBOE** — held. Structural index-options growth with an equity-vol kicker.
- **CME** — approved. Active-rate-path engine; Strategy F trigger ≤ ~$220.
- **ICE** — second choice. Mortgage tech gives it a rates-turn kicker.
- **SPGI** — damaged quality, −29.5% from its high. Indices +20%; Ratings depends on issuance.

**What would invalidate it:** secular volume growth stalling across the group for 4+ quarters while multiples stay above the market's; a regulatory cap on fees or on 0DTE; loss of a proprietary franchise.

**Data stream:** CME and Cboe publish monthly volume on about the second business day of each month, giving this long-horizon program monthly evidence.

### E · Contracted energy and power infrastructure
**Claim:** long-duration growth in energy and power demand can be captured through contracted infrastructure rather than commodity bets.

**Evidence (Cheniere filings, 2025–26):**
- 90% or more of anticipated production is contracted, with ~15-year weighted-average remaining life.
- Fixed fees are payable even if cargoes are cancelled.
- Margin sensitivity is < $50M EBITDA per $1/MMBtu.
- The Sabine expansion is pre-sold for Phase 1 and awaiting FERC/DOE.
- US LNG exports rose 23% in H1 2026 (EIA).

**Counterevidence:**
- A global LNG supply wave lands in 2028–30, when Cheniere's own expansion arrives.
- IPM volumes are international-index-linked, and their share is not disclosed.
- $24B of debt refinances at 5%+ rates.
- WMB shows the opposite failure: 28x forward with negative FCF. "Contracted" is not the same as "cheap".

**Separate always:** contracted cash flow · commodity exposure · expansion economics · financing · regulatory risk · execution · customer concentration.

**Candidates:**
- **LNG** — held. LNG-A carries the position; LNG-B is upside.
- **WMB** — rejected on price.
- **To study later:** contracted versus merchant power (CEG and VST are largely merchant/PPA hybrids); grid equipment (ETN, GEV) is a capex cycle, not a contracted stream.

**What would invalidate it:** contracted share < ~85% or tenor < ~12 years at LNG; expansion permits denied; a supply wave that forces recontracting below current fixed fees.

---

## Methodology findings (preserved observations that revealed them)

1. **Post-shock indicator contamination** (revealed by PT-004 FICO).
   - **Observation:** a 20-day average after a discrete price break is dominated by pre-break prices. FICO's was ~898 on Oct 1 against a 670 price; even with a flat price it reaches ~771 by Oct 13 and ~666 by Oct 27. A "reclaim the 20-day" rule therefore waits on calendar time, not price behaviour.
   - **Same issue elsewhere:** any trailing-window statistic straddling a regime break — IV rank (TLT at 96–100 after a rates-vol regime shift), "% below 52-week high", ATR after a gap.
   - **Research question:** when a discrete event changes the price regime, which trend measures stay informative and which are mechanically contaminated?
   - **Candidates to test (none chosen):** anchored VWAP from the shock day; post-event high/low structure; short post-event averages once enough sessions exist; base length with range contraction; relative strength vs sector; realised-volatility contraction.
   - **Test design:** a pre-registered retrospective study of large-cap single-day shocks ≤ −20% on discrete events. Compare each candidate's forward 20/60-session behaviour against the 20-day-reclaim rule. Track the candidates alongside PT-004 as observations only. PT-004 is not changed.
2. **Mutable intraday references** (revealed by PT-001 ACN).
   - **Observation:** the plan froze "214.50 (gap-day low)" mid-session; the completed low was lower (213.59 by 14:49 ET).
   - **From Round 7, every level is one of three types:**
     - **Fixed known price** — "ACN low as of 13:30 ET = X". The number is frozen.
     - **End-of-session statistic** — "Day-1 RTH low". This cannot be numerically frozen before the close.
     - **Dynamic rule** — "stop = completed Day-1 RTH low". The formula is frozen before the close; the number is filled after it.
   - ACN is not edited; it stays as the observation that revealed the problem.
3. **Thesis vs vehicle.** A correct thesis with a losing option is not a failed thesis, and a profitable option on a bad thesis is not a good decision. Every paper option carries an underlying shadow and a four-way class (`PAPER_TRADES.md` §8). UNDERLYING CORRECT / OPTION FAILED is the most informative cell.
4. **Non-trigger shadows.** Expired setups are tracked through their thesis horizon as counterfactuals. This is how we will learn whether the confirmation filters protect or merely delay. One missed move changes nothing.
5. **Thesis type ≠ mechanics** (revealed by VRT and HWM tagging). Families group by thesis type; the frozen setup letter records mechanics. Keeping both lets the ledger aggregate either way without re-tagging a frozen record.
6. **Event layer ≠ trade layer** (new, Round 7). Studying only setups that fired selects on the outcome. The earnings cohort records every event, so the trade rules can later be judged against the full population.

---

## Earnings-repricing cohort (Oct–Nov 2026)

Dates confirmed by the company unless marked *est.* Prices and distances are Oct 1, 2026 (stockanalysis).

| # | Date | Ticker | Timing | Variation role | % below 52w high | Layer | Notes |
|---|---|---|---|---|---|---|---|
| E-01 | Oct 13 | UNH | Before open (call 8:00 ET) | Damaged former leader / recovery | 21.1% | Event + **Setup A pre-registered Oct 12** | Qualifier (≥ 25%) currently not met — the frozen rule decides |
| E-02 | Oct 15 | TSM | Before open | Strong secular leader at highs (held) | 4.3% | Event | Also decides TSM tranche 2 (three-part confirmation) |
| E-03 | Oct 20 | NFLX | After close | Damaged high-expectation growth | 45.4% | Event + Setup A (rule) | New, found independently; −27% YTD |
| E-04 | Oct 21 *est.* | VRT | Before open *est.* | Broken high-expectation leader | 35.0% | Event + Setup A (rule) | Vendors disagree (Oct 21 vs Oct 28); PT-002 suspension clause applies |
| E-05 | Oct 21 | CME | Before open | Tollbooth (Program D) | 19.3% | Event | Program D check: clearing/transaction revenue growth vs ADV growth |
| E-06 | Oct 22 | PG | Before open (webcast 8:30 ET) | Defensive (staples de-rated) | 13.7% | Event | New |
| E-07 | Oct 26 | NUE | After close | Cyclical with pre-announced guidance | 16.2% | Event | New; tests whether a pre-announcement mutes the reaction |
| E-08 | Oct 27 | SPGI | Before open | Damaged quality compounder (Program D) | 29.5% | Event + Setup A (rule) | |
| E-09 | Oct 29 | LNG | Before open | Contracted infrastructure (Program E) | 10.6% | Event | LNG-A/LNG-B evidence: contract and permit updates |
| E-10 | Oct 30 | CBOE | Before open | Tollbooth (held) | 24.7% | Event; Setup A only if ≥ 25% on Oct 29 | |

**Alternates** (substitute only if a cohort event is cancelled or its date moves out of the window):
- ASML Oct 14
- GE Oct 20
- CLS Oct 26 *est.*, with an investor day Oct 27
- BA Oct 27 (turnaround)
- HWM Oct 29
- ICE Oct 29
- FICO Nov 4 *est.* (overlaps Program F)

**Pre-registration deadlines:** the evening before each report, after the 16:00 ET close and before the release:
- before-open reports: before 06:00 ET on report day;
- after-close reports: before 16:00 ET on report day.

**UNH Oct 12 workflow (scheduled):**
1. After the Oct 12 close (Columbus Day — stocks trade, bonds do not), capture the pre-event fields:
   - close, % below 52-week high, 50- and 200-day position;
   - consensus EPS (Oct 1: $4.15, 23 analysts) and revenue;
   - 2026 guidance ($19.50–20.00);
   - the Oct 16 at-the-money straddle → implied move and IV.
2. Write E-01 (event layer) and PT-011 (Setup A, EARNINGS_CONTINUATION, long), instantiated from the frozen family rules. All levels use the three reference types (stop = completed Day-1 RTH low, filled after the Oct 13 close).
3. Commit and push before 06:00 ET Oct 13.
4. After the Oct 13 close, fill the day-1 fields and evaluate the qualifiers; trigger window is days 2–10.

---

## Research queue (not yet active projects)

| Item | Why it matters | Program | Status |
|---|---|---|---|
| Post-earnings drift literature (Bernard & Thomas 1989 onward; evidence that drift has weakened in large caps since the 2000s — **to verify**) | Program A should know what is already documented before claiming an edge | A | NEW |
| Gap-down continuation setup (short / long put) | Setup A is long-only as frozen; the event layer captures gap-downs, the trade layer cannot | A | NEW — design only after event-layer evidence |
| Does Setup A's "≥ 25% below 52-week high" filter matter? | It excludes leaders (TSM, UNH at 21%); the event layer will show whether leaders' gaps continue as well | A | NEW |
| Post-shock indicator study | Finding 1 | F | Design ready; data source needed (daily OHLCV history for a large-cap shock sample) |
| MOVE/VIX divergence | Record rates vol with calm equity vol: does it resolve by equity vol rising (good for CBOE, relevant to G) or rates vol falling (relevant to C)? | C, D, G | NEW — needs a MOVE history source (not on FRED) |
| Monthly exchange volume releases | Turns Program D into a monthly evidence stream | D | NEW — start with the October releases |
| Past long-end tops (Oct 2023, 2006–07, 1994–95) | What preceded duration turns: Fed, auctions, term premium, curve | C | Next step for C |
| Foreign long ends as US term-premium drivers (JGB 10Y 3.10%, BoJ hiking; OAT 2002 highs) | Possible leading input for C | C | Queue |
| Muni/Treasury ratio (~80%) and mortgage–Treasury spread (~231 bp) as stress gauges | Cross-asset dislocation may lead a duration turn | C | Queue |
| Breadth extreme ("21% above 50-day with the index near highs — three times since 1927", one source) | Verify, then study forward returns | G | Verify first |
| Contracted vs merchant power (CEG, VST vs LNG, WMB) | Program E's central distinction | E | Queue |
| 2028–30 global LNG supply wave vs Cheniere expansion timing | LNG-B's main risk | E | Queue |
| SH path dependence | Measured live when PT-005 triggers (`PAPER_TRADES.md` §4) | G | Waiting on a trigger |

---

## Convergence checkpoint

- **No fixed round cap.** A new round must:
  - discover a materially new opportunity;
  - resolve or sharpen an important disagreement;
  - reveal a methodological problem;
  - convert an observation into a repeatable strategy;
  - materially change a long-horizon thesis; or
  - produce evidence about an existing family.
- **At Round 10:** are we still discovering, or mostly repeating? If converging, draft `MARKET_DOCTRINE_v0.1.md`. Not before.
