#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agentic_os.telemetry import append_event, build_event, read_events, render_report, summarize
from agentic_os.validation import validate_repository

EVENTS = ROOT / "observability/events/loops.jsonl"
RUN_STATE = ROOT / "observability/events/active-runs.json"


def active_runs() -> dict[str, dict[str, object]]:
    if not RUN_STATE.exists():
        return {}
    return json.loads(RUN_STATE.read_text(encoding="utf-8"))


def save_runs(runs: dict[str, dict[str, object]]) -> None:
    RUN_STATE.parent.mkdir(parents=True, exist_ok=True)
    RUN_STATE.write_text(json.dumps(runs, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def ticket_exists(ticket: str) -> bool:
    return any(ticket in path.name for path in (ROOT / "docs/tickets").glob("TICKET-*.md"))


def cmd_validate(args: argparse.Namespace) -> int:
    issues = validate_repository(ROOT)
    try:
        read_events(EVENTS)
    except ValueError as exc:
        from agentic_os.validation import Issue
        issues.append(Issue("EVENT_INVALID", str(exc), str(EVENTS.relative_to(ROOT))))
    if args.json:
        print(json.dumps({"valid": not issues, "issues": [item.as_dict() for item in issues]}, indent=2))
    elif issues:
        for item in issues:
            print(f"ERROR {item.code}: {item.message} [{item.path}]")
    else:
        print("Repository governance is valid.")
    return 1 if issues else 0


def cmd_start(args: argparse.Namespace) -> int:
    if not ticket_exists(args.ticket):
        print(f"Unknown ticket: {args.ticket}", file=sys.stderr)
        return 2
    runs = active_runs()
    if args.ticket in runs:
        print(f"Ticket already has an active run: {runs[args.ticket]['run_id']}", file=sys.stderr)
        return 2
    run_id = args.run_id or str(uuid.uuid4())
    runs[args.ticket] = {"run_id": run_id, "started_monotonic": time.monotonic_ns(), "retries": 0}
    save_runs(runs)
    append_event(EVENTS, build_event("loop.started", run_id, args.ticket, actor=args.actor, retry_count=0))
    print(run_id)
    return 0


def cmd_retry(args: argparse.Namespace) -> int:
    runs = active_runs()
    if args.ticket not in runs:
        print(f"No active run for {args.ticket}", file=sys.stderr)
        return 2
    state = runs[args.ticket]
    state["retries"] = int(state.get("retries", 0)) + 1
    if state["retries"] > 3:
        print("Retry limit exceeded; stop with handoff.", file=sys.stderr)
        return 2
    save_runs(runs)
    append_event(EVENTS, build_event("loop.retried", str(state["run_id"]), args.ticket, actor=args.actor,
                                     retry_count=state["retries"], metadata={"reason": args.reason[:200]}))
    print(f"Retry {state['retries']} recorded.")
    return 0


def cmd_stop(args: argparse.Namespace) -> int:
    runs = active_runs()
    if args.ticket not in runs:
        print(f"No active run for {args.ticket}", file=sys.stderr)
        return 2
    state = runs.pop(args.ticket)
    duration_ms = max(0, (time.monotonic_ns() - int(state["started_monotonic"])) // 1_000_000)
    verification = "passed" if args.outcome == "success" else "failed"
    append_event(EVENTS, build_event("verification.completed", str(state["run_id"]), args.ticket,
                                     actor=args.actor, outcome=verification, duration_ms=duration_ms))
    append_event(EVENTS, build_event("loop.stopped", str(state["run_id"]), args.ticket,
                                     actor=args.actor, outcome=args.outcome, duration_ms=duration_ms,
                                     retry_count=int(state.get("retries", 0)), human_intervention=args.human_intervention))
    save_runs(runs)
    print(f"Run {state['run_id']} stopped: {args.outcome}")
    return 0


def cmd_metrics(_: argparse.Namespace) -> int:
    report = render_report(summarize(read_events(EVENTS)))
    target = ROOT / "docs/metrics/latest.md"
    target.write_text(report, encoding="utf-8")
    print(target.relative_to(ROOT))
    return 0


def cmd_new_ticket(args: argparse.Namespace) -> int:
    if not args.id.startswith("TICKET-") or not args.id[7:].isdigit():
        print("Ticket ID must look like TICKET-002", file=sys.stderr)
        return 2
    target = ROOT / f"docs/tickets/{args.id}-{args.title.lower().replace(' ', '-')}.md"
    if target.exists():
        print(f"Already exists: {target.relative_to(ROOT)}", file=sys.stderr)
        return 2
    text = (ROOT / "docs/tickets/TEMPLATE.md").read_text(encoding="utf-8")
    text = text.replace("TICKET-NNN", args.id).replace("<Title>", args.title)
    target.write_text(text, encoding="utf-8")
    print(target.relative_to(ROOT))
    return 0


def cmd_demo(_: argparse.Namespace) -> int:
    EVENTS.unlink(missing_ok=True)
    RUN_STATE.unlink(missing_ok=True)
    run_id = "demo-" + uuid.uuid4().hex[:12]
    append_event(EVENTS, build_event("loop.started", run_id, "TICKET-001", actor="demo", retry_count=0))
    append_event(EVENTS, build_event("verification.completed", run_id, "TICKET-001", actor="demo", outcome="passed", duration_ms=1250))
    append_event(EVENTS, build_event("loop.stopped", run_id, "TICKET-001", actor="demo", outcome="success", duration_ms=1300, retry_count=0, human_intervention=False))
    cmd_metrics(argparse.Namespace())
    print("Demo complete: one successful governed loop, 100% event completeness.")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Agentic Development OS governance CLI")
    sub = root.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="validate repository governance")
    validate.add_argument("--json", action="store_true")
    validate.set_defaults(func=cmd_validate)
    start = sub.add_parser("loop-start", help="start a governed ticket loop")
    start.add_argument("--ticket", required=True); start.add_argument("--run-id"); start.add_argument("--actor", default=os.getenv("USER", "agent")); start.set_defaults(func=cmd_start)
    retry = sub.add_parser("loop-retry", help="record an active loop retry")
    retry.add_argument("--ticket", required=True); retry.add_argument("--reason", required=True); retry.add_argument("--actor", default=os.getenv("USER", "agent")); retry.set_defaults(func=cmd_retry)
    stop = sub.add_parser("loop-stop", help="verify and stop a governed loop")
    stop.add_argument("--ticket", required=True); stop.add_argument("--outcome", choices=("success", "failure", "handoff"), required=True); stop.add_argument("--human-intervention", action="store_true"); stop.add_argument("--actor", default=os.getenv("USER", "agent")); stop.set_defaults(func=cmd_stop)
    metrics = sub.add_parser("metrics", help="aggregate loop events"); metrics.set_defaults(func=cmd_metrics)
    ticket = sub.add_parser("new-ticket", help="create a ticket from the template")
    ticket.add_argument("--id", required=True); ticket.add_argument("--title", required=True); ticket.set_defaults(func=cmd_new_ticket)
    demo = sub.add_parser("demo", help="run an end-to-end example"); demo.set_defaults(func=cmd_demo)
    return root


if __name__ == "__main__":
    arguments = parser().parse_args()
    raise SystemExit(arguments.func(arguments))
