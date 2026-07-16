# Ticket: TICKET-004 — Pilot professionalization and security baseline

## Metadata
- Owner: Platform
- Risk: R1
- Status: In Progress

## Linked PRD
- PRD-001-R03
- PRD-001-R15

## Linked Spec
- SPEC-001-A03
- SPEC-001-A15

## Goal
Make the harness candidate truthfully inspectable and establish reversible security and adoption gates for the bounded portfolio pilot.

## Scope
Documentation, agent orientation, dependency automation, workflow supply-chain pinning, CodeQL analysis, and the pilot evidence record. This ticket does not change repository settings, release artifacts, licensing, visibility, or consumer repositories.

## Files Allowed
- AGENTS.md
- SECURITY.md
- README.md
- .github/CODEOWNERS
- .github/dependabot.yml
- .github/workflows/governance.yml
- .github/workflows/security.yml
- docs/pilot/
- docs/tickets/TICKET-004-pilot-professionalization.md

## Steps
- Record the repository, history, security, and truth baseline.
- State the candidate role, maturity, limitations, and authority boundaries.
- Define version, compatibility, and upstream-learning contracts.
- Pin workflow actions and add dependency and code-scanning automation.
- Verify local-equivalent and GitHub Actions gates.
- Record completion only after remote checks pass.

## Acceptance Criteria
- [x] Baseline covers all branch heads and reachable history without cloning the repository.
- [x] Public documentation distinguishes shipped source behavior from unproven adoption claims.
- [x] Root agent guidance identifies the repository as non-canonical.
- [x] A security disclosure policy exists.
- [x] Workflow action dependencies are immutable and CodeQL is configured.
- [ ] `make verify` and `make product` pass in GitHub Actions.
- [ ] Governance and Security workflows pass on the pull request.
- [ ] Completion notes record the verified head SHA and check results.

## Verification
- `make verify`
- `make product`

## Stop Conditions
- Acceptance criteria pass.
- A required change falls outside the listed files.
- A change requires settings, credentials, release publication, licensing, visibility, production access, or a consumer repository.
- Risk exceeds R1.

## User Outcome Review
Pending remote verification and pilot-owner review.

## Completion Notes
Pending remote verification.
