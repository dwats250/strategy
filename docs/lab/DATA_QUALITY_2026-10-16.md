# Data quality — SPY 1-minute (Massive): suspicious extreme prints (2026-10-16)

**Status: unresolved, documented, scope measured.** No mask was adopted, no result was replaced, nothing
was re-run.

## What was observed

On **2025-04-23**, from about 11:28 ET onward, over a hundred RTH minutes carry highs at **$544–545**,
while their bodies trade at $534–539 and Massive's own per-minute VWAP stays at the body. The frozen
mask v1.0 (an isolated-spike rule) does not catch a cluster. A trade-blind scan flags 122 such minutes in
the August corpus: 111 on 2025-04-23, and 11 spread over 9 other sessions
(`studies/vwap-ema9-2026-10/analysis/diagnose_offmarket_wicks.py`). Whether these prints were executable
is **unknown**.

## What each check establishes

All Yahoo comparisons come from `studies/vwap-ema9-2026-10/analysis/compare_independent_hourly.py`; its
output is `DIAGNOSTIC_independent_hourly_VWR0-EXP_2026-10-16.txt`.

| Check | Result | What it shows | What it does not show |
|---|---|---|---|
| Second Massive capture (2026-10-16) | All 179,670 overlapping RTH minutes identical (`DATA_COMPARE_a4afaa70_vs_729dc4e9_2026-10-16.json`) | The prints **persist** in the vendor's current data | That they are correct |
| Massive tick trades with condition codes | **HTTP 403**: not included in the plan, and no upgrade was made | — | Whether the prints carry late, out-of-sequence or other non-high/low-eligible conditions |
| **Yahoo Finance hourly bars** (free, no account; independent processing; 2024-12-18 → 2026-08-21) | 2,880 checkable hours. Hourly closes identical to the cent in 89.9% of them (median difference $0.00). On 2025-04-23 Yahoo's **morning** highs match ($545.40 vs $545.43), but every hour from 11:30 has Yahoo highs of **$537.17–$539.59** against Massive's **$544.54–$545.16** | An independent source does **not** show the midday $545 prints | That they were unexecutable: Yahoo applies its own processing and is not ground truth |
| Yahoo's own gaps | 35 Massive hours have no Yahoo bar, and 6 Yahoo bars carry under 50% of Massive's volume. These fall on 15 sessions (for example the early-close 12:30 bars, 2026-01-30, 2026-06-09, 2026-07-13/14) and are treated as **uncheckable** | Yahoo is incomplete in places. One example used in an earlier draft (2026-06-09) was a Yahoo hole, not a Massive anomaly | — |
| Calibration on mask v1.0's prints | Yahoo lacks 4 of the masked minutes' extremes (2024-12-20, 2025-03-14, 2025-04-16, 2025-12-22) but **shows** 4 (2025-05-19 ×3, 2025-05-27). 2024-10-01 is outside Yahoo's span | Yahoo does not simply smooth everything. Mask v1.0 is only partly corroborated | — |
| Wider scan (checkable hours only) | 30 hours where Massive's high (14) or low (16) lies more than $0.50 beyond Yahoo's range | The issue is broader than one session, but rare (~1% of hours) | — |

## Affected scope in recorded results (diagnostic only)

These are stop exits in `VWR0-EXP__20261016T211249Z` whose fill price lies outside Yahoo's range for that
hour, counting checkable hours only. The table uses a **$0.50** tolerance; the $0.01 counts are in brackets.
Smaller exceedances are within ordinary feed disagreement. Per-fill exceedances are listed in the
diagnostic output.

| Config | Checkable stop exits | Outside Yahoo range (> $0.50) [> $0.01] | Their recorded net P&L (> $0.50) | Sessions (> $0.50) |
|---|---|---|---|---|
| VWR0 | 751 | 15 [16] | −$13,186 | 2025-01-06, 03-03, 03-07, 04-23, 2026-02-26 |
| VWR1 | 991 | 15 [16] | −$12,562 | same |
| VWR2 | 377 | 1 [4] | −$469 | 2025-03-07 |
| VWR3 | 937 | 6 [7] | −$6,636 | 2025-04-23 |
| VWR4 | 449 | 1 [1] | −$876 | 2025-04-23 |
| IG-AUSTIN-P0 | 476 | 1 [3] | −$139 | 2025-03-03 |

The "recorded net P&L" is what those trades booked. It is **not** a correction: removing those trades, or
subtracting a day's P&L, is not equivalent to a compounded rerun under a different data treatment. Under a
different treatment the stops might not fire, later entries would change, and sizing would compound
differently. Hours before 2024-12-18, and the uncheckable hours above, cannot be assessed.

## Status and options (Dustin's decision; none taken)

1. **Leave as is** (current): frozen results stand, and this note travels with them.
2. **Mask v2 as a new, frozen data treatment**, applied by timestamp (the two captures are byte-identical).
   Then rerun the affected experiments as new, separately ledgered runs (exploratory data hygiene, not a
   rescue). Candidate rules:
   - (a) the trade-blind wick-with-VWAP-at-body rule in `diagnose_offmarket_wicks.py`;
   - (b) "minute extremes outside an independent hourly range". This depends on Yahoo, which is not ground
     truth, is incomplete in places, and covers only the last two years.
3. **Get condition-coded tick data** (a plan upgrade, or another provider) to classify the prints properly.
   This is the only route to a definitive answer, and it costs money.

The VMR-L proposal recommends running on the fresh capture **with this check pre-committed as a post-run
diagnostic**, rather than adopting a mask before review.
