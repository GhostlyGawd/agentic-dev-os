from __future__ import annotations

import ast
import json
from pathlib import Path


def _module_for(path: Path, root: Path, modules: dict[str, object]) -> str | None:
    relative = str(path.relative_to(root))
    matches = [name for name in modules if relative == name or relative.startswith(name.rstrip("/") + "/")]
    return max(matches, key=len) if matches else None


def validate_architecture(root: Path) -> list[str]:
    config = json.loads((root / "architecture.json").read_text(encoding="utf-8"))
    modules = config["modules"]
    issues: list[str] = []
    graph = {name: set(data.get("may_import", [])) for name, data in modules.items()}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            issues.append(f"dependency cycle includes {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph[node]:
            if dependency in graph:
                visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)
    local_roots = config.get("local_import_roots", {})
    for path in root.rglob("*.py"):
        if any(part in {".git", "__pycache__", ".venv"} for part in path.parts):
            continue
        source_module = _module_for(path, root, modules)
        if not source_module:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            issues.append(f"{path.relative_to(root)} has invalid Python: {exc}")
            continue
        names = [alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names]
        names += [node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        for imported in names:
            target = next((module for prefix, module in local_roots.items() if imported == prefix or imported.startswith(prefix + ".")), None)
            if target and target != source_module and target not in graph[source_module]:
                issues.append(f"{path.relative_to(root)} imports {target}, not allowed by {source_module}")
            if ".internal" in imported and target != source_module:
                issues.append(f"{path.relative_to(root)} imports internal API {imported}")
    return sorted(set(issues))
