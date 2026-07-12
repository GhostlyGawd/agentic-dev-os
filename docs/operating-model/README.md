# Operating Model

`owners.json` is the machine-readable accountability contract. Owners review their artifacts at least quarterly and after any incident. The product owner validates real user outcomes outside the harness. The risk reviewer owns R2/R3 approvals and exception expiry. The trace steward closes broken links; the CI owner maintains enforcement; the metrics owner reviews alerts without optimizing throughput at the expense of quality.

## Exception path

Ambiguous, cross-cutting, product-critical, security-sensitive, costly, or irreversible work exits the normal loop. Create a decision record, raise the risk tier, obtain approval bound to the ticket digest, and return to shadow mode when required. Exceptions must name an owner, rationale, expiry, rollback, and follow-up guardrail.
