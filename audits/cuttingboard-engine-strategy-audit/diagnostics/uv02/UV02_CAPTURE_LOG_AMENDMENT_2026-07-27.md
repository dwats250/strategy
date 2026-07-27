# UV02 Capture Log — Amendment, 2026-07-27

Status: `DATED AMENDMENT — CORRECTIONS AND RECORDED OBSERVATIONS`

Created: 2026-07-27 UTC · Gate: `UV02-E1`

Amends: [`UV02_CAPTURE_LOG.md`](UV02_CAPTURE_LOG.md)

---

## What this document is

A dated amendment under `docs/conventions.md` §b, read across to audit artifacts by §h:
**frozen documents are never edited in place; corrections are dated amendments or new
versioned files.**

`UV02_CAPTURE_LOG.md` is therefore **unedited and byte-identical**, and so is `LEDGER.csv`.
Both remain closed custody evidence. This file carries the corrections; the log carries what
was said on 2026-07-26.

Verify neither changed:

```sh
cd audits/cuttingboard-engine-strategy-audit/diagnostics/uv02
sha256sum LEDGER.csv UV02_CAPTURE_LOG.md
# 374d1e8fce4ad171a2c75b5182b5f8fc8135b96a3e5fefa2a36dfc28001de22f  LEDGER.csv
# f1a339172a560ad8cf791b540b720eae029ac407b36cedc6c0f6503b23ff3111  UV02_CAPTURE_LOG.md
```

**This amendment changes no ledger value and authorizes no ledger change.** See §2.4.

---

## Amendment 1 — the exports do carry the variant, per row

### What the log says

> Against `../../spec/BACKTEST_PROTOCOL.md` § *Required exports* it does **not** carry: … or a
> `variant` field in the rows — the variant is encoded only in the filename.

### Correction

The claim "the variant is encoded only in the filename" is **incorrect**. Every entry row's
`Signal` column carries the variant, in all seven exports:

```sh
P=audits/cuttingboard-engine-strategy-audit/diagnostics/uv02/exports
for v in V0 V1 V2 V3 V4 V5 V6; do
  printf "%s: " "$v"
  tail -n +2 $P/UV02-d2420bc3-SPY-1D-STD-FULL-$v-ASOF-2026-07-24.csv \
    | awk -F',' '{print $4}' | sort -u | tr '\n' '|'; echo
done
```

Observed:

```
V0: Open|STOP|TARGET|V0 LONG|V0 SHORT
V1: Open|STOP|TARGET|V1 LONG|V1 SHORT
V2: Open|STOP|TARGET|V2 LONG|V2 SHORT
V3: Open|STOP|TARGET|V3 LONG|V3 SHORT
V4: Open|STOP|TARGET|V4 LONG|V4 SHORT
V5: Open|STOP|TARGET|V5 LONG|V5 SHORT
V6: Open|STOP|TARGET|V6 LONG|V6 SHORT
```

Sample rows (V6):

```
1,Exit short, 2001-04-10, STOP,     74.45,1,72.36,-2.09,…
1,Entry short,2001-04-03, V6 SHORT, 72.36,1,72.36,-2.09,…
```

### Why it reads that way in the source

`strategy.entry(..., comment = variant_id + " LONG")` and `" SHORT"` (v0.2 source lines 876
and 882) place the variant in the entry comment, which TradingView renders in the `Signal`
column. `strategy.exit(..., comment_loss = "STOP", comment_profit = "TARGET")` (lines 877,
883) does the same for exits.

### Scope of the correction

**Narrowly, the log is right that no column is *named* `variant`.** What is corrected is the
stronger claim that the variant is encoded *only* in the filename. It is not — it is present
per row, and so are direction (`Type`) and exit reason (`Signal` on exit rows).

**Everything else in that paragraph stands and is unaffected.** The exports still carry no
gate boolean, no first-rejection or full rejection set, no regime/posture/confidence/votes, no
structure label, no missing-data mask, no ambiguous-intrabar flag, and no cumulative gate
rejection counts. The log's central finding — *a List of Trades contains only trades that were
taken, and rejections never become trades* — is **correct and unchanged**.

### Consequence

Each row is self-identifying, so the seven exports can be pooled into one table without
relying on filenames. This is a modest strengthening of the evidence base, not a change in
what the study may claim.

---

## Amendment 2 — friction: what the exports report, and what remains unestablished

### Recorded finding

**The exports report commission of zero on every row; slippage remains unestablished.**

