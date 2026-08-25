# scripts/ — VDC v0 source INGESTED / PARITY PENDING

Status (2026-08-25): the exact owner-supplied TradingView Pine source is ingested
verbatim as [`VWAP_Continuation_FastAlpha_v0.pine`](VWAP_Continuation_FastAlpha_v0.pine)
(sha256 `c476429225c2ba4abb7c91d370f3abde893d9e4afe83a41ac8a0069e342c6c9e`) — immutable
source evidence, never cleaned or reformatted; provenance and mechanical
characterization in
[`VWAP_Continuation_FastAlpha_v0_PROVENANCE.md`](VWAP_Continuation_FastAlpha_v0_PROVENANCE.md).
See charter Amendment A2 and `../PARITY_GATES.md`.

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
