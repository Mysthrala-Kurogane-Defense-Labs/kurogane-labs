#!/usr/bin/env python3
"""Finite, deterministic synthetic events. No network or PLC access."""
import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

MODEL = json.loads(Path(__file__).with_name("plant_model.json").read_text(encoding="utf-8"))
START = datetime(2026, 1, 1, tzinfo=timezone.utc)
SCENARIOS = ("basic-plant-monitoring", "alarm-storm", "network-drop", "operator-visibility")

def generate(scenario="basic-plant-monitoring", count=20):
    if scenario not in SCENARIOS:
        raise ValueError("unsupported scenario")
    if not isinstance(count, int) or isinstance(count, bool) or not 1 <= count <= 10000:
        raise ValueError("count must be an integer from 1 to 10000")
    events = []
    def emit(kind, asset, seconds, **fields):
        events.append(dict(type=kind, event_id=f"{scenario}-{len(events)+1:05d}",
                           occurred_at=(START+timedelta(seconds=seconds)).isoformat().replace("+00:00", "Z"),
                           site_id=MODEL["site_id"], asset_id=asset["asset_id"], **fields))
    for asset in MODEL["assets"]:
        emit("asset", asset, 0, name=asset["asset_id"], asset_type=asset["type"])
    if scenario == "alarm-storm":
        for i in range(count):
            emit("alarm", MODEL["assets"][i % 2], i+1,
                 severity="critical" if i % 2 == 0 else "warning", message="Synthetic threshold alert")
    elif scenario == "network-drop":
        for seconds in (0, 60, 420):
            for asset in MODEL["assets"]:
                emit("telemetry", asset, seconds, metric="pressure_bar", value=2.5, unit="bar")
    else:
        for asset in MODEL["assets"]:
            emit("telemetry", asset, 60, metric="pressure_bar", value=2.5, unit="bar")
        emit("alarm", MODEL["assets"][0], 61, severity="warning", message="Synthetic pressure review")
    return events

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=SCENARIOS, default=SCENARIOS[0])
    parser.add_argument("--count", type=int, default=20, help="Alarm count for alarm-storm, 1..10000")
    parser.add_argument("--once", action="store_true", help="Compatibility flag; every run is already finite")
    args = parser.parse_args()
    try:
        events = generate(args.scenario, args.count)
    except ValueError as error:
        parser.error(str(error))
    for event in events:
        print(json.dumps(event, sort_keys=True, allow_nan=False))

if __name__ == "__main__":
    main()
