# Ticket: TICKET-004 — Pilot professionalization and security hardening

## Metadata
- Owner: Platform
- Risk: R3
- Status: Complete

## Linked PRD
- PRD-001-R03
- PRD-001-R04
- PRD-001-R15

## Linked Spec
- SPEC-001-A03
- SPEC-001-A15
- SPEC-001-A19

## Goal
Make the harness candidate truthfully inspectable, remove the privately identified verification execution flaw, and establish reversible security and adoption gates for the bounded portfolio pilot.

## Scope
Documentation, agent orientation, dependency automation, workflow supply-chain pinning, CodeQL analysis, and shell-free allowlisted ticket verification. This ticket does not change repository settings, release artifacts, licensing, visibility, or consumer repositories.

## Files Allowed
- AGENTS.md
- SECURITY.md
- README.md
- ado.config.json
- .ai/requirements/acceptance-criteria.md
- .github/CODEOWNERS
- .github/dependabot.yml
- .github/workflows/governance.yml
- .github/workflows/portable-repository-contract.yml
- .github/workflows/security.yml
- docs/decisions/ADR-002-shell-free-verification.md
- docs/pilot/
- docs/specs/SPEC-001-governance-runtime.md
- docs/tickets/TICKET-004-pilot-professionalization.md
- portfolio-profile.json
- agent/approvals/TICKET-004.json
- src/agentic_os/governance.py
- tests/test_governance.py

## Steps
- Record the repository, history, security, and truth baseline.
- State the candidate role, maturity, limitations, and authority boundaries.
- Define version, compatibility, and upstream-learning contracts.
- Pin workflow actions and add dependency and code-scanning automation.
- Execute ticket verification as reviewed, allowlisted argument vectors without a shell.
- Add positive and negative regression tests and record the decision.
- Convert product evidence about machine-local configuration into a reusable, stack-neutral repository contract.
- Verify local-equivalent and GitHub Actions gates.
- Record completion only after remote checks pass.

## Acceptance Criteria
- [x] Baseline covers all branch heads and reachable history without cloning the repository.
- [x] Public documentation distinguishes shipped source behavior from unproven adoption claims.
- [x] Root agent guidance identifies the repository as non-canonical.
- [x] A security disclosure policy exists.
- [x] Workflow action dependencies are immutable and CodeQL is configured.
- [x] Ticket-authored verification cannot invoke a shell, chain commands, redirect, substitute, or execute a non-allowlisted program.
- [x] Allowlisted verification commands preserve pass/fail behavior.
- [x] The reusable contract validates the portfolio profile using the registry's independent lifecycle, maturity, investment, disposition, and data-classification axes and reports machine-local portability failures only as opaque IDs and status.
- [x] The reusable contract passes against this repository and can be called by consumers at an immutable commit SHA.
- [x] `make verify` and `make product` pass in GitHub Actions.
- [x] Governance and Security workflows pass on the pull request.
- [x] Completion notes record the verified head SHA and check results.

## Verification
- `make verify`
- `make product`

## Stop Conditions
- Acceptance criteria pass.
- A required change falls outside the listed files.
- A change requires settings, credentials, release publication, licensing, visibility, production access, or a consumer repository.
- Risk exceeds R3.

## User Outcome Review
The pilot owner authorized this bounded repository slice. The public surface now states its Lab and non-canonical status; the governance, security, and portable-contract checks prove the repository-level outcome. External usability, consumer acceptance, release, and canonicalization remain separate gates.

## Completion Notes
Implementation head `f438d05d7d8f17c18a002a0d93fadbea11053ded` passed Governance (`29513836145`), Security/CodeQL (`29513836730`), and Portable Repository Contract (`29513836843`). The ticket was then closed, the profile taxonomy was aligned to the central registry, and its R3 approval was rebound to the exact final ticket digest; the metadata-only updates rerun the same checks.
