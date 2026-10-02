# Basic plant monitoring

## Run

From the repository root, after installing `requirements-dev.txt`:

```sh
python synthetic-plant/generate_events.py --scenario basic-plant-monitoring > events.jsonl
python tools/event_contract.py events.jsonl
python tools/analyze_events.py events.jsonl
```

## Expected output

2 asset registrations, 2 pressure measurements and 1 warning alarm. Repeated runs produce the same events and identifiers. Do not concatenate runs without renaming IDs; duplicate IDs are deliberately rejected by the analyzer.

## Exercise

Review the asset IDs and units. Identify the owner who would verify each source and the person who would review the alarm.

## Boundary

Synthetic local files only. No command reaches a PLC, Hub endpoint or industrial network. The output verifies the exercise, not a control implemented in a real installation.
