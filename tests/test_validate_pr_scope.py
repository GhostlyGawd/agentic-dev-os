"""TEST-003 TEST-004 TEST-006 TEST-007; Negative-path coverage for ci/validate_pr_scope.py, the standalone PR-scope
validator that governance CI runs directly as a script. Tests the CLI entry point, TICKET-NNN regex extraction,
and risk-tier approval gate, which are not covered by underlying governance.check_scope() unit tests."""
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))
from agentic_os.governance import grant_approval, ticket_contract


class ValidatePRScopeTests(unittest.TestCase):
    """Tests for validate_pr_scope.py CLI script. Tests run against actual repository
    (not copies) since the script hard-codes absolute ROOT path. Tests restore original
    ticket state after each run."""

    def setUp(self):
        """Capture original TICKET-001 state for restoration."""
        self.ticket_path = ROOT / "docs/tickets/TICKET-001-bootstrap.md"
        self.original_content = self.ticket_path.read_text(encoding="utf-8")
        self.approval_path = ROOT / "agent/approvals/TICKET-001.json"
        self.approval_existed = self.approval_path.exists()
        self.original_approval = self.approval_path.read_text() if self.approval_existed else None

    def tearDown(self):
        """Restore original TICKET-001 and approval state."""
        self.ticket_path.write_text(self.original_content, encoding="utf-8")
        if self.approval_existed and self.original_approval:
            self.approval_path.write_text(self.original_approval, encoding="utf-8")
        elif self.approval_path.exists():
            self.approval_path.unlink()

    def test_ticket_reference_extraction_success(self):
        """TICKET-NNN regex correctly extracts ticket from PR body."""
        result = subprocess.run(
            [sys.executable, str(ROOT / "ci/validate_pr_scope.py"),
             "--body", "This PR fixes TICKET-001 by updating tests",
             "--base", "HEAD"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("TICKET-001", result.stdout)

    def test_ticket_reference_extraction_missing(self):
        """Missing TICKET-NNN reference fails with clear error."""
        result = subprocess.run(
            [sys.executable, str(ROOT / "ci/validate_pr_scope.py"),
             "--body", "This PR has no ticket reference",
             "--base", "HEAD"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("TICKET-NNN reference", result.stderr)

    def test_ticket_reference_two_digit_ignored(self):
        """Two-digit TICKET refs (< 100) are not matched."""
        result = subprocess.run(
            [sys.executable, str(ROOT / "ci/validate_pr_scope.py"),
             "--body", "This PR fixes TICKET-01 by updating README",
             "--base", "HEAD"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("TICKET-NNN reference", result.stderr)

    def test_r1_risk_requires_no_approval(self):
        """R1 risk tickets pass without approval."""
        # TICKET-001 defaults to R1, ensure no approval
        if self.approval_path.exists():
            self.approval_path.unlink()
        result = subprocess.run(
            [sys.executable, str(ROOT / "ci/validate_pr_scope.py"),
             "--body", "Fix for TICKET-001",
             "--base", "HEAD"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False
        )
        self.assertEqual(result.returncode, 0, f"stdout: {result.stdout}, stderr: {result.stderr}")

    def test_r2_risk_requires_approval(self):
        """R2 risk tickets require valid approval."""
        # Set TICKET-001 to R2, remove any approval
        content = self.ticket_path.read_text(encoding="utf-8")
        content = content.replace("- Risk: R1", "- Risk: R2")
        self.ticket_path.write_text(content, encoding="utf-8")
        if self.approval_path.exists():
            self.approval_path.unlink()

        result = subprocess.run(
            [sys.executable, str(ROOT / "ci/validate_pr_scope.py"),
             "--body", "Fix for TICKET-001",
             "--base", "HEAD"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False
        )
        self.assertNotEqual(result.returncode, 0, f"stdout: {result.stdout}, stderr: {result.stderr}")
        self.assertIn("R2", result.stderr)
        self.assertIn("approval", result.stderr.lower())

    def test_r2_risk_with_valid_approval_passes(self):
        """R2 risk tickets pass with valid approval."""
        # Set TICKET-001 to R2
        content = self.ticket_path.read_text(encoding="utf-8")
        content = content.replace("- Risk: R1", "- Risk: R2")
        self.ticket_path.write_text(content, encoding="utf-8")

        # Grant approval
        grant_approval(ROOT, "TICKET-001", "reviewer", "approved")

        result = subprocess.run(
            [sys.executable, str(ROOT / "ci/validate_pr_scope.py"),
             "--body", "Fix for TICKET-001",
             "--base", "HEAD"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False
        )
        self.assertEqual(result.returncode, 0, f"stdout: {result.stdout}, stderr: {result.stderr}")

    def test_r3_risk_requires_approval(self):
        """R3 risk tickets require valid approval."""
        # Set TICKET-001 to R3, remove any approval
        content = self.ticket_path.read_text(encoding="utf-8")
        content = content.replace("- Risk: R1", "- Risk: R3")
        self.ticket_path.write_text(content, encoding="utf-8")
        if self.approval_path.exists():
            self.approval_path.unlink()

        result = subprocess.run(
            [sys.executable, str(ROOT / "ci/validate_pr_scope.py"),
             "--body", "Fix for TICKET-001",
             "--base", "HEAD"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False
        )
        self.assertNotEqual(result.returncode, 0, f"stdout: {result.stdout}, stderr: {result.stderr}")
        self.assertIn("R3", result.stderr)
        self.assertIn("approval", result.stderr.lower())

    def test_r3_risk_with_valid_approval_passes(self):
        """R3 risk tickets pass with valid approval."""
        # Set TICKET-001 to R3
        content = self.ticket_path.read_text(encoding="utf-8")
        content = content.replace("- Risk: R1", "- Risk: R3")
        self.ticket_path.write_text(content, encoding="utf-8")

        # Grant approval
        grant_approval(ROOT, "TICKET-001", "reviewer", "approved")

        result = subprocess.run(
            [sys.executable, str(ROOT / "ci/validate_pr_scope.py"),
             "--body", "Fix for TICKET-001",
             "--base", "HEAD"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False
        )
        self.assertEqual(result.returncode, 0, f"stdout: {result.stdout}, stderr: {result.stderr}")


if __name__ == "__main__":
    unittest.main()
