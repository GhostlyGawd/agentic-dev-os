"""TEST-012; MASTER-TEST-006."""
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src")); sys.path.insert(0,str(ROOT/"tests"))
from agentic_os.tooling import validate_tool_catalog
from helpers import copy_repo


class ToolingTests(unittest.TestCase):
    def test_catalog_is_valid(self): self.assertEqual([],validate_tool_catalog(ROOT))
    def test_bad_name_and_parameter_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); path=root/"tools/catalog.json"; data=json.loads(path.read_text()); data["tools"][0]["name"]="BAD"; data["tools"][0]["parameters"][0]["server_validation"]=""; path.write_text(json.dumps(data)); issues=validate_tool_catalog(root); self.assertGreaterEqual(len(issues),2)


if __name__=="__main__": unittest.main()
