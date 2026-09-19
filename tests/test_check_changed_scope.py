"""Negative-path coverage for ci/check_changed_scope.py, the standalone PR-scope
guard that governance CI runs directly as a script (separate from, and
previously untested relative to, agentic_os.governance.check_scope)."""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_changed_scope", ROOT / "ci/check_changed_scope.py")
check_changed_scope = importlib.util.module_from_spec(SPEC)
sys.modules["check_changed_scope"] = check_changed_scope
SPEC.loader.exec_module(check_changed_scope)


class CheckChangedScopeTests(unittest.TestCase):
    def test_allowed_paths_empty_when_no_files_allowed_heading(self):
        with tempfile.TemporaryDirectory() as d:
            ticket = Path(d) / "TICKET-999-no-scope.md"
            ticket.write_text("## Metadata\n- Risk: R1\n")
            self.assertEqual([], check_changed_scope.allowed_paths(ticket))

    def test_covered_default_denies_when_scope_missing(self):
        self.assertFalse(check_changed_scope.covered("src/agentic_os/governance.py", []))

    def test_covered_allows_dot_wildcard(self):
        self.assertTrue(check_changed_scope.covered("anything/at/all.py", ["."]))

    def test_covered_rejects_prefix_collision(self):
        # "ci_backdoor.py" must not be treated as inside "ci/" scope just
        # because it shares the "ci" string prefix.
        self.assertFalse(check_changed_scope.covered("ci_backdoor.py", ["ci"]))
        self.assertTrue(check_changed_scope.covered("ci/lint.py", ["ci"]))

    def test_covered_exact_file_match(self):
        self.assertTrue(check_changed_scope.covered("README.md", ["README.md"]))
        self.assertFalse(check_changed_scope.covered("README.md.bak", ["README.md"]))


if __name__ == "__main__":
    unittest.main()
