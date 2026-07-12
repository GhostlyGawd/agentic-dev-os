# PRD: Product Strategy Integration

## Overview
Add an upstream product-decision layer without duplicating canonical delivery artifacts.

## Metadata
- ID: PRD-002
- Owner: Product and Platform
- Status: Accepted

## Parent Bet
- BET-001

## Originating Outcome
- O-001

## Originating Opportunity
- OP-001

## Problem
The governed operating system starts at PRDs and cannot enforce that work originates from measurable outcomes, evidenced problems, and validated bets.

## Users
Product and engineering teams coordinating AI-assisted delivery.

## User Stories
- As a product owner, I want every PRD to link to a validated bet so feature work cannot bypass discovery.
- As an engineer, I want one canonical delivery system so upstream context does not create conflicting truth.

## Goals
- Add complete product strategy, discovery, bet, milestone, change-request, review, memory, and command layers.
- Enforce the entire product chain locally and in CI.
- Generate compatibility requirement and trace views from canonical sources.

## Non-Goals
- Replace a hosted research repository.
- Publish externally or gather private user data automatically.
- Move canonical PRDs, specs, tickets, or decisions under `.ai/`.

## Requirements
- PRD-002-R01: Provide context, north-star, product brief, PR/FAQ, outcomes, guardrails, roadmap, and scorecard artifacts.
- PRD-002-R02: Provide evidenced opportunities, customer problems, assumptions, research, and experiments.
- PRD-002-R03: Require bets to link outcomes and opportunities and define success, kill, and advance criteria.
- PRD-002-R04: Require milestones and WBS entries to link bets, PRDs, exit criteria, and human reviews.
- PRD-002-R05: Govern scope changes through linked change requests and release decisions through review records.
- PRD-002-R06: Extend every delivery trace with outcome, opportunity, bet, milestone, change-request, and review references.
- PRD-002-R07: Generate requirements, acceptance criteria, and CSV trace views deterministically from canonical sources.
- PRD-002-R08: Provide portable orient, discover, bet, specify, plan, build, review, and close commands.
- PRD-002-R09: Emit product lifecycle telemetry and calculate product-chain health metrics.
- PRD-002-R10: Enforce positive, negative, and end-to-end product-chain behavior in local and remote CI.

## Success Metrics
- METRIC-012: 100% active PRD product-chain coverage.
- METRIC-013: 100% opportunity evidence coverage.
- METRIC-014: 100% active bets define validation criteria.
- METRIC-015: 100% completed milestones have human reviews.
- Full verification remains below two seconds locally.

## Constraints
All core validation and generation use the Python standard library.

## Dependencies
- PRD-001
- SPEC-001
- CR-001

## Risks
Duplicate truth, document ceremony, weak evidence, and generated-file drift.

## Open Questions
External research and publishing adapters remain deferred until destinations and credentials are explicitly selected.
