# Market Roster (WATCHLIST.md)

**This page answers: "What matters right now?"** Open it on an ordinary market day. It holds:
- the current market state (§1);
- the permanent gauges (§2);
- the long-horizon businesses (§3);
- the active setups (§4);
- the research candidates (§5);
- dated decisions and events (§6).

It is current, not historical:
- stale items leave at the weekly review and are recorded in `ROUNDS.md` (`README.md`, Operating cadence);
- the base case and its rivals are in `MARKET_MODEL.md` §8;
- open research is in `RESEARCH_MAP.md`;
- frozen plans are in `PAPER_TRADES.md`.

**Version:** Round 13 — Claude (Opus 5.5); daily states from the scheduled cycle. §2–§5 values are from the **Oct 1, 2026 close** unless marked; the latest readings are in §1. The time of each change is its git commit time.

---

## 1. DAILY STATE

**Purpose:** identify what changed, decide whether it matters, and decide whether anything deserves attention or capital. It follows the daily cycle in `README.md`: observe → detect change → interpret → cross-market check → opportunity scan → preserve. **NO ACTION is a valid, often the right, conclusion.**

**Rules**
- One line per field. Write "unchanged" where nothing moved. Expand a section only when the market requires it.
- The state answers the six day-start questions:

  | Question | Field |
  |---|---|
  | What we know | *Observed* |
  | What we think | *Interpretation* |
  | Where the evidence disagrees | *Contradiction / alternative* |
  | What we're watching | *Active watches* |
  | What would change our minds | *What changes the view* |
  | What deserves capital | *Capital-moving* |
- Use the claim labels in `README.md`. Cite theses by name (`MARKET_MODEL.md` §6) and contradictions or notes by ID (§7).
- Keep the **latest state and the one before it**. Older states live in git, one commit per state. Daily states do not go into `ROUNDS.md`.
- Template fields change only at a weekly review, with the reason recorded in `ROUNDS.md`. Never change one because a day's data looked interesting.

### Template

```
DAILY STATE — YYYY-MM-DD (close) · previous: YYYY-MM-DD
CHANGED         1–3 material changes since the previous state, or "nothing material"
RATES           Observed: 2Y · 10Y · 30Y · 10Y real · 10Y breakeven · fed funds strip · 2s10s · MOVE
                Interpretation: — | Contradiction / alternative: — | What changes the view: —
CREDIT          Observed: IG / HY / CCC OAS · HYG · BKLN                     (same three fields)
DOLLAR / LIQ.   Observed: broad $ · DXY · USD/JPY · USD/CAD · funding alarm on/off
COMMODITIES     Observed: WTI front · WTI 12-month slope · gold · copper
EQUITIES        Observed: SPY · RSP · IWM vs 50-day · % above 50-day · (weekly) forward P/E
VOL / POSITIONS Observed: VIX · MOVE · systematic-exposure estimate (when published)
ACTIVE WATCHES  setups and regime watches whose status changed · thesis-state changes (+ evidence)
DATED DECISIONS next five sessions (from §6)
CAPITAL-MOVING  alarms tripped · OPPORTUNITY SCAN: NO ACTION | <what, and where it was recorded>
```

### DAILY STATE — 2026-10-05 (close) · previous: 2026-10-02

*Written by the unattended daily cycle; time: see commit. **Data coverage was partial** (same cause as Oct 2: direct FRED, Yahoo-chart and quote-page fetches are blocked in this run; only pages surfaced by web search were readable). Oct 5 rates closes are market quotes; the Treasury par / H.15 row for Oct 5 was not read. Fields not read reliably are UNMEASURED.*

**Changed:**
1. **The long end sold off while the front end held: a bear steepener to new 24-year highs.** OBSERVED (market quotes at the close): 2Y 4.82% (−0.2 to −1.6 bp), 10Y 5.31–5.32% (+3 to +4 bp), 30Y 5.66–5.67% (+4 to +5 bp) (TheStreet 16:07 ET; TradingEconomics). Intraday the 10Y reached ~5.35% and the 30Y ~5.70%, the highest since April / May 2002 (MPA; Invezz; Yahoo). Sources disagree on the 10Y close (5.31–5.35%); two of four put it at 5.31–5.32%. DERIVED: 2s10s ≈ 49 bp (+4), 2s30s ≈ 84 bp (+4).
2. **ISM services prices paid ran hot.** OBSERVED (Yahoo; MPA): September ISM services 54.9 (consensus 55.2, prior 55.4); prices paid 74 (consensus 73, prior 72.6). Sources attribute the long-end move to it and to "momentum selling" (INTERPRETATION by the sources).
3. **Oil kept falling and the October hike stayed mostly out.** WTI Nov settled 89.43 (−1.8%; Rigzone 16:07 ET), Brent Dec 100.32 (−1.9%). October hike odds ~18–22% (CME FedWatch via Invezz: 82% hold; prediction markets 21%).

**Rates**
- *Observed:*
  - **Oct 2 closes confirmed by a second official source** (Fed H.15, read this run): 2Y 4.83 · 10Y 5.28 · 30Y 5.63; 10Y real 2.92 · 30Y real 3.34. Matches the Round 14 Treasury-par read.
  - Oct 5: 2Y · 10Y · 30Y as in Changed 1. 10Y real, breakeven, MOVE: UNMEASURED.
  - Strip: December hike ~84% (FedWatch via Invezz, after the close) against 88.6% cumulative ≥ 25 bp at Friday's close (FedWatch via Phemex, 00:06 Oct 5). Prediction markets: December 74% (DeFi Rate). Different sources; not like-for-like. 2027 strip: UNMEASURED.
