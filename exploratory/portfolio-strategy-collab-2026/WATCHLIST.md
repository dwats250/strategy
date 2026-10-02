# Market Roster (WATCHLIST.md)

**What this file is:** the page to open on an ordinary trading day. It answers:
- what state the market is in, and what would change our reading (the **DAILY STATE**);
- what markets matter, and what each one is telling us;
- what businesses we care about;
- what setups are developing;
- what has gone stale;
- what would actually cause capital to move.

The model behind the daily state (transmission map, instrument map, thesis register, contradictions log, adversarial challenge) lives in `MARKET_MODEL.md`. Research detail lives in `RESEARCH_MAP.md`, trade plans in `PAPER_TRADES.md`, history in `ROUNDS.md`.

**Version:** Round 11 — Claude (Opus 5.5) · values as of the **Oct 1, 2026 close** unless marked. Round 11 did three things to this page:
- added the DAILY STATE;
- sorted the roster into four buckets;
- re-tiered the gauges after the instrument screen.

Round 10's roster is in git history (commit `792fce3`).

**Reading order (≈ 5 minutes):**
1. Today's DAILY STATE against yesterday's — what changed?
2. Thesis states — did any change, and on what evidence?
3. Decision points due in the next five sessions.
4. Active setups.

---

## 1. DAILY STATE

**Purpose: continuity.** Tomorrow's reasoning starts from today's state instead of reconstructing everything.
- One line per field. Write "unchanged" where nothing moved.
- Cite theses by name (`MARKET_MODEL.md` §6) and contradictions by ID (§7).
- Keep the **latest state and the one before it**; older states live in git history, one commit per state (Round 12: this page stays current; history stays recoverable). Daily states do not go into `ROUNDS.md`.
- Template fields are fixed. A field is added or dropped only at a scheduled review (next: Nov 4), never because today's data looked interesting.

### Template

```
DAILY STATE — YYYY-MM-DD (close) · previous: YYYY-MM-DD
RATES          Observed: 2Y · 10Y · 30Y · 10Y real · 10Y breakeven · fed funds strip (next Dec / ~6–8 months out) · 2s10s · MOVE
               Interpretation: — | Contradictions: — | What changes the view: —
CREDIT         Observed: IG / HY / CCC OAS · HYG · BKLN                       (same three fields)
DOLLAR/LIQ.    Observed: broad $ · DXY · USD/JPY · USD/CAD · funding alarm on/off
COMMODITIES    Observed: WTI front · WTI 12-month slope · gold · copper
EQUITIES       Observed: SPY · RSP · IWM vs 50-day · % above 50-day · (weekly) forward P/E
VOL/POSITIONS  Observed: VIX · MOVE · systematic-exposure estimate (when published)
REGIME WATCHES Thesis states changed today (+ evidence note) · regime-watch records' status
CAPITAL-MOVING Dated decisions within 5 sessions · alarms tripped · live-capital status
```

### DAILY STATE — 2026-10-01 (close) · previous: none (first state)

**Rates**
- *Observed:*
  - 2Y 4.88% (Sep 30); ≈ 4.78% on Oct 1, implied by FRED's 2s10s of 0.46 (the Oct 1 2Y print is not yet published) — the front end led Oct 1's rally;
  - 10Y 5.24% · 30Y 5.60%;
  - 10Y real 2.93% (Sep 30) · breakeven 2.36%;
  - fed funds strip: Dec 4.08%, May '27 4.50% against effective 3.88% (≈ 2½ more hikes);
  - 2s10s 46 bp (Oct 1; +11 bp Jun 30 → Sep 30) · MOVE 108.
