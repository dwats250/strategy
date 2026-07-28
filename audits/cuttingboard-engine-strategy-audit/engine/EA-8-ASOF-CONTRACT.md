# EA-8 — As-of Contract and Look-ahead Control

Status: `ACTIVE — MACHINERY BUILT AND PROVEN. REAL-DATA EVALUABLE RANGE IS EMPTY.`

Created: 2026-07-28 UTC

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`

Tools: [`tools/dataset/asof_build.py`](tools/dataset/asof_build.py) (`EA-8-asof-build/1.0.0`) ·
[`tools/dataset/lookahead_assert.py`](tools/dataset/lookahead_assert.py) (`EA-8-lookahead/1.0.0`)
Manifests: [`data/manifests/`](data/manifests/) · Policy: [`data/README.md`](data/README.md)

Governing plan: [`../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md)
§ EA-8, and the dated **2026-07-28 amendment (EA-6-006)**.
Provenance contract: [`../spec/DATA_PROVENANCE_CONTRACT.md`](../spec/DATA_PROVENANCE_CONTRACT.md).

---

## 0. Question and answer

**Question:** can inputs be reconstructed per date with **no look-ahead**?

**Answer, in two parts, kept apart because they differ:**

1. **The mechanism: yes, and it is proven.** As-of truncation, provenance capture, and an
   assertion suite that demonstrably *catches* leakage are built, exercised across a five-date
   range, and committed.
2. **The data: no real market data exists to reconstruct.** No vendor series has been retrieved
   and none is authorized. **The evaluable range on real data is empty.** Per EA-8's stop
   condition the range is narrowed and the limit recorded — it is not approximated.

---

## 1. Why truncation is Strategy's job

At the pin, `runtime._cache_only` reads the cache with **no date filter**:

```python
def _cache_only(symbol):
    cache_path = _ohlcv_cache_path(symbol)
    if not cache_path.exists():
        return None
    return pd.read_parquet(cache_path)
```

**The cache file's contents therefore *are* the as-of boundary.** A full-history cache would
expose future bars to every rolling computation — EMA, ATR, structure, momentum — silently and
without error. This is the leakage crux the plan recorded as I-2, and it is confirmed unchanged
at the pin.

The engine is not at fault here and this is **not** classified as an engine defect: fixture
mode is a test seam, and bounding it is the harness's responsibility. `asof_build.py` is where
that bound is applied.

## 2. The truncation rule

> **Bars where `index <= as_of_boundary`. Nothing after. No fill, no interpolation, no
> resampling.**

Recorded in every manifest as `truncation_rule`, so a dataset that does not declare it fails
assertion A5 rather than being trusted by default.

## 3. The look-ahead assertion suite

Five assertions per dataset. Exit code is 0 only if all pass for all datasets; violations are
reported per-symbol and per-check, never summarised away.

| # | Assertion |
|---|---|
| A1 | Every parquet's maximum bar timestamp is `<=` the as-of boundary — **the invariant** |
| A2 | The manifest's recorded `max_bar_timestamp` matches the file on disk |
| A3 | Every parquet's content digest matches the manifest |
| A4 | No duplicate bar timestamps |
| A5 | The manifest declares both an as-of boundary and a truncation rule |

### 3.1 Results — and the negative control that makes them mean something

```
suite=EA-8-lookahead/1.0.0 datasets=5
  asof-2025-06-30        PASS
  asof-2025-09-30        PASS
  asof-2025-12-31        PASS
  asof-2026-02-27        PASS
  asof-2026-04-10        PASS
SELF-TEST negative control: injected bar 2025-07-30 into AAPL_ohlcv.parquet -> suite CAUGHT it (expected)
    asof-2025-06-30/AAPL: A1 LOOK-AHEAD — max bar 2025-07-30 > as-of 2025-06-30
    asof-2025-06-30/AAPL: A2 manifest max_bar 2025-06-30 != disk 2025-07-30
    asof-2025-06-30/AAPL: A3 content digest mismatch
RESULT: ALL DATASETS PASS
```

**A suite that has never failed proves nothing.** The negative control deliberately injects a
bar 30 days past the boundary and requires the suite to catch it. It did — on A1, and
independently on A2 and A3. This mirrors EA-2's discipline: the control must *fail* for the
enforcement to count.

Full output: [`data/manifests/EA-8-LOOKAHEAD-SUITE-RESULT.txt`](data/manifests/EA-8-LOOKAHEAD-SUITE-RESULT.txt).

