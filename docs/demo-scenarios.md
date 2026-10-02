# Demonstration scenarios

Each advertised scenario has an executable generator option and a regression test. See the [scenario table](../README.md#for-technical-readers) for commands and expected outputs.

Basic monitoring and operator visibility intentionally share the five-event dataset but ask different questions: source mapping versus operator review. Alarm storm varies the finite alarm count. Network drop represents missing telemetry; no real network fault is injected.

`python -m unittest discover -s tests -v` checks contract validity, exact counts, reproducibility, duplicate handling, ordering and the per-asset gap. These checks are functional tests of synthetic examples, not a load test or an OT safety assessment.
