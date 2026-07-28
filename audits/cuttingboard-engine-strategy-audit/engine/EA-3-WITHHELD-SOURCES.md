# EA-3 — Withheld Sources

Status: `ACTIVE — BINDING WITHHOLDING LIST. NONE OF THESE HAS BEEN READ.`

Created: 2026-07-27 UTC

Source pin: `dwats250/cuttingboard@59f8279d796335149afdec4aa507b6f927233518`

Governing plan: [`../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md`](../plans/EA-ENGINE-AUDIT-PROGRAM-REV3.md) § EA-3, § EA-12.

---

## 1. Why this list exists

The pinned engine carries a large corpus of prior audit and review documents. **Reading them
now would anchor this audit's findings to someone else's conclusions**, and would make it
impossible to say later whether we found something independently or merely agreed with a
predecessor.

The plan therefore draws a hard line: **contract documents are the specification and are read
now; findings documents are somebody's conclusions and are read only after this audit has
formed its own.** The withheld corpus is opened at **EA-12**, where it is used as
*corroboration, not authority*, and where agreements and disagreements are recorded separately.

**None of the paths below has been read.** They were enumerated by directory listing only —
listing a path is not reading its content. The audited read set is
[`EA-3-READ-LOG.csv`](EA-3-READ-LOG.csv), which contains **no withheld path**.

---

## 2. Withheld — named files

| # | Path at pin |
|---|---|
| 1 | `audits/FINDINGS.md` |
| 2 | `audits/RECONCILED_FINDINGS.md` |
| 3 | `audits/CODEX_REVIEW.md` |
| 4 | `audits/FABLE_REVIEW.md` |
| 5 | `audits/qualification-tuning-2026-07-05/findings.md` |
| 6 | `audits/codebase-review-2026-07-03/mentor-review.md` |
| 7 | `docs/audit/gate_recon_2026-06-12.md` |

## 3. Withheld — directory sets (all contents)

| # | Directory at pin |
|---|---|
| 1 | `audits/alignment-2026-05-22/` |
| 2 | `audits/inventory-2026-05-22/` |
| 3 | `audits/cleanup-2026-05-22/` |
| 4 | `audits/recon-2026-05-22/` |
| 5 | `audits/recon-2026-05-24/` |
| 6 | `audits/recon-2026-06-22/` |
| 7 | `audits/recon-2026-07-01/` |
| 8 | `audits/prd-lifecycle-audit-2026-07-05/` |

The plan names the `recon-*` set generically; enumeration at the pin resolves it to **four**
directories, all withheld.

## 4. Withheld — glob set

| Pattern at pin | Count |
|---|---|
| `docs/prd_history/*.review.*` | **127 files** |

---

## 5. Scope boundary — read neither now nor withheld

One document is on **neither** list, and is recorded here so the boundary is explicit rather
than accidental:

| Path at pin | Status |
|---|---|
| `docs/system_logic_map.md` | **Not read.** Not on EA-3's authorized read set, and not on the withheld list |

`docs/decision_quality_map.md` §*Anchors* explicitly anchors on it for "runtime decision flow,
decision-affecting modules, display-only modules, sidecar boundary rules, forbidden mutation
paths" — so it is materially relevant. EA-3's authorized work enumerates specific documents and
this is not among them, so it was left unread rather than pulled in by inference.

**Recorded for EA-4:** `docs/system_logic_map.md` is a contract-class document (a logic map, not
a findings document) that EA-4 will likely need. Whether to add it to the authorized contract set
is Dustin's call; it is not withheld, merely unlisted.

---

## 6. Binding rules until EA-12

1. No phase before EA-12 may read any path in §2, §3, or §4.
2. Any read of a withheld path is an **EA-3 stop condition** and must be reported, not absorbed.
3. At EA-12 the corpus is opened and cross-checked: which of our findings it corroborates, which
   it contradicts, which it raises that we missed, and which of its claims our evidence does not
   support. Agreements and disagreements are recorded separately.
4. **A prior finding is corroboration, not authority.** No finding of ours may be revised to
   match a prior audit without independent evidence.

## 7. Amendment rule

Frozen from creation; never edited in place. A correction is a dated amendment file or a new
versioned list, with the version in the filename (`docs/conventions.md` §b, read across by §h).
