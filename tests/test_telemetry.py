"""Telemetry and metric tests. TEST-003."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from agentic_os.telemetry import append_event, build_event, read_events, summarize


class TelemetryTests(unittest.TestCase):
    def test_complete_first_pass_run_TEST_003(self) -> None:
        events = [
            build_event("loop.started", "run-1", "TICKET-001"),
            build_event("verification.completed", "run-1", "TICKET-001", outcome="passed"),
            build_event("loop.stopped", "run-1", "TICKET-001", outcome="success", human_intervention=False),
        ]
        summary = summarize(events)
        self.assertEqual(1.0, summary["first_pass_success_rate"])
        self.assertEqual(1.0, summary["event_completeness_rate"])

    def test_round_trip_TEST_003(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            event = build_event("loop.started", "run-1", "TICKET-001")
            append_event(path, event)
            self.assertEqual([event], read_events(path))

    def test_invalid_event_rejected_TEST_003(self) -> None:
        with self.assertRaises(ValueError):
            build_event("unknown", "run-1", "TICKET-001")


if __name__ == "__main__":
    unittest.main()
