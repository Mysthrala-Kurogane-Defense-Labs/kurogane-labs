#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone

def ts():
    return datetime(2026, 1, 1, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")

events = [
    {"type": "asset", "event_id": "evt-synthetic-asset-001", "occurred_at": ts(), "site_id": "site-synthetic-alpha", "asset_id": "pump-1", "name": "Synthetic Pump 1"},
    {"type": "telemetry", "event_id": "evt-synthetic-telemetry-001", "occurred_at": ts(), "site_id": "site-synthetic-alpha", "asset_id": "compressor-1", "metric": "pressure_bar", "value": 6.4, "unit": "bar"},
    {"type": "alarm", "event_id": "evt-synthetic-alarm-001", "occurred_at": ts(), "site_id": "site-synthetic-alpha", "asset_id": "pump-1", "severity": "warning", "message": "Synthetic pressure deviation"}
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="print one deterministic batch")
    parser.parse_args()
    for event in events:
        print(json.dumps(event, sort_keys=True))
