# CBF05 candidate-fidelity checkpoint

Status: `DIAGNOSTIC RAW EVIDENCE — POSTURE PATCH COMPARISON`

This checkpoint preserves the two materially different BATS:SPY daily bar
exports surrounding the demonstrated v0.5 posture-threshold correction:

```pine
posturePass = confidence >= 0.55
```

The corrected export is the checkpoint artifact. The pre-patch export is kept
only as the comparison baseline so the effect of the correction remains
reproducible.

## Runtime identity

- Chart/export: `BATS:SPY`
- Timeframe: `1D`
- Candle type: standard candles
- Rows: `3,173` data rows
- Date range: `2013-12-12` through `2026-07-28`
- Pine stage: `V4`
- Source script: operator-held `cuttingboard_direct_path_fidelity_v0_5.pine`

The source script is not included in this local staging packet because it was
not uploaded into the workspace. Its exact SHA-256 and the complete TradingView
session/provider settings still belong in a future run record before this is
treated as a full TV-3 package.

## Preserved exports

| File | Role | SHA-256 | V2 candidates | V4 candidates | Selected attempts |
|---|---|---|---:|---:|---:|
| `exports/CBF05_BATS_SPY1D_V4_bars_20131212-20260728_v050-prepatch-c050.csv` | Pre-patch comparison (`>= 0.50`) | `e28aa87468d1922500b119bf02ded470c5528d327edf0bf09d2f124b1448ab8b` | 602 | 170 | 118 |
| `exports/CBF05_BATS_SPY1D_V4_bars_20131212-20260728_v050-postpatch-c055.csv` | Corrected checkpoint (`>= 0.55`) | `2d375b4c1b60671012e834bd093057cdd0c964fee7a09c031e635c1eec5065e9` | 284 | 79 | 62 |

## Standing and limits

This is a diagnostic checkpoint for candidate-fidelity validation. It is not a
TV-3 run package: it does not include a full simulated trade ledger, a run
manifest, the Pine source, or a parity acceptance claim. It makes no
profitability, alpha, options-return, or live-execution claim.

The separate R-01 expansion completeness issue remains open. These exports do
not resolve it.

