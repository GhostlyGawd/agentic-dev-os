#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from agentic_os.config import load_config,load_json,write_json
from agentic_os.governance import LoopManager, archive_ticket, check_scope, grant_approval
from agentic_os.growth import record_conversion, write_growth_report
from agentic_os.metrics import evaluate_alerts, render_dashboard, render_report, summarize
from agentic_os.telemetry import append_event, build_event, read_events
from agentic_os.validation import stale_artifacts, trace_coverage, validate_repository


def validate(args):
    issues=validate_repository(ROOT)
    if args.json: print(json.dumps({"valid":not issues,"issues":[i.as_dict() for i in issues]},indent=2))
    elif issues:
        for i in issues: print(f"ERROR {i.code}: {i.message} [{i.path}]")
    else: print("Repository governance is valid; master compliance is complete.")
    return int(bool(issues))


def new_artifact(args):
    mapping={"prd":("docs/prd/TEMPLATE.md","docs/prd"),"spec":("docs/specs/TEMPLATE.md","docs/specs"),"ticket":("docs/tickets/TEMPLATE.md","docs/tickets")}
    template,directory=mapping[args.kind]; target=ROOT/directory/f"{args.id}-{args.title.lower().replace(' ','-')}.md"
    if target.exists(): raise ValueError("artifact already exists")
    text=(ROOT/template).read_text(encoding="utf-8").replace({"prd":"PRD-NNN","spec":"SPEC-NNN","ticket":"TICKET-NNN"}[args.kind],args.id).replace("<Feature Name>",args.title).replace("<Title>",args.title)
    target.write_text(text,encoding="utf-8")
    event_name={"prd":"prd.created","spec":"spec.created","ticket":"ticket.created"}[args.kind]
    ticket=args.id if args.kind=="ticket" else "SYSTEM"
    append_event(ROOT/load_config(ROOT)["event_file"],build_event(event_name,f"artifact-{uuid.uuid4()}",ticket,"agent",metadata={"path":str(target.relative_to(ROOT)),"artifact_id":args.id}))
    print(target.relative_to(ROOT)); return 0


def emit(args):
    try: metadata=json.loads(args.metadata)
    except json.JSONDecodeError as exc: raise ValueError(f"invalid metadata JSON: {exc}") from exc
    event=build_event(args.event,args.run_id or f"manual-{uuid.uuid4()}",args.ticket,args.actor,outcome=args.outcome,metadata=metadata)
    append_event(ROOT/load_config(ROOT)["event_file"],event); print(event["event_id"]); return 0


def trace_query(args):
    records=load_json(ROOT/"docs/trace/traceability.json")["records"]
    matches=[record for record in records if args.id in record.values()]
    print(json.dumps(matches,indent=2)); return 0 if matches else 1


def set_status(args):
    directories={"prd":"docs/prd","spec":"docs/specs","ticket":"docs/tickets"}; matches=list((ROOT/directories[args.kind]).glob(f"{args.id}-*.md"))
    if len(matches)!=1: raise ValueError("artifact ID did not resolve uniquely")
    path=matches[0]; text=path.read_text(encoding="utf-8")
    if not re.search(r"^- Status: .+$",text,re.MULTILINE): raise ValueError("artifact has no status field")
    text=re.sub(r"^- Status: .+$",f"- Status: {args.status}",text,count=1,flags=re.MULTILINE); path.write_text(text,encoding="utf-8")
    event_name={"prd":"prd.status_changed","spec":"spec.status_changed","ticket":"ticket.status_changed"}[args.kind]; ticket=args.id if args.kind=="ticket" else "SYSTEM"
    append_event(ROOT/load_config(ROOT)["event_file"],build_event(event_name,f"status-{uuid.uuid4()}",ticket,args.actor,metadata={"artifact_id":args.id,"status":args.status}))
    print(path.relative_to(ROOT)); return 0


