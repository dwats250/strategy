# Probe pre-registration — template v0.1

Status: `TEMPLATE — COPY PER PROBE, FILL BEFORE THE RUN, NEVER EDIT AFTER`

Created 2026-07-30 UTC. Adopted from gap register G-06 by
`docs/owner-decisions-2026-07-30.md`. This is the cheap tier between a full study manifest and
nothing: one page, about five minutes, filled **before** the run. It does not make exploratory
work into a study and does not try to. A probe with no completed pre-registration is an
ungoverned exploratory artifact and cannot be cited even weakly.

Copy to a `PROBE_<id>_<slug>.md` beside the work it registers.

---

```markdown
# PROBE <id> — <one line>

Date (UTC):
Status: EXPLORATORY — NO EDGE CLAIM

Symbol / timeframe / session:
Window (absolute timestamps, not relative ranges):
Script file + SHA-256:

trials_planned (N):            <- committed now; cannot be reconstructed later (§b amendment)
dsr_threshold_implied:         <- observed performance needed at this N and sample length

Question (one sentence):
Stop condition (what ends this probe):

Properties: untouched — no commission override, fill-on-bar-close OFF, recalc options OFF
Export: same-day CSV, SHA-256 recorded here after capture:
```

Rules: absolute timestamps because chart-history windows drift; the Properties line is copied
from `CAMPAIGN_MANIFEST_v2.4.md`'s frozen-environment block because Properties-tab settings
silently override the `strategy()` declaration; `trials_planned` counts *independent*
configurations, and numerically identical rows count once. Corrections after the run are dated
amendments (§b), never edits.
