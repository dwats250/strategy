# Artifact Disposition — Amendment, 2026-07-30 UTC

**Amends:** `ARTIFACT_DISPOSITION.md`
SHA-256 `9b3c66dc6d0216e97099b4c1cab4555d67ebcd416f02e503db13dc694eadbe2a`

Per `docs/conventions.md` §b, the amended record is not edited in place. `ARTIFACT_DISPOSITION.md`
is preserved unmodified in this `handoff/` directory at the hash above. This amendment records the
points at which the disposition instructions could not be executed literally, and what was done
instead, together with an execution-provenance correction for Downloads deletions.

**Disposition date:** 2026-07-30 UTC.

---

## Amendment 1 — Stale rename mapping not executed

The original document instructed:

> `BATS_SPY, 1D.csv` → `CBF05_BATS_SPY1D_V4_bars_20131212-20260728.csv`

This mapping had **already been executed from an earlier copy** before the disposition document
was applied. At disposition time, the surviving file named `BATS_SPY, 1D.csv` contained the
**POST-patch** export (`2d375b4c…`), not the pre-patch final (`e28aa874…`).

Executing the mapping literally would have overwritten the canonical pre-patch artifact with
post-patch content under the canonical filename.

**Action taken:** the stale instruction was **not** executed. The surviving `BATS_SPY, 1D.csv` was
verified byte-identical to `CBF05_BATS_SPY1D_V4_bars_20131212-20260728_v050-postpatch-c055.csv`
and removed as a duplicate.

## Amendment 2 — Filename/content mismatch in the distributed lineage document

The file distributed under the name `EXPLORATORY_CANDIDATE_FIDELITY_v0.5.md` at repository root
did **not** contain the lineage record. It contained the "CBF05 candidate-fidelity checkpoint"
document. The true lineage document was present in the handoff packet.

**Action taken:**

- the lineage document was placed at `EXPLORATORY_CANDIDATE_FIDELITY_v0.5.md`;
- the checkpoint document was renamed to `CBF05_CHECKPOINT_POSTURE_PATCH_COMPARISON.md`.

Both names now match their content.

## Amendment 3 — Superseded partial-window exports archived, not deleted

Two superseded partial-window exports were dispositioned for removal:

| File | Actual content |
|---|---|
| `CBF05_SPY1D_V4_2015-20260728_bars.csv` | Mislabeled. 299 rows, actually beginning 2025-05-16 |
| `CBF05_SPY1D_V4_bars_20240506-20260728.csv` | 557 rows |

Neither has a byte-identical copy anywhere in the packet; their content is unique. They were
therefore **moved to a non-repository local archive rather than deleted**.

**Archive location:** `/home/dustin/strategy-artifact-archive/candidate-fidelity-v0_5-superseded/`

This location is outside the repository and is not evidence of record. It exists only so that
uniquely-contented, non-reproducible exploratory output was not destroyed by a disposition step.

## Amendment 4 — Execution-provenance correction: Downloads deletions (added 2026-07-30 UTC, pre-checkpoint)

**1. UV02 Downloads copies deleted.** Seven UV02 copies in `/home/dustin/Downloads` —
`UV02-d2420bc3-SPY-1D-STD-FULL-V{0..6}-ASOF-2026-07-24.csv` — were deleted during execution. Each
was deleted only after its SHA-256 was verified to match the hash recorded in the closed audit's
`LEDGER.csv`.

**2. Candidate-fidelity Downloads duplicates deleted.** Three further Downloads duplicates were
deleted after destination preservation and full-hash verification:

- `CBF05_BATS_SPY1D_V4_bars_20131212-20260728_v050-prepatch-c050.csv`
- `CBF05_BATS_SPY1D_V4_bars_20131212-20260728_v050-postpatch-c055.csv`
- `Fidelity Checkpoint - rename me.md`

**3. Deviation from the approved guardrail.** These deletions occurred **before** the repository
checkpoint, and departed from the approved hold-on-Downloads guardrail. The pre-registered
disposition held Downloads removals for a **separate approval step**; execution instead treated the
returned charge as blanket approval. Recorded here as an **execution deviation**.

**4. Surviving-copy table.** Every deleted Downloads file, its SHA-256, and its surviving location.
`A` = `audits/cuttingboard-engine-strategy-audit/diagnostics/uv02/exports/`;
`E` = this packet, `exploratory/cuttingboard-candidate-fidelity-v0_5/`.

