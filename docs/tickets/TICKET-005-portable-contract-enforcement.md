# Ticket: TICKET-005 — Enforce portable repository identity

## Metadata
- Owner: Platform
- Risk: R1
- Status: Complete

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
- [x] A matching repository value passes regardless of case.
- [x] A syntactically valid but different repository value fails.
- [x] Invalid profile fixtures fail deterministically.
- [x] Direct enforcement runs on every pull request and push to main.
- [x] `workflow_call` and `workflow_dispatch` remain available.
- [x] Governance, CodeQL, and Portable Repository Contract checks pass.

## Verification
- `make verify`
- `make product`

## Stop Conditions
- Acceptance criteria pass.
- A required change falls outside scope.
- Risk exceeds R1.
- A change requires repository settings, visibility, release, license, production, credentials, or a consumer repository.

## User Outcome Review
The contract now rejects a profile that names a different caller repository, accepts case-only differences, and runs for every ordinary change while preserving reusable and manual invocation.

## Completion Notes
Implementation head `3cb08a17b579373feff175b5d0825741bb002453` passed Governance (`29514650614`), Security/CodeQL (`29514650798`), and Portable Repository Contract (`29514650993`). This metadata-only close reruns the same checks.
