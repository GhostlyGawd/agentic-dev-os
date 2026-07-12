# AI Product Operating Layer

This directory holds product strategy and discovery context that sits upstream of the governed delivery system.

## Order of work

1. Orient from context and strategy.
2. Define a measurable outcome.
3. Discover evidenced opportunities.
4. Validate a bounded bet.
5. Create a PRD and milestone only after the bet advances.
6. Execute through canonical specs and tickets under `docs/`.
7. Review the user outcome and close or iterate.

## Canonical boundaries

- `.ai/` owns context, strategy, discovery, bets, milestones, commands, and conventions.
- `docs/prd/`, `docs/specs/`, `docs/tickets/`, and `docs/decisions/` remain canonical delivery records.
- `docs/trace/traceability.json` is the only editable trace source.
- `.ai/requirements/*` files are generated compatibility views; do not edit them manually.
- `agent/` owns enforceable agent behavior and risk policy.

Run `python scripts/ados.py product validate` before planning and `python scripts/ados.py product export` after trace changes.
