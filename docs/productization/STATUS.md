# Productization status

Evaluation date: 2026-07-18
Repository snapshot: `GhostlyGawd/agentic-dev-os@8c053b2be85c5e69f65c6e37f2368e9e476e64c7`
Portfolio standard: `ghostlygawd-portfolio-productization` v1.1.0 from `GhostlyGawd/repo-audit@4a711143844186282c4b5833eac3ce6eae33fcf6`
Reviewed profile: `archived`
Governance: superseded, Lab, maintenance-only, governance-donor-to-recursive-harness

This repository-local assessment mirrors the merged central decision. It does
not change live GitHub archive or visibility settings, publish a release, or
authorize consumer rollout. Recursive Harness is the canonical successor.

## Requirement evidence

| Requirement | Evaluation | Current evidence and boundary |
| --- | --- | --- |
| Clear README proposition, audience, and status | Pass | README leads with the superseded date, maintenance-only expectation, preserved purpose, and canonical successor before setup. |
| Setup and working example | Pass for current-source verification | Prerequisites and `make verify` / `make product` are backed by GitHub-hosted Ubuntu/Python 3.11. `make demo` is explicitly synthetic. No clean-room or five-minute claim is made. |
| Real screenshots, diagrams, or demos | Pass | README has an original system map and sanitized rendering of actual Actions output with source commit, dates, alt text, captions, and provenance. Mermaid diagrams provide text-renderable workflow fallbacks. |
| Architecture and limitations | Pass | `docs/ARCHITECTURE.md` covers components, data flow, trust boundaries, unsupported cases, recovery, and rollback. |
| Security and privacy boundaries | Pass for the Lab surface | `SECURITY.md`, `agent/policies/data-handling.md`, and architecture cover credentials, untrusted input, telemetry, external services, vulnerability reporting, and non-production boundaries. |
| License and provenance | Blocked for release-grade clearance | MIT is declared and assets/references are registered, but incorporated-code ownership and third-party-rights review is not recorded complete. Public status is not treated as proof. |
| Contributing and support guidance | Pass | README limits support to historical/security maintenance; `SUPPORT.md` retains vulnerability and no-SLA expectations. |
| Accurate releases and version claims | Pass | README, AGENTS, SECURITY, and pilot docs agree: source `1.1.0`, zero tags/releases/packages, no stable line, immutable commit evaluation required. |
| GitHub description, topics, homepage, and social preview | Blocked on owner-authorized settings | Live metadata was unset. This branch does not modify protected GitHub settings; suggested values appear below. |
| Natural SEO language without keyword stuffing | Pass | README naturally describes AI agent development, repository-native governance, requirements traceability, bounded agent loops, Python validation, and intended users. |

## Verified execution receipt

- [Governance run 29533739580](https://github.com/GhostlyGawd/agentic-dev-os/actions/runs/29533739580): success; `make verify` reported complete repository governance, 33 passing tests, and all gates passed; `make product` reported a valid product chain and current views.
- [Portable Repository Contract run 29533739561](https://github.com/GhostlyGawd/agentic-dev-os/actions/runs/29533739561): success; `ADO-PORT-001` through `ADO-PORT-006` and the overall contract reported `PASS`.
- [Security run 29533739587](https://github.com/GhostlyGawd/agentic-dev-os/actions/runs/29533739587): success; CodeQL completed.

These are preserved 2026-07-16 receipts for the older
`22523bc78b7d65a4a90b9b01d08b681591fc662f` assessment. They prove only the
named checks on that commit, not current support, clean-room usability,
cross-repository compatibility, production safety, or customer value.

## Suggested GitHub metadata — not applied

For a separate owner-authorized settings change:

- **Description:** Superseded governance reference and capability donor to Recursive Harness.
- **Topics:** `ai-agents`, `developer-tools`, `governance`, `requirements-traceability`, `python`, `software-delivery`, `agentic-workflows`
- **Homepage:** Leave unset until an accurate maintained documentation or demo URL exists.
- **Social preview:** Export a rights-cleared PNG from `docs/assets/agentic-dev-os-system-map.svg` and review it against current behavior before applying it.

## Historical gates and current disposition

1. An unfamiliar tester completes the primary workflow from public documentation and records environment, transcript, elapsed time, interventions, and recovery.
2. The owner records release-grade incorporated-code and third-party-rights review.
3. A reusable learning completes acceptance testing, validation in two unlike consumers, an explicit version decision, and separately accepted consumer PRs.
4. Critical/high security findings and platform controls are reviewed through private and owner-authorized processes.
5. The 2026-07-18 portfolio decision chose to retain this repository as a
   superseded reference and route future capabilities to Recursive Harness.

The remaining historical gates do not block preservation. Any future proposal
to reactivate or release this repository would require a new central governance
decision; capability work proceeds in Recursive Harness instead.
