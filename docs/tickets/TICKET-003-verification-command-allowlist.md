# Ticket: TICKET-003 — Allowlist verification command execution

## Metadata
- Owner: Platform
- Risk: R1
- Status: Complete

## Linked PRD
- PRD-001-R04

## Linked Spec
- SPEC-001-A19

## Goal
Remove the arbitrary command execution path in loop verification by executing ticket verification bullets as allowlisted argv lists instead of shell strings.

## Scope
Verification execution in the governance runtime, its configuration default, its tests, and the decision record. Fixes finding F1 of the 2026-07-12 security audit: `subprocess.run(..., shell=True)` on ticket-authored strings in `src/agentic_os/governance.py`.

## Files Allowed
- src/agentic_os/governance.py
- ado.config.json
- tests/test_governance.py
- .ai/requirements/acceptance-criteria.md
- docs/specs/SPEC-001-governance-runtime.md
- docs/tickets/TICKET-003-verification-command-allowlist.md
- docs/decisions/ADR-002-shell-free-verification.md

## Steps
- Parse each Verification bullet with shlex and validate it against `verification_allowed_commands` before a loop starts and before it verifies.
- Execute validated argv lists with subprocess and no shell; record OS-level launch failures as returncode 127.
- Add negative and positive tests: rejection at start, rejection of shell metacharacters and non-allowlisted programs, real argv execution driving pass and fail outcomes.
- Record the no-shell default in ADR-002 and SPEC-001-A19.

## Acceptance Criteria
- [x] A ticket whose Verification bullets contain non-allowlisted programs or shell metacharacters can neither start nor verify a loop.
- [x] Allowlisted commands execute without a shell and their exit codes drive the verification outcome.
- [x] `make verify` and `make product` pass with the new gates and tests.

## Verification
- `make verify`
- `make product`

## Stop Conditions
- Acceptance criteria pass.
- A required change falls outside scope.
- Risk exceeds R1.

## User Outcome Review
Ticket authors keep `make <target>`-style verification bullets; ticket files can no longer smuggle arbitrary shell into `loop verify`. Extending the allowlist is a deliberate, reviewable config change.

## Completion Notes
Implemented allowlisted argv verification (config default `["make"]`), validated at loop start and verify, executed shell-free, covered by TEST-018 and TEST-019.
