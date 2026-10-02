#!/usr/bin/env python3
"""Read-only report from validated local events. Gaps do not prove network faults."""
import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from event_contract import load, validate

def analyze(events):
    ids, assets, unknown = set(), set(), set()
    counts, alarms, times = Counter(), Counter(), defaultdict(list)
    for event in events:
        validate(event)
        if event["event_id"] in ids:
            raise ValueError("duplicate event_id: " + event["event_id"])
        ids.add(event["event_id"])
        counts[event["type"]] += 1
        asset = event["asset_id"]
        identity = (event["site_id"], asset)
        if event["type"] == "asset":
            assets.add(identity)
        elif identity not in assets:
            unknown.add(identity)
        if event["type"] == "alarm":
            alarms[event["severity"]] += 1
        if event["type"] == "telemetry":
            key = (event["site_id"], asset, event["metric"])
            stamp = datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00"))
            if times[key] and stamp < times[key][-1]:
                raise ValueError("telemetry is out of order for " + repr(key))
            times[key].append(stamp)
    gaps = [{"site_id":site, "asset_id":asset, "metric":metric,
             "max_gap_seconds":max(((b-a).total_seconds() for a,b in zip(stamps, stamps[1:])), default=0)}
            for (site,asset,metric),stamps in sorted(times.items())]
    return {"event_count":len(ids), "counts":dict(sorted(counts.items())),
            "alarm_severities":dict(sorted(alarms.items())), "registered_assets":len(assets),
            "unregistered_when_observed":[{"site_id":s,"asset_id":a} for s,a in sorted(unknown)],
            "telemetry_gaps":gaps, "interpretation":"Synthetic observations; no diagnosis of a physical process or network."}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file")
    args = parser.parse_args()
    print(json.dumps(analyze(load(args.file)), indent=2, allow_nan=False))

if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
