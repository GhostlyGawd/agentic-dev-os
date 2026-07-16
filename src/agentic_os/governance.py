from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import load_config, load_json, write_json
from .telemetry import append_event, build_event

HEADINGS = ("Metadata", "Linked PRD", "Linked Spec", "Goal", "Scope", "Files Allowed", "Steps",
            "Acceptance Criteria", "Verification", "Stop Conditions", "User Outcome Review", "Completion Notes")


def section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def bullets(text: str, heading: str) -> list[str]:
    return [line[2:].strip() for line in section(text, heading).splitlines() if line.startswith("- ")]


def ticket_path(root: Path, ticket_id: str) -> Path | None:
    matches = list((root / "docs/tickets").glob(f"{ticket_id}-*.md")) + list((root / "docs/archive/tickets").glob(f"{ticket_id}-*.md"))
    return matches[0] if len(matches) == 1 else None


def ticket_contract(root: Path, ticket_id: str) -> dict[str, Any]:
    path = ticket_path(root, ticket_id)
    if not path:
        raise ValueError(f"unknown or ambiguous ticket: {ticket_id}")
    text = path.read_text(encoding="utf-8")
    missing = [heading for heading in HEADINGS if not section(text, heading)]
    if missing:
        raise ValueError(f"ticket missing sections: {', '.join(missing)}")
    risk_match = re.search(r"^- Risk:\s*(R[0-3])\s*$", section(text, "Metadata"), re.MULTILINE)
    status_match = re.search(r"^- Status:\s*(.+?)\s*$", section(text, "Metadata"), re.MULTILINE)
    return {
        "path": path, "text": text, "risk": risk_match.group(1) if risk_match else "",
        "status": status_match.group(1) if status_match else "", "allowed": bullets(text, "Files Allowed"),
        "verification": [item.strip("`") for item in bullets(text, "Verification")],
    }


def approval_path(root: Path, ticket_id: str) -> Path:
    return root / f"agent/approvals/{ticket_id}.json"


def grant_approval(root: Path, ticket_id: str, approver: str, reason: str, expires_at: str | None = None) -> dict[str, Any]:
    contract = ticket_contract(root, ticket_id)
    record = {"schema_version":"1.0", "ticket_id":ticket_id, "risk":contract["risk"], "approver":approver,
              "reason":reason, "granted_at":datetime.now(timezone.utc).isoformat(), "expires_at":expires_at,
              "ticket_digest":hashlib.sha256(contract["text"].encode()).hexdigest(), "status":"active"}
    write_json(approval_path(root, ticket_id), record)
    return record


def approval_valid(root: Path, ticket_id: str) -> bool:
    path = approval_path(root, ticket_id)
    if not path.exists():
        return False
    record = load_json(path)
    contract = ticket_contract(root, ticket_id)
    if record.get("status") != "active" or record.get("ticket_digest") != hashlib.sha256(contract["text"].encode()).hexdigest():
        return False
    expires = record.get("expires_at")
    return not expires or datetime.fromisoformat(expires) > datetime.now(timezone.utc)


def check_scope(root: Path, ticket_id: str, changed_files: list[str]) -> list[str]:
    allowed = [item.rstrip("/") for item in ticket_contract(root, ticket_id)["allowed"]]
    return [path for path in changed_files if not any(rule == "." or path == rule or path.startswith(rule + "/") for rule in allowed)]


def changed_files(root: Path, base: str = "HEAD") -> list[str]:
    result = subprocess.run(["git", "diff", "--name-only", base], cwd=root, text=True, capture_output=True, check=False)
    return [line for line in result.stdout.splitlines() if line]


