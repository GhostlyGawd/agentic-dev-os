# Exceptions and Harness Audits

Normal loops stop when scope, risk, or context becomes uncertain. An exception requires an ADR containing owner, risk, approval, expiry, rollback, and user-outcome review. New behavior begins in shadow mode. Quarterly harness audits review stale rules, friction, bypasses, false-positive alerts, metric gaming, permissions, and user feedback. Repeated failures must produce a test, policy, metric, or approval gate and a `guardrail.created` event.
