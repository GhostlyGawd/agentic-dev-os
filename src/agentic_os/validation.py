from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .architecture import validate_architecture
from .config import load_config, load_json
from .governance import HEADINGS, section
from .telemetry import read_events
from .tooling import validate_tool_catalog

REQUIREMENT=re.compile(r"\bPRD-\d{3,}-R\d{2,}\b")
SPEC=re.compile(r"\bSPEC-\d{3,}-A\d{2,}\b")
TICKET=re.compile(r"\bTICKET-\d{3,}\b")
TEST=re.compile(r"\bTEST-\d{3,}\b")
METRIC=re.compile(r"\bMETRIC-\d{3,}\b")
TRACE_FIELDS={"requirement_id","requirement","source_origin","spec_ref","ticket_ref","code_ref","test_ref","telemetry_event","metric_ref","completion_note","status","version"}


@dataclass(frozen=True)
class Issue:
    code:str; message:str; path:str=""
    def as_dict(self)->dict[str,str]: return {"code":self.code,"message":self.message,"path":self.path}


def issue_list(code:str,path:str,messages:list[str])->list[Issue]:
    return [Issue(code,message,path) for message in messages]


def validate_structure(root:Path)->list[Issue]:
    required=["README.md","MASTER.md","ado.config.json","agent/AGENTS.md","agent/policies/tool-naming.md",
              "architecture.json","docs/prd","docs/specs","docs/tickets","docs/archive","docs/findings","docs/decisions",
              "docs/metrics","docs/growth","docs/operating-model/owners.json","docs/trace/traceability.json",
              "docs/trace/master-compliance.json","observability/schema/event.schema.json","observability/dashboards/default.json",
              "scripts/ados.py","scripts/metrics","tools/catalog.json","ci","tests"]
    return [Issue("STRUCTURE_MISSING",f"required path missing: {item}",item) for item in required if not (root/item).exists()]


def validate_tickets(root:Path)->list[Issue]:
    issues=[]
    paths=list((root/"docs/tickets").glob("TICKET-*.md"))+list((root/"docs/archive/tickets").glob("TICKET-*.md"))
    for path in sorted(paths):
        text=path.read_text(encoding="utf-8")
        for heading in HEADINGS:
            if not section(text,heading): issues.append(Issue("TICKET_SECTION",f"missing section: {heading}",str(path.relative_to(root))))
        if not REQUIREMENT.search(text): issues.append(Issue("TICKET_PRD","no requirement link",str(path.relative_to(root))))
        if not SPEC.search(text): issues.append(Issue("TICKET_SPEC","no spec acceptance link",str(path.relative_to(root))))
        if not re.search(r"^- Risk: R[0-3]$",section(text,"Metadata"),re.MULTILINE): issues.append(Issue("TICKET_RISK","missing valid risk tier",str(path.relative_to(root))))
    return issues


def _corpus(root:Path,pattern:str)->str:
    return "\n".join(path.read_text(encoding="utf-8") for path in root.glob(pattern))


