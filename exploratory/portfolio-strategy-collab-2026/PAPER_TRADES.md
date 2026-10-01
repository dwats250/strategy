# PAPER_TRADES — prospective setups and decision-quality ledger

**Canonical location:** `dwats250/strategy/exploratory/portfolio-strategy-collab-2026/PAPER_TRADES.md`
**Opened:** Round 5 — Claude (Fable 5.1) · 2026-10-01 14:10 ET
**Revised:** Round 6 — Claude (Opus 5.5) · 2026-10-01 ~15:00 ET — measurement infrastructure only.
The ten original plans below are **unchanged** (verbatim, under "Frozen plan"); Round 6 adds
annotations beneath each one. The only plan edit is the one ChatGPT Round 6 mandated for PT-006's
option clause, shown struck through rather than deleted.

**Purpose:** learn whether we form good observations, theses, setups, triggers, invalidations,
instrument choices and exits. Not a simulated brokerage. Results are reported in R, never in
simulated dollars.

## 1. Rules (binding)

1. **No hindsight.** A setup becomes a paper trade only if its plan was written before the trigger fired. Every entry is timestamped. After activation the thesis, entry, invalidation, setup, family and target logic are frozen; new information closes the record and opens a new one.
2. **Non-trades are data.** A setup whose confirmation fails is marked **EXPIRED — NO TRIGGER**, stays in the ledger permanently and is never loosened retroactively. It then gets a **SHADOW — counterfactual observation only** record through its original thesis horizon.
3. **One observation never changes a rule.** Rule changes need repeated evidence across a family.
4. **Ladder:** OBSERVATION → WATCH → FULLY SPECIFIED → PAPER TRIGGER → PAPER TRADE → REPEATED OBSERVATIONS → MICRO-LIVE CANDIDATE → larger capital only after evidence. Paper results show executability and coherence, not statistical edge; a family that keeps looking promising graduates to a retrospective study or forward sample next.
5. **Grades:** A good decision/good result · B good decision/bad result · C bad decision/good result (a warning) · D bad/bad. Optimise for A + B.
6. **Market Brief** is read-only evidence; decisions live here.
7. **Accounts never gate a setup.** TFSA, margin or LIRA is an execution note chosen at the trigger (tax and permission fit), not a research filter.
8. **Level-numbers govern (new records only, from Round 6).** Every level is written as a number fixed at the timestamp, with its description in brackets — e.g. "close < 214.50 [gap-day low at 14:10 ET]". If the described reference later moves, the number governs. Existing records are not edited; see PT-001's annotation for why this was added.

## 2. Capital gates — PAPER eligibility is separate from LIVE eligibility

**PAPER eligibility (research).** No dollar maximum. A paper option must be: a real listed
contract; quoted with bid, ask and mid at a contemporaneous timestamp; chosen before the move
being tested; liquid enough for a credible entry (§3); and executable under long-calls/long-puts
permissions apart from capital size. Stock vehicles need no gate beyond a real quote.

**MICRO-LIVE eligibility (current C$5,000 sleeve).**

| Vehicle | Normal | A+ |
|---|---|---|
| Long option — premium at risk (the whole premium counts, whatever stop is intended) | ≤ C$100 (2%) | ≤ C$150 (3%) |
| Shares — risk = shares × (entry − frozen invalidation) × USD/CAD | ≤ C$100 (2%) | ≤ C$150 (3%) |
| Shares — notional | ≤ C$1,500 (30%) | ≤ C$1,500 |

**A+** is earned by a family, not claimed by a trade: the family needs ≥ 3 completed paper
observations graded A or B with no process violation, and the current trigger must meet every
confirmation condition on its first test. Until then every live trade uses Normal. No limit is
raised because a good contract costs more; a strategy that works but does not fit becomes a
**future scale candidate**.

**Capital-eligibility labels (per vehicle):** `PAPER + MICRO-LIVE` · `PAPER ONLY — size` ·
`PAPER ONLY — permissions` · `PAPER ONLY — liquidity`. Labels on WATCH setups are provisional
(based on Oct 1 prices) and are re-assigned from the live quote at the trigger.

