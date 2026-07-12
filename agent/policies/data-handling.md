# Data Handling Policy

- Never place secrets, credentials, tokens, personal data, or production payloads in prompts, events, fixtures, or findings.
- Emit stable identifiers and aggregate values, not raw user content.
- Redact sensitive tool output before persistence.
- Agents receive the minimum file, tool, and network access required by the ticket.
- Security-sensitive changes are R3 and require explicit review.
