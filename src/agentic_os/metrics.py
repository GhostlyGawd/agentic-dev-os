from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import load_config, write_json


def summarize(events: list[dict[str, Any]], trace_coverage: float = 0.0) -> dict[str, float | int]:
    runs: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        runs.setdefault(event["run_id"], []).append(event)
    starts = {r for r, items in runs.items() if any(e["event_name"] == "loop.started" for e in items)}
    stops = {r for r, items in runs.items() if any(e["event_name"] == "loop.stopped" for e in items)}
    successes = {r for r in stops if any(e["event_name"] == "loop.stopped" and e.get("outcome") == "success" for e in runs[r])}
    first_pass = {r for r in successes if not any(e["event_name"] == "loop.retried" for e in runs[r])}
    complete = {r for r in starts if {"loop.started", "verification.completed", "loop.stopped", "metric.summary"}.issubset({e["event_name"] for e in runs[r]})}
    stopped_events = [e for e in events if e["event_name"] == "loop.stopped"]
    total_cost = sum(float(e.get("cost_usd", 0)) for e in stopped_events)
    total_duration = sum(int(e.get("duration_ms", 0)) for e in stopped_events)
    interventions = sum(bool(e.get("human_intervention")) for e in stopped_events)
    regressions = sum(bool(e.get("regression")) for e in stopped_events) + sum(e["event_name"] == "reversal.completed" for e in events)
    retries = [int(e.get("retry_count", 0)) for e in stopped_events]
    verifications = [e for e in events if e["event_name"] == "verification.completed"]
    architecture = sum(int(e.get("architecture_violations", 0)) for e in events if e["event_name"] in {"dependency.violation", "ci.gate_completed"})
    count = len(stops)
    return {
        "task_completion_rate": len(successes) / len(starts) if starts else 0.0,
        "first_pass_success_rate": len(first_pass) / count if count else 0.0,
        "human_intervention_rate": interventions / count if count else 0.0,
        "retry_depth": sum(retries) / count if count else 0.0,
        "cost_per_successful_task": total_cost / len(successes) if successes else 0.0,
        "lead_time_ms": total_duration / count if count else 0.0,
        "spec_adherence_rate": sum(e.get("outcome") == "passed" for e in verifications) / len(verifications) if verifications else 0.0,
        "traceability_coverage": trace_coverage,
        "regression_rate": regressions / count if count else 0.0,
        "architecture_violation_count": architecture,
        "event_completeness_rate": len(complete) / len(starts) if starts else 0.0,
        "runs_started": len(starts), "runs_stopped": count,
    }


def evaluate_alerts(root: Path, summary: dict[str, float | int]) -> list[dict[str, Any]]:
    thresholds = load_config(root)["metric_thresholds"]
    alerts = []
    for metric, rule in thresholds.items():
        value = summary.get(metric, 0)
        breached = ("minimum" in rule and value < rule["minimum"]) or ("maximum" in rule and value > rule["maximum"])
        if breached:
            alerts.append({"metric":metric, "value":value, "rule":rule, "severity":"warning"})
    write_json(root / "observability/alerts/latest.json", {"alerts":alerts})
    return alerts


def render_report(summary: dict[str, float | int], alerts: list[dict[str, Any]]) -> str:
    labels = {
        "task_completion_rate":"Task completion", "first_pass_success_rate":"First-pass success",
        "human_intervention_rate":"Human intervention", "retry_depth":"Retry depth",
        "cost_per_successful_task":"Cost per successful task", "lead_time_ms":"Lead time (ms)",
        "spec_adherence_rate":"Spec adherence", "traceability_coverage":"Traceability coverage",
        "regression_rate":"Regression rate", "architecture_violation_count":"Architecture violations",
        "event_completeness_rate":"Event completeness",
        "product_chain_coverage":"Product-chain coverage",
        "opportunity_evidence_coverage":"Opportunity evidence coverage",
        "validated_bet_rate":"Validated bet rate",
        "milestone_review_coverage":"Milestone review coverage",
        "product_outcome_count":"Product outcomes",
    }
    rows=[]
    for key, label in labels.items():
        value=summary[key]
        display=f"{value:.1%}" if key.endswith("_rate") or key.endswith("_coverage") else f"{value:.2f}" if isinstance(value,float) else str(value)
        rows.append(f"| {label} | {display} |")
    alert_text = "None." if not alerts else "\n".join(f"- {a['metric']}: {a['value']} breached {a['rule']}" for a in alerts)
    return "# Agentic Delivery Metrics\n\n| Metric | Value |\n| --- | ---: |\n"+"\n".join(rows)+f"\n\n## Active alerts\n\n{alert_text}\n"


def render_dashboard(root: Path, summary: dict[str, float | int], alerts: list[dict[str, Any]]) -> Path:
    cards="".join(f'<article><h2>{key.replace("_"," ").title()}</h2><strong>{value:.2f}</strong></article>' for key,value in summary.items() if key not in {"runs_started","runs_stopped"})
    warnings="".join(f'<li>{a["metric"]}: {a["value"]}</li>' for a in alerts) or "<li>No active alerts</li>"
    html=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Agentic Delivery Health</title><style>body{{font:16px system-ui;margin:2rem;background:#0b1020;color:#ecf2ff}}main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem}}article{{background:#18213b;padding:1rem;border-radius:12px}}strong{{font-size:2rem;color:#7dd3fc}}.alerts{{margin-top:2rem}}</style></head><body><h1>Agentic Delivery Health</h1><main>{cards}</main><section class="alerts"><h2>Alerts</h2><ul>{warnings}</ul></section></body></html>'''
    target=root/"observability/reports/dashboard.html"
    target.parent.mkdir(parents=True,exist_ok=True); target.write_text(html,encoding="utf-8")
    write_json(root/"observability/reports/metrics.json",summary)
    return target
