"""TEST-019 TEST-020 TEST-021 TEST-022 TEST-023 TEST-024 TEST-025 TEST-026 TEST-027 TEST-028; MASTER-TEST-013."""
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src")); sys.path.insert(0,str(ROOT/"tests"))
from agentic_os.product import export_product_views,product_metrics,validate_product
from helpers import copy_repo


class ProductIntegrationTests(unittest.TestCase):
    def test_complete_product_chain_is_valid_TEST_019(self):
        self.assertEqual([],validate_product(ROOT))

    def test_outcome_contract_is_required_TEST_019(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); path=root/".ai/strategy/desired-outcomes.md"; path.write_text(path.read_text().replace("### Baseline","### Removed"))
            self.assertTrue(any("Baseline" in issue for issue in validate_product(root)))

    def test_opportunity_requires_evidence_TEST_020(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); path=root/".ai/discovery/opportunity-tree.md"; path.write_text(path.read_text().replace("- Current repository trace starts at PRD requirements.","No evidence recorded."))
            self.assertIn("opportunity tree requires evidence",validate_product(root))

    def test_unvalidated_bet_blocks_prds_TEST_021(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); path=root/".ai/bets/BET-001-product-strategy-layer.md"; path.write_text(path.read_text().replace("## Status\nValidated","## Status\nProposed"))
            self.assertTrue(any("validated bet" in issue for issue in validate_product(root)))

    def test_milestone_requires_human_review_TEST_022(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); path=root/".ai/milestones/M-002.md"; path.write_text(path.read_text().replace("REVIEW-002","REVIEW-999"))
            self.assertTrue(any("invalid review" in issue for issue in validate_product(root)))

    def test_change_and_review_records_are_complete_TEST_023(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); path=root/"docs/change-requests/CR-001-product-strategy-integration.md"; path.write_text(path.read_text().replace("## Decision","## Removed"))
            self.assertTrue(any("Decision" in issue for issue in validate_product(root)))

    def test_trace_upstream_references_resolve_TEST_024(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); path=root/"docs/trace/traceability.json"; data=json.loads(path.read_text()); data["records"][0]["outcome_ref"]="O-999"; path.write_text(json.dumps(data))
            self.assertTrue(any("outcome_ref" in issue for issue in validate_product(root)))

    def test_generated_views_are_deterministic_and_drift_checked_TEST_025(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); self.assertEqual([],export_product_views(root,check=True)); path=root/".ai/requirements/requirements.md"; path.write_text(path.read_text()+"manual edit\n"); self.assertEqual([".ai/requirements/requirements.md"],export_product_views(root,check=True)); export_product_views(root); self.assertEqual([],export_product_views(root,check=True))

    def test_command_set_is_complete_TEST_026(self):
        names={path.stem for path in (ROOT/".ai/commands").glob("*.md")}; self.assertEqual({"orient","discover","bet","specify","plan","build","review","close"},names)

    def test_product_metrics_cover_entire_chain_TEST_027(self):
        metrics=product_metrics(ROOT); self.assertEqual(1.0,metrics["product_chain_coverage"]); self.assertEqual(1.0,metrics["opportunity_evidence_coverage"]); self.assertEqual(1.0,metrics["validated_bet_rate"]); self.assertEqual(1.0,metrics["milestone_review_coverage"])

    def test_generated_views_are_marked_noncanonical_TEST_028(self):
        for path in (ROOT/".ai/requirements").iterdir(): self.assertIn("GENERATED",path.read_text().splitlines()[0])


if __name__=="__main__": unittest.main()
