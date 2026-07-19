# Ticket: TICKET-008 — Synchronize superseded donor status

## Metadata
- Owner: Documentation and Platform
- Risk: R1
- Status: In Review

## Linked PRD
- PRD-001-R01
- PRD-001-R15

## Linked Spec
- SPEC-001-A01
- SPEC-001-A15

## Goal
Make every current repository entry surface identify Agentic Dev OS as a
superseded governance donor whose canonical successor is Recursive Harness.

## Scope
Synchronize the local governance mirror and status prose after the authoritative
portfolio decision merged. Preserve historical evidence, source verification,
security boundaries, and live GitHub settings.

## Files Allowed
- AGENTS.md
- README.md
- portfolio-profile.json
- docs/productization/STATUS.md
- docs/change-requests/CR-002-sync-superseded-donor-status.md
- docs/tickets/TICKET-008-sync-superseded-donor-status.md

## Steps
- Copy governed fields from the merged central registry into the local profile.
- Replace active-candidate routing and status claims with superseded-donor and
  Recursive-successor language.
- Keep point-in-time pilot and CI evidence visibly historical.
- Run the full repository and product verification commands.

## Acceptance Criteria
- [x] `portfolio-profile.json` matches all governed fields in the central record.
- [x] AGENTS guidance routes new reusable work to Recursive Harness.
- [x] README names the successor, maintenance expectation, and historical role
  before any setup instructions.
- [x] Productization status uses the archived profile and preserves dated
  evidence without presenting it as current product support.
- [x] No source behavior, release, live archive state, visibility, settings,
  historical receipt, or security boundary changes.
- [ ] `make verify` and `make product` pass.

## Verification
- `make verify`
- `make product`
- `python ../repo-audit/codex/skills/portfolio-governance/scripts/portfolio_context.py GhostlyGawd/agentic-dev-os`

## Stop Conditions
- Acceptance criteria pass and required remote checks complete.
- A required change falls outside the six allowed files.
- The change would mutate GitHub settings or rewrite point-in-time evidence.
- Risk exceeds R1.

## User Outcome Review
The repository becomes unambiguous to agents and people: it is useful donor
evidence, while Recursive Harness owns future reusable harness development.

## Completion Notes
Pending local and protected pull-request verification.
