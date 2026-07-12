"""TEST-005; MASTER-TEST-003."""
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src")); sys.path.insert(0,str(ROOT/"tests"))
from agentic_os.architecture import validate_architecture
from helpers import copy_repo


class ArchitectureTests(unittest.TestCase):
    def test_current_architecture_is_valid(self): self.assertEqual([],validate_architecture(ROOT))
    def test_cycle_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); path=root/"architecture.json"; data=json.loads(path.read_text()); data["modules"]["src/agentic_os"]["may_import"]=["scripts"]; path.write_text(json.dumps(data))
            self.assertTrue(any("cycle" in issue for issue in validate_architecture(root)))
    def test_cross_layer_import_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); path=root/"src/agentic_os/bad.py"; path.write_text("import scripts.ados\n")
            self.assertTrue(any("not allowed" in issue for issue in validate_architecture(root)))


if __name__=="__main__": unittest.main()
