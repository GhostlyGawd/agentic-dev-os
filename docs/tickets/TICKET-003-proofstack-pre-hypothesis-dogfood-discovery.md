# Ticket: TICKET-003 — Proofstack dogfood learnings and adoption handoff

## Metadata
- Owner: Discovery and Product
- Risk: R1
- Status: Complete

## Linked PRD
- PRD-002-R02
- PRD-002-R03

## Linked Spec
- SPEC-003-A01
- SPEC-003-A02
- SPEC-003-A03

## Goal
Record the operating-system-level learnings from the first Proofstack dogfood cycle — the synthetic-demo-hypothesis failure converted into a guardrail (FINDING-001) — and hand the Proofstack product chain itself to the `niche-finder` repository, which adopted this operating system.

## Scope
OS-level guardrail, memory, glossary, roadmap, finding, and ticket documentation only. The Proofstack product chain (its outcomes, opportunities, experiments, and bets) lives in `niche-finder` under its own `.ai/` layer and is out of scope here. No PRD, milestone, spec, source-code, or trace changes. Tracked as dogfood issue #5.

## Files Allowed
- .ai/context/glossary.md
- .ai/memory/pitfalls.md
- .ai/strategy/guardrails.md
- .ai/strategy/roadmap.md
- docs/findings/FINDING-001-synthetic-demo-hypothesis.md
- docs/tickets/TICKET-003-proofstack-pre-hypothesis-dogfood-discovery.md

## Steps
- Convert the synthetic-demo-hypothesis failure into FINDING-001 with a policy guardrail.
- Add the guardrail to Must Not Happen and the pitfall to memory.
- Add Proofstack, dogfood issue, and synthetic demo hypothesis to the glossary.
- Point the roadmap at the adoption dogfood: the OS installed into `niche-finder`, which carries the product chain.

## Acceptance Criteria
- [x] `make verify` passes with this repository's strategy layer self-describing (no second-product outcomes).
- [x] FINDING-001 exists with a policy guardrail referenced from `.ai/strategy/guardrails.md`.
- [x] The Proofstack chain exists in `niche-finder` (its O-001 → OP-001 → EXP-001 → BET-001), not here.
- [x] Every reference to the seeded accounting example is labeled synthetic demo hypothesis.

## Verification
- `python3 scripts/ados.py product validate`
- `python3 scripts/ados.py product export --check`
- `make verify`

## Stop Conditions
- Any change would require a new outcome, PRD, milestone, or trace record in this repository.
- Any file outside the allowed list needs modification.
- Risk exceeds R1.

## User Outcome Review
Reviewed against the founder's placement decision (2026-07-13): each governed repository carries its own product chain, so this repository stays self-describing while `niche-finder` (Proofstack) runs its own O-001 → OP-001 → EXP-001 → BET-001 chain on the adopted runtime. The reusable evidence-integrity learning stays here as FINDING-001 and its guardrail. Tracked as dogfood issue #5.

## Completion Notes
Converted the synthetic-demo-hypothesis failure into FINDING-001 with a Must Not Happen guardrail, pitfall, and glossary entries, and pointed the roadmap at the adoption dogfood. The Proofstack product chain was handed to the `niche-finder` repository (its TICKET-001), which installed this operating system. No PRD, milestone, outcome, or trace record was created here.
