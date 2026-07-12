# Spec: Adoption and Governance Rollout

## Metadata
- ID: SPEC-002
- PRD: PRD-001
- Owner: Platform
- Status: Accepted

## Stages

1. Baseline: measure current lead time, retries, regressions, and intervention.
2. Shadow: agents propose plans and scopes; humans approve and execute.
3. Guarded: R0/R1 work executes automatically; R2/R3 stays gated.
4. Optimized: tune templates and checks using observed failures.

## Graduation gates

- Trace coverage is at least 95%.
- Required-event coverage is at least 95%.
- First-pass success is stable for four weeks.
- No unresolved high-severity policy incident exists.
- A human owner accepts the next stage.

## Rollback

Any material security, data, or user-outcome failure returns the affected work class to shadow mode until a guardrail is added and verified.
