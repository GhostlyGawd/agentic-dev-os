# Finding: FINDING-001 — Synthetic demo hypothesis treated as market input

## Ticket
TICKET-003 (discovery intake). Observed during a Proofstack dogfood session on 2026-07-13, outside a governed loop; recorded here because the discovery is reusable.

## Observation
The accounting niche hypothesis handled while dogfooding Proofstack was not invented by the founder, independently researched, or discovered during the session. It is the `niche-finder` repository's hardcoded synthetic worked example (`seed.ts`), seeded with fictional evidence and founder-access claims. It briefly circulated in working discussion as if it were a real candidate before being identified.

## Evidence
- Founder dogfood report (2026-07-13): the hypothesis matches the seeded example in `seed.ts`, whose evidence and founder-access claims are fictional.
- No discovery record from the session produced or corroborated the hypothesis independently.

## Recurrence
Likely for every new user and every future dogfood cycle: seeded examples are the first content a user sees, and neither the product nor our process labeled them synthetic.

## User Impact
A founder could spend a full validate → experiment → productize cycle on fabricated market input — the exact failure Proofstack exists to prevent.

## Decision
Label the seeded example a "synthetic demo hypothesis" everywhere it is referenced; exclude synthetic records from all evidence and validation claims; require provenance at investigation promotion so origins stay attached (BET-002, EXP-002).

## Guardrail
- Type: Policy
- Reference: `.ai/strategy/guardrails.md` Must Not Happen — a synthetic or seeded demo record is counted as market validation; reinforced in `.ai/memory/pitfalls.md`, O-002 guardrail metrics, and the EXP-002 success threshold.

## Owner
Discovery owner (research).

## Status
Adopted
