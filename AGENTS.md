# Repository agent guidance

## Repository role

This repository is the **candidate shared Agentic Development Harness** for the portfolio pilot. It is not yet the canonical portfolio standard, a stable release, or an authorization to update other repositories.

Current classification:

- maturity: Lab
- investment: Supported pilot candidate
- visibility: Public
- source version: `1.1.0`
- release status: No tagged release

Portfolio inventory and rollout authority live in `GhostlyGawd/repo-audit`. Query that control plane when portfolio context is needed; do not copy the entire portfolio registry into this repository.

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
- Keep product-specific lessons in the product repository. Propose a general learning here only with evidence and an acceptance test.
- A harness change becomes reusable only after pilot-repository verification and an explicit version decision.
- Consumer updates are proposed as pull requests and are never merged automatically.

## Authority boundaries

Agents may inspect, test, document, and propose reversible changes. Without explicit human authorization, agents must not:

- claim this implementation is canonical, Stable, or production-proven;
- publish a release or package;
- change visibility, licensing, repository settings, or branch protection;
- rotate credentials or disclose security details publicly;
- update, archive, or merge changes in consumer repositories;
- weaken a security, traceability, or approval gate.

Security findings belong in a private channel and should be referenced publicly only by an opaque identifier.
