# Ticket: TICKET-005 — Enforce portable repository identity

## Metadata
- Owner: Platform
- Risk: R1
- Status: In Progress

## Linked PRD
- PRD-001-R15

## Linked Spec
- SPEC-001-A15

## Goal
Ensure the portable repository contract validates the caller's identity and runs for every ordinary repository change.

## Scope
The reusable portability workflow, its deterministic inline self-tests, and its contract documentation. No repository settings, visibility, release, license, production, credential, or consumer change is included.

## Files Allowed
- .github/workflows/portable-repository-contract.yml
- docs/pilot/PORTABLE_REPOSITORY_CONTRACT.md
- docs/tickets/TICKET-005-portable-contract-enforcement.md

## Steps
- Bind the declared repository to the GitHub caller identity with case-insensitive comparison.
- Add deterministic positive, case-variant, wrong-repository, and invalid-profile self-tests.
- Run the direct workflow on every pull request and push to main.
- Preserve reusable and manual invocation.
- Verify all repository workflows.

## Acceptance Criteria
- [ ] A matching repository value passes regardless of case.
- [ ] A syntactically valid but different repository value fails.
- [ ] Invalid profile fixtures fail deterministically.
- [ ] Direct enforcement runs on every pull request and push to main.
- [ ] `workflow_call` and `workflow_dispatch` remain available.
- [ ] Governance, CodeQL, and Portable Repository Contract checks pass.

## Verification
- `make verify`
- `make product`

## Stop Conditions
- Acceptance criteria pass.
- A required change falls outside scope.
- Risk exceeds R1.
- A change requires repository settings, visibility, release, license, production, credentials, or a consumer repository.

## User Outcome Review
Pending remote verification.

## Completion Notes
Pending remote verification.
