# Finding: FINDING-002 — Adoption frictions when the OS governs a non-Python repository

## Ticket
Dogfood issue GhostlyGawd/agentic-dev-os#5; observed while delivering PRD-001/M-001 in GhostlyGawd/niche-finder (branch `claude/pre-hypothesis-funnel`).

## Observation
Three framework assumptions surfaced as friction when the operating system governed a TypeScript product repository:

1. `ci/lint.py` walked vendored and generated directories (`node_modules`, `dist`, `coverage`, `data`) because its exclusion set only covered Python conventions.
2. The trace validator resolves `test_ref` exclusively against `tests/test_*.py`, so vitest suites cannot carry trace identifiers directly; niche-finder bridged this with a `tests/test_funnel_trace.py` file that pins TEST ids to named vitest tests.
3. `product validate` compares a bet's whole `## Status` section against the literal `Validated`, so any status prose breaks the validated-bet check; the contract is undocumented in the template.

## Evidence
`GhostlyGawd/niche-finder` `.ai/memory/implementation-notes.md` (2026-07-13 and 2026-08-14 entries) and the delivery commits on `claude/pre-hypothesis-funnel`.

## Recurrence
Every non-Python repository that adopts the OS will hit items 1 and 2; item 3 hits any bet whose status carries an explanation. Confirmed twice in one adoption (governance install and funnel delivery).

## User Impact
Adopters pay a local-adaptation tax and the framework forks silently — the exact failure mode the portfolio's donor lineage is meant to avoid.

## Decision
This repository is superseded and maintenance-only, so the fix here is minimal and documentary: the `ci/lint.py` exclusion set is extended in place (the roadmap's named first candidate), and items 2 and 3 are recorded for the successor harness — test-corpus patterns and status parsing should be configurable per repository (e.g. via `ado.config.json`) rather than convention-bound.

## Guardrail
- Type: Policy
- Reference: `ci/lint.py` exclusion set; successor-harness requirement recorded here and in niche-finder's implementation notes.

## Owner
Founder (GhostlyGawd)

## Status
Lint exclusions fixed in place; items 2 and 3 open as successor-harness requirements.
