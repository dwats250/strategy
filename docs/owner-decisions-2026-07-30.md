# Owner decisions — 2026-07-30

Status: `DECISION RECORD — decided by Dustin, 2026-07-30 UTC`

Gate 3 of the program scoped in the intake review of the 2026-07-29 drafts
(`docs/drafts-intake-2026-07-30.md`). Three decisions were put to Dustin explicitly and
answered; this record is the durable form, per the retrospective's rule that decisions are
written down, not settled in chat.

## 1. §i repository boundary — **HYBRID adopted**

Of the options analyzed in `engine-program-draft-2026-07-29.md` §C: a Dustin-owned fork becomes
the development mutation target (in its own sessions); the audited pin keeps the per-change
charge rule; the no-back-feeding lock is restated explicitly — audit-derived changes need their
own commission wherever they land; merge-back to production is its own governance event.
Implemented as the dated amendment "Development boundary — amendment 2026-07-30" in
`conventions.md` §i.

## 2. Governance adoptions — **all three adopted**

- **G-03 trial budget**: `trials_planned` + `dsr_threshold_implied` required in future
  manifests and probe pre-registrations — amendment appended to `conventions.md` §b.
- **G-04 embargo**: deferred-inspection windows separated from fitted windows by at least the
  longest indicator lookback — amendment appended to `conventions.md` §g.
- **G-06 probe template**: `docs/PROBE_TEMPLATE_v0.1.md` created as the exploratory
  pre-registration path.

## 3. TradingView capture campaign — **DEFERRED, revisit shortly**

No campaign is chartered today. TradingView Premium runs to approximately 2026-08-29; if
specific strategy families and questions are brought as a charter within that window, each
capture gets a probe pre-registration under the new template. Nothing is captured ahead of a
stated question. Declining to capture is an accepted outcome.

## Explicitly still open (not decided here)

The `GATE_TRANSLATION_MATRIX.md` Q-03 correction implied by the Gate 2 analysis (its own dated
correction, kept out of Gate 2 by instruction); any engine program phase; the metrics harness;
data acquisition under `DATA_PROVENANCE_CONTRACT.md`.
