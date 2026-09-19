# Ticket: TICKET-010 — Remove unused growth experiment lifecycle events

## Metadata
- Owner: Founder (GhostlyGawd)
- Implementer: Claude
- Risk: R1
- Status: Proposed
- Branch: `swarm/draft-ticket-growth-events`

## Linked PRD
- PRD-001-R15

## Linked Spec
- SPEC-001-A15

## Goal
Remove the declared but unused "growth.experiment_started" and "growth.experiment_completed" events from the telemetry EVENT_NAMES catalog to reduce noise and clarify that experiment lifecycle tracking is not yet implemented.

## Scope
Maintenance-only removal of two unused event declarations. The growth.py module currently emits only "growth.conversion_recorded" for conversion funnel tracking; experiment-level lifecycle tracking is not yet implemented and should be added in a future feature ticket if needed. This ticket establishes the accurate state of the telemetry contract.

## Files Allowed
- src/agentic_os/telemetry.py
- docs/tickets/TICKET-010-remove-unused-growth-events.md

## Steps
- Remove "growth.experiment_started" and "growth.experiment_completed" from EVENT_NAMES in telemetry.py.
- Run the full verification gates.

## Acceptance Criteria
- [ ] "growth.experiment_started" is removed from telemetry.py EVENT_NAMES.
- [ ] "growth.experiment_completed" is removed from telemetry.py EVENT_NAMES.
- [ ] `make verify` passes.
- [ ] No other growth.py or telemetry.py behavior changes.

## Verification
- `make verify`

## Stop Conditions
- Acceptance criteria pass.
- A required change falls outside scope.
- Risk exceeds the declared tier.

## User Outcome Review
Pending product validation on whether experiment lifecycle tracking should be a future feature.

## Completion Notes
Pending.
