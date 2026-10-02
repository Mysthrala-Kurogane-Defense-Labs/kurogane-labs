# Operator visibility

## Run

From the repository root, after installing `requirements-dev.txt`:

```sh
python synthetic-plant/generate_events.py --scenario operator-visibility > events.jsonl
python tools/event_contract.py events.jsonl
python tools/analyze_events.py events.jsonl
```

## Expected output

5 events: 2 assets, 2 telemetry events and 1 warning; no unregistered assets. Repeated runs produce the same events and identifiers. Do not concatenate runs without renaming IDs; duplicate IDs are deliberately rejected by the analyzer.

## Exercise

Read the local report and list information an operator still needs: source reliability, expected intervals, alarm owner and review time. The report is not a process-control interface.

## Boundary

Synthetic local files only. No command reaches a PLC, Hub endpoint or industrial network. The output verifies the exercise, not a control implemented in a real installation.
