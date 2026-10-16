# scripts/ — VDC v0 source INGESTED / PARITY PENDING

Status (2026-08-25): the exact owner-supplied TradingView Pine source is ingested
verbatim as [`VWAP_Continuation_FastAlpha_v0.pine`](VWAP_Continuation_FastAlpha_v0.pine)
(sha256 `c476429225c2ba4abb7c91d370f3abde893d9e4afe83a41ac8a0069e342c6c9e`) — immutable
source evidence, never cleaned or reformatted; provenance and mechanical
characterization in
[`VWAP_Continuation_FastAlpha_v0_PROVENANCE.md`](VWAP_Continuation_FastAlpha_v0_PROVENANCE.md).
See charter Amendment A2 and `../PARITY_GATES.md`.

**2026-08-25 — R1 instrumented variant added:**
[`VWAP_Continuation_FastAlpha_v0_R1_instrumented_v1.0.pine`](VWAP_Continuation_FastAlpha_v0_R1_instrumented_v1.0.pine)
(sha256 `32aaaa4d2148186774921c8529c5ab3600bfe4110ffff2fd0213a6631ff72bc4`) — v0 trading
sections byte-identical (v0 lines 19–349 == R1 lines 41–371); observational-only A1/PVAE
instrumentation appended as section 13, exported via `display.data_window` plots. Static
and local containment proofs recorded in `../manifests/RUN_VDC_SPY_5m_dev_R1_PREP_v0.1.md`;
local mirror `../analysis/instrumentation_r1.py`. Not a run authorization; v0 remains the
R0 source of record (§c: both versions retained).

**2026-08-26 — V1 EMA 10/22 controlled perturbation added:**
[`VWAP_Continuation_FastAlpha_V1_EMA10_22.pine`](VWAP_Continuation_FastAlpha_V1_EMA10_22.pine)
(sha256 `bca7f7eaf8fd7c93e3400dd72a8661f3d8f9d99219509a2f0fedf3cc03b32519`) — byte-identical to
v0 except four lines: the FastAlpha trading EMA pair `EMA_FAST_LEN 9→10` / `EMA_SLOW_LEN 20→22`
(lines 79–80, the sole strategy-semantic change) and the strategy title/short-title (lines 3–4,
identity). Static diff proof + flat-agnostic candidate sanity: `../analysis/v1_ema1022_diff_proof.py`;
PREP manifest `../manifests/RUN_VDC_SPY_5m_dev_V1_EMA10_22_PREP_v0.1.md`. No identity gate (V1 is a
deliberate perturbation). Not a run authorization; v0 remains the R0 source of record.

Historical status (accurate until 2026-08-25 ingest — retained, not rewritten):

**No strategy script is present, and none may be written by reconstruction.**

`VDC_SOURCE_STATUS = SOURCE_REQUIRED`. There is no exact current FastAlpha / VWAP Drift v0 Pine
source in `dwats250/strategy` or its history. The VDC trigger/entry/stop/exit/timing/Pine
implementation is **unresolved** and must **not** be reconstructed from chat-memory summaries,
`session_compass_v2.3.pine`, older VWAP indicators, or conceptual descriptions — those are context
only, not source authority (charter §8).

A strategy script lands here only when one of the following occurs:

- Dustin supplies the **actual TradingView Pine source**, ingested and pinned; or
- Dustin **explicitly commissions a brand-new VDC-0 specification**, from which a script is then
  written.

When a script does land:

- It is **versioned** (`docs/conventions.md` §c). Any change that can change results bumps the
  version; retired versions stay here alongside the current one.
- Its **sha256** is recorded in each run manifest and ledger row that uses it.
- Live chart indicators do **not** belong here (they live in the repo-root `indicators/`); only
  this study's experiment scripts do (§a).

VMR and VREV have no sprint implementation (VMR defined only; VREV held at 0 tests).
