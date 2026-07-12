# ADR-002: Verification commands run as allowlisted argv, never through a shell

- Status: Accepted
- Date: 2026-07-12

## Decision
`loop verify` executes ticket Verification bullets as argv lists whose program must appear in `verification_allowed_commands` (default: `make`) and whose arguments must be plain words. Governance code never passes repository-authored strings to a shell.

## Rationale
Ticket files are agent-authored input, so running their bullets through `shell=True` made every ticket author a code-execution principal (2026-07-12 security audit, finding F1). An argv allowlist keeps verification reproducible while removing chaining, redirection, and substitution.

## Consequences
Verification bullets are limited to `make <target>`-style commands unless the allowlist is deliberately extended in `ado.config.json`, which is a governed config change. Complex verification belongs in Makefile targets, where it is code-reviewed rather than smuggled through ticket text.
