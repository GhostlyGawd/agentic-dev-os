"""Tests for ci/lint.py script.

Tests cover:
- File type filtering and exclusion logic
- Trailing whitespace detection
- Tab character detection with Makefile exception
- Directory exclusion patterns
- UnicodeDecodeError handling for binary files
"""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


class LintTests(unittest.TestCase):
    """Test suite for the lint.py CI script."""

    def run_lint(self, root: Path) -> tuple[int, str, str]:
        """Execute lint.py script and return exit code, stdout, stderr."""
        env = os.environ.copy()
        env["LINT_ROOT"] = str(root)
        result = subprocess.run(
            [sys.executable, str(ROOT / "ci" / "lint.py")],
            cwd=root,
            capture_output=True,
            text=True,
            env=env,
        )
        return result.returncode, result.stdout, result.stderr

    def test_clean_directory_passes(self):
        """Happy path: clean files with no whitespace or tab issues."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            # Create clean Python file
            (root / "test.py").write_text("def hello():\n    return 'world'\n")
            # Create clean Markdown file
            (root / "README.md").write_text("# Title\n\nSome content\n")
            # Create clean JSON file
            (root / "config.json").write_text('{"key": "value"}\n')
            # Create clean YAML file
            (root / "config.yml").write_text("key: value\n")

            code, stdout, stderr = self.run_lint(root)
            self.assertEqual(code, 0, f"Expected pass but got: {stderr}")
            self.assertIn("lint passed", stdout)

    def test_trailing_whitespace_detection(self):
        """Error case: trailing whitespace should be detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            # Create file with trailing whitespace
            (root / "bad.py").write_text("def hello():  \n    return 'world'\n")

            code, stdout, stderr = self.run_lint(root)
            self.assertNotEqual(code, 0, "Expected failure for trailing whitespace")
            self.assertIn("trailing whitespace", stderr)
            self.assertIn("bad.py:1", stderr)

    def test_tab_character_detection(self):
        """Error case: tab characters should be detected in Python files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            # Create file with tab character
            (root / "bad.py").write_text("def hello():\n\treturn 'world'\n")

            code, stdout, stderr = self.run_lint(root)
            self.assertNotEqual(code, 0, "Expected failure for tab character")
            self.assertIn("tab character", stderr)
            self.assertIn("bad.py:2", stderr)

    def test_tab_character_allowed_in_makefile(self):
        """Exception: Makefile is allowed to have tabs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            # Create Makefile with tabs (valid)
            (root / "Makefile").write_text("test:\n\techo 'hello'\n")

            code, stdout, stderr = self.run_lint(root)
            self.assertEqual(code, 0, f"Makefile tabs should be allowed: {stderr}")

    def test_file_type_filtering(self):
        """Edge case: unsupported file types should be skipped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            # Create unsupported file types with issues (should be skipped)
            (root / "binary.exe").write_text("bad\t content  \n")
            (root / "image.png").write_text("fake\t png  \n")
            (root / "archive.zip").write_text("fake\t zip  \n")
            # Create a clean supported file
            (root / "clean.py").write_text("clean = True\n")

            code, stdout, stderr = self.run_lint(root)
            self.assertEqual(code, 0, f"Unsupported files should be skipped: {stderr}")

    def test_supported_file_types(self):
        """Verify only supported file types are checked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            # Test TOML file with trailing whitespace
            (root / "config.toml").write_text("[tool]  \nkey = 'value'\n")

            code, stdout, stderr = self.run_lint(root)
            self.assertNotEqual(code, 0, "TOML files should be checked")
            self.assertIn("config.toml:1", stderr)

    def test_directory_exclusion_git(self):
        """Edge case: .git directory should be excluded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            git_dir = root / ".git" / "objects"
            git_dir.mkdir(parents=True)
            # Create file with issues in .git directory (should be skipped)
            (git_dir / "bad.py").write_text("bad\t content  \n")
            # Create clean file outside .git
            (root / "clean.py").write_text("clean = True\n")

            code, stdout, stderr = self.run_lint(root)
            self.assertEqual(code, 0, "Files in .git should be excluded")

    def test_directory_exclusion_pycache(self):
        """Edge case: __pycache__ directory should be excluded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pycache_dir = root / "__pycache__"
            pycache_dir.mkdir()
            # Create file with issues in __pycache__ (should be skipped)
            (pycache_dir / "bad.py").write_text("bad\t content  \n")
            # Create clean file outside __pycache__
            (root / "clean.py").write_text("clean = True\n")

            code, stdout, stderr = self.run_lint(root)
            self.assertEqual(code, 0, "Files in __pycache__ should be excluded")

    def test_directory_exclusion_venv(self):
        """Edge case: .venv, node_modules, dist, coverage, data directories excluded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            for excluded_dir in [".venv", "node_modules", "dist", "coverage", "data"]:
                dir_path = root / excluded_dir
                dir_path.mkdir()
                # Create file with issues in excluded directory
                (dir_path / "bad.py").write_text("bad\t content  \n")

            # Create clean file at root
            (root / "clean.py").write_text("clean = True\n")

            code, stdout, stderr = self.run_lint(root)
            self.assertEqual(code, 0, f"Excluded directories should be skipped: {stderr}")

    def test_dotfile_gitignore_checked(self):
        """Verify .gitignore file is checked (special case)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            # .gitignore has trailing whitespace
            (root / ".gitignore").write_text("*.pyc  \n*.log\n")

            code, stdout, stderr = self.run_lint(root)
            self.assertNotEqual(code, 0, ".gitignore should be checked")
            self.assertIn(".gitignore:1", stderr)

    def test_multiple_issues_reported(self):
        """Verify multiple issues in same file are all reported."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            # File with multiple issues
            (root / "bad.py").write_text("line1  \nline2\t\nline3  \n")

            code, stdout, stderr = self.run_lint(root)
            self.assertNotEqual(code, 0)
            # Check that both trailing whitespace and tab issues are reported
            self.assertIn("bad.py:1", stderr)  # trailing whitespace
            self.assertIn("bad.py:2", stderr)  # tab character
            self.assertIn("bad.py:3", stderr)  # trailing whitespace

    def test_unicode_decode_error_handling(self):
        """Edge case: binary files with decode errors should be skipped gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            # Create a binary file (Python file with invalid UTF-8)
            binary_path = root / "binary.py"
            binary_path.write_bytes(b"\x80\x81\x82")
            # Create a clean text file
            (root / "clean.py").write_text("clean = True\n")

            code, stdout, stderr = self.run_lint(root)
            self.assertEqual(code, 0, f"Binary files should be gracefully skipped: {stderr}")

    def test_mixed_issues_across_files(self):
        """Integration test: multiple files with different issue types."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            # File 1: Python with trailing whitespace
            (root / "file1.py").write_text("def foo():  \n    pass\n")
            # File 2: Markdown with tabs
            (root / "file2.md").write_text("# Title\n\t* item\n")
            # File 3: Clean JSON
            (root / "file3.json").write_text('{"ok": true}\n')

            code, stdout, stderr = self.run_lint(root)
            self.assertNotEqual(code, 0)
            self.assertIn("file1.py:1", stderr)
            self.assertIn("file2.md:2", stderr)
            # file3.json should have no issues


if __name__ == "__main__":
    unittest.main()
