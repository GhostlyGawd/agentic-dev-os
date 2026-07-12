"""TEST-016; MASTER-TEST-007."""
import tempfile
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src")); sys.path.insert(0,str(ROOT/"tests"))
from agentic_os.growth import growth_summary,load_growth_events,record_conversion,write_growth_report
from helpers import copy_repo


class GrowthTests(unittest.TestCase):
    def test_funnel_recording_and_reporting(self):
        with tempfile.TemporaryDirectory() as d:
            root=copy_repo(Path(d)); record_conversion(root,"GROWTH-001","github","visitor",100); record_conversion(root,"GROWTH-001","github","demo",25); summary=growth_summary(load_growth_events(root)); self.assertEqual(.25,summary["conversion_rates"]["visitor_to_demo"]); self.assertTrue(write_growth_report(root).exists())
    def test_invalid_growth_data_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): record_conversion(Path(d),"bad","x","unknown",-1)


if __name__=="__main__": unittest.main()