## 3. Contract-selection rule (written before any trigger; applied only at the trigger)

Sequence: THESIS → SETUP → TRIGGER → **live chain inspection** → contract selection → trade.
Reference contracts recorded on Oct 1 are illustrations, never specifications.

| Family | Delta target (est.) | Minimum DTE at entry | Expiry over earnings |
|---|---|---|---|
| EARNINGS_CONTINUATION, TREND_PULLBACK, BROKEN_LEADER_RECLAIM, TACTICAL_COMPOUNDER_ENTRY | calls 0.55–0.70 | max(75, 2 × planned max hold in calendar days + 21) | Allowed; record it and the pre-event IV |
| POST_SHOCK_REVERSAL | calls 0.50–0.65 | 90 | Allowed; record it |
| MACRO_DURATION_TURN | calls 0.40–0.60 | 90 | n/a |
| INDEX_DOWNSIDE | puts −0.35 to −0.55 | 75 | n/a |

- **Liquidity (paper credibility):** bid > 0; (ask − bid) ≤ 10% of mid (≤ 15% if mid < $1.00); open interest ≥ 250 at the strike **or** that day's volume ≥ 100.
- **Choice:** the first listed expiry at or beyond the minimum DTE, then the strike whose delta is nearest the family midpoint, ties broken by the tighter spread.
- **Delta:** Yahoo does not display delta; record "delta (est.)" computed with Black-Scholes from the quoted IV, mid, DTE and the 3-month bill yield.
- **None qualifies →** record **THESIS VALID / OPTION NO TRADE**; the share vehicle proceeds on its own.
- **Prices recorded:** mid (research result) **and** ask-in / bid-out (conservative result). The gap between them is the execution cost the lab measures.
- **Exit:** the underlying plan governs (invalidation, target, time stop). Option-specific: close when DTE reaches 21, or at the setup's time stop, whichever comes first. No premium stop on paper — the premium is the risk — but record what a −50% premium stop would have done.

## 4. SH (−1× S&P 500, daily reset) — tactical bearish vehicle

Permitted only inside an INDEX_DOWNSIDE record with: an explicit entry trigger, a thesis horizon,
a maximum hold and a time stop (PT-005: 2–6 weeks, time stop 20 sessions). Never a standing
allocation. Every SH record also records, over the identical close-to-close interval:

| Field | Definition |
|---|---|
| SPY return | close(exit) / close(entry) − 1, price only |
| Naïve expected inverse | −(SPY return) |
| Ideal daily −1× | ∏(1 − r_t) − 1 over each daily SPY return r_t in the interval |
| Actual SH return | SH close(exit) / close(entry) − 1 |
| Path effect | Ideal daily −1× − Naïve expected inverse (compounding/path dependence) |
| Fund drag | Actual SH − Ideal daily −1× (fees, financing, tracking) |

For any bearish thesis longer than 6 weeks, the record must also carry a long-put paper
vehicle selected under §3, so the lab can compare SH against waiting for a put.

## 5. Strategy families

| Family | Thesis type | Setups (mechanics, frozen) | Records |
|---|---|---|---|
| EARNINGS_CONTINUATION | Institutions re-rate after a de-risking print | A | PT-001 |
| TREND_PULLBACK | A leader in a rising trend is bought on an orderly pullback | B | PT-003, PT-010 |
| BROKEN_LEADER_RECLAIM | A growth leader that broke trend (below its 50/200-day) bases and reclaims | E | PT-002, PT-008 |
| POST_SHOCK_REVERSAL | An event-driven collapse overshoots the impairment | C | PT-004 |
| MACRO_DURATION_TURN | Long rates reverse; duration and rate-sensitive equity rerate | Duration rules (WATCHLIST §1) | PT-006, PT-009 |
| INDEX_DOWNSIDE | Index loses trend with weak breadth and high rates | D | PT-005 |
| TACTICAL_COMPOUNDER_ENTRY | A durable compounder shaken out without fundamental cause is re-entered on reclaim | E | PT-007 |

