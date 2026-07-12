from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EVENT_NAMES = {
    "prd.created", "prd.updated", "prd.status_changed", "spec.created", "spec.updated",
    "spec.status_changed", "ticket.created", "ticket.updated", "ticket.status_changed",
    "loop.planned", "loop.started", "loop.retried", "loop.stopped", "agent.action",
    "verification.started", "verification.completed", "test.completed", "ci.gate_completed",
    "dependency.violation", "human.reviewed", "human.intervened", "approval.granted",
    "approval.revoked", "trace.updated", "metric.summary", "alert.triggered",
    "artifact.archived", "reversal.completed", "finding.recorded", "guardrail.created",
    "growth.experiment_started", "growth.experiment_completed", "growth.conversion_recorded",
    "outcome.created", "outcome.updated", "opportunity.created", "opportunity.updated",
    "experiment.started", "experiment.completed", "bet.created", "bet.status_changed",
    "milestone.created", "milestone.reviewed", "change_request.created", "change_request.decided",
    "product_review.completed", "product_export.completed",
}
OUTCOMES = {"success", "failure", "handoff", "passed", "failed", "approved", "rejected", "cancelled"}
SENSITIVE = re.compile(r"token|secret|password|credential|authorization", re.IGNORECASE)


def _sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: "[REDACTED]" if SENSITIVE.search(key) else _sanitize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    return value


def build_event(event_name: str, run_id: str, ticket_id: str, actor: str = "agent", **fields: Any) -> dict[str, Any]:
    event = {
        "schema_version": "1.0", "event_name": event_name, "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(), "run_id": run_id,
        "ticket_id": ticket_id, "actor": actor,
    }
    event.update({key: _sanitize(value) for key, value in fields.items() if value is not None})
    validate_event(event)
    return event


def validate_event(event: dict[str, Any]) -> None:
    required = {"schema_version", "event_name", "event_id", "timestamp", "run_id", "ticket_id", "actor"}
    missing = required - event.keys()
    if missing:
        raise ValueError(f"missing event fields: {', '.join(sorted(missing))}")
    if event["schema_version"] != "1.0" or event["event_name"] not in EVENT_NAMES:
        raise ValueError("unsupported schema version or event name")
    if event["ticket_id"] != "SYSTEM" and not re.fullmatch(r"TICKET-\d{3,}", str(event["ticket_id"])):
        raise ValueError("ticket_id must be SYSTEM or TICKET-NNN")
    if event.get("outcome") not in OUTCOMES | {None}:
        raise ValueError("unsupported outcome")
    for key in ("duration_ms", "retry_count", "cost_usd", "tests_passed", "tests_failed", "architecture_violations"):
        if key in event and (not isinstance(event[key], (int, float)) or event[key] < 0):
            raise ValueError(f"{key} must be non-negative")
    if _sanitize(event) != event:
        raise ValueError("event contains sensitive metadata keys")


def append_event(path: Path, event: dict[str, Any]) -> None:
    validate_event(event)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def read_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
            validate_event(event)
            events.append(event)
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValueError(f"invalid event at line {number}: {exc}") from exc
    return events