- *Interpretation:* POLICY-LED REAL-RATE REPRICING — ACTIVE. Term premium is a large minority (~45%, model-dependent). OIL → FED REACTION — FORMING (inferred; the Fed's statement does not name energy). DURATION TURN — DORMANT.
- *Contradictions:* C-008 (oil hasn't reached breakevens), C-009 (not global).
- *What changes the view:* WTI front-month below $80 without the 10Y falling (W1); breakevens > 2.60% (W4); the 2Y ignoring oil through October plus a growth-based FOMC rationale (W5); long-end auction tails ≥ 2 bp on Oct 7–8.

**Credit**
- *Observed:* IG OAS 0.84% · HY 3.12% (+44 bp in the week) · CCC 11.79% · HYG 76.90 (52-week low) · BKLN 20.46 (price flat; +2.2% total return in 3 months).
- *Interpretation:* repricing with a deteriorating tail. CCC TAIL REPRICING — ACTIVE; CREDIT STRESS (broad) — DORMANT.
- *Contradictions:* C-003 (conditions looser), C-004 (loans fine while CCC widens).
- *What changes the view:* IG ≥ 1.00% together with HY ≥ 3.75%; BKLN closes below 20.21.

**Dollar / liquidity**
- *Observed:* DXY 102.02 (52-week high) · broad dollar 120.33 (Sep 25; 120.92 on Jun 30) · USD/JPY 157.9 · USD/CAD 1.4222 · SOFR 3.90% = IORB · ON RRP ≈ 0.
- *Interpretation:* euro weakness, not broad dollar strength. DOLLAR CHANNEL — FORMING. Funding alarm off.
- *Contradictions:* C-001, C-007.
- *What changes the view:* broad dollar > 2% above its Jun 30 level with rate spreads widening. Funding: SOFR − IORB > +5 bp outside month-end moves it to daily watch; > +10 bp outside quarter-end is a regime-break alarm.

**Commodities**
- *Observed:* WTI 93.00 (Dec '27 75.29: −19% backwardation) · Brent Dec 102.43 · gold 4,211.5 (−21% from the January high, +4% since Jun 30) · copper 6.58.
- *Interpretation:* the oil shock is priced as temporary (LOOP-1's premise). Gold tracks the dollar more than real yields: GOLD AS A RATE CASUALTY — WEAKENING.
- *Contradictions:* C-002, C-008.
- *What changes the view:* WTI < $80 with the backwardation narrowing (the P6 test); a month of gold falling with real yields while the dollar is flat.

**Equities / breadth**
- *Observed:* SPY 763.99 (on its 50-day, −1.8% from its high) · RSP −3.6% and IWM −3.7% over 1 month · 23% of S&P above the 50-day · forward P/E 19.2 and Q3 EPS est. +29% (Sep 25).
- *Interpretation:* BREADTH / RATE-SENSITIVE ROTATION — ACTIVE; INDEX EARNINGS OFFSET — ACTIVE. At the index, earnings growth has so far offset the discount rate (C-005 open on why).
- *Contradictions:* C-005.
- *What changes the view:* how broad the Q3 beats are; breadth > 50% with the 10Y ≥ 5% (W3).

**Volatility / positioning**
- *Observed:* VIX 16.39 (200-day 18.1 — ordinary, not unusually calm) · MOVE 108.1 (March peak 115) · vol-control exposure at the 98th–100th percentile.
- *Interpretation:* fuel without a trigger. SYSTEMATIC DELEVERAGING — FORMING.
- *Contradictions:* C-006.
- *What changes the view:* VIX > 20 with realised vol rising and SPY below its 50-day.

**Active regime watches**
- PT-006 TLT / PT-009 ITB: ACTIVE REGIME WATCH — LAST REVIEWED 2026-10-01. M1/M2 not met; the thesis is DORMANT.
- PT-005 SPY: WATCH. 2 of 5 conditions met (breadth, 10Y high); trigger needs a close < 750. C-005 is its main counter-evidence; review Nov 2.
- State changes today: register opened; GOLD → WEAKENING; OIL → FED REACTION opened at FORMING.

**Capital-moving conditions**
- Within 5 sessions: none dated.
- Evidence dates: Oct 7 NFCI (week to Oct 2) and 10Y auction · Oct 8 30Y auction · Oct 14 CPI · Oct 15 TSM (sleeve tranche-2 rule).
- Regime-break alarms (review every core thesis): HY OAS ≥ 4% · IG OAS ≥ 1.10% · SOFR − IORB ≥ +10 bp outside quarter-end · VIX > 20 with rising realised vol. None tripped.
- Live tactical capital: none (no family has paper evidence).

## 2. Base case and its rival (full version: `MARKET_MODEL.md` §8)

*Last changed: 2026-10-01 (Round 11 — replaces Round 10's narrative).*
- **Base case: policy-led real-rate repricing, most likely triggered by the oil supply shock.** The Fed hiked with core CPI at 2.4% and headline at 3.4%; its statement does not name energy, so the oil link is inferred. The 10Y's rise is ~85% real, and roughly 55% policy path / 45% term premium.
  - Transmission is visible where the link is mechanical, or plausible and observed: mortgages, homebuilders, small caps, the CCC tail.
  - It is not visible in IG credit, bank lending, funding or financial-conditions indices. At the index, earnings have so far offset it.
  - It is self-limiting if oil rolls over.
  - It is tested against the benign alternative by P5, P6, P8 and P10, with P8 and P10 testable without any oil move.
- **Best alternative: growth-led normalisation.** Strong profits justify higher real rates; nothing cascades; yields stay high even if oil falls.
- **Second alternative (less supported, not by a wide margin): fiscal/term-premium stress** ending in a funding accident. Term premium is a large minority, and the curve has bear-steepened mildly.
- **Round 10 statements corrected** (logged in `MARKET_MODEL.md` §7, not erased; C-006 is graded a research note):
  - "the pressure is global" (C-009);
  - "the dollar is transmitting the shock" (C-001);
  - "gold reflects real-yield pressure" (C-002);
  - "equity vol is calm" (C-006 — VIX is ordinary; the anomaly is MOVE vs VIX).

## 3. PERMANENT GAUGES (never expire while useful)

Tiered after the Round 11 instrument screen (`MARKET_MODEL.md` §4–§5). Yahoo daily closes unless marked; FRED series carry their own date.

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

## 4. LONG-HORIZON BUSINESSES (remain while the thesis is active)

A business sits here only with a written thesis and counter-thesis. Roles describe its place in Dustin's **whole program**, not its sleeve weight.

| Business | Program | Role (program level) | Oct 1 | vs 50d / 200d · off high | Status | Next review event | What would change it | Regime link (Round 11) |
|---|---|---|---|---|---|---|---|---|
| **CBOE** (sleeve: held) | D | CORE candidate (named dependency: SPX × retail short-dated × regulation) | 277.19 | 288.0 / 287.0 · −24% | Thesis intact | Q3, Oct 30; monthly volume (~Oct 2–5) | Options volume negative y/y for two quarters; a fee or 0DTE rule; loss of exclusivity | Volumes respond to *equity* vol. A rates-only shock (C-006) is a weak kicker |
| **CME** | D | CORE candidate (not held) | 265.10 | 270.3 / 278.5 · −19% | Approved candidate; Strategy F trigger ≤ ~$220 or clearing growth ≥ ADV growth | **Q3, Oct 21**; September volume | FMX share gains; a volume regime pinned at zero rates | **Supportive:** its engine is an active rate path, which is today's regime (~2½ hikes priced, MOVE 108). Not a trigger |
| **LNG** (sleeve: held) | E | CORE (existing asset) + embedded growth option | 272.40 | 272.1 / 246.5 · −8% | Thesis intact (LNG-A / LNG-B) | **Q3, Oct 29**; FERC on the expansion (late 2026) | LNG-A: contracted share < ~85% or tenor < ~12 years. LNG-B: permit denial, or FID slipping past 2027 | Fees are contracted, so oil and gas prices do not drive LNG-A. Higher real yields lower the value of long-dated cash flows and raise LNG-B's financing cost |
| **TSM** (sleeve: held, 26% of the sleeve) | H | **SATELLITE** (geopolitical tail) | 459.20 | 423.8 / 386.2 · −4% | Thesis intact; tranche 2 conditional on Oct 15 | **Q3, Oct 15**; monthly revenue (~10th) | Two hyperscalers cutting capex; N2 failure; a cross-strait event (handled by size) | Long-duration growth whose discount-rate exposure is so far outrun by earnings (FY26 EPS +63%). Not a rates bet |

## 5. ACTIVE SETUPS (each has activation, invalidation and horizon — or it is archived)

Full plans and annotations are in `PAPER_TRADES.md`.

| Record | Family | Watch type | Activation (frozen) | Invalidation | Expires / reviewed | Oct 1 status | Thesis link (`MARKET_MODEL.md` §6) |
|---|---|---|---|---|---|---|---|
| PT-002 VRT | Broken-leader reclaim | Tactical setup | Weekly close > 262 on ≥ 1.5× volume | Close < 232 | **Oct 20 close** | 246.12 | — |
| PT-003 MU | Trend pullback | Tactical setup | Pullback ≥ 8% touching the 20/50-day, then a close above the prior high | Close below the pullback low | First close below the 50-day without a qualifying pullback, or Dec earnings | 1,097 — extended | — |
| PT-004 FICO | Post-shock reversal | Tactical setup | 10 sessions without a close < 586.05 + reclaim of the 20-day + close above the base high | Close below the base low | Next earnings (est. Nov 4), or a close < 586.05 | 661.75 — session 2 of 10 | — |
| PT-005 SPY | Index downside (G) | Regime-linked tactical | Close < 750 with ≥ 3 of 5 conditions | Close above the 50-day | Monthly (next **Nov 2**) and after FOMC (Oct 28) | 763.99; 2 of 5 met | BREADTH ROTATION (ACTIVE) vs EARNINGS OFFSET (ACTIVE); C-005 |
| PT-006 TLT | Duration turn (C) | **ACTIVE REGIME WATCH — LAST REVIEWED 2026-10-01** | M1–M3 + 1 optional (weekly) | 10Y +40 bp / trigger-week low | Monthly; after CPI (Oct 14), FOMC (Oct 28), refunding (Nov 4) | 77.71 | DURATION TURN (DORMANT); route most likely LOOP-1 |
| PT-007 CBOE | Tactical compounder entry | Tactical setup | Close > 288 on ≥ 1.5× volume | Close < 262 | **Oct 29 close** | 277.19 | — |
| PT-008 HWM | Broken-leader reclaim | Tactical setup | Close > 248 on ≥ 1.5× volume, then a weekly close > 260 | Close < 222 | **Oct 28 close** | 228.38 | — |
| PT-009 ITB | Duration turn (C) | **ACTIVE REGIME WATCH — LAST REVIEWED 2026-10-01** | M1 + MND ≤ 7.35% + close above the 20-day | Close < 84.00 | With PT-006 | 87.37 | DURATION TURN (DORMANT); HOUSING TRANSMISSION (ACTIVE) |
| PT-010 CLS | Trend pullback | Tactical setup | 8–12% pullback holding the 20-day, then a close above the prior high | Pullback low / 50-day | **Oct 26 close** | 373.09 — extended | — |
| Cohort E-01…E-10 | Earnings (A) | Event | Setup A / A-M per the mechanical rule | Completed day-1 RTH low | Each closes at its D+20 | First: UNH, Oct 13 (pre-registration Oct 12) | — |

## 6. RESEARCH CANDIDATES (interesting, not promoted)

**Lifecycle (Round 11):** a candidate is reviewed at its next evidence event. It is promoted only by a written thesis (→ §4) or a frozen setup (→ §5). If two evidence events pass without a promotion case, it is archived.

| Candidate | Program | Why it is interesting | What would promote it | Next evidence |
|---|---|---|---|---|
| **ICE** | D | Exchanges + data + mortgage technology; the mortgage segment is the kicker in a rates turn | A written thesis with counter-thesis and a trigger | Q3, Oct 29 |
| **SPGI** | D | A damaged tollbooth (−25% from its high); ratings issuance + indices | Cohort E-08 outcome plus a thesis on issuance cyclicality | Q3, Oct 27 |
| **MU** | H / B | Memory-cycle leader. Its role is TACTICAL; a business case needs underwriting through the cycle | A through-cycle thesis (contract pricing, capex discipline) | Dec earnings; TrendForce pricing |
| **VRT** | H / B | AI power and cooling; −35% from its high | Post-earnings thesis on orders and backlog | Q3, Oct 21 (est.) |
| **CLS** | H / B | AI hardware manufacturing; customer concentration | Investor Day evidence on customer breadth | Q3, Oct 26; Investor Day Oct 27 |
| **UNH** | A | First cohort event; a damaged leader | The cohort event itself (PT-011 pre-registered the evening before) | Oct 13 |

## 7. What would actually cause capital to move (decision points, dated)

**Note (Round 12):** the sleeve is **not executed** (`PROPOSAL.md`). The "tranche 2 / third share" decisions below assume a first tranche that does not yet exist. Unless Dustin executes tranche 1 first, each date is a **first-entry** decision under the same written conditions.

| Date | Decision | Rule already written | Where |
|---|---|---|---|
| Oct 15 | TSM tranche 2 (sleeve) | Buy only if Q4 guidance ≥ consensus **and** 2026 capex is held or raised **and** the > 40% growth outlook is intact | PROPOSAL §1; ROUNDS R5 |
| Oct 21 | CME — candidate to enter | Strategy F: ≤ ~$220 **or** clearing/transaction revenue growing at least as fast as ADV. Entering would also need the capital-reallocation comparison (PROPOSAL §7) | ROUNDS R5–R6 |
| Oct 29 | LNG tranche 2 (sleeve) | After the print, unless LNG-A is invalidated | PROPOSAL §1 |
| Oct 30 | CBOE third share (sleeve) | After the print, unless options volume is negative y/y, a fee/0DTE rule appears, or exclusivity is lost | PROPOSAL §1 |
| Any day | A regime break | **HY OAS ≥ 4%, IG OAS ≥ 1.10%, SOFR − IORB ≥ +10 bp outside quarter-end, or VIX > 20 with rising realised vol** → review every core thesis (Round 11 adds the IG and funding alarms) | §1; `MARKET_MODEL.md` §8 |
| Any day | Capital needed beyond the sleeve | **Which dollar has the weakest forward case?** Unrealised gain or loss is not a reason (Round 11) | PROPOSAL §7 |
| Not yet | Tactical capital | **None.** No family has completed paper evidence; live capital needs PAPER TRADE + REPEATED OBSERVATIONS | PAPER_TRADES rule 4 |
| Any day | Speculation | Only with the loss accepted in writing beforehand | PROPOSAL §6 |

## 8. Watch lifecycle

| Type | Bucket | Examples | Expiry |
|---|---|---|---|
| **Permanent gauge** | PERMANENT GAUGES | SPY, 10Y, real yield, CCC OAS | None while useful. Re-screened when an instrument screen shows a cleaner source (Round 11 screened out 22 instruments) |
| **Long-horizon business thesis** | LONG-HORIZON BUSINESSES | CBOE, CME, LNG, TSM | Active until the thesis evidence changes. Reviewed after major information events |
| **Event watch** | ACTIVE SETUPS | Earnings cohort | When the pre-specified window closes; untriggered → EXPIRED — NO TRIGGER (+ SHADOW where specified) |
| **Tactical setup** | ACTIVE SETUPS | MU pullback, CBOE reclaim | When its horizon passes, its price structure changes or its thesis changes. Entry levels are never moved; a fresh setup needs a fresh record |
| **Regime watch** | ACTIVE SETUPS | Duration turn, index downside | Months, with dated reconfirmation ("ACTIVE REGIME WATCH — LAST REVIEWED <date>") tied to a thesis state in `MARKET_MODEL.md` §6 |
| **Research candidate** (new, Round 11) | RESEARCH CANDIDATES | ICE, SPGI | Reviewed at each evidence event; archived after two events without a promotion case |

## 9. Stale / archived

Archived ideas are not refuted. They are no longer described by a live thesis, setup and horizon. Reviving one needs a fresh record.

| Item | Archived | Why |
|---|---|---|
| Round 4 tactical board | R10 | Superseded by `PAPER_TRADES.md` |
| MBB → TLT duration ladder | R10 | Superseded by PT-006/PT-009. MBB is now a **gauge only** (Round 11: negative convexity makes it a poor duration vehicle) |
| Gold/metals entry rules | R10 | Gold is a gauge. Metals decisions belong to the exposure map and the capital-reallocation comparison |
| Power and electrification (GEV, ETN, BE, GRID, VST, CEG) | R10 | No live record; AI-power is studied through VRT, CLS and HWM |
| Energy tactical rules (XLE, XEG) | R10 | Energy is a gauge; no live energy thesis |
| Semiconductors/SMH | R10 | Covered by TSM and MU |
| Brazil/EWZ · uranium · the parked list · the chaos-regime map | R10 | No live thesis (details in git history before `f4757b7`) |
| **PT-001 ACN** | **R11** | EXPIRED — NO TRIGGER (Oct 1). Its SHADOW record continues in `PAPER_TRADES.md` to Dec 11; it no longer needs a roster line |
| **WMB** | **R11** | Never a thesis we held: "not attractive at price" (28x forward, negative FCF) and kept only as LNG's comparison. Revival: forward P/E < ~20 or FCF turning positive |
| **Rates/credit instruments removed by the Round 11 screen** | **R11** | USFR, SHV, BIL · VGIT, SHY, GOVT · EDV, ZROZ · TIP, SCHP, STIP, VTIP · VMBS · VCSH, IGSB · JNK · SRLN, FLOT · XHB · XLU, VNQ, IYR as rate gauges. Each duplicates a kept instrument or a direct FRED series, or mixes drivers (`MARKET_MODEL.md` §4) |
| **Round 10 narrative claims** | **R11** | "Pressure is global", "dollar transmission", "gold real-yield pressure", "equity vol calm" — corrected, with the evidence in contradictions C-001, C-002, C-006, C-009 |

## 10. Research questions that deserve time now

The full queue is in `RESEARCH_MAP.md`. The four nearest to changing decisions:
1. **The cohort analysis.** Frozen before UNH (Oct 13); a single readout after the last cohort event's D+20 (~Nov 30).
2. **The exposure map.** The schema is defined (`RESEARCH_MAP.md`, Mandate). Filling it is the precondition for any capital moving outside the sleeve; it does not need to wait for the cohort readout.
3. **What ended past real-rate repricings** (2006–07, 2018, Oct 2023): oil, data, or the Fed? This is the LOOP-1 test and sharpens PT-006 before it is needed.
4. **Gold attribution** — dollar vs real yields vs official buying, month by month since 2022. This matters for Dustin's metals holdings more than for any trade.
