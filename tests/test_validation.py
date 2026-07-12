"""TEST-001 TEST-002 TEST-013 TEST-014 TEST-015 TEST-017; MASTER-TEST-001."""
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src")); sys.path.insert(0,str(ROOT/"tests"))
from agentic_os.validation import validate_compliance,validate_repository,validate_trace
from helpers import copy_repo


class ValidationTests(unittest.TestCase):
    def test_complete_repository_is_valid(self): self.assertEqual([],validate_repository(ROOT))

    def test_missing_trace_field_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); path=root/"docs/trace/traceability.json"; data=json.loads(path.read_text()); del data["records"][0]["source_origin"]; path.write_text(json.dumps(data))
            self.assertTrue(any(i.code=="TRACE_FIELDS" for i in validate_trace(root)))

    def test_master_matrix_is_sequential_complete_and_resolved(self): self.assertEqual([],validate_compliance(ROOT))


if __name__=="__main__": unittest.main()
