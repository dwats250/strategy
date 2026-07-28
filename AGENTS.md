# strategy — Codex boundary

Codex is primarily an **orchestrator and reviewer** here, not the implementation harness. That
role is Claude Code's — see [`CLAUDE.md`](CLAUDE.md).

Follow the current committed plan and [`docs/conventions.md`](docs/conventions.md). Both are
authoritative; this file is neither.

**Implementation and mutation authority cannot be inferred.** Reviewing a plan, being handed
context, or having credentials that would permit a write is not authorization to implement,
commit, push, or mutate anything. Authorization comes from Dustin, explicitly, for a named
scope.

Mutate only `dwats250/strategy`, and only when explicitly authorized. `dwats250/cuttingboard` is
a read-only evidence source and a forbidden mutation target. The complete rule is
`docs/conventions.md` §i.
