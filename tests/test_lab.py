import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from event_contract import validate
from analyze_events import analyze
spec = importlib.util.spec_from_file_location("generator", ROOT / "synthetic-plant/generate_events.py")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)

class LabTest(unittest.TestCase):
    def test_every_scenario_has_valid_unique_events(self):
        for scenario in generator.SCENARIOS:
            events = generator.generate(scenario)
            for event in events:
                validate(event)
            self.assertEqual(len(events), len({event["event_id"] for event in events}))
            self.assertEqual(analyze(events)["unregistered_when_observed"], [])

    def test_alarm_count_and_severities(self):
        report = analyze(generator.generate("alarm-storm", 20))
        self.assertEqual(report["event_count"], 22)
        self.assertEqual(report["alarm_severities"], {"critical":10,"warning":10})

    def test_gap_is_measured_per_site_asset_metric(self):
        events = generator.generate("network-drop")
        report = analyze(events)
        self.assertEqual(report["counts"], {"asset":2,"telemetry":6})
        self.assertEqual([row["max_gap_seconds"] for row in report["telemetry_gaps"]], [360,360])
        other_site = copy.deepcopy(events[-1])
        other_site.update(site_id="other-site", event_id="other-site-event")
        other_site["occurred_at"] = "2026-01-01T00:00:00Z"
        self.assertEqual(analyze(events+[other_site])["unregistered_when_observed"],
                         [{"site_id":"other-site","asset_id":"compressor-1"}])

    def test_basic_and_operator_reports(self):
        for scenario in ("basic-plant-monitoring", "operator-visibility"):
            report = analyze(generator.generate(scenario))
            self.assertEqual(report["counts"], {"alarm":1,"asset":2,"telemetry":2})
            self.assertEqual(report["registered_assets"], 2)

    def test_duplicate_invalid_and_out_of_order_rejected(self):
        events = generator.generate("network-drop")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            analyze(events+[events[-1]])
        invalid = copy.deepcopy(events)
        invalid[-1]["value"] = True
        with self.assertRaises(ValueError):
            analyze(invalid)
        with self.assertRaisesRegex(ValueError, "out of order"):
            analyze(events[:2]+list(reversed(events[2:])))

    def test_cli_is_reproducible_and_finite(self):
        for scenario in generator.SCENARIOS:
            cmd = [sys.executable, str(ROOT / "synthetic-plant/generate_events.py"), "--scenario", scenario]
            first = subprocess.check_output(cmd, timeout=10)
            self.assertEqual(first, subprocess.check_output(cmd, timeout=10))
            self.assertEqual(len(first.splitlines()), len(generator.generate(scenario)))
            for line in first.splitlines():
                validate(json.loads(line))

    def test_cli_invalid_count_fails(self):
        for count in (0,10001):
            result = subprocess.run([sys.executable, str(ROOT / "synthetic-plant/generate_events.py"),
                                     "--count", str(count)], capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 2)

    def test_nodered_flow_uses_same_valid_synthetic_dataset(self):
        flow = json.loads((ROOT / "nodered/flows.example.json").read_text(encoding="utf-8"))
        self.assertEqual({node["type"] for node in flow}, {"tab", "inject", "function", "debug"})
        function = next(node for node in flow if node["type"] == "function")
        payload = function["func"].split("const events = ", 1)[1].split(";\nreturn", 1)[0]
        events = json.loads(payload)
        self.assertEqual(events, generator.generate())
        for event in events:
            validate(event)

if __name__ == "__main__":
    unittest.main()
