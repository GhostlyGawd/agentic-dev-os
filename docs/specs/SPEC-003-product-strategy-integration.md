# Spec: Product Strategy Integration

## Metadata
- ID: SPEC-003
- PRD: PRD-002
- Owner: Product and Platform
- Status: Accepted

## Summary
Add Markdown product artifacts, machine validation, deterministic exports, lifecycle telemetry, health metrics, and CI gates above the existing delivery system.

## Architecture
`src/agentic_os/product.py` owns product-chain parsing, validation, metrics, and exports. `.ai/` owns upstream context. Delivery truth remains under `docs/`. The general validator composes product validation and trace validation.

## Public Interfaces
- `ados.py product validate`
- `ados.py product export`
- `ados.py product metrics`
- `ados.py product gate --prd PRD-NNN`

## Data Model
Stable references use O-NNN, OP-NNN, EXP-NNN, BET-NNN, M-NNN, CR-NNN, REVIEW-NNN, PRD-NNN, SPEC-NNN, and TICKET-NNN. Trace records store the upstream references directly.

## Workflow
Orient → discover → experiment → bet → PRD → milestone → spec/ticket → build → review → close.

## Edge Cases
- Orphan outcomes, opportunities, bets, PRDs, milestones, and reviews fail validation.
- Generated views with manual drift fail deterministic comparison.
- Null change requests are allowed for unchanged scope.
- Proposed bets cannot authorize a PRD.

## Security and Privacy
Research files must not contain credentials or unredacted private production data. External adapters remain outside the autonomous core.

## Non-Goals
Hosted databases, automatic research ingestion, and external publishing.

## Acceptance Criteria
- SPEC-003-A01: All required context and strategy artifacts validate.
- SPEC-003-A02: Opportunities require outcomes and evidence.
- SPEC-003-A03: Bets require valid upstream links and validation criteria.
- SPEC-003-A04: Milestones require valid bets, PRDs, exits, and review records.
- SPEC-003-A05: Approved scope changes and review decisions validate.
- SPEC-003-A06: Trace records require and resolve all upstream references.
- SPEC-003-A07: Generated views are deterministic and marked non-canonical.
- SPEC-003-A08: Eight product workflow command guides exist and validate.
- SPEC-003-A09: Product metrics and lifecycle events are supported.
- SPEC-003-A10: CI and end-to-end tests reject broken chains and generated drift.

## Test Plan
TEST-019 through TEST-028 cover product validation, exports, metrics, gates, and full integration.

## Telemetry
Outcome, opportunity, experiment, bet, milestone, change-request, review, and product-export lifecycle events are catalogued.

## Rollout and Rollback
Begin in shadow mode. Rollback removes the `.ai/` composition gate while preserving delivery artifacts; generated views can be recreated at any time.

## Traceability
- PRD-002-R01 through PRD-002-R10 map one-to-one to SPEC-003-A01 through SPEC-003-A10.
