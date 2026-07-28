# EA-7 Run Manifest — `EA-7-halted-validation`

Status: `ARCHIVED — REPLAYABLE`

Created: 2026-07-28 UTC · Case: `halted-validation`

SPY (a HALT_SYMBOLS member) removed — validation HALT

## Frozen identities

| Field | Value |
|---|---|
| CuttingBoard snapshot | `59f8279d796335149afdec4aa507b6f927233518` |
| `config.toml` SHA-256 | `329c2ea58ee2373eb8722b738b9cc6453c4d4b359c57657b32da2db4524318cb` |
| Environment lockfile SHA-256 | `3fd88335fb95aee68a18c06e0ced50f1d35ba47f7107690a54e2df3f4c5300d0` |
| Quote fixture SHA-256 | `7c21a518bb0d2ae08759c62548f63349c7e3b93b6521093c396c26833593c790` |
| OHLCV input | NOT USED — this case halts before derived metrics run |
| Input generator | `../../fixtures/build_inputs.py` |
| Capture wrapper | `EA-6-capture/1.0.0` |
| Replay harness | `EA-7-replay/1.0.0` |
| Trace schema | `EA-6-trace/v1` |

## Reproduction target

**Canonical decision payload SHA-256:**

```
a8ff926c05ff0aa2b4e231b04ce41aec581519f5acda2f210bf7366f848cec4f
```

Computed over `canonical_decision_payload` only, serialized `sort_keys=True`,
`ensure_ascii=False`, `separators=(",",":")`, UTF-8.

## Envelope — excluded from equality by design

Enumerated, not implied:

- `run_dir_basename`
- `pipeline_record_count`
- `artifacts_present`

These carry sandbox- and host-specific values. They are recorded in every trace and
never compared.

## Replay command

```sh
python3 ../../tools/replay/replay.py \
    --src <extracted-pin> --base <base-fixture> --work <scratch> \
    --case halted-validation --expect a8ff926c05ff0aa2b4e231b04ce41aec581519f5acda2f210bf7366f848cec4f \
    --snapshot-sha 59f8279d796335149afdec4aa507b6f927233518 --env-lock-sha 3fd88335fb95aee68a18c06e0ced50f1d35ba47f7107690a54e2df3f4c5300d0
```

Run under `bwrap --unshare-net`, read-only root, single writable bind.

## Parity scope

- **Logic parity:** tested here. Same inputs, same pinned code path, same canonical payload.
- **Data-provider parity:** **unavailable.** No live CuttingBoard output exists to compare
  against, and obtaining one would require live market data. Not estimated.
- **Accepted path:** **unavailable** per the 2026-07-28 plan amendment (EA-6-006). This
  manifest makes no accepted-trade claim.
