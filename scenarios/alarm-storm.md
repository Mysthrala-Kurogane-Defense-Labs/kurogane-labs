# Alarm storm

## Run

From the repository root, after installing `requirements-dev.txt`:

```sh
python synthetic-plant/generate_events.py --scenario alarm-storm > events.jsonl
python tools/event_contract.py events.jsonl
python tools/analyze_events.py events.jsonl
```

## Expected output

22 events: 2 asset registrations, 10 critical alarms and 10 warning alarms. Repeated runs produce the same events and identifiers. Do not concatenate runs without renaming IDs; duplicate IDs are deliberately rejected by the analyzer.

## Exercise

Compare severity counts. Decide what deduplication, escalation and acknowledgment policy a real receiver would need. This finite dataset does not benchmark receiver throughput.

## Boundary

Synthetic local files only. No command reaches a PLC, Hub endpoint or industrial network. The output verifies the exercise, not a control implemented in a real installation.
