# strategy — agent entrypoint

## Cross-repository isolation — binding

> When operating under this repository or any CuttingBoard audit charge, an
> agent may mutate only `dwats250/strategy`. The repository
> `dwats250/cuttingboard`, every local CuttingBoard checkout, and every
> CuttingBoard remote are read-only evidence sources. Possession of credentials
> capable of writing to CuttingBoard does not grant authority to use them. No
> agent may create, update, delete, push, merge, comment, dispatch, configure,
> or otherwise mutate any CuttingBoard file, ref, branch, pull request, issue,
> review, workflow, release, setting, or remote. If the work appears to require
> a CuttingBoard mutation, stop and request a separate Dustin-authorized
> CuttingBoard charge in a separate session rooted in that repository.

> Results from this audit may become evidence for a later independent
> CuttingBoard review. They do not authorize refactoring, issue creation,
> parameter changes, documentation changes, or any other back-feed into
> CuttingBoard.

Every GitHub or connector mutation must supply its repository target
explicitly, and that target must be exactly `dwats250/strategy`. A missing,
inferred, or ambiguous target is a STOP condition. A CuttingBoard target is a
STOP condition.

**Read the complete cross-repository isolation section in
[`docs/conventions.md`](docs/conventions.md) §i before acting.** It carries the
full rule, the capability-is-not-authorization principle, the pinned-SHA
evidence-access rules, and the mandatory session preflight.

## Repository conventions

[`docs/conventions.md`](docs/conventions.md) holds the standing rules for this
research lab — study layout, pre-registered manifests, script versioning,
immutable exports, the ledger, holdout definition, and how audits differ from
studies. Read it before adding a study or audit, or amending a manifest.
