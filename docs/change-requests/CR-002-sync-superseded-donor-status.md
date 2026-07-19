# Change Request: CR-002 — Synchronize the superseded donor status

## Metadata
- ID: CR-002
- Owner: GhostlyGawd
- Status: Approved
- Risk: R1

## Request
Synchronize this repository's local governance mirror and user-facing status
with the merged portfolio decision that selected Recursive Harness as the
canonical harness target.

## Reason
`GhostlyGawd/repo-audit@4a711143844186282c4b5833eac3ce6eae33fcf6`
classifies Agentic Dev OS as a superseded, maintenance-only capability donor.
The current local profile, AGENTS guidance, README, and productization status
still describe an active supported candidate and now contradict the
authoritative registry.

## Impact
- Scope: Governance mirror and status documentation only.
- Timeline: One bounded pull request after the central decision merged.
- Cost: No runtime or dependency change.
- Risk: Historical evidence could be accidentally rewritten or live GitHub
  archival could be implied.
- Dependencies: Merged `GhostlyGawd/repo-audit#12` and
  `GhostlyGawd/recursive-harness#243`.

## Linked Artifacts
- Outcome: O-001
- Opportunity: OP-001
- Bet: BET-001
- PRD: PRD-001
- Requirements: PRD-001-R01, PRD-001-R15

## Decision
Approved

## Approval
The owner approved consolidating Agentic Dev OS capability gaps into Recursive
Harness, then merged the paired canonicalization and governance pull requests
on 2026-07-18.

## Notes
This change does not archive the live GitHub repository, change visibility or
settings, move code, or alter historical execution receipts. It only makes the
local product surfaces tell the merged governance truth.
