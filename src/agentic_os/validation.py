from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

REQUIREMENT = re.compile(r"\bPRD-\d{3,}-R\d{2,}\b")
SPEC = re.compile(r"\bSPEC-\d{3,}-A\d{2,}\b")
TICKET = re.compile(r"\bTICKET-\d{3,}\b")
TEST = re.compile(r"\bTEST-\d{3,}\b")
METRIC = re.compile(r"\bMETRIC-\d{3,}\b")
REQUIRED_TICKET_SECTIONS = (
    "## Metadata", "## Linked PRD", "## Linked Spec", "## Goal", "## Scope",
    "## Files Allowed", "## Acceptance Criteria", "## Verification",
    "## Stop Conditions", "## Completion Notes",
)


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    path: str = ""

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message, "path": self.path}


def _texts(paths: list[Path]) -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def validate_structure(root: Path) -> list[Issue]:
    required = [
        "README.md", "agent/AGENTS.md", "architecture.json", "docs/prd",
        "docs/specs", "docs/tickets", "docs/trace/traceability.json",
        "observability/schema/event.schema.json", "scripts/ados.py", "tests",
    ]
    return [Issue("STRUCTURE_MISSING", f"Required path is missing: {item}", item)
            for item in required if not (root / item).exists()]


def validate_tickets(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for path in sorted((root / "docs/tickets").glob("TICKET-*.md")):
        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_TICKET_SECTIONS:
            if section not in text:
                issues.append(Issue("TICKET_SECTION", f"Missing section: {section}", str(path.relative_to(root))))
        if not REQUIREMENT.search(text):
            issues.append(Issue("TICKET_PRD", "Ticket has no requirement link", str(path.relative_to(root))))
        if not SPEC.search(text):
            issues.append(Issue("TICKET_SPEC", "Ticket has no spec acceptance link", str(path.relative_to(root))))
        files = _section_lines(text, "Files Allowed")
        if not files:
            issues.append(Issue("TICKET_SCOPE", "Files Allowed must contain at least one path", str(path.relative_to(root))))
    return issues


def _section_lines(text: str, heading: str) -> list[str]:
    match = re.search(rf"^## {re.escape(heading)}\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
    if not match:
        return []
    return [line[2:].strip() for line in match.group(1).splitlines() if line.startswith("- ")]


def validate_trace(root: Path) -> list[Issue]:
    path = root / "docs/trace/traceability.json"
    if not path.exists():
        return [Issue("TRACE_MISSING", "Traceability file is missing", str(path.relative_to(root)))]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [Issue("TRACE_JSON", str(exc), str(path.relative_to(root)))]
    issues: list[Issue] = []
    records = payload.get("records", [])
    if not isinstance(records, list) or not records:
        return [Issue("TRACE_EMPTY", "Traceability records must be a non-empty list", str(path.relative_to(root)))]
    prd_text = _texts(list((root / "docs/prd").glob("PRD-*.md")))
    spec_text = _texts(list((root / "docs/specs").glob("SPEC-*.md")))
    ticket_text = _texts(list((root / "docs/tickets").glob("TICKET-*.md")))
    test_text = _texts(list((root / "tests").glob("test_*.py")))
    metric_text = _texts(list((root / "docs/metrics").glob("*.md")))
    required = {"requirement_id", "requirement", "spec_ref", "ticket_ref", "code_ref", "test_ref", "metric_ref", "status", "version"}
    seen: set[str] = set()
    for index, record in enumerate(records):
        label = f"record[{index}]"
        missing = required - set(record)
        if missing:
            issues.append(Issue("TRACE_FIELDS", f"{label} missing: {', '.join(sorted(missing))}", str(path.relative_to(root))))
            continue
        req = record["requirement_id"]
        if req in seen:
            issues.append(Issue("TRACE_DUPLICATE", f"Duplicate requirement: {req}", str(path.relative_to(root))))
        seen.add(req)
        checks = ((req, prd_text, "requirement"), (record["spec_ref"], spec_text, "spec"),
                  (record["ticket_ref"], ticket_text, "ticket"), (record["test_ref"], test_text, "test"),
                  (record["metric_ref"], metric_text, "metric"))
        for reference, corpus, kind in checks:
            if reference not in corpus:
                issues.append(Issue("TRACE_TARGET", f"Unknown {kind} reference: {reference}", str(path.relative_to(root))))
        code_path = root / record["code_ref"]
        if not code_path.exists():
            issues.append(Issue("TRACE_CODE", f"Code path does not exist: {record['code_ref']}", str(path.relative_to(root))))
    all_requirements = set(REQUIREMENT.findall(prd_text))
    for requirement in sorted(all_requirements - seen):
        issues.append(Issue("TRACE_COVERAGE", f"Untraced requirement: {requirement}", str(path.relative_to(root))))
    return issues


def validate_repository(root: Path) -> list[Issue]:
    return validate_structure(root) + validate_tickets(root) + validate_trace(root)
