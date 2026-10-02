# Synthetic plant

`plant_model.json` declares two invented assets: pump-1 and compressor-1 at site-synthetic-alpha. `generate_events.py` reads this model and emits a finite JSONL stream with fixed timestamps, values and unique IDs within one run.

Use `--scenario` to select an exercise and `--count 1..10000` to choose the number of alarms in alarm-storm. The flag is ignored by the other scenarios after validating the bound. There is no clock-driven simulator, process model, industrial protocol or network connection.

See the [root README](../README.md) for validation and analysis commands. Model changes require updating expected observations and tests; a configurable plant simulator is outside this example's scope.
