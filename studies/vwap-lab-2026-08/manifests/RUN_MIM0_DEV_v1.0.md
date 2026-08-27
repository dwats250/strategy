# RUN RECORD — MIM-0 first development run · v1.0 · 2026-08-27

The first MIM development configuration (MIM-0), unblocked by the owner/HELM-authorized
State Street corporate-action seam (2026-08-27) and run under
`docs/research/FAMILY_AUTONOMY_PROTOCOL_v1.0.md`. This is a **frozen pre-registration**:
the dividend-neutral convention, the sidecar, and the code were fixed and committed
**before any MIM outcome was accessed**; results are recorded by a dated **result
amendment** (§b/§c). The MIM-0 baseline and the kill/advance gates were already frozen
in `MIM_CHARTER_v0.1.md`; this record adds only the corporate-action resolution.

## Blocker resolution (owner/HELM authorization 2026-08-27)

One narrow external reference seam authorized: **State Street / SPDR official US
historical distributions for SPY**, for **corporate-action normalization only** (not a
price/intraday/paid/general dependency; the MIM hypothesis is unchanged). The six SPY
ex-dividend distributions in the development window were **independently verified before
freezing** (not trusted from the charge) — see `data/SPY_EX_DIVIDENDS_v1.0.json`:
confirmed to 5 decimals against a public dividend-history record, corroborated by search
citing State Street's Sep-2025 $1.831 figure, all six on SPY's quarterly cadence and
present as corpus sessions:

| ex-date | cash/share |
|---|---:|
| 2024-09-20 | 1.745531 |
| 2024-12-20 | 1.965548 |
| 2025-03-21 | 1.695528 |
| 2025-06-20 | 1.761117 |
| 2025-09-19 | 1.831114 |
| 2025-12-19 | 1.993368 |

## Dividend-neutral early_return (frozen PRIMARY convention)

- Ordinary session: `early_return = (P_10_00 − previous_close) / previous_close`.
- SPY ex-dividend session: `early_return = (P_10_00 + cash_distribution − previous_close)
  / previous_close` — removes the mechanical ex-dividend price drop while preserving the
  session and its genuine overnight/intraday information.

This is the **primary** MIM signal convention. **No other frozen MIM-0 semantic is
modified** — 10:00 / 15:30 / 16:00 clock, sign strategy, OLS β>0 with HC1 robust SE,
and the frozen cost views are exactly as `MIM_CHARTER_v0.1.md`.

## Sensitivity (diagnostic only)

MIM results are additionally reported with the six ex-dividend sessions **excluded
entirely** — a corporate-action **sensitivity diagnostic only**. It is **not** a second
configuration, a rescue, or a gate-selection opportunity. The dividend-neutral screened
result remains **primary**.

## Kill / advance gates (already frozen — MIM_CHARTER §3)

FAMILY DEAD if `β ≤ 0` OR gross sign-strategy expectancy `≤ 0` OR positive gross does not
survive the frozen conservative cost stress (5 bps RT). Else **EDGE CANDIDATE —
VALIDATION DECISION REQUIRED** (validation NOT run autonomously). No rescue.

## Code & data (frozen)

| File | SHA256 |
|---|---|
| `analysis/mim.py` | `f80474fdfb38cf948c9dd86c9f32f3dc0e9fe81ec536dbf62b64c7ad1a80f222` |
| `analysis/test_mim.py` | `f9fe0733ffd2a0b1233ea807704bd3622677544b1ffa6d1a982d66802a6fe34e` |
| `data/SPY_EX_DIVIDENDS_v1.0.json` | `40b09763d7dc844f9f0d65714411f0173c5b3531601ba1eb601d0cf3d6394622` |

Corpus sha256 `a4afaa704e6ded54f62f1670c52ff74070338ccb943eebcc2f73fe9c170ed97a`. Screened
(frozen `CORPUS_MASK_v1.0`) primary, raw sensitivity. Tests 7/7 synthetic (incl. the
dividend-neutral adjustment). No engine change; MIM is a standalone module.

## Budget (§9/§f)

MIM interpreted-development **0 → 1/4** (config 1; default new-family allowance ≤4).
Ledger row `MIM0_DEV_2024-09-03_2025-12-31`.

## Reproduction

```
cd studies/vwap-lab-2026-08/analysis
python3 mim.py               # -> MIM0_DEV_2026-08-27.json
python3 test_mim.py          # 7/7 synthetic
```

## Amendments

### Amendment 1 — result (2026-08-27) — **MIM FAMILY DEAD**

Run under the frozen pre-registration; `mim.py` unchanged since the freeze commit
`8eabc76`. Evidence `analysis/MIM0_DEV_2026-08-27.json` sha256
`1bc6434789b8f2374a8f56d67e4315721f1183e53e470f01ef8ecb5b9fbbdb3c`; byte-identical
across reruns. All six dev-window SPY ex-dividend sessions received the dividend-neutral
adjustment. **N = 328** observations.

**Primary — dividend-neutral, screened (regression `late = α + β·early`):**

| quantity | value |
|---|---:|
| **β** | **−0.01674** |
| HC1 SE (primary) | 0.03169 |
| t (HC1) | −0.528 |
| 95% CI (HC1) | [−0.07884, +0.04536] |
| R² | 0.00248 |
| N | 328 |

**Primary condition β > 0: FAIL** (β = −0.0167 ≤ 0; the estimate is if anything weakly
*contrarian* and statistically indistinguishable from zero — t −0.53, CI straddles).

**Sign strategy (dividend-neutral, screened):** mean **−0.59 bps**/trade, cumulative
−193.4 bps, PF 0.928, win 50.5%, max-DD 554 bps; long −0.60 bps (n=187), short −0.58 bps
(n=140); bootstrap mean CI95 [−3.20, +1.98] bps (straddles zero); 8/16 profitable months.
**Gross expectancy ≤ 0.** Costs: zero −0.59, lab-slippage −0.92, 5 bps-stress −5.59 bps
(**does not survive**).

**Robustness (all three views agree):** raw sensitivity is identical to screened
(β −0.01674; the 9 masked bad-tick bars are not MIM clock bars, so screened == raw,
N=328 both). The **ex-dividend-EXCLUDED** sensitivity (diagnostic only): β −0.01569,
gross −0.573 bps → still **FAMILY DEAD**. The dividend handling did not change the
conclusion; the momentum simply is not present.

**Verdict — FAMILY DEAD** by the frozen gate (β ≤ 0; independently, gross ≤ 0 and fails
the cost stress). The previous-close→10:00 return does **not** positively predict the
final-30-minute return for SPY in the development window. Per the frozen no-rescue rule:
**report and stop** — no alternative early/late windows, no high-vol/high-volume subset,
no macro days, no long-only, no rest-of-day predictor. STOP at **A — MIM FAMILY DEAD**.

MIM interpreted-development **0 → 1/4** (config 1; the remaining ≤3 are **not** earned by
a failed baseline). Ledger row `MIM0_DEV_2024-09-03_2025-12-31`.
