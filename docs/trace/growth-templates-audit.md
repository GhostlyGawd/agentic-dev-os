# Growth Templates Audit — 2026-09-19

## Finding

All template files in `docs/growth/templates/` are **stub/placeholder files with only section headers and no real copy-ready content**:

1. `docs/growth/templates/case-study.md` — 10 section headers, no content
2. `docs/growth/templates/content-brief.md` — 12 section headers, no content
3. `docs/growth/templates/launch-post.md` — 7 section headers, no content
4. `docs/growth/templates/weekly-review.md` — 8 section headers, no content
5. `docs/growth/templates/community-post.md` — 6 section headers, no content
6. `docs/growth/templates/seo-brief.md` — 8 section headers, no content
7. `docs/growth/templates/experiment.md` — 14 section headers, no content

## Requirement Gap

MASTER.md § "Required growth system" explicitly mandates:
> Define audience, pain, hypothesis, positioning, messaging, organic channels, **content**, community, product-led sharing, SEO, conversion path, staged launch, adoption metrics, failure modes, weekly cadence, experiments, and **copy-ready templates**.

These templates violate that requirement — they are scaffolds only, not reusable copy-ready assets.

## Ticket Scope

TICKET-001 "Bootstrap governance runtime" (Status: Complete) covers these files through its Files Allowed entry for `docs/`.

## Verification Status

`make verify` passes (33 tests OK) — the audit is structural, not caught by current validation tests.

## Recommendation

Either:
1. Populate templates with actual copy-ready examples and guidance, or
2. Mark this as a Known Limitation in a separate ticket for future work (growth template population).
