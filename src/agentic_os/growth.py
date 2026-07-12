from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import write_json
from .config import load_config
from .telemetry import append_event, build_event


FUNNEL = ("visitor", "demo", "trial", "adopted", "retained", "advocate")


def load_growth_events(root: Path) -> list[dict[str, Any]]:
    path=root/"docs/growth/data/events.jsonl"
    if not path.exists(): return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def record_conversion(root: Path, experiment_id: str, channel: str, stage: str, count: int) -> None:
    if stage not in FUNNEL or count < 0 or not re.fullmatch(r"GROWTH-\d{3,}",experiment_id):
        raise ValueError("invalid growth conversion")
    event={"timestamp":datetime.now(timezone.utc).isoformat(),"experiment_id":experiment_id,"channel":channel,"stage":stage,"count":count}
    path=root/"docs/growth/data/events.jsonl"; path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8") as handle: handle.write(json.dumps(event,sort_keys=True)+"\n")
    append_event(root/load_config(root)["event_file"],build_event("growth.conversion_recorded",f"growth-{experiment_id}","SYSTEM","growth",metadata=event))


def growth_summary(events: list[dict[str, Any]]) -> dict[str, Any]:
    totals={stage:sum(e["count"] for e in events if e["stage"]==stage) for stage in FUNNEL}
    conversions={}
    for before,after in zip(FUNNEL,FUNNEL[1:]):
        conversions[f"{before}_to_{after}"]=totals[after]/totals[before] if totals[before] else 0.0
    return {"totals":totals,"conversion_rates":conversions}


def write_growth_report(root: Path) -> Path:
    summary=growth_summary(load_growth_events(root)); write_json(root/"docs/growth/data/latest.json",summary)
    rows="\n".join(f"| {stage} | {count} |" for stage,count in summary["totals"].items())
    rates="\n".join(f"- {name.replace('_',' ')}: {rate:.1%}" for name,rate in summary["conversion_rates"].items())
    target=root/"docs/growth/report.md"; target.write_text(f"# Growth Report\n\n| Stage | Count |\n| --- | ---: |\n{rows}\n\n## Conversion rates\n\n{rates}\n",encoding="utf-8")
    return target
