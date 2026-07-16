# Pilot baseline and truth audit

Snapshot date: 2026-07-16  
Repository: `GhostlyGawd/agentic-dev-os`  
Default branch: `main`  
Audited default SHA: `aef53865f839190c4efa8b335510044c28c66776`

This is an evidence snapshot for a bounded pilot. It does not declare this repository canonical and does not authorize portfolio rollout.

## Classification

| Field | Pilot classification | Evidence |
| --- | --- | --- |
| Portfolio role | Candidate shared Agentic Development Harness | Governance runtime, agent policies, templates, CI, metrics, and trace model are present |
| Maturity | Lab | No tagged release, package, external usability proof, or supported version line |
| Investment tier | Supported pilot candidate | Selected for active pilot evaluation, not flagship treatment |
| Visibility intent | Public engineering product | Repository is public and contains reusable code and documentation |
| Data class | Public code and synthetic/project documentation | No production dataset or credential file is expected |
| Canonical status | Not canonical | Adoption contract and portfolio charter require evidence and an explicit decision |

## Repository state

- Five branches were inspected.
- Thirteen commits are reachable from the branch heads.
- The default history contains six commits.
- There are no tags or releases.
- The latest `main` Governance run passed.
- One draft hardening pull request is open and must be reconciled with current `main` before any merge.
- `main` is not protected.
- Repository description, topics, and homepage are unset.
- GitHub Discussions and Issues are enabled.
- The project declares Python 3.11+ and has no declared runtime dependencies.

## Security baseline

The current trees and reachable branch history were inspected remotely without cloning the product repository. A high-confidence scan covered 222 unique blobs across all reachable commits for private keys, common provider tokens, credential-bearing URLs, credential assignments, suspicious credential filenames, and user-specific Windows paths. No high-confidence match was found.

That negative result is evidence, not a guarantee. The following platform gaps remain:

- GitHub secret scanning and push protection are disabled.
- Code scanning has not produced an analysis.
- Actions currently permits all actions and does not require SHA pinning.
- The Governance workflow references mutable action tags.
- The default branch has no protection rule.
- A code-level security review has unresolved privately tracked findings; public artifacts must use opaque identifiers only.
- Dependabot security updates are enabled and the open alert list was empty at the snapshot.

Publication/security status: **not yet cleared for Stable or release promotion**.

## Product truth

| Claim or capability | Evidence | Current truth |
| --- | --- | --- |
| Governance validation | Source, tests, and successful GitHub Actions runs | Shipped in the source snapshot |
| Product-to-delivery trace model | PRDs, specs, tickets, trace data, validators, and generated views | Shipped in the source snapshot |
| Metrics and static dashboard | Source, tests, and committed synthetic output | Shipped for local/synthetic evidence |
| No runtime dependencies | `pyproject.toml` and imports | True for the current Python source |
| Five-minute use | Two-command README quick start | Plausible for a prepared Unix-like environment, not independently proven |
| Cross-repository adoption | Guidance documents only | Not proven; there is no installer, migration tool, or consumer compatibility test |
| Versioned shared harness | `pyproject.toml` says `1.1.0` | Source version only; no tag, release, package, or update channel |
| Production readiness | No production evidence | Not claimed |
| Portfolio-wide standard | Pilot selection only | Not authorized |

## Principal gaps

1. The implementation is broad, but its primary user workflow is not packaged or externally tested.
2. Documentation mixes implemented framework behavior with future adoption ambition.
3. Security automation and branch controls are incomplete.
4. No release artifact establishes a stable, reproducible consumer boundary.
5. No real learning has completed the required product → harness → version → consumer-update round trip.
6. Existing branches and hardening work need reconciliation before a release decision.
7. Discovery metadata is absent.

## Baseline decision

Continue the bounded pilot, but keep the repository at **Lab** maturity and **not canonical**. The next decision must be based on the gates in [REMEDIATION_PLAN.md](REMEDIATION_PLAN.md), not on implementation volume or documentation completeness alone.
