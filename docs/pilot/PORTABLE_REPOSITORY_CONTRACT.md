# Portable repository contract

This reusable workflow is the first shared-harness proposal derived from evidence in more than one pilot product. Both products contained machine-local configuration that would make a public checkout misleading or non-portable.

The workflow is deliberately small. It does not install the harness, modify the caller, inspect credentials, or upload repository content.

## Contract

The caller must commit `portfolio-profile.json` with:

- `schema_version`
- `repository`
- `purpose`
- `family`
- `maturity`
- `visibility_intent`
- `owner`
- `lineage`
- `data_class`
- `harness_ref`

The validation job also scans tracked text files for loopback hostnames, a common machine-local proxy marker, and user-specific absolute home paths. Binary files, files larger than 2 MB, the workflow implementation itself, and explicit contract fixtures are excluded.

Output contains only opaque rule IDs and `PASS` or `FAIL`. It never prints matched content, file paths, profile values, or surrounding lines.

## Consumer call

After this pull request is merged, a consumer may add a small caller workflow:

```yaml
name: Portfolio contract

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  portable-contract:
    uses: GhostlyGawd/agentic-dev-os/.github/workflows/portable-repository-contract.yml@<40-character-merge-sha>
```

Replace the placeholder with the immutable merge commit SHA. Do not use `main`, a moving tag, or an unreleased version label.

GitHub checks out the caller repository. The reusable workflow runs read-only, uses the standard library available on the GitHub-hosted runner, and has only `contents: read` permission. It does not copy a harness directory into the consumer.

## Verification model

The workflow runs directly on changes to its own implementation or profile, in addition to supporting `workflow_call`. Every run:

1. self-tests the three portability detectors using synthetic values assembled at runtime;
2. validates this repository's positive profile;
3. scans tracked text without emitting matched content;
4. exits nonzero if any opaque rule fails.

Consumer repositories remain responsible for their own domain, security, build, and product checks. Passing this contract proves only the small profile and portability boundary.

## Learning status

- Product evidence: observed in two distinct pilot products.
- General classification: accepted as a candidate cross-repository contract.
- Harness implementation and acceptance run: this workflow.
- Consumer update pull requests: required next.
- Version/release decision: not made.

The learning round trip is not complete until consumer checks pass and humans decide whether to accept their update pull requests.
