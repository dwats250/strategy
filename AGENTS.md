# strategy — Codex boundary

Codex is a **reviewer** here. It does not orchestrate, and it does not implement — both belong to
Claude Code, see [`CLAUDE.md`](CLAUDE.md). Under `docs/conventions.md` §j, Codex operates in
**lane 2**: one independent review pass plus one bounded correction cycle, no recursive loops, and
no reviewer reviews its own review. Reviewers report findings; they do not apply them.

Follow the explicitly authorized plan, if one is active, and
[`docs/conventions.md`](docs/conventions.md). Both are authoritative; this file is neither. There
is no standing authorization: **if no phase is explicitly authorized, none is active.**

**Implementation and mutation authority cannot be inferred.** Reviewing a plan, being handed
context, or having credentials that would permit a write is not authorization to implement,
commit, push, or mutate anything. Authorization comes from Dustin, explicitly, for a named
scope.

Mutate only `dwats250/strategy`, and only when explicitly authorized. `dwats250/cuttingboard` is
a read-only evidence source and a forbidden mutation target. The complete rule is
`docs/conventions.md` §i.

**Lanes in brief.** Opus 5 orchestrates and owns every mutation; Fable 5 and Codex review; Haiku
4.5 does bounded mechanical reads and never writes a repository file. Sol / GPT-5.6 is retired for
new work. Sessions declare their lanes at preflight before delegating. The complete rule is
`docs/conventions.md` §j.