- *Interpretation (low confidence):* the 10Y and 30Y rose with the 2Y flat and no sign of the strip adding hikes. That is the written down-condition of POLICY-LED REAL-RATE REPRICING ("10Y rises with the strip flat → term premium story") and the up-condition of LONG-RATE STRESS TRANSMISSION. Three explanations are open: (a) term premium / supply concession ahead of the Oct 7–8 auctions (stress family; PLAUSIBLE / UNTESTED); (b) an inflation-expectations response to ISM prices paid (breakeven; W4 watch zone); (c) a path repricing beyond December that the Oct/Dec odds do not capture. The real/breakeven split separates (b). **One session; no state change.** Oil fell 1.8% the same day, so the long-end rise was not oil-led.
- *Contradiction / alternative:* **candidate, not admitted.** Admission rule pre-committed here: if the Oct 5 H.15 row shows the 10Y up ≥ 3 bp with the 2Y flat or lower, and the 10Y real yield carries most of the rise, admit **C-012** against POLICY-LED REAL-RATE REPRICING's §6 down-condition. If the breakeven carries it, record a W4-zone note instead (`MARKET_MODEL.md` §8, Next discriminators 1).
- *What changes the view:* the Oct 5 H.15 row; the 10Y (Oct 7) and 30Y (Oct 8) auctions (tail ≥ 2 bp with indirect < 65%).

**Credit**
- *Observed:* HYG 76.87 (−0.06%, 13:15 ET) · BKLN 20.49 (+0.05%, 12:04 ET) (stockanalysis). IG, HY, CCC OAS: UNMEASURED.
- *Interpretation:* unchanged. No price sign of spread stress on a 24-year-high long-end day.

**Dollar / liquidity**
- *Observed:* DXY 102.14 (+0.2%) · USD/JPY 157.96 (+0.06%) · USD/CAD 1.4255 (flat) (TradingEconomics, time n/s, single source). Broad dollar and SOFR − IORB: UNMEASURED; funding alarm last read off (Sep 30).
- *Interpretation:* unchanged. A firmer dollar with US yields up does not test C-001.

**Commodities**
- *Observed:* WTI and Brent as in Changed 3; TradingEconomics' 89.36 (−1.9%) corroborates the level. WTI 12-month slope: UNMEASURED. Gold 4,139–4,190 (sources disagree on level and sign: TE −0.03%, Yahoo +0.11%, TheStreet +0.65%). Copper 6.58 (+1.4%; TE).
- *Interpretation:* day 2 of the G7 release. WTI 91.11 → 89.43; the curve and breakevens that would show transmission are unmeasured (natural experiment, `MARKET_MODEL.md` §8 item 4). Nothing to conclude.

**Equities / breadth**
- *Observed (closes, stockanalysis unless marked):* SPY 774.83 (+0.67%) · RSP 211.14 (+0.67%) · IWM 283.92 (+0.85%, 15:25 ET) · QQQ UNMEASURED (Nasdaq Composite +0.95–1.05%; TheStreet, Yahoo). S&P 500 7,774–7,775 (+0.66–0.68%). Breadth: UNMEASURED.
- *Interpretation:* unchanged. Equities rose for a second session while the long end sold off (§3: yields ↔ equities not linked at the index). Small caps beat SPY on a day the 10Y rose: one day of evidence against P5's direction, which resolves over the window.

**Volatility / positioning**
- *Observed:* VIX 15.55 (+1.6%; Yahoo, time n/s). MOVE: UNMEASURED.
- *Interpretation:* unchanged. SYSTEMATIC DELEVERAGING: FORMING.

