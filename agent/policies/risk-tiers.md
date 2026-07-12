# Risk and Approval Policy

| Tier | Examples | Execution rule |
| --- | --- | --- |
| R0 | Read-only inspection, local analysis | Autonomous |
| R1 | Reversible, bounded code or docs change | Autonomous after ticket validation |
| R2 | Cross-module API, dependency, data migration, material cost | Human approval before execution |
| R3 | Production, secrets, security controls, deletion, external communication | Explicit human approval at action time |

Unknown risk defaults to the next higher tier. Approval does not expand ticket scope. Emergency exceptions require a decision record and follow-up guardrail.
