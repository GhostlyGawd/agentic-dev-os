"""TEST-003 TEST-004 TEST-006 TEST-007 TEST-011; MASTER-TEST-002 MASTER-TEST-008 MASTER-TEST-009."""
import os
import tempfile
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src")); sys.path.insert(0,str(ROOT/"tests"))
from agentic_os.governance import LoopManager,approval_valid,archive_ticket,check_scope,grant_approval
from agentic_os.validation import stale_artifacts
from helpers import copy_repo,ready_ticket


class GovernanceTests(unittest.TestCase):
    def test_r2_requires_digest_bound_approval(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); ready_ticket(root,"R2"); manager=LoopManager(root)
            with self.assertRaises(ValueError): manager.start("TICKET-001","agent")
            grant_approval(root,"TICKET-001","reviewer","approved test"); self.assertTrue(approval_valid(root,"TICKET-001")); manager.start("TICKET-001","agent")
            path=root/"docs/tickets/TICKET-001-bootstrap.md"; path.write_text(path.read_text()+"\nchanged\n"); self.assertFalse(approval_valid(root,"TICKET-001"))

    def test_scope_retry_verify_and_completion_gates(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); ready_ticket(root); manager=LoopManager(root); manager.start("TICKET-001","agent")
            manager.action("TICKET-001","agent","edit",["README.md"])
            with self.assertRaises(ValueError): manager.action("TICKET-001","agent","edit",["forbidden.txt"])
            manager.retry("TICKET-001","agent","correction"); manager.verify("TICKET-001","agent",execute=False); manager.stop("TICKET-001","agent","success")

    def test_archive_and_stale_audit(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); destination=archive_ticket(root,"TICKET-001","agent"); self.assertTrue(destination.exists())
            prd=root/"docs/prd/PRD-001-agentic-development-os.md"; os.utime(prd,(1,1)); self.assertIn(str(prd.relative_to(root)),stale_artifacts(root,1))


if __name__=="__main__": unittest.main()
