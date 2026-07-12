# Contributing

Every behavioral change must have a ticket, an allowed file scope, acceptance criteria, verification, and a trace update. Run `make verify` before opening a pull request.

## Pull request contract

- Link the ticket and requirement IDs.
- Explain the user outcome, not only the implementation.
- Include tests or explain why the change is documentation-only.
- Update `docs/trace/traceability.json` in the same change.
- Record exceptions and high-risk approvals explicitly.

Do not commit secrets or raw production data to telemetry fixtures.
