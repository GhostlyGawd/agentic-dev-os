# Ticket: TICKET-007 — Adopt the portfolio productization evidence surface

## Metadata
- Owner: Documentation and Platform
- Risk: R1
- Status: In Review

## Linked PRD
- PRD-001-R01
- PRD-001-R15

## Linked Spec
- SPEC-001-A15
- SPEC-001-A18

## Goal
Make the Lab-stage harness candidate understandable, runnable from current-source documentation, visually inspectable, and honest about evidence and remaining gates under portfolio productization standard v1.0.0.

## Scope
Documentation and evidence adoption only. Clarify the README; add architecture, provenance, support, and productization status; and add static visuals derived from documented architecture and actual sanitized CI output. Do not change harness behavior, contracts, source version, canonical status, releases, tags, consumers, or repository settings.

## Files Allowed
- README.md
- SUPPORT.md
- docs/ARCHITECTURE.md
- docs/PROVENANCE.md
- docs/assets/agentic-dev-os-system-map.svg
- docs/assets/governance-ci-evidence.svg
- docs/productization/STATUS.md
- docs/tickets/TICKET-007-productization-adoption.md

## Steps
- Reconcile proposition, audience, source workflow, version, and candidate status against live repository and pilot evidence.
- Map all ten public-product requirements to evidence or a named blocker.
- Add a workflow visual and sanitized terminal rendering sourced from successful default-branch Actions logs.
- Document architecture, limitations, security/privacy, provenance, support, and recovery.
- Verify the repository and product chain without changing behavior.

## Acceptance Criteria
- [x] README identifies the product, audience, outcome, Lab maturity, unreleased state, and candidate-not-canonical role.
- [x] Setup commands are copyable without a five-minute or package-install claim.
- [x] Visuals have alt text, captions, source commit, dates, sanitization, and rights/generation provenance.
- [x] Execution evidence cites successful Actions runs and does not fabricate output.
- [x] All ten productization requirements have evidence or a named blocker.
- [x] Protected GitHub metadata remains unchanged and is recorded as an owner gate.
- [x] No harness behavior, contract, source version, consumer, or canonical-status change is included.

## Verification
- `make verify`
- `make product`

## Stop Conditions
- Acceptance criteria pass and required remote checks complete.
- A required change falls outside declared scope.
- A change would alter behavior, security gates, releases, settings, consumers, governance, or canonical status.
- Evidence cannot be tied to an exact source, run, commit, or date.

## User Outcome Review
An unfamiliar-user clean-room workflow remains pending under pilot remediation Phase 3. This documentation adoption does not satisfy that external usability gate.

## Completion Notes
The branch documents the current source and renders only sanitized output from successful default-branch Governance run 29533739580 and Portable Repository Contract run 29533739561 at `22523bc78b7d65a4a90b9b01d08b681591fc662f`. Final merge and all protected settings or release decisions remain outside this ticket.