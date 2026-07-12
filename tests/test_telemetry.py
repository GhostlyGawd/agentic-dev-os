"""TEST-009; MASTER-TEST-004."""
import tempfile
import json
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from agentic_os.telemetry import EVENT_NAMES,append_event,build_event,read_events


class TelemetryTests(unittest.TestCase):
    def test_every_catalogued_event_validates(self):
        for name in EVENT_NAMES: build_event(name,"run-1","SYSTEM" if not name.startswith("loop.") else "TICKET-001")
        schema=json.loads((ROOT/"observability/schema/event.schema.json").read_text())
        self.assertEqual(EVENT_NAMES,set(schema["properties"]["event_name"]["enum"]))

    def test_sensitive_metadata_is_redacted(self):
        event=build_event("agent.action","r","TICKET-001",metadata={"token":"unsafe","nested":{"password":"unsafe"}})
        self.assertEqual("[REDACTED]",event["metadata"]["token"]); self.assertEqual("[REDACTED]",event["metadata"]["nested"]["password"])

    def test_jsonl_round_trip_and_invalid_line(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"events.jsonl"; event=build_event("loop.started","r","TICKET-001"); append_event(path,event); self.assertEqual([event],read_events(path)); path.write_text("{}\n")
            with self.assertRaises(ValueError): read_events(path)


if __name__=="__main__": unittest.main()
