"""Dependency boundary tests. TEST-004."""
from __future__ import annotations

import ast
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ArchitectureTests(unittest.TestCase):
    def test_declared_modules_are_acyclic_TEST_004(self) -> None:
        modules = json.loads((ROOT / "architecture.json").read_text())["modules"]
        graph = {name: set(config["may_import"]) for name, config in modules.items()}
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str) -> None:
            if node in visiting:
                self.fail(f"dependency cycle at {node}")
            if node in visited:
                return
            visiting.add(node)
            for dependency in graph[node]:
                if dependency in graph:
                    visit(dependency)
            visiting.remove(node); visited.add(node)

        for node in graph:
            visit(node)

    def test_core_does_not_import_scripts_TEST_004(self) -> None:
        for path in (ROOT / "src/agentic_os").glob("*.py"):
            tree = ast.parse(path.read_text())
            imports = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
            imports |= {node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
            self.assertFalse(any(name == "scripts" or name.startswith("scripts.") for name in imports))


if __name__ == "__main__":
    unittest.main()
