# Repository agent guidance

## Repository role

This repository is a **superseded governance reference and capability donor**.
`GhostlyGawd/recursive-harness` is the canonical multi-agent harness target.
Preserve useful evidence here, but do not start new reusable harness behavior
or provider adapters in this repository.

Current classification:

- maturity: Lab
- investment: Maintenance-only
- visibility: Public
- source version: `1.1.0`
- lifecycle: Superseded
- disposition: Archive governance profile; live GitHub remains public and unarchived
- release status: No tagged release

Portfolio inventory and rollout authority live in `GhostlyGawd/repo-audit`. Query that control plane when portfolio context is needed; do not copy the entire portfolio registry into this repository.

## Portfolio synchronization

Before material work, resolve this repository's live owner/name, default branch,
and current commit SHA. Then read the matching central record in
`GhostlyGawd/repo-audit` together with this repository's local instructions.

`portfolio-profile.json` is a mirror of the central governance record, not an
independent source of truth. Propose a `repo-audit` update when identity, family,
lifecycle, maturity, investment, disposition, visibility intent, lineage, data
classification, or capability role changes. After that decision is merged,
synchronize this local mirror through an explicit product pull request.
## Orientation order

Before changing anything:

1. Read `.ai/context/`, `.ai/strategy/`, and `.ai/operating-rules.md`.
2. Read the active ticket and its linked PRD, spec, milestone, and policies.
3. Read `agent/AGENTS.md` for execution-loop rules.
4. Check `docs/pilot/BASELINE.md`, `docs/pilot/ADOPTION_CONTRACT.md`, and open pull requests for current pilot constraints.

More-specific `AGENTS.md` files override this file within their directory.

## Working contract

- One bounded ticket, one declared scope, one verification path.
- Run `make verify` and `make product` before completion.
- Treat generated files under `.ai/requirements/` as outputs; regenerate them instead of editing them.
- Keep product-specific lessons in the product repository. Route a general
  harness learning to `GhostlyGawd/recursive-harness` with evidence and an
  acceptance test.
- Treat code and documents here as donor evidence. Adapt capabilities through
  Recursive's adoption matrix instead of extending this runtime in parallel.
- Consumer updates are proposed as pull requests and are never merged automatically.

## Authority boundaries

Agents may inspect, test, document, and propose reversible changes. Without explicit human authorization, agents must not:

- claim this implementation is active, canonical, Stable, or production-proven;
- publish a release or package;
- change visibility, licensing, repository settings, or branch protection;
- rotate credentials or disclose security details publicly;
- update, archive, or merge changes in consumer repositories;
- weaken a security, traceability, or approval gate.

Security findings belong in a private channel and should be referenced publicly only by an opaque identifier.
