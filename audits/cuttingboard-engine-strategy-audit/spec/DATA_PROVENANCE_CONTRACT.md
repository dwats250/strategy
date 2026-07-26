# Data Provenance Contract

Status: `DRAFT / EXPLORATORY — FROZEN IMPLEMENTATION NOT AUTHORIZED`

This document is **not** part of the frozen TV-0 contract. It defines what provenance a
dataset must carry *if and when* offline data work is authorized. It selects no provider,
authorizes no download, and specifies no acquisition code.

Offline CSV and external historical-data work is exploratory during the preliminary round
and is the next major focus **after** the TradingView audit reaches a recorded stopping
point. That work gets its own future charge, likely TV-4.

TV-0R may review this document for boundary and provenance implications only.

## Required provenance fields

Every dataset admitted to this audit carries a manifest recording all of the following. A
dataset missing any field is not admitted — it is not silently used with the field left blank.

### Source and retrieval

| Field | Meaning |
|---|---|
| `source_name` | Vendor or platform that produced the data |
| `source_endpoint` | Exact API endpoint, export path, or UI action used |
| `retrieval_timestamp_utc` | When the data was actually pulled, in UTC |
| `retrieved_by` | Operator or process responsible |
| `access_terms_reviewed` | Whether redistribution terms were read at retrieval time |

### Symbol identity

| Field | Meaning |
|---|---|
| `vendor_symbol` | The vendor's exact ticker string, verbatim |
| `canonical_symbol` | This project's canonical name for the instrument |
| `exchange` | Listing or quoting exchange |
| `instrument_type` | Equity, ETF, index, futures continuation, FX pair, rate proxy, crypto pair |

Vendor symbol and canonical symbol are recorded separately and never collapsed. Cross-symbol
mapping is a declared translation, not an assumed identity — a provider's VIX, DXY, 10-year
yield, or BTC series is a mapping decision that must survive review, not a lookup.

### Temporal contract

| Field | Meaning |
|---|---|
| `timeframe` | Bar interval |
| `timezone` | Timezone the timestamps are expressed in |
| `exchange_session` | Regular hours, extended hours, or 24h |
| `session_calendar` | Holiday and half-day calendar the series follows |
| `bar_timestamp_convention` | Whether a bar's timestamp marks its open or its close |

Bar-timestamp convention is recorded explicitly. An off-by-one-bar convention mismatch is
indistinguishable from lookahead in results, and is one of the more likely ways this study
could produce a wrong answer that looks clean.

### Price semantics

| Field | Meaning |
|---|---|
| `ohlcv_basis` | Raw/unadjusted or adjusted |
| `split_treatment` | How splits are reflected |
| `dividend_treatment` | Whether dividends are reflected, and how |
| `adjustment_as_of` | The date the adjustment factors were computed |

Raw and adjusted OHLCV are different series and are never mixed inside one run. Adjusted
series are retroactively mutable — the same request on a later date can return different
history — so `adjustment_as_of` is mandatory, not optional.

### Coverage and integrity

| Field | Meaning |
|---|---|
| `date_range_start`, `date_range_end` | First and last bar present |
| `row_count` | Exact number of rows |
| `missing_bar_policy` | How sessions absent from the data are handled |
| `missing_bar_count`, `missing_bar_dates` | Which sessions are absent |
| `duplicate_bar_policy` | How duplicate timestamps are handled |
| `duplicate_bar_count` | How many were found |
| `file_sha256` | Checksum of the file as retrieved |

**Missing-bar policy.** Missing bars are recorded as missing. They are never forward-filled,
interpolated, or silently dropped in a way that changes a rolling-window computation. A gap
that shortens a lookback window must be flagged on every bar whose value it affects. This
mirrors the frozen contract's rule that missing cross-symbol values stay missing and never
become neutral.

**Duplicate-bar policy.** Duplicates are reported and resolved by a recorded rule, never
deduplicated silently.

## Immutable raw data

Raw vendor exports are **immutable once written**. They are never edited, re-sorted,
re-encoded, cleaned, or partially corrected in place.

Every correction produces a new normalized file that references the immutable raw manifest it
derives from. If a raw file is wrong, the record of it being wrong is part of the evidence.

Raw files live only under the ignored `data/raw/` location. See `../data/README.md`.

## Normalized schema expectations

A normalized dataset must:

- point back to the `file_sha256` of every raw input it derives from;
- record the transformation applied, in a form that can be re-executed;
- carry its own checksum, row count, and date range;
- preserve the missing-data mask rather than resolving it;
- use canonical symbols, with the vendor-symbol mapping retained in the manifest;
- state its timezone and bar-timestamp convention explicitly, not by inheritance.

A normalized file whose raw ancestry cannot be reconstructed is not evidence.

## TradingView export roles

Two TradingView artifacts have distinct and non-interchangeable roles:

- **Chart data** — the price series the strategy actually evaluated. It defines what the run
  saw, and is the reference for offline reproduction.
- **Strategy Report / List of Trades** — the run's decisions and outcomes. It is the trade
  ledger, not a price source.

Neither substitutes for the other, and neither substitutes for the run manifest. Screenshots
and summary tables are supplementary and never replace the raw ledger.

TradingView chart data is a provider snapshot subject to revision. Its retrieval timestamp
matters for the same reason `adjustment_as_of` does.

## Redistribution and licensing

Vendor data is typically licensed for use, not redistribution. Until redistribution rights for
a specific dataset are affirmatively known:

- raw vendor exports stay untracked and out of any commit, PR, or published artifact;
- manifests, checksums, schemas, and derived aggregate results may be tracked, provided the
  derived result does not reconstitute the raw series;
- "it is only a small sample" is not a rights determination.

Unknown rights are treated as no rights.

## Parity requirements

Offline reproduction is accepted only on **trade-by-trade** parity with the TradingView run,
not on aggregate agreement. Matching summary statistics with a differing trade list means two
errors cancelled, which is a worse state than a visible mismatch.

Parity acceptance records, per trade: signal date, fill date, direction, variant, entry, stop,
target, signal ATR, exit reason, and the ambiguous-intrabar flag.

Bounded, disclosed exceptions are permitted where a proxy is declared — EMA and ATR warm-up
divergence being the known cases. Exceptions are measured and bounded, never waved through.

## Discrepancy logging

Every discrepancy is logged with: what differed, on which bars or trades, magnitude, the
suspected cause, and whether it is resolved or accepted as a bounded exception.

Discrepancies are never resolved by adjusting the offline implementation until it agrees.
Provider and session mismatches are recorded rather than hidden — a documented mismatch is a
finding, not a failure.

## Future sequence

1. **TradingView parity** — establish the reference run under the frozen contract.
2. **Offline normalization** — build normalized datasets under this contract.
3. **Bounded reproduction** — trade-by-trade parity against the reference run.
4. **Expanded historical testing** — only after reproduction holds.

Each step completes before the next begins. Step 2 requires its own charge. No step
authorizes CuttingBoard mutation or parameter back-feeding.
