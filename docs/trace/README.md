# Traceability

`traceability.json` is canonical. A record is complete only when every reference resolves from outcome, opportunity, bet, and milestone through PRD, spec, ticket, code, test, event, metric, review, and completion. `python scripts/ados.py validate` enforces this contract.

`.ai/requirements/traceability.csv` is a generated compatibility view. Regenerate it with `python scripts/ados.py product export`; never edit it directly.

Statuses: `Planned`, `In Progress`, `Blocked`, `Complete`, `Archived`.