def validate_trace(root:Path)->list[Issue]:
    path=root/"docs/trace/traceability.json"; issues=[]
    try: records=load_json(path).get("records",[])
    except (FileNotFoundError,json.JSONDecodeError) as exc: return [Issue("TRACE_JSON",str(exc),str(path.relative_to(root)))]
    corpora={"requirement":_corpus(root,"docs/prd/PRD-*.md"),"spec":_corpus(root,"docs/specs/SPEC-*.md"),
             "ticket":_corpus(root,"docs/tickets/TICKET-*.md")+_corpus(root,"docs/archive/tickets/TICKET-*.md"),
             "test":_corpus(root,"tests/test_*.py"),"metric":_corpus(root,"docs/metrics/*.md")}
    seen=set()
    for index,record in enumerate(records):
        missing=TRACE_FIELDS-set(record)
        if missing: issues.append(Issue("TRACE_FIELDS",f"record[{index}] missing {', '.join(sorted(missing))}",str(path.relative_to(root)))); continue
        req=record["requirement_id"]
        if req in seen: issues.append(Issue("TRACE_DUPLICATE",f"duplicate requirement {req}",str(path.relative_to(root))))
        seen.add(req)
        for ref,kind in ((req,"requirement"),(record["spec_ref"],"spec"),(record["ticket_ref"],"ticket"),(record["test_ref"],"test"),(record["metric_ref"],"metric")):
            if ref not in corpora[kind]: issues.append(Issue("TRACE_TARGET",f"unknown {kind}: {ref}",str(path.relative_to(root))))
        if not (root/record["code_ref"]).exists(): issues.append(Issue("TRACE_CODE",f"missing code: {record['code_ref']}",str(path.relative_to(root))))
        if not record["completion_note"].strip(): issues.append(Issue("TRACE_COMPLETION",f"empty completion note: {req}",str(path.relative_to(root))))
    for req in sorted(set(REQUIREMENT.findall(corpora["requirement"]))-seen): issues.append(Issue("TRACE_COVERAGE",f"untraced requirement: {req}",str(path.relative_to(root))))
    return issues


def trace_coverage(root:Path)->float:
    requirements=set(REQUIREMENT.findall(_corpus(root,"docs/prd/PRD-*.md")))
    traced={r.get("requirement_id") for r in load_json(root/"docs/trace/traceability.json").get("records",[])}
    return len(requirements&traced)/len(requirements) if requirements else 1.0


def validate_compliance(root:Path)->list[Issue]:
    path=root/"docs/trace/master-compliance.json"; payload=load_json(path); issues=[]
    records=payload.get("requirements",[]); expected=set(range(1,payload.get("expected_count",0)+1)); found=set()
    test_text=_corpus(root,"tests/test_*.py")
    for record in records:
        number=int(record["id"].split("-")[1]); found.add(number)
        if record.get("status")!="Complete": issues.append(Issue("MASTER_INCOMPLETE",record["id"],str(path.relative_to(root))))
        if record.get("test_ref") not in test_text: issues.append(Issue("MASTER_TEST",f"missing evidence {record.get('test_ref')}",str(path.relative_to(root))))
        for ref in record.get("implementation_refs",[]):
            if not (root/ref).exists(): issues.append(Issue("MASTER_REF",f"missing {ref}",str(path.relative_to(root))))
    if found!=expected: issues.append(Issue("MASTER_SEQUENCE",f"expected {len(expected)} sequential requirements, found {len(found)}",str(path.relative_to(root))))
    return issues


def validate_owners(root:Path)->list[Issue]:
    payload=load_json(root/"docs/operating-model/owners.json"); required={"prd","spec","modules","traceability","metrics","ci","loops","risk_review"}
    missing=required-set(payload.get("owners",{})); return [Issue("OWNER_MISSING",name,"docs/operating-model/owners.json") for name in sorted(missing)]


def stale_artifacts(root:Path,days:int|None=None)->list[str]:
    days=days or load_config(root)["stale_after_days"]; now=datetime.now(timezone.utc).timestamp(); stale=[]
    for pattern in ("docs/prd/PRD-*.md","docs/specs/SPEC-*.md","docs/tickets/TICKET-*.md"):
        for path in root.glob(pattern):
            if (now-path.stat().st_mtime)/86400>days: stale.append(str(path.relative_to(root)))
    return sorted(stale)


def validate_repository(root:Path)->list[Issue]:
    issues=validate_structure(root)
    if issues: return issues
    issues+=validate_tickets(root)+validate_trace(root)+validate_compliance(root)+validate_owners(root)
    issues+=issue_list("ARCHITECTURE","architecture.json",validate_architecture(root))
    issues+=issue_list("TOOL_NAMING","tools/catalog.json",validate_tool_catalog(root))
    try: read_events(root/load_config(root)["event_file"])
    except ValueError as exc: issues.append(Issue("EVENT_INVALID",str(exc),load_config(root)["event_file"]))
    return issues
