# Bounded pilot remediation plan

This plan starts from the [baseline](BASELINE.md). Each phase has a stop gate. Success permits an explicit decision; it never triggers automatic rollout.

## Phase 1 — Truthful and inspectable surface

Owner: repository maintainer
Risk: R1

- Add root agent guidance and a security disclosure policy.
- Mark the repository Lab-stage, unreleased, and non-canonical.
- Separate source-proven capabilities from unproven adoption and production claims.
- Add this baseline and the adoption contract.
- Add CODEOWNERS and dependency-update configuration.
- Pin third-party workflow actions to reviewed commit SHAs.
- Add CodeQL analysis with least-privilege workflow permissions.

Exit evidence:

- `make verify` passes.
- `make product` passes.
- Governance and Security workflows pass on the pilot branch.
- README, security policy, and pilot documents agree on maturity and release status.

Stop if the change requires repository settings, credentials, licensing, production access, or consumer-repository changes.

## Phase 2 — Security reconciliation

Owner: maintainer with private security context
Risk: R2/R3 when a finding or control change warrants it

- Rebase and re-verify the open hardening change against current `main`.
- Resolve duplicate artifact identifiers before merge.
- Remediate privately tracked findings and add regression tests.
- Review command execution, path handling, telemetry rendering, archive operations, and agent-controlled input boundaries.
- Enable platform secret scanning, push protection, and an appropriate default-branch ruleset only through a separately authorized settings change.
- Re-run current-tree and reachable-history scans.
- Confirm zero unresolved critical or high findings.

Exit evidence:

- opaque finding register shows no unresolved critical/high item;
- CodeQL analysis exists and actionable alerts are resolved or explicitly accepted;
- no suspicious high-confidence secret/history match;
- hardening changes pass all governance checks.

Stop before publishing exploit details, rotating credentials, changing settings without authority, or rewriting history.

## Phase 3 — Reproducibility and usability proof

Owner: an unfamiliar tester or clean-room agent

Use only the public README and a clean environment:

1. Identify prerequisites.
2. Run the primary local workflow.
3. Explain what the system does and does not do.
4. Exercise one positive and one negative governance path.
5. Attempt the documented adoption path in a disposable sample.
6. Record elapsed time, interventions, confusing claims, failures, and cleanup.

Required outputs:

- an immutable test environment description;
- command transcript with secrets and personal paths removed;
- pass/fail results;
- issue list and documentation corrections;
- verified recovery instructions.

Exit gate: the tester completes the primary workflow without private context and can explain limitations. A source-only demo does not count as successful cross-repository adoption.

## Phase 4 — Real learning round trip

- Observe one concrete issue in `vantage` or `Tycoon`.
- Classify it as local or general.
- For a general lesson, propose a harness change with a failing acceptance test.
- Verify it against both pilot product contracts.
- Make an explicit version decision.
- Open consumer update pull requests.
- Let each consumer's own checks and human decision determine acceptance.

Exit gate: one evidenced round trip completes without copying files manually or auto-merging a consumer change.

## Phase 5 — Retrospective and decision

Measure:

- maintainer effort;
- setup and update time per consumer;
- first-pass success and intervention rate;
- regressions or unintended constraints;
- local exceptions;
- security findings;
- documentation failures;
- value delivered to each product.

Choose exactly one outcome:

- continue toward a release proposal;
- revise the contracts and run another bounded pilot;
- keep the repository as a reference implementation;
- stop and retain only proven components.

Even a positive outcome does not authorize portfolio-wide rollout.

## Deferred settings and presentation work

The following are evidence-backed recommendations but are intentionally not performed by this branch:

- default-branch protection/ruleset;
- secret scanning and push protection;
- repository description, topics, homepage, and social preview;
- release or package publication;
- visibility or license changes;
- consumer-repository updates.

They require separate authorization because they change repository state, publication posture, or downstream behavior.
