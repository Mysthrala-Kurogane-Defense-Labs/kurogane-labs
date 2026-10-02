# Kurogane Labs

Four finite, reproducible exercises for asset visibility, alarms and missing telemetry. Everything is synthetic and local. There are no PLC drivers, production connections or private Hub integration.

## For businesses

Start with **operator-visibility** to see what a small asset and alarm report can show. Use it to ask who owns the assets, who reviews alarms and what evidence is missing. A demonstration does not measure risk in your plant; use the [preparation guide](https://github.com/Mysthrala-Kurogane-Defense-Labs/kurogane-docs/blob/main/docs/sme-onboarding.md) for that conversation.

## For technical readers

Requires Python >= 3.11. Docker Compose is optional.

```sh
python -m venv .venv
# Activate .venv: source .venv/bin/activate (Unix), .venv\Scripts\Activate.ps1 (PowerShell)
python -m pip install -r requirements-dev.txt
python synthetic-plant/generate_events.py --scenario basic-plant-monitoring > events.jsonl
python tools/event_contract.py events.jsonl
python tools/analyze_events.py events.jsonl
python -m unittest discover -s tests -v
```

Output files are ignored by Git. Every generator invocation terminates; `--once` remains a compatibility flag. On Windows PowerShell 5, use PowerShell 7 or save stdout as UTF-8 without a BOM, because older shell redirection defaults to UTF-16.

| Scenario | Command option | Expected observation |
| --- | --- | --- |
| [Basic monitoring](scenarios/basic-plant-monitoring.md) | `--scenario basic-plant-monitoring` | 2 assets, 2 telemetry events, 1 warning |
| [Alarm storm](scenarios/alarm-storm.md) | `--scenario alarm-storm --count 20` | 20 alarms: 10 critical, 10 warning |
| [Telemetry gap](scenarios/network-drop.md) | `--scenario network-drop` | 6 measurements; 360-second gap per asset |
| [Operator visibility](scenarios/operator-visibility.md) | `--scenario operator-visibility` | Read-only report for 2 registered assets |

## Optional containers and visualization

```sh
docker compose config --quiet
docker compose run --rm synthetic-plant
docker compose --profile visualization up -d nodered
```

Node-RED is pinned by version and digest, available at `http://127.0.0.1:1880`, and not started by default. Follow the [import instructions](nodered/README.md) to load the real sample flow; merely mounting the directory does not import it. The editor has no configured authentication and is for a trusted local machine only. Loopback publishing reduces exposure; it is not an authorization mechanism.

Stop this project with `docker compose --profile visualization down`. Its named volume retains your editor changes; it contains no required customer data. OpenPLC notes are an extension boundary, not an included PLC runtime.

## Data and limits

The [contract 0.2 schemas](schemas/) mirror the [Satellite SDK](https://github.com/Mysthrala-Kurogane-Defense-Labs/kurogane-satellite-sdk). The analyzer rejects invalid events, duplicate IDs and reversed measurement times. It reports unregistered assets and measures gaps per site, asset and metric. A gap means absent observations, not proof of a network fault or unsafe process.

Read [safety notes](docs/safety-notes.md), [data policy](docs/data-synthetic-policy.md) and [lab overview](docs/lab-overview.md). Code is Apache-2.0; See [license](LICENSE.md).
