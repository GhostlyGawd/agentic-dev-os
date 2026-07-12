"""TEST-008 TEST-010; MASTER-TEST-005."""
import tempfile
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src")); sys.path.insert(0,str(ROOT/"tests"))
from agentic_os.metrics import evaluate_alerts,render_dashboard,summarize
from agentic_os.telemetry import build_event
from helpers import copy_repo


class MetricTests(unittest.TestCase):
    def events(self):
        return [build_event("loop.started","r","TICKET-001"),build_event("verification.completed","r","TICKET-001",outcome="passed"),build_event("loop.stopped","r","TICKET-001",outcome="success",duration_ms=1000,retry_count=0,cost_usd=2.0,human_intervention=False,regression=False),build_event("metric.summary","r","TICKET-001",outcome="success")]
    def test_all_master_metrics_are_calculated(self):
        summary=summarize(self.events(),1.0)
        expected={"task_completion_rate","first_pass_success_rate","human_intervention_rate","retry_depth","cost_per_successful_task","lead_time_ms","spec_adherence_rate","traceability_coverage","regression_rate","architecture_violation_count","event_completeness_rate"}
        self.assertTrue(expected.issubset(summary)); self.assertEqual(2.0,summary["cost_per_successful_task"])
    def test_alerts_and_dashboard_are_generated(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); alerts=evaluate_alerts(root,summarize([],0.0)); target=render_dashboard(root,summarize([],0.0),alerts); self.assertTrue(alerts); self.assertIn("Agentic Delivery Health",target.read_text())


if __name__=="__main__": unittest.main()