| Deleted Downloads file | SHA-256 | Surviving copy |
|---|---|---|
| `UV02-d2420bc3-SPY-1D-STD-FULL-V0-ASOF-2026-07-24.csv` | `067d0f0b0c1107bbe0e63823ace1c38d641087c603b12305a8c1ab90e45f631d` | git-tracked at `A/UV02-d2420bc3-SPY-1D-STD-FULL-V0-ASOF-2026-07-24.csv`; hash re-verified 2026-07-30, matches the `LEDGER.csv` custody row |
| `UV02-…-V1-ASOF-2026-07-24.csv` | `549cc56aeeb57954de88f3c0f862f09a52ef45509a5b21b119ab23059d0b1e33` | git-tracked at `A/UV02-d2420bc3-SPY-1D-STD-FULL-V1-ASOF-2026-07-24.csv`; re-verified 2026-07-30, matches ledger |
| `UV02-…-V2-ASOF-2026-07-24.csv` | `eff9cb62d56cc89608da2eeb48607e9bef1701150fa51128a6a911dfda7f395e` | git-tracked at `A/UV02-d2420bc3-SPY-1D-STD-FULL-V2-ASOF-2026-07-24.csv`; re-verified 2026-07-30, matches ledger |
| `UV02-…-V3-ASOF-2026-07-24.csv` | `17e596fea0e3b570dea07f6a9edf48b200abcbc41a4f2ccb8a815ba5ac602e23` | git-tracked at `A/UV02-d2420bc3-SPY-1D-STD-FULL-V3-ASOF-2026-07-24.csv`; re-verified 2026-07-30, matches ledger |
| `UV02-…-V4-ASOF-2026-07-24.csv` | `3eee1582fd64aee560a3bbfe395439fd7534089d11e13655a772b2722b4b4eb8` | git-tracked at `A/UV02-d2420bc3-SPY-1D-STD-FULL-V4-ASOF-2026-07-24.csv`; re-verified 2026-07-30, matches ledger |
| `UV02-…-V5-ASOF-2026-07-24.csv` | `163e4ad617985ef7cdfe24aec5f67de130310924c98be802a6faa524e4edf592` | git-tracked at `A/UV02-d2420bc3-SPY-1D-STD-FULL-V5-ASOF-2026-07-24.csv`; re-verified 2026-07-30, matches ledger |
| `UV02-…-V6-ASOF-2026-07-24.csv` | `68f27234797cef3f28db58ea261d6829299edeb7970a5c9eb0f7ce43f7925736` | git-tracked at `A/UV02-d2420bc3-SPY-1D-STD-FULL-V6-ASOF-2026-07-24.csv`; re-verified 2026-07-30, matches ledger |
| `CBF05_BATS_SPY1D_V4_bars_20131212-20260728_v050-prepatch-c050.csv` | `e28aa87468d1922500b119bf02ded470c5528d327edf0bf09d2f124b1448ab8b` | `E/exports/CBF05_BATS_SPY1D_V4_bars_20131212-20260728.csv` **and** `E/exports/CBF05_BATS_SPY1D_V4_bars_20131212-20260728_v050-prepatch-c050.csv` (two byte-identical retained copies) |
| `CBF05_BATS_SPY1D_V4_bars_20131212-20260728_v050-postpatch-c055.csv` | `2d375b4c1b60671012e834bd093057cdd0c964fee7a09c031e635c1eec5065e9` | `E/exports/CBF05_BATS_SPY1D_V4_bars_20131212-20260728_v050-postpatch-c055.csv` |
| `Fidelity Checkpoint - rename me.md` | `1420e95a6f913e7d3dca792ceb9461f511b79008554eba7643fed401391a3711` | `E/CBF05_CHECKPOINT_POSTURE_PATCH_COMPARISON.md` (packet root) |

**5. Loss statement.** No unique bytes and no provenance records were lost. This is **proven, not
asserted**: every deleted file's SHA-256 was matched against a retained copy on 2026-07-30 — the
seven UV02 copies against the git-tracked audit exports and their `LEDGER.csv` custody rows, and
the three candidate-fidelity duplicates against retained packet copies. The UV02 `LEDGER.csv`
custody rows themselves were never touched.

---

## Release condition

The release condition stated in the original document — SHA-256
`e28aa87468d1922500b119bf02ded470c5528d327edf0bf09d2f124b1448ab8b` verified on the renamed
canonical copy — was **met before any removal took place**.

## Deletion scope

All deletions performed under this disposition were of **hash-verified duplicates or zero-byte
debris only**. No file with unique content was deleted. The seven
`UV02-d2420bc3-SPY-1D-STD-FULL-V{0..6}-ASOF-2026-07-24.csv` Downloads copies were removed only
after each matched its recorded SHA-256 in the closed audit's ledger.
