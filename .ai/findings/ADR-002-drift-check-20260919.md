# ADR-002 Allowlist Drift Check — 2026-09-19

## Finding

**Drift Confirmed**: Tickets in the repository reference verification commands that are NOT allowlisted in `ado.config.json`, violating ADR-002's requirement that all verification commands must use an allowlisted program.

## Evidence

### ADR-002 Requirement
From `docs/decisions/ADR-002-shell-free-verification.md`:
> "Verification bullets are limited to `make <target>`-style commands unless the allowlist is deliberately extended in `ado.config.json`, which is a governed config change."

### Current Allowlist
`ado.config.json` line 7:
```json
"verification_allowed_commands": ["make"]
```

### Tickets Using Non-Allowlisted Commands

1. **TICKET-002-product-strategy-integration.md** (Files Allowed covers this ticket):
   - Uses: `python scripts/ados.py product validate`
   - Uses: `python scripts/ados.py product export --check`
   - Program `python` NOT in allowlist

2. **TICKET-003-proofstack-pre-hypothesis-dogfood-discovery.md**:
   - Uses: `python3 scripts/ados.py product validate`
   - Uses: `python3 scripts/ados.py product export --check`
   - Program `python3` NOT in allowlist

3. **TICKET-008-sync-superseded-donor-status.md** (Related to portfolio governance):
   - Uses: `python ../repo-audit/codex/skills/portfolio-governance/scripts/portfolio_context.py GhostlyGawd/agentic-dev-os`
   - Program `python` NOT in allowlist

## Governance

**TICKET-004** (`docs/tickets/TICKET-004-pilot-professionalization.md`) covers both:
- `docs/decisions/ADR-002-shell-free-verification.md` (Files Allowed line 11)
- `ado.config.json` (Files Allowed line 7)
- `src/agentic_os/governance.py` (Files Allowed line 17)

## Verification

- `make verify` passes (33 tests, no failures)
- Tests include verification allowlist enforcement (`test_verification_commands_must_be_allowlisted`, `test_malicious_ticket_verification_cannot_start_or_verify`)
- **However**: Tests use a temporary fixture config; they do not validate against actual tickets in the repository

## Recommendation

Extend `ado.config.json` to include `python` and `python3` as allowlisted programs in `verification_allowed_commands`, OR revise the affected tickets to use `make`-based verification targets instead.
