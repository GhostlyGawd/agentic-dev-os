# Security policy

## Support status

Agentic Development Operating System is currently a **Lab-stage pilot candidate**. The repository contains a `1.1.0` source snapshot, but there is no tagged release or formally supported stable line.

| Version | Status |
| --- | --- |
| `main` | Best-effort security fixes during the pilot |
| Tagged releases | None published |

Do not treat the current source as a hardened production boundary for untrusted input.

## Reporting a vulnerability

Do not disclose suspected vulnerabilities in a public issue, discussion, pull request, or commit message.

1. Use GitHub's private vulnerability-reporting flow for this repository when it is available.
2. If that flow is unavailable, contact the repository owner through GitHub without exploit details and request a private channel.
3. Include affected version or commit, impact, minimum reproduction, and a proposed mitigation when possible.
4. Remove credentials, personal data, client data, and production data from evidence.

The maintainer will acknowledge a report when practicable, validate severity, coordinate a fix, and disclose only after remediation. No response-time SLA is promised during the Lab pilot.

## Security expectations

- Never commit secrets or raw production data.
- Use least-privilege credentials and disposable test data.
- Treat tickets, telemetry, repository content, and agent-generated instructions as untrusted input.
- Require explicit approval for production access, credential changes, destructive operations, or public disclosure.
- Run the repository's governance and security workflows before merging.
