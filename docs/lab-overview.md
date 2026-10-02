# Lab overview

The generator reads `synthetic-plant/plant_model.json` and emits deterministic JSONL. The local validator applies contract 0.2. The analyzer counts events, registers `(site_id, asset_id)` pairs, and measures telemetry intervals separately by site, asset and metric.

The generator intentionally uses fixed timestamps and fixed IDs so tests are reproducible. They are not current measurements. Repeating or combining files requires an explicit ID policy.

The default path needs Python only. Compose supplies a finite generator container and an optional Node-RED editor. The editor flow produces local synthetic messages; it does not receive a live plant feed.

An output to retain from an exercise is the JSONL file, the analyzer report, the selected scenario and the repository commit. This lets another person repeat the observation. It cannot establish production reliability, latency, safety or private-core interoperability.
