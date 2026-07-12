# Product Strategy Integration

## Purpose

The `.ai/` product layer prevents delivery from becoming self-consistent but disconnected from customer value. It is upstream of the existing governed execution system and does not replace it.

## Canonical source map

| Truth | Canonical location | Generated or supporting view |
| --- | --- | --- |
| Context and constraints | `.ai/context/` | Agent orientation summaries |
| Outcomes and guardrails | `.ai/strategy/` | Outcome scorecard |
| Opportunities and evidence | `.ai/discovery/` | Experiments |
| Product hypotheses | `.ai/bets/` | Roadmap references |
| Reviewable increments | `.ai/milestones/` | WBS |
| Product requirements | `docs/prd/` | `.ai/requirements/requirements.md` |
| Acceptance contracts | `docs/specs/` | `.ai/requirements/acceptance-criteria.md` |
| Architecture decisions | `docs/decisions/` | Linked ADR references |
| Executable work | `docs/tickets/` | Backlog or status reports |
| Scope changes | `docs/change-requests/` | Trace references |
| Human outcome decisions | `docs/review/` | Release readiness |
| Trace relationships | `docs/trace/traceability.json` | `.ai/requirements/traceability.csv` |
| Durable learnings | `docs/findings/` | `.ai/memory/` conventions and pitfalls |

## Enforced lifecycle

1. Orient from context and strategy.
2. Define an outcome with a metric, baseline, target, horizon, and guardrails.
3. Record an opportunity with evidence and assumptions.
4. Run the smallest useful experiment.
5. Advance a bet only with success, kill, and advance criteria.
6. Create a PRD from the validated bet.
7. Plan a milestone, spec, and bounded tickets.
8. Route scope changes through an approved change request.
9. Execute and verify through the existing governed loop.
10. Record human milestone and release reviews.
11. Measure the outcome, capture findings, and close or iterate.

## Compatibility views

The files under `.ai/requirements/` are deterministic exports. They exist for tools or people that prefer consolidated Markdown or CSV, but they are not writable truth. CI fails if they drift from PRDs, specs, or canonical trace JSON.

## Adoption

Use shadow mode first: teams create the upstream links while humans continue making existing decisions. Graduate to enforced PRD gates after current work has valid ancestry and the product-chain metrics remain at 100% without unacceptable process friction.