**Why VRT and HWM are not TREND_PULLBACK** (ChatGPT's Round 6 example list put them there): both
sit below their 50-day and 200-day averages (VRT 50d 261.7 < 200d 264.1; HWM price 228 under both),
so by the frozen definition of setup B ("50-day > 200-day, both rising; pullback 8–20%") they are
not pullbacks in a trend. They were written as setup E; changing the family would change the frozen
setup. BROKEN_LEADER_RECLAIM is added so they aggregate honestly.

**Why PT-006 and PT-009 are one family:** both depend on the same macro condition M1 (10Y weekly
close below its 10-week average). If both fire they count **once** for thesis quality and **twice**
(TLT shares, TLT call, ITB shares) for vehicle quality — a built-in vehicle comparison.

## 6. Ledger (status as of 2026-10-01 ~14:50 ET)

| ID | Written | Symbol | Setup | Family | Dir | Vehicles · capital eligibility (provisional) | Status | Thesis | Timing | Vehicle | Grade |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PT-001 | 10-01 14:10 ET | ACN | A | EARNINGS_CONTINUATION | Long | Shares: PAPER + MICRO-LIVE · Call: PAPER ONLY — size | WATCH — day-1 test resolves at 16:00 ET (14:49: 214.86 vs ≥ 221.07 needed) | — | — | — | — |
| PT-002 | 10-01 14:10 ET | VRT | E | BROKEN_LEADER_RECLAIM | Long | Shares: PAPER + MICRO-LIVE (2 sh normal) · Call: PAPER ONLY — size | WATCH | — | — | — | — |
| PT-003 | 10-01 14:10 ET | MU | B | TREND_PULLBACK | Long | Shares: PAPER ONLY — size · Call: PAPER ONLY — size | WATCH | — | — | — | — |
| PT-004 | 10-01 14:10 ET | FICO | C | POST_SHOCK_REVERSAL | Long | Shares: PAPER + MICRO-LIVE if stop ≤ US$70 · Option: PAPER ONLY — liquidity | WATCH — session 2 of 10 | — | — | — | — |
| PT-005 | 10-01 14:10 ET | SPY | D | INDEX_DOWNSIDE | Short | SH: PAPER + MICRO-LIVE · Put: PAPER ONLY — size | WATCH | — | — | — | — |
| PT-006 | 10-01 14:10 ET | TLT | Duration A | MACRO_DURATION_TURN | Long | Shares: PAPER + MICRO-LIVE · Call: chosen at trigger (Oct 1 strikes ≥ 84 fit Normal) | WATCH | — | — | — | — |
| PT-007 | 10-01 14:10 ET | CBOE | E | TACTICAL_COMPOUNDER_ENTRY | Long | Shares: PAPER + MICRO-LIVE (2 sh normal) · Call: PAPER ONLY — size | WATCH | — | — | — | — |
| PT-008 | 10-01 14:10 ET | HWM | E | BROKEN_LEADER_RECLAIM | Long | Shares: PAPER + MICRO-LIVE (2 sh normal) · Call: PAPER ONLY — size (expected) | WATCH | — | — | — | — |
| PT-009 | 10-01 14:10 ET | ITB | Duration equity | MACRO_DURATION_TURN | Long | Shares: PAPER + MICRO-LIVE · Option: PAPER ONLY — liquidity | WATCH | — | — | — | — |
| PT-010 | 10-01 14:10 ET | CLS (TSX) | B | TREND_PULLBACK | Long | Shares: PAPER + MICRO-LIVE (1 sh normal) · Option: PAPER ONLY — liquidity (TSX chain unverified) | WATCH | — | — | — | — |

Status vocabulary: WATCH · TRIGGERED → PAPER TRADE · CLOSED · **EXPIRED — NO TRIGGER** (+ SHADOW).
Completion columns: Thesis = confirmed / invalidated / unresolved · Timing = good / early / late /
never triggered / triggered falsely · Vehicle = appropriate / poor.

Regime/context common to all records (Oct 1, 2026): 10Y 5.29% close Sep 30 (24-yr high), 5.24%
intraday Oct 1 (range 5.21–5.34); Fed 3.75–4.00% after a Sep 16 hike; MOVE ~102–107 (record) vs
VIX ~16.5; 21% of S&P 500 above 50-day, 40% above 200-day (Sep 30); XLK the only sector up in
September; WTI ~$90; gold −25% from January record.

---

## 7. Detailed records

### PT-001 — ACN · post-earnings gap continuation (A) · Long

*Frozen plan (written 2026-10-01 14:10 ET):*
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

**Round 6 annotation — 2026-10-01 14:50 ET (plan above unchanged)**
- **Frozen:** yes. Family EARNINGS_CONTINUATION. Terminology: "void" in the plan now reads **EXPIRED — NO TRIGGER** (meaning unchanged).
- **Capital eligibility:** shares PAPER + MICRO-LIVE (3 sh, risk ≈ C$57, Normal). Call: PAPER ONLY — size (Oct 1 references: Dec 240 call ask 10.40 ≈ C$1,480; Nov 240 call ask 6.20 ≈ C$880). If the setup triggers, the paper call is chosen under §3 from the live chain.
- **Status:** WATCH. At 14:49 ET ACN 214.86 (+17.2%), day range 213.59–227.58, volume 22.3M vs 6.3M average (3.5×). Day-1 confirmation requires a close ≥ 221.07; it resolves at 16:00 ET. A scheduled follow-up records the close and, if it fails, marks **EXPIRED — NO TRIGGER** and opens the shadow.
- **Spec finding (not a rule change):** the plan wrote invalidation as "close < 214.50 (gap-day low)". By 14:49 the gap day's actual low was 213.59, so the number and its description diverged. Not material here (the setup is not active), but it is exactly the ambiguity that produces hindsight edits. Rule 8 (numbers govern) is adopted for new records only.
- **Shadow plan (if expired):** from the Oct 1 close through **Dec 11, 2026** (10-session entry window + 40-session time stop = session 50). Record: MFE and MAE from the Oct 1 close; whether 2R (~255) was reached before a close < 214.50; and whether a looser rule — entering on a close > 227.63 with no day-1 condition — would have triggered and how it would have resolved.

### PT-002 — VRT · base breakout after momentum break (E) · Long

*Frozen plan (written 2026-10-01 14:10 ET):*
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

**Round 6 annotation — 2026-10-01 14:50 ET (plan above unchanged)**
- **Frozen:** yes. Family BROKEN_LEADER_RECLAIM (not TREND_PULLBACK — see §5).
- **Capital eligibility:** shares PAPER + MICRO-LIVE at 2 sh (risk ≈ C$85 Normal); the plan's 3–4 sh is A+ territory and A+ is not yet earned. Call: PAPER ONLY — size (Oct 1 reference Dec 260 call ≈ C$3,170).
- **Status:** WATCH. Oct 1 14:49 ET: 247.06 (+2.4%), range 238.30–249.49. First possible test: the weekly close on Fri Oct 2 (needs > 262 on ≥ 1.5× volume). Suspension date Oct 20 (pre-earnings) unchanged.

### PT-003 — MU · pullback continuation in a leader (B) · Long

*Frozen plan (written 2026-10-01 14:10 ET):*
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

**Round 6 annotation — 2026-10-01 14:50 ET (plan above unchanged)**
- **Frozen:** yes. Family TREND_PULLBACK.
- **Capital eligibility:** shares PAPER ONLY — size (1 sh ≈ C$1,547 > C$1,500 notional cap; risk at a 10% stop ≈ C$155 > A+). Call: PAPER ONLY — size (Oct 1 reference Dec 1100 call ≈ C$14,000). MU is the clearest **future scale candidate** in the lab.
- **Status:** WATCH. 1,086.00 (+2.0%), range 1,022.90–1,095.13. A qualifying pullback needs ≥ 8% off the post-earnings high (≤ ~1,008 from 1,095.13) and a touch of the 20/50-day (50d ≈ 953).

### PT-004 — FICO · post-shock mean reversion (C) · Long

*Frozen plan (written 2026-10-01 14:10 ET):*
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

**Round 6 annotation — 2026-10-01 14:50 ET (plan above unchanged)**
- **Frozen:** yes. Family POST_SHOCK_REVERSAL.
- **Capital eligibility:** shares PAPER + MICRO-LIVE only if the base (high − low) ≤ ~US$70 per share (Normal) or ≤ ~US$105 (A+, not yet earned); otherwise PAPER ONLY — size. Option: fails **paper** liquidity as of Oct 1 (Dec chain $5–18 wide, OI < 50) → expected THESIS VALID / OPTION NO TRADE unless the chain normalises by the trigger.
- **Status:** WATCH — session 2 of 10 without a close below 586.05 (Sep 30 close 592.47 = session 1; Oct 1 ~669, +13%). Session 10 = **Oct 13**.
- **Observation (not a rule change):** the "close above the 20-day" condition is time-gated by the average's memory. FICO's 20-day was ~898 on Oct 1 because it still holds pre-shock closes near 930–1,000. If FICO simply holds 670, the 20-day falls to ~771 by Oct 13 and ~666 by Oct 27; at 750 it is ~803 and ~738. So the earliest realistic trigger is late October, after the Nov 4 earnings date approaches. The shadow/outcome will show whether that delay protects us or makes the setup systematically late; one record cannot decide it.

### PT-005 — SPY · macro downside (D) · Short

*Frozen plan (written 2026-10-01 14:10 ET):*
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

**Round 6 annotation — 2026-10-01 14:50 ET (plan above; vehicle clause clarified per ChatGPT Round 6)**
- **Frozen:** yes (trigger, invalidation, exits, horizon). Family INDEX_DOWNSIDE.
- **Vehicles at trigger (three, all from the same timestamp):** (1) **SH shares** — PAPER + MICRO-LIVE (~30 sh ≈ C$1,380, risk ≈ C$60 Normal); (2) **SPY put** chosen under §3 (delta −0.35 to −0.55, ≥ 75 DTE) — PAPER ONLY — size (Oct 1 references: Dec 740 put ≈ C$1,697; Dec 700 put ≈ C$862); (3) **short SPY** as the underlying reference. The SH record carries the §4 fields (naïve inverse, ideal daily −1×, path effect, fund drag); the put carries the §8 underlying shadow. Together they answer "SH now vs an affordable put later" with data.
- **Status:** WATCH. SPY 764.31 at 14:49 ET (range 758.79–765.33); trigger needs a close < 750 with ≥ 3 of 5 conditions. Breadth condition met (21%, Sep 30); the 10Y condition is evaluated at trigger (the 10Y eased to 5.24% intraday Oct 1).

### PT-006 — TLT · duration turn, Stage A (regime) · Long

*Frozen plan (written 2026-10-01 14:10 ET):*
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
  - Long call, only if ≥ 90 DTE remain at trigger: **TLT Jan 15 2027 82 call** — read live Oct 1 ~14:00 ET: bid 1.05 / ask 1.07 / mid 1.06, IV 15.7%, OI 28,594, vol 827, 106 DTE, premium US$107 = **C$152**, thesis expiry Dec 15 (30 DTE). Delta not shown (est. ~0.25 from moneyness). Also read: Jan 80 call 1.70/1.71 (OI 67,473, C$243 — over budget); Jan 83 call 0.82/0.83 (OI 32,044, C$118); Dec 80 call 1.40/1.44 (C$205). Breakeven 83.06 (+6.5%); at TLT 86 (+10%) intrinsic 4.00 = 3.8× premium. Theta: ~1% of premium per day at 60 DTE. **Versus shares:** the call pays ~4× on a 10% move where 10 shares pay +US$78; it loses 100% on a correct-but-late thesis. ~~Rule: the call only if the trigger fires by Oct 17 (≥ 90 DTE); after that, shares.~~ *(withdrawn Round 6 — see annotation)*

**Round 6 annotation — 2026-10-01 14:50 ET (trigger unchanged; option clause amended per ChatGPT Round 6)**
- **Frozen:** trigger M1–M3 + one optional, invalidation, exits, horizon — unchanged. Family MACRO_DURATION_TURN.
- **Amendment (pre-activation, vehicle only):** the clause "Rule: the call only if the trigger fires by Oct 17 (≥ 90 DTE); after that, shares" is **withdrawn**. The date existed only because the plan was bound to one contract (Jan 15 '27 82 call); there is no market or catalyst reason for Oct 17. The Jan '27 82 call stays as an Oct 1 **reference**. At trigger: open the live chain and select under §3 (delta 0.40–0.60, ≥ 90 DTE); if none qualifies → THESIS VALID / OPTION NO TRADE; shares remain a separate vehicle either way.
- **Capital eligibility:** shares PAPER + MICRO-LIVE (10 sh ≈ C$1,110, risk ≈ C$40). Call: decided at trigger. On Oct 1 prices the 82 call (ask 1.07 ≈ C$152) misses even A+ by C$2; the 83 (ask 0.83 ≈ C$118) needs A+; the 84 (ask 0.65 ≈ C$93) fits Normal — but 84 is further OTM than the delta target. A live-eligible duration call may therefore be a *worse* expression than the paper one; the lab records both.
- **How the frozen trigger maps to ChatGPT's activation list:** long yield stops making higher highs → M1 (10Y weekly close below its 10-week average, average no longer rising); TLT stops making lower lows / reclaims trend → M2 (TLT weekly close above its 50-day); real-yield pressure stabilises → optional (a) 30Y real ≥ 20 bp off its high; curve not contradicting → not mandatory in the frozen rule. That gap is noted, not patched; it becomes a candidate for a successor record only if a duration turn fires with a contradicting curve.
- **Status:** WATCH. Oct 1: TLT printed a **new 52-week low of 76.76 intraday**, then traded 77.74 (+0.3%); 10Y 5.24% (−5 bp, range 5.21–5.34). Daily closes Sep 16→Sep 30 fell from 80.88 to 77.78. No weekly condition can be met before the Oct 2 close.

### PT-007 — CBOE · 50-day reclaim after a shakeout (E) · Long (tactical, separate from the strategic hold)

*Frozen plan (written 2026-10-01 14:10 ET):*
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

**Round 6 annotation — 2026-10-01 14:50 ET (plan above unchanged)**
- **Frozen:** yes. Setup E; family TACTICAL_COMPOUNDER_ENTRY (thesis is the business, mechanics are the reclaim).
- **Capital eligibility:** shares PAPER + MICRO-LIVE at 2 sh (risk ≈ C$74 Normal; the plan's 3 sh ≈ C$110 is A+). Call: PAPER ONLY — size (Oct 1 reference Jan '27 300 call ≈ C$2,190; IV ~40%).
- **Status:** WATCH. 277.96 (+1.0%), range 273.94–283.46; trigger needs a close > 288 on ≥ 1.5× volume.
- **Note:** this is the tactical record only. The strategic CBOE holding and CME's separate thesis are in `ROUNDS.md` Round 6.

### PT-008 — HWM · base breakout (E) · Long

*Frozen plan (written 2026-10-01 14:10 ET):*
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

**Round 6 annotation — 2026-10-01 14:50 ET (plan above unchanged)**
- **Frozen:** yes. Family BROKEN_LEADER_RECLAIM.
- **Capital eligibility:** shares PAPER + MICRO-LIVE at 2 sh (risk ≈ C$74 Normal); the plan's 4 sh ≈ C$148 is A+. Call: not inspected; PAPER ONLY — size expected.
- **Status:** WATCH. 228.31 (+0.9%), range 225.00–229.29 — still inside the 224–233 range; trigger needs a close > 248.

### PT-009 — ITB · rates-turn equity expression (new, independent) · Long

*Frozen plan (written 2026-10-01 14:10 ET):*
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

**Round 6 annotation — 2026-10-01 14:50 ET (plan above unchanged)**
- **Frozen:** yes. Family MACRO_DURATION_TURN (equity expression; shares M1 with PT-006).
- **Capital eligibility:** shares PAPER + MICRO-LIVE (12 sh, risk ≈ C$55). Option: fails paper liquidity on Oct 1 (non-standard adjusted strikes, OI mostly < 500) → OPTION NO TRADE unless the chain normalises.
- **Status:** WATCH. 87.15 (+0.1%) after a **new 52-week low of 84.81 intraday** Oct 1 — 0.81 above the frozen 84.00 invalidation, which only applies after activation. M1 not met; the mortgage condition needs MND ≤ 7.35% (7.60% on Sep 30).

### PT-010 — CLS · pullback continuation in a leader (B, new independent) · Long

*Frozen plan (written 2026-10-01 14:10 ET):*
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

**Round 6 annotation — 2026-10-01 14:50 ET (plan above unchanged)**
- **Frozen:** yes. Family TREND_PULLBACK.
- **Capital eligibility:** TSX shares PAPER + MICRO-LIVE (1 sh ≈ C$531, risk ≈ C$56 Normal; 2 sh = A+). Option: TSX chain liquidity unverified → PAPER ONLY — liquidity until inspected; NYSE CLS options expected PAPER ONLY — size.
- **Status:** WATCH. CLS.TO C$531.15 (+3.2%), range 505.43–537.00 — extending, not pulling back. Oct 26 earnings/Investor Day re-arm clause unchanged.

---

## 8. Completion records (templates)

**Every completed record — three separate questions.**

```
Entry timestamp: | Entry reference price: | Planned R (entry − frozen invalidation):
MFE (R): | MAE (R): | Exit timestamp: | Exit reference price: | Exit reason (target / invalidation / time / pre-specified rule):
THESIS QUALITY   — did the underlying thesis occur? confirmed / invalidated / unresolved (+ evidence)
TIMING / SETUP   — good / early / late / never triggered / triggered falsely (+ evidence)
VEHICLE QUALITY  — shares: did the stop structure make sense?
                   option: delta useful? theta material? IV expansion helped / compression hurt?
                           expiry appropriate? strike appropriate? bid/ask damage (mid vs ask-in/bid-out)?
Process violation: yes / no | Grade: A / B / C / D | Primary lesson (one sentence):
```

**Every paper option — underlying shadow from the same timestamps.**

```
Underlying: entry | exit | MFE | MAE | direction correct / incorrect
Option:     entry mid (ask) | exit mid (bid) | MFE | MAE | IV entry→exit | DTE lost | result (× premium)
Class:      UNDERLYING CORRECT / OPTION CORRECT
            UNDERLYING CORRECT / OPTION FAILED      ← the structure destroyed a useful idea
            UNDERLYING WRONG   / OPTION LOST
            UNDERLYING WRONG   / OPTION PROFITED    ← a warning, not a success
```

**Every SH record — §4 fields** (SPY return, naïve inverse, ideal daily −1×, actual SH, path effect, fund drag).

**Every expired setup — shadow.**

```
SHADOW — counterfactual observation only (not a paper trade)
Window: from the expiry timestamp through the original thesis horizon
Subsequent MFE: | Subsequent MAE: | Did the original directional thesis occur? yes / no / partly
Would a looser rule have worked? (name the looser rule, state the result) | Evidence weight: one observation
```

---

## 9. Observations not advanced to setups (recorded so they are not re-invented)

- **EWZ post-election** (Round 3): regime position; re-specify after Oct 4 / Oct 25 if desired.
- **QQQ downside:** correlated with PT-005; one index short at a time.
- **UNH Oct 13 reaction:** eligible for a Strategy A record if it gaps ≥ 8% on a beat/raise; write the record **before** the print, not after.
- **CME ≤ ~$225 (≈ 18x forward):** a Strategy F durable-hold trigger, not a paper trade (see `ROUNDS.md` Round 5).
- **U.UN / uranium:** SPUT discount < 5% trigger (`WATCHLIST.md` §5b).
