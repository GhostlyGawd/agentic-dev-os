# Provenance and asset register

This document makes the current repository's licensing, source lineage, references, synthetic evidence, and documentation assets reviewable. It is an evidence record, not a legal ownership opinion.

## Repository license

The repository declares the MIT License in [LICENSE](../LICENSE), and `pyproject.toml` repeats that declaration for the Python source snapshot. The core declares no required runtime dependencies.

A public repository and license file do not prove ownership of every incorporated contribution. Before a formal release or redistribution claim, the owner should review commit authorship, imported code, contribution authority, and third-party notices. That owner/legal review is not recorded as complete.

## Portfolio lineage

`portfolio-profile.json` records `agentic-system`, `agentic-engineering`, and `agentic-engineering-max` as reviewed governance predecessors. This explains design lineage; it is not proof that code was copied. Durable classification remains owned by `GhostlyGawd/repo-audit`.

## External references and automation

- `docs/references/sources.md` links background reading. Those sources are not vendored or runtime dependencies and remain under their owners' terms.
- Workflows invoke third-party actions pinned to immutable SHAs. GitHub fetches them at workflow time; they remain governed by their repositories and licenses.
- No external font, stock image, icon set, customer dataset, or model-generated bitmap appears in the productization assets below.

## Evidence and media register

| Asset | Purpose | Source and date | Rights and generation provenance |
| --- | --- | --- | --- |
| `docs/assets/agentic-dev-os-system-map.svg` | Static system explanation | Architecture at `22523bc78b7d65a4a90b9b01d08b681591fc662f`; created 2026-07-17 | Original vector documentation; system fonts only; no external media or generative-image model |
| `docs/assets/governance-ci-evidence.svg` | Terminal-style rendering of verified output | Actions runs `29533739580` and `29533739561`; captured 2026-07-16, rendered 2026-07-17 | Original layout; sanitized repository CI log text; no fabricated result or external media |
| `observability/reports/dashboard.html` | Generated framework dashboard | Repository event fixtures and metric generator | Synthetic evidence; not production or customer data |

README alt text and captions accompany both SVGs. SVG is the static fallback; no motion-only media is required.

## Synthetic and private data

Demo events, metrics, and examples are synthetic unless explicitly evidenced otherwise. Synthetic data must not be described as customer validation, market proof, or production behavior. Credentials, personal paths, client data, production data, and private research must not appear in source, telemetry, examples, captures, or generated assets.

## Release blocker

Release-grade incorporated-code ownership and third-party-rights review remains an owner decision. Until it is recorded, the source can state its declared MIT license but must not claim formal provenance clearance.