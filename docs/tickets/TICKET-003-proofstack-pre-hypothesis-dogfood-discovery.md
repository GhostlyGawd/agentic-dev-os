# Ticket: TICKET-003 — Proofstack pre-hypothesis dogfood discovery

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
Record the Proofstack pre-hypothesis funnel gap found while dogfooding as an evidenced discovery chain (O-002, OP-002, EXP-002, BET-002) with the seeded accounting example labeled a synthetic demo hypothesis, without advancing any unvalidated bet into delivery.

## Scope
Discovery, strategy, memory, finding, and ticket documentation only. No PRD, milestone, spec, source-code, or trace changes; no implementation in the `niche-finder` repository. Tracked as dogfood issue #5.

## Files Allowed
- .ai/bets/BET-002-proofstack-pre-hypothesis-funnel.md
- .ai/context/glossary.md
- .ai/discovery/assumptions.md
- .ai/discovery/customer-problems.md
- .ai/discovery/experiments/EXP-002.md
- .ai/discovery/opportunity-tree.md
- .ai/discovery/research-notes.md
- .ai/memory/pitfalls.md
- .ai/strategy/desired-outcomes.md
- .ai/strategy/guardrails.md
- .ai/strategy/outcome-scorecard.md
- .ai/strategy/roadmap.md
- .ai/wbs.md
- docs/findings/FINDING-001-synthetic-demo-hypothesis.md
- docs/tickets/TICKET-003-proofstack-pre-hypothesis-dogfood-discovery.md

## Steps
- Capture dogfood observations and label the seeded accounting example a synthetic demo hypothesis (FINDING-001).
- Define O-002 with metric, baseline, target, horizon, and guardrail metrics.
- Record OP-002 with cited evidence and update the opportunity tree.
- Add assumptions A-004 to A-006 and dogfood experiment EXP-002 with Result pending.
- Draft BET-002 as Proposed with success, kill, and advance criteria.
- Update roadmap, scorecard, WBS, glossary, pitfalls, and guardrails to match.

## Acceptance Criteria
- [x] `python scripts/ados.py product validate` passes with the new chain.
- [x] BET-002 status is Proposed and no new PRD, milestone, or trace record exists.
- [x] Every reference to the seeded accounting example is labeled synthetic demo hypothesis.
- [x] `make verify` passes.

## Verification
- `python3 scripts/ados.py product validate`
- `python3 scripts/ados.py product export --check`
- `make verify`

## Stop Conditions
- Any change would require a new PRD, milestone, or trace record; that work is gated on BET-002 validation.
- Any file outside the allowed list needs modification.
- Risk exceeds R1.

## User Outcome Review
Reviewed against the 2026-07-13 dogfood session: the recorded gap matches observed usage (investigations require supplied hypotheses; discovery happens outside the product), and the chain preserves evidence integrity by keeping BET-002 unvalidated and the seeded accounting example labeled a synthetic demo hypothesis. Tracked as dogfood issue #5.

## Completion Notes
Recorded the O-002 → OP-002 → EXP-002 → BET-002 (Proposed) discovery chain, FINDING-001, and matching strategy, memory, WBS, glossary, and guardrail updates. Delivery remains gated on EXP-002 evidence per the bet's advance criteria; no PRD, milestone, or trace record was created.
