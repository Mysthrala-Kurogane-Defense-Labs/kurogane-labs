# Safety notes

Run these exercises on a development machine using synthetic files. No plant network, customer endpoint or real controller is needed.

- Keep the unauthenticated Node-RED editor on loopback. A shared machine still needs an access decision.
- Do not add production credentials or tunnel the editor to the Internet.
- Do not treat generated alarms as process limits, interlocks or safety instructions.
- Do not scan, poll or modify real OT equipment from this lab without a separate approved scope and vendor constraints.

There is no production deployment, transport authentication, process actuation or safety certification here. A successful lab proves that the documented synthetic exercise ran. For a real assessment, agree the asset owner, authorized read-only sources, permitted activity, maintenance window and stop conditions separately.
