#!/usr/bin/env python3
"""Validate changed files against a ticket's Files Allowed list."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def allowed_paths(ticket: Path) -> list[str]:
    text = ticket.read_text(encoding="utf-8")
    match = re.search(r"^## Files Allowed\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
    return [line[2:].strip().rstrip("/") for line in match.group(1).splitlines() if line.startswith("- ")] if match else []


def covered(path: str, allowed: list[str]) -> bool:
    return any(item in {".", path} or path.startswith(item + "/") for item in allowed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticket", required=True, type=Path)
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    allowed = allowed_paths(args.ticket)
    violations = [path for path in args.files if not covered(path, allowed)]
    if violations:
        raise SystemExit("Files outside ticket scope: " + ", ".join(violations))
