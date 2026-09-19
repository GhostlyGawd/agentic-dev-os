# Loop Execution Contract

## Preconditions

- One valid ticket with linked PRD and spec.
- A valid outcome → opportunity → validated bet → PRD product chain.
- Explicit `Files Allowed`, acceptance criteria, verification, owner, and risk tier.
- Human approval when required by the risk tier.

## Procedure

1. Emit `loop.planned` (during planning phase).
2. Emit `loop.started` (when execution begins).
3. Inspect the allowed scope and plan the smallest change.
4. Emit `agent.action` for each significant action with paths taken.
5. Implement without leaving scope.
6. Emit `verification.started`, then run ticket verification and `make verify`.
7. Emit `verification.completed` (mandatory; indicates pass/fail outcome).
8. Update trace status, findings, and completion notes.
9. Emit `loop.stopped` with outcome (`success`, `failure`, or `handoff`).
10. Emit `metric.summary` (recorded alongside `loop.stopped`).

Retries must emit `loop.retried` with a non-sensitive reason. Stop after three retries and hand off unless the ticket explicitly sets a lower limit.

## Event Completeness

A run is considered complete when all four lifecycle events are present:
- `loop.started` — marks loop entry and permitted file scope
- `verification.completed` — outcome of all ticket verification checks
- `loop.stopped` — final outcome and metrics (duration, cost, intervention, regression)
- `metric.summary` — summary metrics for aggregation
