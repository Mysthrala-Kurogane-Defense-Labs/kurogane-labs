# Synthetic data policy

Use invented site and asset identifiers, fixed synthetic timestamps and explicit simulated values. Do not copy customer inventory, packet captures, credentials, names, addresses, topology or configuration into examples or issues.

Generated files remain local and ignored by Git. Before contributing a fixture, confirm its provenance and validate it with `tools/event_contract.py`. Check that every event is invented, every identifier is synthetic, and no URL or extension contains a secret.

The schema accepts extension fields but cannot detect sensitive information. Passing validation does not authorize publication. Fixtures in this repository are illustrative and must not be mistaken for physical measurements.