```sh
for v in V0 V1 V2 V3 V4 V5 V6; do
  printf "%s: " "$v"
  tail -n +2 $P/UV02-d2420bc3-SPY-1D-STD-FULL-$v-ASOF-2026-07-24.csv \
    | awk -F',' '{print $10}' | sort -u | tr '\n' ' '; echo
done
# V0: 0   V1: 0   V2: 0   V3: 0   V4: 0   V5: 0   V6: 0
```

Net PnL reconciles to the exact price difference with no commission residual:

```
short  entry 72.36 → exit 74.45   Net PnL -2.09  = 72.36 - 74.45   commission 0
long   entry 75.14 → exit 74.15   Net PnL -0.99  = 74.15 - 75.14   commission 0
```

### 2.1 This is a statement about reported values, not about the setting

Three limits are recorded rather than stepped over:

1. **A reported zero is not a proven Properties setting.** `BASE` is 0.01% per transaction; at
   these price levels that is well under a cent per fill. Whether TradingView's export renders
   such a value as `0` is a **display-rounding question that has not been characterized.** The
   reported zeros are *in tension with* `BASE` and `STRESS`. They are **not a disproof** of
   either, and this amendment does not claim they are.
2. **Slippage is unestablished outright.** Slippage moves the fill price, and the export
   carries no independent reference price to compare a fill against.
3. **A zero-commission / nonzero-slippage configuration matches none of the three defined
   scenarios**, so even a confirmed zero commission would not by itself name a scenario.

### 2.2 The log's original finding stands

`UV02_CAPTURE_LOG.md` records the friction scenario as `UNRECOVERABLE` because the Properties
tab overrides the declaration defaults and no Properties screenshot was saved. **That is
correct and this amendment does not disturb it.** What is added is a verifiable observation
about the reported values — not a recovered setting.

### 2.3 Effect on the required export

`../../spec/BACKTEST_PROTOCOL.md` requires "gross and friction-adjusted return." Because the
scenario is unestablished, **no scenario-valid friction-adjusted return can be read off these
exports.** What they carry is reported PnL under an unestablished friction configuration, plus
MFE/MAE. That is not the required field, and it may not be presented as one.

### 2.4 Explicit separation from any ledger amendment

> This is a **finding about the reported values in the artifacts.**
>
> It is **not** a ledger amendment. It **does not authorize** one. It **does not** establish
> the commission setting that was in force.
>
> `LEDGER.csv` is unchanged, byte-identical, and remains the authoritative record under
> `docs/conventions.md` §f. Its `friction`, `commission`, and `slippage_ticks` values stay
> `UNRECOVERABLE`, which — given §2.1 — is the **correct** label for what the artifacts
> support.
>
> Any future change to the ledger is a separate action requiring Dustin's explicit
> authorization, outside this gate.

For how a future run should record a compound field of this shape, see the
`PARTIALLY_RECOVERED` rule in
[`manifests/UV02_RUN_MANIFEST_v0.1.md`](manifests/UV02_RUN_MANIFEST_v0.1.md).

---

## Amendment 3 — the 49 data-window series are verified present; the export path is untested

`UV02_CAPTURE_LOG.md` states the script "already instruments 49 `display.data_window` plot
series" and that whether *Export chart data* emits them "is an open empirical question and is
the first item of `UV02-E1`."

**The count is verified:**

```sh
grep -c 'display\.data_window' \
  audits/cuttingboard-engine-strategy-audit/diagnostics/uv02/cuttingboard_direct_proxy_v0.2.pine
# 49
```

**The export path remains untested.** No probe has been run and no result is claimed here.

One clarification, recorded because a later stage could otherwise assume more than is true:
the script *computes* `first_rejection` as a named variable with an explicit precedence order
(source lines 821–847), but **does not plot it.** It reaches only the last-bar state table.
Its value is derivable offline from the emitted series for variants V0–V5, and only partially
for V6. Full detail, including two ways a naive derivation would go wrong, is in
[`UV02_EVIDENCE_CAPABILITY.md`](UV02_EVIDENCE_CAPABILITY.md) §4.

---

## What this amendment does not do

- It does not edit `UV02_CAPTURE_LOG.md`, `LEDGER.csv`, `UNIVERSE_V0.2.md`,
  `cuttingboard_direct_proxy_v0.2.pine`, or any file under `exports/`.
- It does not change any recorded value, hash, or status label.
- It makes no profitability, alpha, live-execution, options-return, or parity claim.
- It does not describe 2022-01-01 – 2026-07-24 as untouched, out-of-sample, or a forward
  holdout. That period was inspected in the FULL-history capture and its pre-inspection status
  cannot be restored.
- It reads, references, and mutates nothing in `dwats250/cuttingboard`.
