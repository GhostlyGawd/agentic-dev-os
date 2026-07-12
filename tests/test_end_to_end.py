"""TEST-018; MASTER-TEST-010 MASTER-TEST-011 MASTER-TEST-012."""
import tempfile
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src")); sys.path.insert(0,str(ROOT/"tests"))
from agentic_os.governance import LoopManager
from agentic_os.metrics import evaluate_alerts,render_dashboard,summarize
from agentic_os.telemetry import read_events
from agentic_os.validation import trace_coverage,validate_repository
from helpers import copy_repo,ready_ticket


class EndToEndTests(unittest.TestCase):
    def test_full_ticket_to_dashboard_path(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); self.assertEqual([],validate_repository(root)); ready_ticket(root); manager=LoopManager(root); manager.plan("TICKET-001","agent"); manager.start("TICKET-001","agent"); manager.action("TICKET-001","agent","implement",["src/agentic_os/metrics.py"]); self.assertTrue(manager.verify("TICKET-001","agent",execute=False)); manager.stop("TICKET-001","agent","success",cost_usd=.25)
            events=read_events(root/"observability/events/loops.jsonl"); summary=summarize(events,trace_coverage(root)); alerts=evaluate_alerts(root,summary); self.assertTrue(render_dashboard(root,summary,alerts).exists()); self.assertEqual(1.0,summary["task_completion_rate"]); self.assertEqual(1.0,summary["event_completeness_rate"])


if __name__=="__main__": unittest.main()