def trace_status(args):
    path=ROOT/"docs/trace/traceability.json"; payload=load_json(path); matches=[r for r in payload["records"] if r["requirement_id"]==args.requirement]
    if len(matches)!=1: raise ValueError("requirement did not resolve uniquely")
    matches[0]["status"]=args.status
    if args.completion_note: matches[0]["completion_note"]=args.completion_note
    write_json(path,payload); append_event(ROOT/load_config(ROOT)["event_file"],build_event("trace.updated",f"trace-{uuid.uuid4()}","SYSTEM",args.actor,metadata={"requirement_id":args.requirement,"status":args.status}))
    print(args.requirement); return 0


def approve(args):
    record=grant_approval(ROOT,args.ticket,args.approver,args.reason,args.expires_at)
    append_event(ROOT/load_config(ROOT)["event_file"],build_event("approval.granted",f"approval-{uuid.uuid4()}",args.ticket,args.approver,outcome="approved",metadata={"risk":record["risk"]}))
    print("Approval recorded and bound to the ticket digest."); return 0


def loop(args):
    manager=LoopManager(ROOT); actor=args.actor
    if args.action=="plan": print(manager.plan(args.ticket,actor))
    elif args.action=="start": print(manager.start(args.ticket,actor,args.run_id))
    elif args.action=="record-action": manager.action(args.ticket,actor,args.description,args.paths); print("Action recorded.")
    elif args.action=="retry": print(manager.retry(args.ticket,actor,args.reason))
    elif args.action=="verify": print("passed" if manager.verify(args.ticket,actor,not args.dry_run) else "failed")
    elif args.action=="stop": print(manager.stop(args.ticket,actor,args.outcome,args.cost_usd,args.human_intervention,args.regression))
    return 0


def scope(args):
    violations=check_scope(ROOT,args.ticket,args.files)
    if violations: print("Outside scope: "+", ".join(violations)); return 1
    print("All files are inside ticket scope."); return 0


def metrics(_):
    events=read_events(ROOT/load_config(ROOT)["event_file"]); summary=summarize(events,trace_coverage(ROOT)); alerts=evaluate_alerts(ROOT,summary)
    (ROOT/"docs/metrics/latest.md").write_text(render_report(summary,alerts),encoding="utf-8"); dashboard=render_dashboard(ROOT,summary,alerts)
    for alert in alerts: append_event(ROOT/load_config(ROOT)["event_file"],build_event("alert.triggered",f"alert-{uuid.uuid4()}","SYSTEM","metrics",metadata=alert))
    print(f"docs/metrics/latest.md\n{dashboard.relative_to(ROOT)}"); return 0


def archive(args): print(archive_ticket(ROOT,args.ticket,args.actor).relative_to(ROOT)); return 0


def audit(_):
    stale=stale_artifacts(ROOT)
    if stale: print("\n".join(stale)); return 1
    print("No stale active artifacts."); return 0


def impacted(args):
    config=json.loads((ROOT/"ci/impact-map.json").read_text()); tests=set(config["default"])
    for file in args.files:
        for prefix,mapped in config["paths"].items():
            if file.startswith(prefix): tests.update(mapped)
    print(" ".join(sorted(tests))); return 0


def growth(args):
    if args.growth_action=="record": record_conversion(ROOT,args.experiment,args.channel,args.stage,args.count); print("Conversion recorded.")
    else: print(write_growth_report(ROOT).relative_to(ROOT))
    return 0


def demo(_):
    event_path=ROOT/load_config(ROOT)["event_file"]; event_path.unlink(missing_ok=True)
    run="demo-"+uuid.uuid4().hex[:10]
    for event,fields in [("loop.started",{}),("agent.action",{"metadata":{"action":"demo","paths":["README.md"]}}),("verification.completed",{"outcome":"passed"}),("loop.stopped",{"outcome":"success","duration_ms":1200,"retry_count":0,"cost_usd":0.01,"human_intervention":False,"regression":False}),("metric.summary",{"outcome":"success","duration_ms":1200,"retry_count":0,"cost_usd":0.01})]: append_event(event_path,build_event(event,run,"TICKET-001","demo",**fields))
    metrics(argparse.Namespace()); print("End-to-end demo completed."); return 0


