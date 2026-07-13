# Finding: FINDING-001 — Synthetic demo hypothesis treated as market input

## Ticket
TICKET-003 (dogfood learning intake). Observed during a Proofstack dogfood session on 2026-07-13, outside a governed loop; recorded here because the discovery is reusable across products governed by this operating system.

## Observation
The accounting niche hypothesis handled while dogfooding Proofstack was not invented by the founder, independently researched, or discovered during the session. It is the `niche-finder` repository's hardcoded synthetic worked example (`src/server/seed.ts`), seeded with fictional quotes and founder-access claims. It briefly circulated in working discussion as if it were a real candidate before being identified.

## Evidence
- Founder dogfood report (2026-07-13), later verified against the source: the hypothesis matches the seeded example in `src/server/seed.ts`, whose quotes and founder-access claims are fictional.
- No discovery record from the session produced or corroborated the hypothesis independently.

## Recurrence
Likely for every new user and every future dogfood cycle of any seeded product: seeded examples are the first content a user sees, and nothing labeled them synthetic.

## User Impact
A founder could spend a full validate → experiment → productize cycle on fabricated market input — the exact failure the affected product exists to prevent.

## Decision
Label seeded examples "synthetic demo hypothesis" everywhere they are referenced; exclude synthetic records from all evidence and validation claims; require provenance when a hypothesis is promoted into an investigation. The product-side enforcement lives in the `niche-finder` repository (its guardrails, O-001 guardrail metrics, and the EXP-001 success threshold of its BET-001 chain).

## Guardrail
- Type: Policy
- Reference: `.ai/strategy/guardrails.md` Must Not Happen — a synthetic or seeded demo record is counted as market validation; reinforced in `.ai/memory/pitfalls.md` and mirrored in the `niche-finder` repository's guardrails.

## Owner
Discovery owner (research).

## Status
Adopted
