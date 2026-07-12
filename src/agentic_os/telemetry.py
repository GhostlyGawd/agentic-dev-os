from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALLOWED_EVENTS = {"loop.started", "loop.retried", "verification.completed", "loop.stopped", "human.intervened"}
ALLOWED_OUTCOMES = {"success", "failure", "handoff", "passed", "failed"}


def build_event(event_name: str, run_id: str, ticket_id: str, actor: str = "agent", **fields: Any) -> dict[str, Any]:
    event = {
        "schema_version": "1.0", "event_name": event_name,
        "event_id": str(uuid.uuid4()), "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id, "ticket_id": ticket_id, "actor": actor,
    }
    event.update({key: value for key, value in fields.items() if value is not None})
    validate_event(event)
    return event


def validate_event(event: dict[str, Any]) -> None:
    required = {"schema_version", "event_name", "event_id", "timestamp", "run_id", "ticket_id", "actor"}
    missing = required - event.keys()
    if missing:
        raise ValueError(f"missing event fields: {', '.join(sorted(missing))}")
    if event["schema_version"] != "1.0":
        raise ValueError("unsupported schema_version")
    if event["event_name"] not in ALLOWED_EVENTS:
        raise ValueError(f"unsupported event_name: {event['event_name']}")
    if not str(event["ticket_id"]).startswith("TICKET-"):
        raise ValueError("ticket_id must start with TICKET-")
    if event.get("outcome") not in ALLOWED_OUTCOMES | {None}:
        raise ValueError("unsupported outcome")
    for key in ("duration_ms", "retry_count", "cost_usd"):
        if key in event and event[key] < 0:
            raise ValueError(f"{key} cannot be negative")


def append_event(path: Path, event: dict[str, Any]) -> None:
    validate_event(event)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def read_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events = []
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


def summarize(events: list[dict[str, Any]]) -> dict[str, float | int]:
    runs: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        runs.setdefault(event["run_id"], []).append(event)
    started = {run for run, items in runs.items() if any(x["event_name"] == "loop.started" for x in items)}
    stopped = {run for run, items in runs.items() if any(x["event_name"] == "loop.stopped" for x in items)}
    successful = {run for run, items in runs.items() if any(x["event_name"] == "loop.stopped" and x.get("outcome") == "success" for x in items)}
    first_pass = {run for run in successful if not any(x["event_name"] == "loop.retried" for x in runs[run])}
    complete = {run for run in started if {"loop.started", "verification.completed", "loop.stopped"}.issubset({x["event_name"] for x in runs[run]})}
    intervened = {run for run in stopped if any(x.get("human_intervention") or x["event_name"] == "human.intervened" for x in runs[run])}
    return {
        "runs_started": len(started), "runs_stopped": len(stopped), "successful_runs": len(successful),
        "first_pass_success_rate": len(first_pass) / len(stopped) if stopped else 0.0,
        "human_intervention_rate": len(intervened) / len(stopped) if stopped else 0.0,
        "event_completeness_rate": len(complete) / len(started) if started else 0.0,
        "retry_events": sum(1 for event in events if event["event_name"] == "loop.retried"),
    }


def render_report(summary: dict[str, float | int]) -> str:
    return f"""# Agentic Delivery Metrics\n\nGenerated from the local event stream.\n\n| Metric | Value |\n| --- | ---: |\n| Runs started | {summary['runs_started']} |\n| Runs stopped | {summary['runs_stopped']} |\n| Successful runs | {summary['successful_runs']} |\n| First-pass success | {summary['first_pass_success_rate']:.1%} |\n| Human intervention | {summary['human_intervention_rate']:.1%} |\n| Event completeness | {summary['event_completeness_rate']:.1%} |\n| Retry events | {summary['retry_events']} |\n\nReview these with regression and user-outcome evidence before optimizing throughput.\n"""
