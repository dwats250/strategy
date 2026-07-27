# UV02 Evidence Capability — what the artifacts can and cannot establish

Status: `ANALYSIS — WRITTEN BEFORE THE CAPABILITY PROBE. NO PROBE RESULT IS RECORDED HERE.`

Created: 2026-07-27 UTC · Gate: `UV02-E1`

Governed by [`UV02_STUDY_CONTRACT.md`](UV02_STUDY_CONTRACT.md).

Subject artifacts: the seven exports under `exports/`, and
`cuttingboard_direct_proxy_v0.2.pine` at SHA-256
`d2420bc398d3e23f477d71edbd5e6f1cdb51e377380c2e000f1a0bc63eba53ce`.

> **Amendment rule.** This document is frozen from creation. It is **never edited in place**,
> including by a later probe result. If the capability probe described in §5 is run, its
> result is recorded in a **new dated probe-note file**, which carries a pointer back to this
> document and states plainly anything here that it supersedes.

---

## 1. What the seven CSVs establish

Each export is a TradingView **List of Trades** with a 17-column header, identical across all
seven files. Two rows per trade — one `Entry`, one `Exit`.

| Column | Establishes |
|---|---|
| `Trade number` | Pairing of entry and exit rows |
| `Type` | `Entry long` / `Entry short` / `Exit long` / `Exit short` → **direction, per row** |
| `Date and time` | The **fill** bar date — see §3, kind 3 |
| `Signal` | On entry rows, `V<n> LONG` / `V<n> SHORT` → **the variant, per row**. On exit rows, `STOP` / `TARGET` / `Open` → **exit reason, per row** |
| `Price USD` | Fill price |
| `Size (qty)`, `Size (value)` | One directional unit, and its notional |
| `Net PnL USD`, `Return %` | **Reported** PnL |
| `Commission USD` | **Reported** commission — `0` on every row of all seven files |
| `Favorable/Adverse excursion USD/%` | MFE / MAE |
| `Cumulative PnL USD/%` | Running total |
| `Duration (bars)` | Holding period in bars |

Verify:

```sh
P=audits/cuttingboard-engine-strategy-audit/diagnostics/uv02/exports
for v in V0 V1 V2 V3 V4 V5 V6; do
  printf "%s: " "$v"
  tail -n +2 $P/UV02-d2420bc3-SPY-1D-STD-FULL-$v-ASOF-2026-07-24.csv \
    | awk -F',' '{print $4}' | sort -u | tr '\n' '|'; echo
done
# V0: Open|STOP|TARGET|V0 LONG|V0 SHORT     (…V1–V6 identically)
```

**Correction to the capture log.** `UV02_CAPTURE_LOG.md` states the exports do not carry "a
`variant` field in the rows — the variant is encoded only in the filename." Narrowly there is
no column *named* `variant`, but the variant **is** present per row in the `Signal` column.
Corrected in [`UV02_CAPTURE_LOG_AMENDMENT_2026-07-27.md`](UV02_CAPTURE_LOG_AMENDMENT_2026-07-27.md).

### 1.1 Friction — what is and is not established

**The exports report commission of zero on every row; slippage remains unestablished.**

That is a statement about the **reported values**, deliberately not about the TradingView
Properties setting in force. Three limits, stated rather than stepped over:

1. **A reported zero is not a proven setting.** `BASE` is 0.01% per transaction; at these
   price levels that is well under a cent per fill. Whether the export renders such a value as
   `0` is a **display-rounding question that has not been characterized.** The reported zeros
   are *in tension with* `BASE` and `STRESS`; they are not a disproof of either.
2. **Slippage is unestablished outright.** Slippage moves the fill price, and the export
   carries no independent reference price to compare a fill against.
3. **A zero-commission / nonzero-slippage configuration matches none of the three defined
   scenarios**, so even a confirmed zero commission would not by itself name a scenario.

`friction` in `LEDGER.csv` therefore **remains correctly `UNRECOVERABLE`**, and this document
proposes no change to it.

**Consequently there is no scenario-valid friction-adjusted return in these artifacts.** The
protocol requires "gross and friction-adjusted return." What the exports carry is reported PnL
under an unestablished friction configuration, plus MFE/MAE. That is not the required field.

---

## 2. What the seven CSVs structurally cannot establish

**A List of Trades contains only trades that were taken, and rejections never become trades.**
This is structural, not a capture defect. No re-export of the same run can fix it.

Absent, against `../../spec/BACKTEST_PROTOCOL.md` § *Required exports*:

- any gate boolean;
- the first rejection gate, or the full rejection set;
- regime, posture, confidence, net score, vote coverage, or any of the eight R-02 votes;
- the structure label or its derived inputs;
- the missing-data mask;
- breadth and leadership counts;
- the `AMBIGUOUS_INTRABAR` flag;
- cumulative gate rejection counts;
- results grouped by regime, posture, or structure;
- the signal-bar date (§3, kind 3);
- any bar on which no trade occurred — which is the overwhelming majority of bars, and
  precisely where rejection evidence lives.

---

## 3. What the script already instruments

