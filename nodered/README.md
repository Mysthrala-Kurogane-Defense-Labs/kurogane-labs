# Optional Node-RED visualization

The sample flow uses builtin Inject, Function and Debug nodes. One button emits five fixed synthetic events; no HTTP, MQTT or PLC nodes are included.

1. Run `docker compose --profile visualization up -d nodered` from the repository root.
2. Open `http://127.0.0.1:1880`. If the port is occupied, set `LAB_HTTP_PORT` to another port before starting Compose.
3. In the editor menu, choose **Import**, select `nodered/flows.example.json` from your checkout and import it as a new flow.
4. Click **Deploy**, open the Debug sidebar, then click the Inject button once. Expect five messages: two assets, two telemetry events and one warning alarm.
5. Confirm there are no external network nodes. Deploy saves to the writable named volume. `/data/public-examples` is read-only reference material, not an automatically loaded flow.

The editor is unauthenticated. Keep it local and do not publish it through a tunnel or reverse proxy. For any shared use, follow [Node-RED security guidance](https://nodered.org/docs/user-guide/runtime/securing-node-red). Read [Docker port-publishing behavior](https://docs.docker.com/engine/network/port-publishing/) for your engine version.

Stop with `docker compose --profile visualization down`; editor changes persist in the named volume. Importing the example repeatedly creates duplicate exercises; delete duplicates through the editor if needed.