def parser():
    p=argparse.ArgumentParser(description="Agentic Development Operating System"); sub=p.add_subparsers(dest="command",required=True)
    v=sub.add_parser("validate"); v.add_argument("--json",action="store_true"); v.set_defaults(func=validate)
    n=sub.add_parser("new"); n.add_argument("kind",choices=("prd","spec","ticket")); n.add_argument("--id",required=True); n.add_argument("--title",required=True); n.set_defaults(func=new_artifact)
    a=sub.add_parser("approve"); a.add_argument("--ticket",required=True); a.add_argument("--approver",required=True); a.add_argument("--reason",required=True); a.add_argument("--expires-at"); a.set_defaults(func=approve)
    l=sub.add_parser("loop"); l.add_argument("action",choices=("plan","start","record-action","retry","verify","stop")); l.add_argument("--ticket",required=True); l.add_argument("--actor",default=os.getenv("USER","agent")); l.add_argument("--run-id"); l.add_argument("--description",default=""); l.add_argument("--paths",nargs="*",default=[]); l.add_argument("--reason",default=""); l.add_argument("--dry-run",action="store_true"); l.add_argument("--outcome",choices=("success","failure","handoff"),default="success"); l.add_argument("--cost-usd",type=float,default=0); l.add_argument("--human-intervention",action="store_true"); l.add_argument("--regression",action="store_true"); l.set_defaults(func=loop)
    s=sub.add_parser("scope-check"); s.add_argument("--ticket",required=True); s.add_argument("files",nargs="+"); s.set_defaults(func=scope)
    m=sub.add_parser("metrics"); m.set_defaults(func=metrics)
    ar=sub.add_parser("archive"); ar.add_argument("--ticket",required=True); ar.add_argument("--actor",default=os.getenv("USER","agent")); ar.set_defaults(func=archive)
    au=sub.add_parser("audit-stale"); au.set_defaults(func=audit)
    i=sub.add_parser("impacted-tests"); i.add_argument("files",nargs="+"); i.set_defaults(func=impacted)
    g=sub.add_parser("growth"); g.add_argument("growth_action",choices=("record","report")); g.add_argument("--experiment",default="GROWTH-001"); g.add_argument("--channel",default="direct"); g.add_argument("--stage",choices=("visitor","demo","trial","adopted","retained","advocate"),default="visitor"); g.add_argument("--count",type=int,default=1); g.set_defaults(func=growth)
    e=sub.add_parser("emit"); e.add_argument("--event",required=True); e.add_argument("--ticket",default="SYSTEM"); e.add_argument("--run-id"); e.add_argument("--actor",default=os.getenv("USER","agent")); e.add_argument("--outcome",choices=("success","failure","handoff","passed","failed","approved","rejected","cancelled")); e.add_argument("--metadata",default="{}"); e.set_defaults(func=emit)
    tq=sub.add_parser("trace-query"); tq.add_argument("--id",required=True); tq.set_defaults(func=trace_query)
    st=sub.add_parser("status"); st.add_argument("kind",choices=("prd","spec","ticket")); st.add_argument("--id",required=True); st.add_argument("--status",required=True); st.add_argument("--actor",default=os.getenv("USER","agent")); st.set_defaults(func=set_status)
    ts=sub.add_parser("trace-status"); ts.add_argument("--requirement",required=True); ts.add_argument("--status",required=True); ts.add_argument("--completion-note"); ts.add_argument("--actor",default=os.getenv("USER","agent")); ts.set_defaults(func=trace_status)
    d=sub.add_parser("demo"); d.set_defaults(func=demo)
    return p


if __name__=="__main__":
    try: args=parser().parse_args(); raise SystemExit(args.func(args))
    except ValueError as exc: print(f"ERROR: {exc}",file=sys.stderr); raise SystemExit(2)
