# Metric Catalog

| ID | Metric | Definition | Guardrail |
| --- | --- | --- | --- |
| METRIC-001 | Trace coverage | traced PRD requirements / all PRD requirements | >= 95% |
| METRIC-002 | First-pass success | successful runs with zero retries / stopped runs | >= 80% |
| METRIC-003 | Human intervention rate | intervened stopped runs / stopped runs | trend down, review quality |
| METRIC-004 | Event completeness | runs with start, verification, and stop / started runs | >= 95% |
| METRIC-005 | Architecture violations | undeclared local imports found in CI | 0 |

Review outcome quality and regressions alongside speed and completion.