**Active watches**
- PT-002 VRT 253.62 (+0.6%): no weekly test today. WATCH.
- PT-004 FICO close 689.61 (+4.3%; low 648.95): **session 4 of 10** without a close < 586.05.
- PT-005 SPY 774.83, above the 50-day: no trigger. WATCH.
- **PT-007 CBOE, Oct 2 read:** close 271.26 (< 288): not triggered; above the 262 invalidation. Oct 5 ~276.07 (+1.8%, quote time n/s). WATCH.
- **PT-008 HWM, Oct 2 read:** close 231.27 (< 248): not triggered; above the 222 invalidation. Oct 5 UNMEASURED. WATCH.
- PT-003 MU, PT-010 CLS (CLS.TO), PT-009 ITB: Oct 5 UNMEASURED. MU's Oct 2 close 1,074.89 (stockanalysis) confirms the 15:44 read. CLS (NYSE) 382.69 (−1.2%) is not the frozen TSX instrument; no pullback signal either way.
- PT-006 TLT 77.11 (−0.5%, 15:24 ET); 52-week low 76.69 held. Regime review is weekly (next Oct 9).
- **CBOE September volume (§3 review event):** index options ADV +22.3% y/y; record monthly SPX 0DTE ADV 3.4M; multi-listed options +0.7%; futures −7.6% (Cboe release via StockTitan, Oct 5). The thesis-breaker (options volume negative y/y for two quarters) is not in sight. Thesis intact; evidence supportive.
- P8: Oct 5 does not qualify (WTI −1.8%). Tally stays 0 of 1.
- C-009 test (long-end selloff day): Bund +5 bp, Gilt +4, JGB −1, Canada +1 (TradingEconomics; the Bund page's text is internally inconsistent). European and Tokyo sessions mostly closed before the 10:00 ET ISM release, so the timing confounds it. Not discriminating; stays OPEN.
- Thesis-state changes today: **none.**

**Dated decisions (next five sessions):** Oct 7 NFCI (C-003) · 10Y auction · FOMC minutes (per press) · Oct 8 30Y auction · Oct 9 PT-006/PT-009 weekly review · Oct 12 UNH pre-registration (scheduled separately).

**Capital-moving:** no measured alarm tripped (OAS and SOFR − IORB unmeasured; HYG and BKLN flat; VIX 15.6). Live tactical capital: none. **Opportunity scan: NO ACTION.** The steepener sharpens the question the Oct 7–8 auctions answer. It does not move any setup or the duration watch, which needs yields falling.

### DAILY STATE — 2026-10-02 (close) · previous: 2026-10-01

*Written by the unattended daily cycle; time: see commit. **Data coverage was partial.** Direct reads of FRED and Yahoo's chart API were blocked in this run, and so were many quote pages; only pages surfaced by web search could be read. Fields not read reliably are UNMEASURED. Several rates figures are **post-release intraday** readings, not closes, and are labelled that way. (STRUCTURAL GAP — REVIEW REQUIRED: see `ROUNDS.md`, Weekly review — week ending 2026-10-02.)*

**Interactive reconciliation (Round 14, Claude; time: see commit). Supersedes the scheduled text below where they conflict; the scheduled text is kept as written.**
- **Event path** (times ET; sources disagree on some levels, so ranges are shown):

  | | Before 08:30 | Initial reaction | Later session | Close |
  |---|---|---|---|---|
  | 2Y | 4.78% (Oct 1 par) | 4.72–4.76% (−3 to −7 bp; Reuters, Indexbox) | UNMEASURED | **4.83% (+5 bp; Treasury par)** · TE 4.85% |
  | 10Y | 5.23–5.24% | 5.175–5.21% (−3 to −7 bp) | back to 5.28% by 13:32 (HousingWire) | **5.28% (+4 bp; Treasury par)** · TE 5.28%; IEF −0.27% ≈ +4 bp |
  | 30Y | 5.61% | 5.57–5.59% (−2 to −4 bp) | UNMEASURED | **5.63% (+2 bp; Treasury par)** · TE 5.61%; TLT −0.36% ≈ +2 bp |
  | 10Y real · breakeven | 2.88% · 2.36% (Oct 1 par real) | UNMEASURED | UNMEASURED | **2.92% (+4 bp) · 2.36% (unchanged)** (Treasury par real; breakeven DERIVED) |
  | October hike odds | ~28% (investinglive), ~70% on Monday | 12–14% (Reuters; FedWatch via Schwab) | ~21% (Reuters); "one in four" at 15:08 (BNN) | 18% at 16:26 (TheStreet / FedWatch) |
  | Equities | S&P fut +0.5%, NQ +0.7% (Yahoo; time n/s) | S&P opened +0.9% (Reuters) | gains held | SPY +0.74% · QQQ +1.02% · IWM +0.90% · RSP +0.39% (stockanalysis) |
  | WTI | ~89.2 (−3.9%; G7 news out by 06:40) | ~89.4 (Schwab 09:13) | recovered to ~91.4 | **91.11 settle (−1.9%)** · Brent 102.25 (−0.1%) (Rigzone 16:10) |
  | Gold · DXY | ~4,217 · ~102.0 | +0.8–0.9% · 101.8–101.9 | — | ~4,214–4,217 (+0.3%) · UNMEASURED |

  **Closes are from Treasury's par and real curves, read once at ~14:22 PT.** A second, cache-busted read did not yet show the Oct 2 row, so re-read it next run. The values agree with TradingEconomics, TLT and IEF. 30Y real 3.34% (+3 bp); 30Y breakeven 2.29% (−1 bp, DERIVED). The strip beyond October: UNMEASURED.
- **Release (BLS, OBSERVED):** payrolls +29k; July revised to −10k and August to +133k (−60k combined); unemployment 4.2% ("changed little"; 4.1% prior per secondary sources); AHE +0.1% m/m, +3.0% y/y; workweek 34.4h. Consensus ~84–90k; sources differ.
- **What the path shows (INTERPRETATION):** weak payrolls were followed by a curve-wide rally, then a curve-wide reversal.
  - The reversal was **strongest in the front end and belly**: from intraday low to close, 2Y ≈ +7 to +11 bp, 10Y ≈ +7 to +11 bp, 30Y ≈ +4 to +6 bp. Close to close: 2Y +5, 10Y +4, 30Y +2.
  - The long end moved least. 2s10s closed at 45 bp (−1) and 2s30s at 80 bp (−3): a mild bear flattener, not the bear steepener the scheduled text suspected.
  - **The 10Y's rise was all real yield** (+4 bp real, breakeven unchanged at 2.36%). That rules out an inflation-expectations move. It does **not** separate the expected real policy path from term premium or other real-yield components: October odds closed *below* their pre-release level (~28% → 18–25%) while the curve closed higher, so October odds cannot attribute the rise. The strip beyond October is needed (UNMEASURED).
  - October hike odds kept part of their drop (28% → 18–25%).
- **Corrections to the scheduled text:** "Changed" item 3 and the Rates interpretation's bear-steepening line are not supported by the closes as measured. P8: Oct 2 **does not qualify** (WTI −1.9% at settlement, below the ±2% threshold), so the tally stays 0 of 1.
- **Research note, not a contradiction:** Treasuries gave back their rally while equities kept theirs. No expectation written beforehand covered payroll-day co-movement (P9 covers CPI and FOMC only), so it is recorded under C-011, not admitted. It fits §3's existing reading: yields and equities are not linked at the index.
- **Thesis states:** unchanged (one session). Evidence notes are in `MARKET_MODEL.md` C-011 and §8 "Next discriminators".
- **Next run:** confirm the Oct 2 par and real rows (read only once; FRED DGS2/DGS10/DGS30, DFII10, T10YIE are the cross-check). Read the strip beyond October if any source allows.

**Changed:**
1. **The October hike was largely priced out.** September payrolls came in at +29k against ~85–90k expected. Unemployment rose to 4.2%; average hourly earnings rose 0.1% m/m and 3.0% y/y; July and August were revised down a combined 60k (BLS). OBSERVED: October-hike odds fell to 12% (Reuters) or 14% (CME FedWatch via Schwab), from ~70% early in the week (Schwab). The sources attribute the repricing to payrolls. WTI was also falling before the release (−3.9% at 06:00 ET), so causality is unclear (research note C-011).
2. **G7 announced a 100M-barrel oil and diesel reserve release**, spread over four months with diesel front-loaded. WTI traded down 2–4% intraday (low 88.06). Its settlement is UNMEASURED. *[Settlement read in the reconciliation: 91.11, −1.9% (Rigzone).]*
3. **The front end rallied after the release; the long end's close is unresolved.** TLT stood at 77.43 (−0.36%) at 15:36 ET, after a high of 78.32. That says the long end gave back its morning rally (DERIVED; see Rates). *[Superseded: the whole curve reversed, front end and belly most, long end least. See the interactive reconciliation above.]*

**Rates**
- *Observed:*
  - Oct 1 closes confirmed: 2Y 4.78% (−10 bp; stockmarketwatch, matching the derived value in the Oct 1 state) · 10Y 5.24% · 30Y 5.61%.
  - **Oct 2, post-release intraday (Reuters via investing.com):** 2Y 4.716% (−7 bp) · 10Y 5.176% (−6 bp) · 30Y 5.569% (−4 bp). The 10Y at 5.17–5.18% is corroborated by Yahoo ^TNX, Schwab and Quartz.
  - **Oct 2 closes: UNMEASURED.** Sources conflict. TradingEconomics reports the 10Y at 5.28% (+4 bp), the 2Y at 4.85% and the 30Y at 5.63% late in the day, but its pages were inconsistent between reads (one TE page showed the 30Y at 5.57%, −4 bp). Next run: read FRED DGS2, DGS10 and DGS30 for Oct 2. *[Read in the reconciliation: Treasury par 4.83 / 5.28 / 5.63.]*
  - DERIVED, intraday: 2s10s ≈ 46 bp.
  - 10Y real, breakeven, fed funds strip levels, MOVE: UNMEASURED. Only the October-meeting probability was read (above).
- *Interpretation:* the front end repriced on a growth (labour) shock, by the sources' account, with oil falling the same morning. A labour route is neither the base case's oil route (LOOP-1) nor the benign alternative's strong economy. POLICY-LED REAL-RATE REPRICING: ACTIVE, unchanged; one session is not enough to move it, and the December/2027 strip is unmeasured. DURATION TURN: DORMANT, unchanged. Its up-condition ("strip removes ≥ 1 hike" plus M1) is not met: DERIVED, about 0.56–0.58 of a hike came out of October (70% → 12–14%), the removal across the whole strip is unmeasured, and M1 is far from met. INTERPRETATION, low confidence: the long end did not follow the front end, which would be the bear-steepening the stress alternative predicts. It stays unconfirmed until the closes are read. *[Superseded: not supported by the closes as measured; see the interactive reconciliation above.]*
- *Contradiction / alternative:* new research note **C-011** (labour data, alongside oil, moved the front end). P8 evidence so far runs against the base case (see Active watches).
- *What changes the view:* the Oct 2 closes. If the 10Y closed near unchanged with the 2Y lower, the curve steepened on a dovish front end, a stress-alternative signature worth a note. Also: the Oct 7–8 long-end auctions and Oct 14 CPI.

**Credit**
- *Observed:* HYG 76.91 (+0.01) · BKLN 20.48 (+0.02), both Oct 2 closes (stockanalysis). IG, HY and CCC OAS: UNMEASURED (FRED unreadable).
- *Interpretation:* unchanged. No sign of spread stress in the price gauges. CCC TAIL REPRICING ACTIVE and CREDIT STRESS DORMANT, both unchanged.
- *Contradiction / alternative:* unchanged (C-003; C-004).
- *What changes the view:* unchanged.

**Dollar / liquidity**
- *Observed:* DXY 101.79–101.90 (−0.2%, intraday; Reuters, Schwab). Broad dollar, USD/JPY, USD/CAD and SOFR − IORB: UNMEASURED.
- *Interpretation:* unchanged. A weaker DXY on a dovish repricing is consistent with every explanation, so it is not a test. The funding alarm was last read off (Sep 30).

**Commodities**
- *Observed:* WTI front-month: Oct 1 settlement 92.87 (+2.7%; fxstreet; level corroborated by TradingEconomics' implied prior). Oct 2: 89.09–89.41 in the morning (−4%), 91.40–91.49 later (−1.6%), intraday low 88.06; **settlement UNMEASURED**. Brent Dec 102.78 (+0.45%, TradingEconomics, single source). WTI 12-month slope: UNMEASURED. Gold ~4,219–4,240 (+~1%, intraday; Reuters, Schwab). Copper: UNMEASURED.
- *Interpretation:* the G7 release is the first policy supply response to the shock. Whether it reaches the curve (front down, backwardation narrowing) is P6's condition. One day is not evidence of that.
- *What changes the view:* WTI below $80 with backwardation narrowing (P6 / W1).

**Equities / breadth**
- *Observed (Oct 2 closes, stockanalysis):* SPY 769.64 (+0.74%; 50-day was 763.1 on Oct 1, so it closed above it) · QQQ 749.58 (+1.02%) · IWM 281.52 (+0.90%) · RSP 209.82 (+0.39%). S&P 500 7,725.55 (+0.73%, TradingEconomics). The Nasdaq-100 printed an intraday record (CNBC headline). Breadth (% above 50-day): UNMEASURED.
- *Interpretation:* unchanged. A leadership-led rally (QQQ > SPY > RSP) is consistent with BREADTH ROTATION and EARNINGS OFFSET, both ACTIVE. It does not test C-005.

**Volatility / positioning**
- *Observed:* VIX 15.59 (−4.9%, intraday; Schwab) · 15.97 pre-market (Yahoo). MOVE: UNMEASURED.
- *Interpretation:* unchanged. SYSTEMATIC DELEVERAGING: FORMING (fuel without a trigger).

**Active watches**
- **PT-002 VRT, first weekly test: not triggered.** The weekly close was 252.18 (+2.5% on the day; Yahoo and stockanalysis) against the > 262 trigger. WATCH; expires at the Oct 20 close.
- **PT-006 TLT / PT-009 ITB weekly regime review: no change.** M1 is not met: the 10Y is ≥ 5.17% whichever source is used, far above a 10-week average near the 50-day (4.82 on Oct 1). M2 is not met: TLT was ~77.4 against a 50-day of ~81.8. M3 is moot (breakeven UNMEASURED). Status: **ACTIVE REGIME WATCH — LAST REVIEWED 2026-10-02.** ITB close: UNMEASURED.
- PT-004 FICO: close 661.25 (intraday low 609.00) → **session 3 of 10** without a close < 586.05.
- PT-003 MU: 1,075.64 (15:44 ET, −2.0%); 50-day 956.08. No qualifying pullback. WATCH.
- PT-005 SPY: 769.64, no trigger (needs a close < 750). Conditions were not re-read: VIX < 18, and breadth is unmeasured.
- PT-010 CLS: C$544.70 (Oct 2, last read), extending. No pullback. WATCH.
- PT-007 CBOE and PT-008 HWM: closes UNMEASURED. A trigger needs a close > 288 (+3.9% from Oct 1) and > 248 (+8.6%) respectively. **Next run: read the Oct 2 closes and volume.**
- **P8 evidence (first entries):** Oct 1: WTI +2.7%, 2Y −10 bp → opposite direction. Oct 2: WTI ≥ 2% qualification UNMEASURED (it depends on settlement); if it qualifies, the 2Y moved the same way, with oil and payrolls confounded. Tally: 0 of 1 qualifying sessions moved the same way. *[Reconciliation: Oct 2 does not qualify (WTI −1.9%); tally stays 0 of 1.]*
- Thesis-state changes today: **none**.

**Dated decisions (next five sessions):** Oct 5 Cboe September volume (~Oct 2–5) · Oct 7 NFCI (week to Oct 2) and 10Y auction · Oct 8 30Y auction.

**Capital-moving:** no measured alarm tripped. HY OAS, IG OAS and SOFR − IORB are unmeasured today, but HYG and BKLN were flat and VIX was 15.6. Live tactical capital: none. **Opportunity scan: NO ACTION.** The jobs-driven repricing is the first step toward the DURATION TURN's up-condition, not the condition itself. Nothing triggered.

## 2. PERMANENT GAUGES (never expire while useful)

These are gauges for understanding conditions, not trade candidates. They were tiered after the Round 11 instrument screen (`MARKET_MODEL.md` §4–§5). Values are Yahoo daily closes unless marked; FRED series carry their own date. A gauge is added only where it materially improves understanding, and one that adds nothing is dropped at a weekly review.

**Daily core**

| Group | Gauge | Oct 1 | Context | What it tells us |
|---|---|---|---|---|
| Equity regime | SPY · QQQ | 763.99 · 742.03 | 50d 763.1 / 200d 720.0 · 715.7 / 667.9 | Headline trend; growth leadership |
| | RSP · IWM | 209.00 · 279.02 | 216.7 / 205.7 · 292.8 / 276.2 | The average stock; small caps carrying floating debt |
| | % of S&P above 50d / 200d | 23.0% / 40.9% | thetrading.tools | Participation |
| Rates | 2Y · 10Y · 30Y | 4.88% (Sep 30) · 5.24% · 5.60% | 10Y 50d 4.82 / 200d 4.44 | Policy path; discount rate |
| | 10Y real · 10Y breakeven | 2.93% (Sep 30) · 2.36% | +73 / +12 bp since Jun 30 | **New.** Real-rate shock or inflation shock? |
| | Fed funds strip (ZQ) | Dec 4.08% · May '27 4.50% | Effective 3.88% | **New.** Hikes priced |
| | 2s10s | 46 bp (Oct 1) | +11 bp Jun 30 → Sep 30 | Path vs term premium |
| | TLT | 77.71 | 81.8 / 85.5 | The duration vehicle; 52-week-low close |
| Credit | IG · HY · CCC OAS | 0.84% · 3.12% · 11.79% (Sep 30) | +8 · +37 · +209 bp since Jun 30 | **New split.** Where the stress actually sits |
| | HYG · BKLN | 76.90 · 20.46 | 79.1 / 79.9 · 20.52 / 20.58 | Rates + spread · near-pure credit (**new**) |
| Volatility | VIX · MOVE | 16.39 · 108.1 | 200d 18.1 · 50d 80.0 | Equity vs rates uncertainty |
| Dollar | Broad dollar (FRED) · DXY | 120.33 (Sep 25) · 102.02 | Jun 30: 120.92 · 101.19 | **New.** Broad vs euro-weighted |
| | USD/JPY · USD/CAD | 157.9 · 1.4222 | Jun 30: 162.6 · 1.4205 | Repatriation channel; Dustin's own currency risk (**new**) |
| Commodities | WTI front · Dec '27 | 93.00 · 75.29 | −19% backwardation | **New slope.** Is the oil shock priced as temporary? |
| | Gold (front future) · copper | 4,211.5 · 6.58 | Gold 50d 4,364 / 200d 4,554 | Dollar/official bid · industrial demand |
| Housing/banks | 30Y mortgage · ITB · KRE | 7.28% Freddie Mac / 7.60% MND · 87.37 · 69.95 | Mortgage − 10Y ≈ 2.0 pp | Housing transmission; bank channel |

**Weekly:** NFCI (−0.548, Sep 25) · Kim–Wright term premium (1.02%, Sep 25) · Bund / JGB / Canada 10Y (3.53 / 3.10 / 3.93%) · MBB vs IEF (duration-adjusted) · LQD · forward P/E (19.2) · silver (front future 61.26) · XLE (62.70).
**Event:** Treasury auctions (10Y Oct 7, 30Y Oct 8) · CPI (Oct 14) · TIC (Oct 16) · FOMC (Oct 28) · refunding (Nov 4).
**Alarm (glance weekly; daily only if tripped):** SOFR − IORB (0 bp) · standing repo facility use ($1.2B, Sep 30) · ON RRP (≈ 0) · reserves ($2.95T).
**Dropped from the daily list:** IEF (now the denominator for MBB and LQD ratios), 5s30s (2s10s carries the path-vs-premium question), silver, XLE and LQD (to weekly).

**Market Brief / market-review** stays read-only evidence. Hypotheses H1–H5 (Sep 30) map onto these rows.

## 3. LONG-HORIZON BUSINESSES (remain while the thesis is active)

A business sits here only with a written thesis and counter-thesis. Roles describe its place in Dustin's **whole program**, not its sleeve weight. The sleeve is **proposed, not executed** (`PROPOSAL.md`).

| Business | Program | Role (program level) | Oct 1 | vs 50d / 200d · off high | Status | Next review event | What would change it | Regime link (Round 11) |
|---|---|---|---|---|---|---|---|---|
| **CBOE** (sleeve: proposed, not executed) | D | CORE candidate (named dependency: SPX × retail short-dated × regulation) | 277.19 | 288.0 / 287.0 · −24% | Thesis intact | Q3, Oct 30; monthly volume (~Oct 2–5) | Options volume negative y/y for two quarters; a fee or 0DTE rule; loss of exclusivity | Volumes respond to *equity* vol. A rates-only shock (C-006) is a weak kicker |
| **CME** | D | CORE candidate (not held) | 265.10 | 270.3 / 278.5 · −19% | Approved candidate; Strategy F trigger ≤ ~$220 or clearing growth ≥ ADV growth | **Q3, Oct 21**; September volume | FMX share gains; a volume regime pinned at zero rates | **Supportive:** its engine is an active rate path, which is today's regime (~2½ hikes priced, MOVE 108). Not a trigger |
| **LNG** (sleeve: proposed, not executed) | E | CORE (existing asset) + embedded growth option | 272.40 | 272.1 / 246.5 · −8% | Thesis intact (LNG-A / LNG-B) | **Q3, Oct 29**; FERC on the expansion (late 2026) | LNG-A: contracted share < ~85% or tenor < ~12 years. LNG-B: permit denial, or FID slipping past 2027 | Fees are contracted, so oil and gas prices do not drive LNG-A. Higher real yields lower the value of long-dated cash flows and raise LNG-B's financing cost |
| **TSM** (sleeve: proposed at 26%, not executed) | H | **SATELLITE** (geopolitical tail) | 459.20 | 423.8 / 386.2 · −4% | Thesis intact; entry rule conditional on Oct 15 | **Q3, Oct 15**; monthly revenue (~10th) | Two hyperscalers cutting capex; N2 failure; a cross-strait event (handled by size) | Long-duration growth whose discount-rate exposure is so far outrun by earnings (FY26 EPS +63%). Not a rates bet |

## 4. ACTIVE SETUPS (thesis, trigger, invalidation, horizon and current state — or archived)

Full plans and annotations are in `PAPER_TRADES.md`; frozen plans are never rewritten.

| Record | Family | Watch type | Activation (frozen) | Invalidation | Expires / reviewed | Latest status (Oct 5 unless marked) | Thesis link (`MARKET_MODEL.md` §6) |
|---|---|---|---|---|---|---|---|
| PT-002 VRT | Broken-leader reclaim | Tactical setup | Weekly close > 262 on ≥ 1.5× volume | Close < 232 | **Oct 20 close** | 253.62 · Oct 2 weekly test not triggered (252.18 vs > 262); next weekly test Oct 9 | — |
| PT-003 MU | Trend pullback | Tactical setup | Pullback ≥ 8% touching the 20/50-day, then a close above the prior high | Close below the pullback low | First close below the 50-day without a qualifying pullback, or Dec earnings | Oct 2 close 1,074.89 — extended; 50-day 956 · Oct 5 UNMEASURED | — |
| PT-004 FICO | Post-shock reversal | Tactical setup | 10 sessions without a close < 586.05 + reclaim of the 20-day + close above the base high | Close below the base low | Next earnings (est. Nov 4), or a close < 586.05 | 689.61 — session 4 of 10 | — |
| PT-005 SPY | Index downside (G) | Regime-linked tactical | Close < 750 with ≥ 3 of 5 conditions | Close above the 50-day | Monthly (next **Nov 2**) and after FOMC (Oct 28) | 774.83 (above the 50-day); 2 of 5 met (Oct 1) | BREADTH ROTATION (ACTIVE) vs EARNINGS OFFSET (ACTIVE); C-005 |
| PT-006 TLT | Duration turn (C) | **ACTIVE REGIME WATCH — LAST REVIEWED 2026-10-02** | M1–M3 + 1 optional (weekly) | 10Y +40 bp / trigger-week low | Monthly; after CPI (Oct 14), FOMC (Oct 28), refunding (Nov 4) | 77.11 (15:24 ET); M1, M2 not met (weekly review Oct 2; next Oct 9) | DURATION TURN (DORMANT); route most likely LOOP-1 |
| PT-007 CBOE | Tactical compounder entry | Tactical setup | Close > 288 on ≥ 1.5× volume | Close < 262 | **Oct 29 close** | Oct 2 close 271.26 (not triggered) · Oct 5 ~276.07 | — |
| PT-008 HWM | Broken-leader reclaim | Tactical setup | Close > 248 on ≥ 1.5× volume, then a weekly close > 260 | Close < 222 | **Oct 28 close** | Oct 2 close 231.27 (not triggered) · Oct 5 UNMEASURED | — |
| PT-009 ITB | Duration turn (C) | **ACTIVE REGIME WATCH — LAST REVIEWED 2026-10-02** | M1 + MND ≤ 7.35% + close above the 20-day | Close < 84.00 | With PT-006 | Oct 1: 87.37 · Oct 2 and Oct 5 UNMEASURED; M1 not met | DURATION TURN (DORMANT); HOUSING TRANSMISSION (ACTIVE) |
| PT-010 CLS | Trend pullback | Tactical setup | 8–12% pullback holding the 20-day, then a close above the prior high | Pullback low / 50-day | **Oct 26 close** | CLS.TO C$544.70 (Oct 2) — extended, no pullback · Oct 5 UNMEASURED | — |
| Cohort E-01…E-10 | Earnings (A) | Event | Setup A / A-M per the mechanical rule | Completed day-1 RTH low | Each closes at its D+20 | First: UNH, Oct 13 (pre-registration Oct 12) | — |

## 5. RESEARCH CANDIDATES (interesting, not promoted)

A candidate is reviewed at its next evidence event and promoted only by a written thesis (→ §3) or a frozen setup (→ §4). It is archived after two evidence events pass without a promotion case.

**Independent discovery.** A name does not stay here because it appeared in earlier conversation, or because Dustin likes it. A name that leaves can return only with new evidence, and independent rediscovery counts for more than repeated confirmation.

| Candidate | Program | Why it is interesting | What would promote it | Next evidence |
|---|---|---|---|---|
| **ICE** | D | Exchanges + data + mortgage technology; the mortgage segment is the kicker in a rates turn | A written thesis with counter-thesis and a trigger | Q3, Oct 29 |
| **SPGI** | D | A damaged tollbooth (−25% from its high); ratings issuance + indices | Cohort E-08 outcome plus a thesis on issuance cyclicality | Q3, Oct 27 |
| **MU** | H / B | Memory-cycle leader. Its role is TACTICAL; a business case needs underwriting through the cycle | A through-cycle thesis (contract pricing, capex discipline) | Dec earnings; TrendForce pricing |
| **VRT** | H / B | AI power and cooling; −35% from its high | Post-earnings thesis on orders and backlog | Q3, Oct 21 (est.) |
| **CLS** | H / B | AI hardware manufacturing; customer concentration | Investor Day evidence on customer breadth | Q3, Oct 26; Investor Day Oct 27 |
| **UNH** | A | First cohort event; a damaged leader | The cohort event itself (PT-011 pre-registered the evening before) | Oct 13 |

## 6. DATED DECISIONS AND EVENTS

**The sleeve is not executed.** The "tranche 2 / third share" rules in `PROPOSAL.md` assumed a first tranche that does not exist. Unless Dustin executes tranche 1 first, each sleeve date below is a **first-entry** decision under the same written conditions.

| Date | Event | Decides or tests | Record / rule |
|---|---|---|---|
| ~Oct 5 | Cboe September volume — **done Oct 5**: index options ADV +22.3% y/y, record SPX 0DTE; CME's UNMEASURED | Program D evidence (CBOE, CME) | §3 |
| Oct 7 | NFCI (week to Oct 2) · 10Y auction | C-003 · LONG-RATE STRESS (tail ≥ 2 bp with indirect < 65%) | `MARKET_MODEL.md` §6–§7 |
| Oct 8 | 30Y auction | LONG-RATE STRESS | `MARKET_MODEL.md` §6 |
| Oct 12 (evening) | UNH pre-registration (scheduled) | Cohort mechanics | `RESEARCH_MAP.md` cohort |
| Oct 13 | UNH Q3 | First cohort event | `RESEARCH_MAP.md` cohort |
| Oct 14 | CPI | P9 · PT-006/PT-009 regime review | `MARKET_MODEL.md` §8 · `PAPER_TRADES.md` |
| Oct 15 | TSM Q3 | Sleeve entry rule (Q4 guide ≥ consensus, capex held or raised, > 40% outlook intact) · first post-earnings thesis review (tests underwritability) | `PROPOSAL.md` §1 |
| Oct 16 | TIC (August) | Foreign Treasury demand | `MARKET_MODEL.md` §8 Q1 |
| Oct 20 (close) | PT-002 VRT expires if not triggered | — | `PAPER_TRADES.md` §10 |
| Oct 21 | CME Q3 · VRT Q3 (est.) | CME: Strategy F (≤ ~$220, or clearing growth ≥ ADV growth) plus the reallocation comparison | `PROPOSAL.md` §7 |
| Oct 26 (close) · Oct 27 | PT-010 CLS expires · SPGI Q3 · CLS Investor Day | Research-candidate evidence | §5 |
| Oct 28 | FOMC · PT-008 HWM expires at the close | P10, W5 · PT-005 post-FOMC review · PT-006/PT-009 review | `MARKET_MODEL.md` §8 |
| Oct 29 | LNG Q3 · ICE Q3 · PT-007 CBOE expires at the close | LNG sleeve entry rule (unless LNG-A is invalidated) | `PROPOSAL.md` §1 |
| Oct 30 | CBOE Q3 | CBOE sleeve entry rule (options volume, fee/0DTE rule, exclusivity) | `PROPOSAL.md` §1 |
| Nov 2 | PT-005 monthly review | — | `PAPER_TRADES.md` §10 |
| Nov 4 | Treasury refunding · FICO earnings (est.) | Full base-case re-run · PT-004 expiry | `MARKET_MODEL.md` §8 |
| ~Nov 30 | Cohort readout (single read) | Program A | `RESEARCH_MAP.md` |
| Dec 11 | PT-001 ACN shadow ends | Did the confirmation filter protect or delay? | `PAPER_TRADES.md` |
| End-January 2027 | Program C falsification test | Has the daily state changed or prevented a recorded decision? | `RESEARCH_MAP.md` Program C |

**Standing conditions**

| When | Decision | Rule |
|---|---|---|
| Any day | A regime break: HY OAS ≥ 4%, IG OAS ≥ 1.10%, SOFR − IORB ≥ +10 bp outside quarter-end, or VIX > 20 with rising realised vol | Review every core thesis |
| Any day | Capital needed beyond the sleeve | *Which dollar has the weakest forward case?* Default is no swap (`PROPOSAL.md` §7) |
| Not yet | Tactical capital | **None** until a family has paper evidence (`PAPER_TRADES.md` rule 4) |
| Any day | Speculation | Only with the loss accepted in writing beforehand (`PROPOSAL.md` §6) |

## 7. Roster rules

| Type | Bucket | Examples | Expiry |
|---|---|---|---|
| **Permanent gauge** | PERMANENT GAUGES | SPY, 10Y, real yield, CCC OAS | None while useful. Re-screened when an instrument screen shows a cleaner source (Round 11 screened out 22 instruments) |
| **Long-horizon business thesis** | LONG-HORIZON BUSINESSES | CBOE, CME, LNG, TSM | Active until the thesis evidence changes. Reviewed after major information events |
| **Event watch** | ACTIVE SETUPS | Earnings cohort | When the pre-specified window closes; untriggered → EXPIRED — NO TRIGGER (+ SHADOW where specified) |
| **Tactical setup** | ACTIVE SETUPS | MU pullback, CBOE reclaim | When its horizon passes, its price structure changes or its thesis changes. Entry levels are never moved; a fresh setup needs a fresh record |
| **Regime watch** | ACTIVE SETUPS | Duration turn, index downside | Months, with dated reconfirmation ("ACTIVE REGIME WATCH — LAST REVIEWED <date>") tied to a thesis state in `MARKET_MODEL.md` §6 |
| **Research candidate** | RESEARCH CANDIDATES | ICE, SPGI | Reviewed at each evidence event; archived after two events without a promotion case. Resurfacing needs new evidence, not prior mention |

**Leaving this page.** Stale or archived items leave at the weekly review and are recorded in `ROUNDS.md` with the reason. Archived does not mean refuted; reviving an item needs a fresh record and new evidence. The pre-Round 13 archive table now lives in `ROUNDS.md` (Round 13), and older roster versions are in git.
