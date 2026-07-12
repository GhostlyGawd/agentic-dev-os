#!/usr/bin/env python3
"""Stable entry point for CI and scheduled metric aggregation."""
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
raise SystemExit(subprocess.call([sys.executable,str(ROOT/"scripts/ados.py"),"metrics"],cwd=ROOT))
