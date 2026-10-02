# Telemetry gap

## Run

From the repository root, after installing `requirements-dev.txt`:

```sh
python synthetic-plant/generate_events.py --scenario network-drop > events.jsonl
python tools/event_contract.py events.jsonl
python tools/analyze_events.py events.jsonl
```

## Expected output

8 events: 2 assets and 6 telemetry events, with a maximum gap of 360 seconds for each asset. Repeated runs produce the same events and identifiers. Do not concatenate runs without renaming IDs; duplicate IDs are deliberately rejected by the analyzer.

## Exercise

Compare the timestamps at 0, 60 and 420 seconds. The script omits observations; it does not interrupt a real connection. A network fault, stopped source or collection failure would require separate evidence.

## Boundary

Synthetic local files only. No command reaches a PLC, Hub endpoint or industrial network. The output verifies the exercise, not a control implemented in a real installation.
