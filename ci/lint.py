#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
issues=[]
for path in ROOT.rglob("*"):
    if not path.is_file() or any(part in {".git","__pycache__",".venv"} for part in path.parts): continue
    if path.suffix not in {".py",".md",".json",".yml",".yaml",".toml"} and path.name not in {"Makefile",".gitignore"}: continue
    try: lines=path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError: continue
    for number,line in enumerate(lines,1):
        if line.rstrip()!=line: issues.append(f"{path.relative_to(ROOT)}:{number}: trailing whitespace")
        if "\t" in line and path.name!="Makefile": issues.append(f"{path.relative_to(ROOT)}:{number}: tab character")
if issues: raise SystemExit("\n".join(issues))
print("Text and source lint passed.")
