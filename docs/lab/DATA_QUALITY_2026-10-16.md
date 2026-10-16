# Data quality — SPY 1-minute (Massive): suspicious extreme prints (2026-10-16)

**Status: unresolved, documented, scope measured.** No mask was adopted, no result was replaced, nothing
was re-run.

## What was observed

On **2025-04-23**, from about 11:28 ET onward, over a hundred RTH minutes carry highs at **$544–545**,
while their bodies trade at $534–539 and Massive's own per-minute VWAP stays at the body. The frozen
mask v1.0 (an isolated-spike rule) does not catch a cluster. A trade-blind scan flags 122 such minutes in
the August corpus: 111 on 2025-04-23, and 11 spread over 9 other sessions
(`studies/vwap-ema9-2026-10/analysis/diagnose_offmarket_wicks.py`).

## What each check establishes

| Check | Result | What it shows | What it does not show |
|---|---|---|---|
| Second Massive capture (2026-10-16) | All 179,670 overlapping RTH minutes identical (`DATA_COMPARE_a4afaa70_vs_729dc4e9_2026-10-16.json`) | The prints **persist** in the vendor's current data. The August capture did not garble them. | That they are correct |
| Massive tick trades with condition codes | **HTTP 403**: not included in the plan, and no upgrade was made | — | Whether the prints carry late, out-of-sequence or other non-high/low-eligible conditions |
| **Yahoo Finance hourly bars** (free, no account; independent processing) | Hourly closes identical to the cent in 85% of 2,886 hours (median difference $0.00). On 2025-04-23 Yahoo's **morning** highs match ($545.40 vs $545.43), but every hour from 11:30 has Yahoo highs of **$537.17–$539.59** against Massive's **$544.54–$545.16** | An independent source does **not** show the midday $545 prints | That they were unexecutable: Yahoo may apply its own filters, and it is not ground truth |
| Calibration on mask v1.0's prints | Yahoo also lacks 4 of the masked minutes' extremes (2024-12-20, 2025-03-14, 2025-04-16, 2025-12-22) but **shows** 2 (2025-05-19, 2025-05-27) | Yahoo is not simply smoothing everything, and mask v1.0 is only partly corroborated | — |
| Wider scan | 31 hours (2024-12-18 → 2026-08-21) where Massive's high or low lies more than $0.50 beyond Yahoo's: 14 highs and 17 lows, including unmasked ones such as 2026-06-09 (Massive low $730.77 vs Yahoo $740.35) | The issue is broader than one day, but rare | — |

## Affected scope in recorded results (diagnostic only)

These are stop exits in `VWR0-EXP__20261016T211249Z` whose fill price lies outside Yahoo's range for that
hour (`analysis/compare_independent_hourly.py`, output `DIAGNOSTIC_independent_hourly_VWR0-EXP_2026-10-16.txt`):

| Config | Checkable stop exits | Outside Yahoo range | Their recorded net P&L | Sessions |
|---|---|---|---|---|
| VWR0 | 753 | 16 | −$13,260 | 2025-01-06, 01-14, 03-03, 03-07, 04-23, 2026-02-26 |
| VWR1 | 995 | 16 | −$12,638 | same |
| VWR2 | 378 | 4 | −$988 | 2025-01-06, 03-07, 04-07, 2026-02-06 |
| VWR3 | 939 | 7 | −$6,753 | 2025-04-23, 06-23 |
| VWR4 | 449 | 1 | −$876 | 2025-04-23 |
| IG-AUSTIN-P0 | 476 | 3 | −$468 | 2025-03-03, 04-07, 2026-02-26 |

The "recorded net P&L" is what those trades booked. It is **not** a correction: removing those trades, or
subtracting a day's P&L, is not equivalent to a compounded rerun under a different data treatment. Under a
different treatment the stops might not fire, later entries would change, and sizing would compound
differently. Hours before 2024-12-18 cannot be checked (Yahoo's hourly history is about two years).

## Status and options (Dustin's decision; none taken)

1. **Leave as is** (current): frozen results stand, and this note travels with them.
2. **Mask v2 as a new, frozen data treatment**, applied by timestamp (the two captures are byte-identical).
   Then rerun the affected experiments as new, separately ledgered runs (exploratory data hygiene, not a
   rescue). Candidate rules:
   - (a) the trade-blind wick-with-VWAP-at-body rule in `diagnose_offmarket_wicks.py`;
   - (b) "minute extremes outside an independent hourly range". This depends on Yahoo, which is not ground
     truth, and covers only the last two years.
3. **Get condition-coded tick data** (a plan upgrade, or another provider) to classify the prints properly.
   This is the only route to a definitive answer, and it costs money.

The VMR-L proposal recommends running on the fresh capture **with this note as a pre-committed post-run
diagnostic**, rather than adopting a mask before review.
