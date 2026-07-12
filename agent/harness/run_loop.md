# Loop Execution Contract

## Preconditions

- One valid ticket with linked PRD and spec.
- Explicit `Files Allowed`, acceptance criteria, verification, owner, and risk tier.
- Human approval when required by the risk tier.

## Procedure

1. Emit `loop.started`.
2. Inspect the allowed scope and plan the smallest change.
3. Implement without leaving scope.
4. Run ticket verification and `make verify`.
5. Emit `verification.completed`.
6. Update trace status, findings, and completion notes.
7. Emit `loop.stopped` with `success`, `failure`, or `handoff`.

Retries must emit `loop.retried` with a non-sensitive reason. Stop after three retries and hand off unless the ticket explicitly sets a lower limit.
