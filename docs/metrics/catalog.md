# Metric Catalog

| ID | Metric | Definition | Guardrail |
| --- | --- | --- | --- |
| METRIC-001 | Task completion | successful stopped runs / started runs | baseline, then improve |
| METRIC-002 | First-pass success | successful zero-retry runs / stopped runs | >= 80% |
| METRIC-003 | Human intervention | intervened stopped runs / stopped runs | review with outcome quality |
| METRIC-004 | Retry depth | retry count / stopped runs | investigate sustained increases |
| METRIC-005 | Cost per success | total recorded cost / successful runs | baseline by work class |
| METRIC-006 | Lead time | total run duration / stopped runs | detect harness friction |
| METRIC-007 | Spec adherence | passed verifications / verifications | >= 95% |
| METRIC-008 | Traceability coverage | traced requirements / PRD requirements | >= 95% |
| METRIC-009 | Regression rate | regressed stopped runs / stopped runs | <= 5% |
| METRIC-010 | Architecture violations | recorded boundary violations | 0 |
| METRIC-011 | Event completeness | runs with start, verification, stop, and summary / starts | >= 95% |
| METRIC-012 | Product-chain coverage | PRDs linked to valid bet, opportunity, and outcome / active PRDs | 100% |
| METRIC-013 | Opportunity evidence coverage | opportunities with recorded evidence / opportunities | 100% |
| METRIC-014 | Validated bet rate | bets with success, kill, and advance criteria / bets | 100% |
| METRIC-015 | Milestone review coverage | completed milestones with human review / completed milestones | 100% |

Interpret metrics together. High retry depth signals ambiguous work; high intervention signals weak self-sufficiency; low trace coverage signals broken intent; architecture violations signal unenforced boundaries; and lead-time growth signals excessive harness friction.
