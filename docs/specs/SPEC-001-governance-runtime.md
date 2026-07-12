# Spec: Governance Runtime

## Metadata
- ID: SPEC-001
- PRD: PRD-001
- Owner: Platform
- Status: Accepted

## Summary
A dependency-free CLI validates governed artifacts, writes structured events, aggregates metrics, and scaffolds tickets.

## Architecture
`scripts/ados.py` is the interface. Reusable validation and telemetry logic lives in `src/agentic_os`. Canonical trace data is JSON so agents and CI can modify it without third-party parsers.

## Public Interfaces
- `ados.py validate [--json]`
- `ados.py loop-start --ticket ID`
- `ados.py loop-retry --ticket ID --reason TEXT`
- `ados.py loop-stop --ticket ID --outcome OUTCOME`
- `ados.py metrics`
- `ados.py new-ticket --id ID --title TITLE`
- `ados.py demo`

## Data Model
Trace rows contain requirement, spec, ticket, code, test, metric, status, and version. Events contain schema version, event name, event ID, timestamp, run ID, ticket ID, actor, outcome, duration, intervention, cost, retry count, and metadata.

## Acceptance Criteria
- SPEC-001-A01: Invalid or missing trace targets fail validation.
- SPEC-001-A02: Incomplete ticket contracts fail validation.
- SPEC-001-A03: Valid loop events append as JSON Lines.
- SPEC-001-A04: Metric reports aggregate completed runs.
- SPEC-001-A05: Architecture tests reject undeclared local imports.

## Test Plan
TEST-001 covers traces; TEST-002 covers tickets; TEST-003 covers events and metrics; TEST-004 covers architecture.

## Telemetry
METRIC-001 through METRIC-005 are defined in `docs/metrics/catalog.md`.

## Rollout and Rollback
Adopt in shadow mode, then enable enforcement per repository. Rollback is removal of the CI workflow; repository artifacts remain readable.

## Traceability
- PRD-001-R01 -> SPEC-001-A01 -> TICKET-001 -> TEST-001 -> METRIC-001
- PRD-001-R02 -> SPEC-001-A02 -> TICKET-001 -> TEST-002 -> METRIC-001
- PRD-001-R03 -> SPEC-001-A03 -> TICKET-001 -> TEST-003 -> METRIC-004
- PRD-001-R04 -> SPEC-001-A05 -> TICKET-001 -> TEST-004 -> METRIC-005
