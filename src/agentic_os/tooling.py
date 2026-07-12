from __future__ import annotations

import json
import re
from pathlib import Path

NAME = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")


def validate_tool_catalog(root: Path) -> list[str]:
    payload = json.loads((root / "tools/catalog.json").read_text(encoding="utf-8"))
    issues: list[str] = []
    seen: set[str] = set()
    required = {"name", "description", "when_to_use", "returns", "example", "parameters", "namespace"}
    for index, tool in enumerate(payload.get("tools", [])):
        missing = required - tool.keys()
        if missing:
            issues.append(f"tool[{index}] missing {', '.join(sorted(missing))}")
            continue
        name = tool["name"]
        if not NAME.fullmatch(name):
            issues.append(f"invalid tool name: {name}")
        if name in seen:
            issues.append(f"duplicate tool name: {name}")
        seen.add(name)
        if len(name) > 48:
            issues.append(f"tool name too long: {name}")
        if not tool["description"] or not tool["when_to_use"] or not tool["returns"] or not tool["example"]:
            issues.append(f"tool metadata incomplete: {name}")
        for parameter in tool["parameters"]:
            if not re.fullmatch(r"^[a-z][a-z0-9_]*$", parameter.get("name", "")):
                issues.append(f"invalid parameter name in {name}")
            if parameter.get("type") not in {"string", "integer", "number", "boolean", "array", "object", "enum"}:
                issues.append(f"untyped parameter in {name}: {parameter.get('name')}")
            if not parameter.get("server_validation"):
                issues.append(f"missing server validation in {name}: {parameter.get('name')}")
    return issues
