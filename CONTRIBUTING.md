# Contributing

Every behavioral change must have a ticket, an allowed file scope, acceptance criteria, verification, and a trace update. Run `make verify` before opening a pull request.

New product work must also link a measurable outcome, evidenced opportunity, validated bet, and milestone. Scope changes require an approved record under `docs/change-requests/`. Run `make product` after changing strategy, PRDs, specs, or trace data; generated files under `.ai/requirements/` must be committed but never edited manually.

## Pull request contract

- Link the ticket and requirement IDs.
- Link the outcome, opportunity, bet, and milestone IDs.
- Explain the user outcome, not only the implementation.
- Include tests or explain why the change is documentation-only.
- Update `docs/trace/traceability.json` in the same change.
- Record exceptions and high-risk approvals explicitly.

Do not commit secrets or raw production data to telemetry fixtures.
