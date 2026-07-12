# ADR-001: Use JSON for canonical governance data

- Status: Accepted
- Date: 2026-07-11

## Decision
Use JSON for trace and event schemas, JSON Lines for event streams, and Markdown for human contracts.

## Rationale
Python can validate JSON without dependencies; JSON is portable across CI systems; Markdown remains readable in code review.

## Consequences
Comments are not allowed in canonical data. Human rationale belongs in adjacent Markdown.