The v0.2 source emits **exactly 49** `display.data_window` plot series, **per bar, including
on bars that never became trades.** Count:

```sh
grep -c 'display\.data_window' \
  audits/cuttingboard-engine-strategy-audit/diagnostics/uv02/cuttingboard_direct_proxy_v0.2.pine
# 49
```

| Group | Series |
|---|---|
| Identity / state (6) | `variant_index`, `regime_code`, `posture_code`, `structure_code`, `candidate_direction`, `entry_direction` |
| Regime arithmetic (5) | `confidence_bounded`, `net_score_raw`, `bounded_net`, `vote_coverage`, `missing_votes` |
| The eight R-02 votes (8) | `vote_spy`, `vote_qqq`, `vote_iwm`, `vote_vix_level`, `vote_vix_pct`, `vote_dxy`, `vote_tnx`, `vote_btc` |
| R-01 (3) | `r01_advancing_of_16`, `r01_leading`, `r01_expansion` |
| Derived metrics (7) | `atr14_cb_equivalent`, `atr_div_vs_pine_pct`, `ema9_div_vs_pandas`, `ema21_div_vs_pandas`, `momentum_5d`, `volume_ratio`, `ema9_21_spread_pct` |
| Reference geometry (4) | `ref_entry`, `ref_stop`, `ref_target`, `ref_rr` |
| Gates (11) | `gate1_regime`, `gate2_confidence_INERT`, `gate3_direction_INERT`, `gate4_structure`, `gate5_stop_defined_INERT`, `gate6_stop_distance`, `gate7_rr_INERT`, `gate8_max_risk_INERT`, `gate10_extension`, `gate11_time_UNAVAILABLE` (+ `soft_fail_count_available_only`) |
| Aggregate / meta (5) | `macro_pressure_code`, `kill_switch`, `missing_symbol_count`, `signal_pass`, `ambiguous_intrabar` |

**This is the rejection evidence the List of Trades cannot carry.** It exists in committed
code today. Whether TradingView will export it is §5.

---

## 4. The remaining shortfalls — three different kinds of problem

These must not be pooled. They have different causes and different remedies.

### Kind 1 — instrumentation gap

**Not emitted, and not derivable from what is emitted.**

| Item | Why not derivable |
|---|---|
| `t01_complete` (T-01 thesis) | Built from `t01_catalyst`, `t01_confirmation`, `t01_invalidation`, `t01_conflicted` — none emitted |
| `i01_pass` (I-01 invalidation) | `g5_pass and not t01_conflicted`; `t01_conflicted` not emitted |
| `e05_pass` (E-05 entry quality) | Depends on `t01_conflicted` and `barstate.isconfirmed`; neither emitted |

**Remedy:** a script change — i.e. a **possible v0.3**. That is a new file and a new SHA-256,
its own gate with its own approval, never an in-place edit to v0.2. Scope if ever authorized:
three additional `plot(... display=display.data_window)` lines. Note that these three gates are
classified `CURRENTLY_INERT` in the frozen matrix and are expected to add little or no
rejection power, so the value of closing this gap is *confirmatory*, not exploratory.

### Kind 2 — derivable, conditional only on the export path working

**No script change required.** These are computable offline from the emitted series.

The script already computes `first_rejection` as a named string with an explicit precedence
order (source lines 821–847). It is **not plotted** — it reaches only the last-bar state
table — but the derivation reproduces it exactly, because every input except Kind 1 is
emitted:

| Target | Derivation from emitted series |
|---|---|
| `v0_direction`, `v0_pass` | From `regime_code`: `RISK_ON(1)`/`EXPANSION(5)` → LONG, `RISK_OFF(2)` → SHORT, else NONE |
| `posture_direction`, `v1_pass` | From `posture_code` and `gate1_regime`, requiring `posture_direction == v0_direction` |
| `v2_pass` | `= gate4_structure` |
| `v3_pass` | `= (soft_fail_count_available_only == 0)` |
| `v4_pass` | `= not kill_switch` |
| `v5_pass` | `macro_conflict = (macro_pressure_code == RISK_OFF and candidate_direction == LONG) or (macro_pressure_code == RISK_ON and candidate_direction == SHORT)` |
| Cumulative rejection sets | Sum the per-bar booleans over the window |

**Two things a naive derivation would get wrong, recorded so it does not:**

1. **The rejection precedence is not the variant order.** `K-01_KILL_SWITCH` is tested
   *before* `V0_NO_REGIME_DIRECTION` (lines 824–827). A derivation that walked V0→V6 would
   mis-attribute every bar where both fire. The order is: `OUT_OF_WINDOW` → `K-01` → `V0` →
   `GATE1` → `V1` → `GATE4` → `GATE6` → `GATE10` → `Q12` → `E-04` → `T-01` → `I-01` → `E-05`.
2. **`macro_conflict` keys off `candidate_direction`, not `entry_direction` or `v0_direction`.**
   `candidate_direction` follows C-01 and can be non-`NONE` on a computed `NEUTRAL` bar where
   `v0_direction` is `NONE`. Both are emitted; use the right one.

