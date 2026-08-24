# scripts/ — SOURCE_REQUIRED

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
