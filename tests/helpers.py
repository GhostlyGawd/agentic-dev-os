from __future__ import annotations

import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def copy_repo(destination:Path)->Path:
    target=destination/"repo"
    shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns(".git","__pycache__","*.pyc","*.jsonl","latest.md","active-runs.json","dashboard.html","metrics.json"))
    return target


def ready_ticket(root:Path,risk:str="R1")->None:
    path=root/"docs/tickets/TICKET-001-bootstrap.md"
    text=path.read_text(encoding="utf-8").replace("- Status: Complete","- Status: Ready").replace("- Risk: R1",f"- Risk: {risk}")
    path.write_text(text,encoding="utf-8")