class LoopManager:
    def __init__(self, root: Path):
        self.root = root
        self.config = load_config(root)
        self.events = root / self.config["event_file"]
        self.state_path = root / "observability/events/active-runs.json"

    def _state(self) -> dict[str, Any]:
        return load_json(self.state_path) if self.state_path.exists() else {}

    def _save(self, state: dict[str, Any]) -> None:
        write_json(self.state_path, state)

    def plan(self, ticket_id: str, actor: str) -> str:
        contract = ticket_contract(self.root, ticket_id)
        if contract["status"] not in {"Ready", "In Progress"}:
            raise ValueError("ticket must be Ready or In Progress")
        run_id = str(uuid.uuid4())
        append_event(self.events, build_event("loop.planned", run_id, ticket_id, actor, metadata={"allowed_files":contract["allowed"]}))
        return run_id

    def start(self, ticket_id: str, actor: str, run_id: str | None = None) -> str:
        contract = ticket_contract(self.root, ticket_id)
        if contract["status"] not in {"Ready", "In Progress"}:
            raise ValueError("ticket must be Ready or In Progress")
        if contract["risk"] in self.config["risk_approval_required"] and not approval_valid(self.root, ticket_id):
            raise ValueError(f"valid human approval required for {contract['risk']}")
        state = self._state()
        if state:
            raise ValueError("only one loop may be active in this checkout")
        run_id = run_id or str(uuid.uuid4())
        state[ticket_id] = {"run_id":run_id, "started_ns":time.monotonic_ns(), "retries":0,
                            "allowed":contract["allowed"], "verification":contract["verification"]}
        self._save(state)
        append_event(self.events, build_event("loop.started", run_id, ticket_id, actor, retry_count=0))
        return run_id

    def action(self, ticket_id: str, actor: str, action: str, paths: list[str]) -> None:
        state = self._state()
        if ticket_id not in state:
            raise ValueError("ticket has no active loop")
        violations = check_scope(self.root, ticket_id, paths)
        if violations:
            raise ValueError("paths outside ticket scope: " + ", ".join(violations))
        append_event(self.events, build_event("agent.action", state[ticket_id]["run_id"], ticket_id, actor,
                                              metadata={"action":action[:120], "paths":paths}))

    def retry(self, ticket_id: str, actor: str, reason: str) -> int:
        state = self._state()
        if ticket_id not in state:
            raise ValueError("ticket has no active loop")
        state[ticket_id]["retries"] += 1
        if state[ticket_id]["retries"] > self.config["max_retries"]:
            raise ValueError("retry limit exceeded; stop with handoff")
        self._save(state)
        append_event(self.events, build_event("loop.retried", state[ticket_id]["run_id"], ticket_id, actor,
                                              retry_count=state[ticket_id]["retries"], metadata={"reason":reason[:200]}))
        return state[ticket_id]["retries"]

    def verify(self, ticket_id: str, actor: str, execute: bool = True) -> bool:
        state = self._state()
        if ticket_id not in state:
            raise ValueError("ticket has no active loop")
        run = state[ticket_id]
        append_event(self.events, build_event("verification.started", run["run_id"], ticket_id, actor))
        passed = True
        results = []
        for command in run["verification"]:
            if not execute:
                results.append({"command":command, "returncode":0})
                continue
            result = subprocess.run(command, cwd=self.root, shell=True, text=True, capture_output=True, check=False)
            results.append({"command":command, "returncode":result.returncode})
            passed = passed and result.returncode == 0
        append_event(self.events, build_event("verification.completed", run["run_id"], ticket_id, actor,
                                              outcome="passed" if passed else "failed", metadata={"checks":results}))
        run["verified"] = passed
        self._save(state)
        return passed

    def stop(self, ticket_id: str, actor: str, outcome: str, cost_usd: float = 0.0,
             human_intervention: bool = False, regression: bool = False) -> str:
        state = self._state()
        if ticket_id not in state:
            raise ValueError("ticket has no active loop")
        run = state[ticket_id]
        if outcome == "success" and not run.get("verified"):
            raise ValueError("successful loop requires passing verification")
        if outcome == "success":
            contract = ticket_contract(self.root, ticket_id)
            if "Pending" in section(contract["text"], "Completion Notes") or "Pending" in section(contract["text"], "User Outcome Review"):
                raise ValueError("completion notes and user outcome review must be resolved")
        duration_ms = (time.monotonic_ns() - run["started_ns"]) // 1_000_000
        append_event(self.events, build_event("loop.stopped", run["run_id"], ticket_id, actor, outcome=outcome,
                                              duration_ms=duration_ms, retry_count=run["retries"], cost_usd=cost_usd,
                                              human_intervention=human_intervention, regression=regression))
        append_event(self.events, build_event("metric.summary", run["run_id"], ticket_id, actor, outcome=outcome,
                                              duration_ms=duration_ms, retry_count=run["retries"], cost_usd=cost_usd,
                                              human_intervention=human_intervention, regression=regression))
        del state[ticket_id]
        self._save(state)
        return run["run_id"]


def archive_ticket(root: Path, ticket_id: str, actor: str) -> Path:
    contract = ticket_contract(root, ticket_id)
    if contract["status"] not in {"Complete", "Cancelled"}:
        raise ValueError("only complete or cancelled tickets may be archived")
    destination = root / "docs/archive/tickets" / contract["path"].name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(contract["path"]), destination)
    append_event(root / load_config(root)["event_file"], build_event("artifact.archived", f"archive-{uuid.uuid4()}", ticket_id, actor,
                                                                      outcome="success", metadata={"path":str(destination.relative_to(root))}))
    return destination