**Coverage:** the derivation reproduces `first_rejection` **exactly for V0–V5**. For **V6** it
reproduces every branch up to `E-04`, and can identify that a bar reached the diagnostic stage
— but cannot say which of `T-01` / `I-01` / `E-05` rejected it. That residue is Kind 1.

One further input, `in_window`, is not emitted. For a FULL-history run it is always true; for a
windowed run it is recoverable from the run configuration rather than from the series, and the
manifest records the window.

**A derivation is preferable to reading a counter.** The script's cumulative counters appear
only in the last-bar table; a derivation from per-bar booleans is independently checkable and
re-runnable, and it can be validated against `signal_pass`, which *is* emitted.

### Kind 3 — timestamp / export-design gap

**Signal-bar date versus fill date.** The protocol requires "signal date and next-open fill
date." The List of Trades carries the **fill** bar. Under the frozen timing model the signal
bar is the prior *trading* bar, which is not recoverable by subtracting a day — it needs a bar
calendar.

This is neither an instrumentation defect nor a derivation problem. It is an **export-design
decision** to be settled when the per-bar export format is specified: either emit the signal
bar's timestamp explicitly, or join the trade list against the per-bar export on the fill date
and step back one row. The second costs nothing extra if the per-bar export exists.

---

## 5. The open empirical question — and the probe that settles it

Everything in Kind 2 is conditional on one untested assumption:

> **Does TradingView's *Export chart data* emit series plotted with
> `display = display.data_window`?**

This has **not been tested.** Nothing in this document assumes an answer, and no capability in
§3 or §4 may be relied on until it is settled.

### Probe design — not a UV02 capture

The question is a property of **TradingView**, not of the CuttingBoard proxy. It is therefore
answerable with a throwaway indicator on any chart:

```pine
//@version=6
indicator("data_window export probe", overlay = false)
plot(bar_index,      "probe_visible")                                   // control
plot(close,          "probe_datawindow", display = display.data_window) // subject
```

Attempt *Export chart data* and record: whether `probe_datawindow` appears as a column; the
exact column header; row granularity; any row limit; and whether `na` bars are emitted.

Why this and not a study rerun:

- **not a UV02 capture** — no study script, no study chart, no export enters custody;
- **produces exactly one artifact**, a dated probe note. No new script hash, no ledger row, no
  change to any custodied file;
- **cannot inspect any study window**, so it cannot deepen the recorded 2022–2026 inspection;
- **strictly prior** — running the seven-variant study to obtain gate evidence before knowing
  whether the export mechanism works risks a wasted rerun.

**Stop conditions.** If the probe cannot be done without opening the UV02 study script or
chart, **stop** — that is a rerun, requiring its own authorization. If it cannot be done
without inspecting a study window, **stop**.

---

## 6. Pine instrumentation versus an offline runner — kept apart

These are different things at different points in the written sequence, and conflating them
would smuggle TV-4 work into a diagnostic gate.

| | Pine instrumentation (a possible v0.3) | Offline runner |
|---|---|---|
| What it is | A change to the **measuring instrument** | A reimplementation of the frozen contract |
| Cost to custody | **New file, new SHA-256.** The existing seven captures are bound to `d2420bc3`; a v0.3 does not re-attribute them and cannot be compared to them without stating the change | None to UV02 custody |
| Standing | Its own gate, its own approval | **TV-4** — after TV-2 parity acceptance and TV-3 runs |
| Proposed here? | Only if Kind 1 must be closed, and only after §5 | **No.** Out of scope at this stage |

`../../README.md` places offline reproduction at TV-4; `../../spec/DATA_PROVENANCE_CONTRACT.md`
is `DRAFT / EXPLORATORY — FROZEN IMPLEMENTATION NOT AUTHORIZED` and states offline work "gets
its own future charge, likely TV-4." No offline runner, no data download, and no external
dataset is proposed by this document.

---

## 7. Smallest truthful path to candidate, gate-pass, and rejection evidence

In dependency order. Each step is separately authorized; none is authorized by this document.

1. **Run the §5 probe.** Cost: minutes. Settles everything below.
2. **If the probe succeeds** — specify the per-bar export format (resolving Kind 3), export
   per-bar state for each variant, and derive candidate states, `first_rejection`, and
   cumulative rejection sets per Kind 2. **No script change. No new script hash. The seven
   existing captures keep their binding.** Validate the derivation against the emitted
   `signal_pass` and against the entry rows of the existing List of Trades — they must agree
   on every bar that produced a trade.
3. **If the probe fails** — the gap is an export-mechanism limitation, not a script defect.
   That, and only that, is what would justify considering a v0.3 whose series are emitted in a
   form the export path does carry. Still a new gate.
4. **Kind 1 (`t01`/`i01`/`e05`) closes only with a v0.3**, whatever the probe returns. Given
   those three gates are `CURRENTLY_INERT` in the frozen matrix, this is low-value and should
   not drive the decision.

**What none of this produces.** Even with per-bar state fully exported, UV02 still yields no
parity evidence (the universe departs from the pin by construction), no scenario-valid
friction-adjusted return (§1.1), and no profitability, alpha, or options-return claim. It
yields gate selectivity under a stated universe — which is what the study is for.
