"""Governance contract tests. TEST-001 and TEST-002."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from agentic_os.validation import validate_repository, validate_tickets, validate_trace


class ValidationTests(unittest.TestCase):
    def test_repository_is_valid_TEST_001(self) -> None:
        self.assertEqual([], validate_repository(ROOT))

    def test_broken_code_reference_fails_TEST_001(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns("__pycache__", "*.jsonl", "latest.md"))
            trace = copy / "docs/trace/traceability.json"
            data = json.loads(trace.read_text())
            data["records"][0]["code_ref"] = "src/missing.py"
            trace.write_text(json.dumps(data))
            self.assertTrue(any(issue.code == "TRACE_CODE" for issue in validate_trace(copy)))

    def test_incomplete_ticket_fails_TEST_002(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns("__pycache__", "*.jsonl", "latest.md"))
            ticket = copy / "docs/tickets/TICKET-001-bootstrap.md"
            ticket.write_text(ticket.read_text().replace("## Verification", "## Removed"))
            self.assertTrue(any(issue.code == "TICKET_SECTION" for issue in validate_tickets(copy)))


if __name__ == "__main__":
    unittest.main()
