# Kurogane Labs

Kurogane Labs is a synthetic lab environment in the public technical ecosystem around Kurogane Hub. It demonstrates OT cybersecurity and industrial monitoring concepts without exposing production code, customer configurations, detection logic, or real plant data.

The lab is designed for education, evaluation, and technical discussion by Elixir, Phoenix, PLC, SCADA, NIS2, METI, digital twin, data sovereignty, operational risk, and cyber-physical systems audiences.

## What It Demonstrates

- Basic plant monitoring with synthetic assets.
- Alarm storm behavior using generated events.
- Network drop scenarios with synthetic connectivity loss.
- Remote visibility without remote control.

## Safety

Do not connect this lab to real plants, PLCs, SCADA environments, customer networks, or production Kurogane Hub systems. It is a synthetic lab environment for public demonstration only.

## Run

```bash
docker compose up
python3 synthetic-plant/generate_events.py
```

The compose file uses only public local services and sample containers. It does not require private MKDL infrastructure.

## License

Code, examples, generated data, and lab material are licensed under Apache-2.0.
