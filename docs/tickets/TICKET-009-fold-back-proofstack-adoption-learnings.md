# Ticket: TICKET-009 — Fold back Proofstack adoption learnings

## Metadata
- Owner: Founder (GhostlyGawd)
- Implementer: Claude
- Risk: R1
- Status: In Review
- Branch: `claude/report-status-ul2edz`

## Linked PRD
- PRD-001-R15

## Linked Spec
- SPEC-001-A15

## Goal
Land the adoption-dogfood fold-back from the Proofstack (niche-finder) funnel delivery: the lint-exclusion fix the roadmap named, the FINDING-002 record of the remaining adaptation frictions, and the roadmap's dogfood-closeout state.

## Scope
Maintenance-only documentation and one guarded lint change, consistent with this repository's superseded, maintenance-only posture. No behavior beyond the exclusion set changes.

## Files Allowed
- ci/lint.py
- docs/findings/FINDING-002-ts-repo-adaptation-frictions.md
- docs/tickets/TICKET-009-fold-back-proofstack-adoption-learnings.md
- .ai/strategy/roadmap.md

## Steps
- Extend the `ci/lint.py` exclusion set with non-Python vendored and generated directories.
- Record FINDING-002 with the three adaptation frictions and their dispositions.
- Update the roadmap Now/Next/Notes to the dogfood-closeout state.
- Run the full verification gates.

## Acceptance Criteria
- [x] `ci/lint.py` skips `node_modules`, `dist`, `coverage`, and `data`.
- [x] FINDING-002 records all three frictions with owner and status.
- [x] The roadmap reflects the issue #5 closeout state and the fold-back note.
- [x] `make verify` passes.

## Verification
- `make verify`

## Stop Conditions
- Acceptance criteria pass.
- A required change falls outside scope.
- Risk exceeds the declared tier.

## User Outcome Review
Covered by the dogfood issue #5 thread; the founder's standing authorization of 2026-08-14 covers the merge.

## Completion Notes
Delivered on `claude/report-status-ul2edz`; pending merge.
