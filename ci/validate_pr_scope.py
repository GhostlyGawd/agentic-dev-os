#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from agentic_os.governance import approval_valid,check_scope,ticket_contract

parser=argparse.ArgumentParser(); parser.add_argument("--body",required=True); parser.add_argument("--base",required=True); args=parser.parse_args()
match=re.search(r"\bTICKET-\d{3,}\b",args.body)
if not match: raise SystemExit("Pull request body must contain a TICKET-NNN reference")
ticket=match.group(0); result=subprocess.run(["git","diff","--name-only",args.base+"...HEAD"],cwd=ROOT,text=True,capture_output=True,check=True)
files=[line for line in result.stdout.splitlines() if line]; violations=check_scope(ROOT,ticket,files)
if violations: raise SystemExit("Files outside ticket scope: "+", ".join(violations))
contract=ticket_contract(ROOT,ticket)
if contract["risk"] in {"R2","R3"} and not approval_valid(ROOT,ticket): raise SystemExit(f"{contract['risk']} requires a valid committed approval")
print(f"PR scope and approval are valid for {ticket} ({len(files)} changed files).")