## 4. The evaluable range — stated with its limits

### 4.1 What exists

| Property | Value |
|---|---|
| Datasets | 5 (`asof-2025-06-30`, `-2025-09-30`, `-2025-12-31`, `-2026-02-27`, `-2026-04-10`) |
| Symbols per dataset | 20 |
| Source series span | 2025-04-14 … 2026-04-10, 260 business days |
| Look-ahead suite | **passes on all five**; negative control caught |
| Manifest per dataset | yes, with per-symbol `file_sha256` and `content_digest_sha256` |

### 4.2 What it is — and is not

**The data is SYNTHETIC.** It is produced by a committed deterministic generator, not retrieved
from any vendor. It exercises code paths and validates the as-of machinery. **It supports no
claim about market behaviour, and no result derived from it may be presented as an empirical
finding about trading.**

Every manifest records this explicitly rather than by omission:
`ohlcv_basis: "SYNTHETIC — neither raw-vendor nor adjusted"`,
`source_name: "SYNTHETIC-EA7-LIBRARY"`,
`access_terms_reviewed: "NOT_APPLICABLE_SYNTHETIC — no vendor data retrieved"`.

### 4.3 Real-data evaluable range: **EMPTY**

No vendor series has been retrieved. `spec/DATA_PROVENANCE_CONTRACT.md` is
`DRAFT / EXPLORATORY — FROZEN IMPLEMENTATION NOT AUTHORIZED` and "selects no provider,
authorizes no download, and specifies no acquisition code." This charge separately forbids
accessing live services or market data.

**Per EA-8's stop condition, the range is narrowed to what can actually be reconstructed and
the limit is recorded here. Nothing is approximated.**

### 4.4 Provenance fields that cannot be populated for real data

Recorded because a later phase must not mistake a synthetic placeholder for an established
value. For the synthetic library these are `NOT_APPLICABLE_SYNTHETIC`; for any real dataset they
would be **mandatory and currently unobtainable**:

`source_endpoint` · `retrieval_timestamp_utc` · `access_terms_reviewed` · `vendor_symbol`
(as distinct from canonical) · `exchange` · `exchange_session` · `session_calendar` ·
`bar_timestamp_convention` (open-labelled vs close-labelled) · `ohlcv_basis` (raw vs adjusted) ·
`split_treatment` · `dividend_treatment` · `adjustment_as_of`.

The contract's own warning applies with full force: **an off-by-one bar-timestamp convention is
indistinguishable from look-ahead in results.** The suite in §3 checks the boundary against the
timestamps a dataset declares; it cannot detect a systematically mislabelled convention. That
check requires vendor documentation, and is unavailable.

## 5. Unresolved constraints carried forward

| # | Constraint | Consequence |
|---|---|---|
| C-1 | **No real market data** (§4.3) | EA-9's outcome labels and EA-10's attribution cannot be computed on real history under current authorization |
| C-2 | **Bar-timestamp convention unverifiable** (§4.4) | For any future real dataset, convention must be established from vendor documentation, not inferred |
| C-3 | **Accepted path unavailable** — binding per the 2026-07-28 amendment (EA-6-006) | Any metric requiring an accepted population is reported unavailable. **No accepted-trade quality, frequency, value, or comparable-path claim appears in EA-8.** Harness constraint, not an engine defect |
| C-4 | **Per-gate vector not persisted** (EA5-002 / EA-6-001) | Unchanged by EA-8; as-of datasets do not create observability that the engine does not emit |

## 6. Completion statement

| Criterion | Status |
|---|---|
| Look-ahead suite passes across the full replay range | **MET** — 5 of 5, plus a negative control proving the suite can fail |
| Every dataset carries an immutable manifest and checksum | **MET** — per-dataset manifest, per-symbol `file_sha256` and `content_digest_sha256`, plus `MANIFEST-CHECKSUMS.sha256` |
| Evaluable range stated with coverage limits | **MET** — §4, including the empty real-data range |

**No stop condition fired in the terminal sense.** The stop condition *did* engage as designed —
a required input (real vendor history) could not be reconstructed as-of, so the evaluable range
was **narrowed and the limit recorded** rather than approximated. That is the prescribed
response, not a failure.

**EA-9 is not authorized by this document.** The plan gates it on Dustin's approval of this
as-of contract and the evaluable range.

## 7. Amendment rule

Frozen from creation; never edited in place. A correction is a dated amendment or a new
versioned contract, with the version in the filename (`docs/conventions.md` §b, read across
by §h).
