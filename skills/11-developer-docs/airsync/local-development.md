# Run connector events locally

Source: <https://developer.devrev.ai/airsync/local-development>
Scraped: 2026-11-03

Run template fixtures to inspect one phase at a time. Your external API client may still make real requests.

## Run a fixture

From the template's `code/` directory:

```bash
npm ci
cp .env.example .env
npm start -- --fixturePath start_extracting_data
npm start -- --fixturePath start_extracting_data_selective
npm start -- --fixturePath start_loading_data
```

Set the variables referenced by the selected fixture in `code/.env`. Each fixture lives in `code/fixtures/<name>/` and contains `event.json`; it can also contain `state.json` and `extraction_scope.json`. For a continuation fixture, `state.json` must contain the complete captured SDK state envelope, including connector and SDK state; it is not just `adapter.state`. The runner resolves `${VARIABLE_NAME}` placeholders using environment values, merges the event with SDK defaults and serves the supplied state and scope through its mock server. An unset referenced variable fails before the worker runs.

The runner executes one supplied event. It serves the fixture state unchanged and does not save worker state updates back to `state.json` or schedule continuation events. Rerunning the same fixture starts again from the same input. Use the [continuation capture procedure](validation.md#capture-state-for-a-continuation-fixture) to preserve a real run's state.

The runner sets `AIRSYNC_LOCAL_DEVELOPMENT=1`. Local logging and artifact copies are enabled, with artifacts written to `code/extracted_files/`. When invoking your own runner directly, set the same environment variable. Inspect artifacts for the current run rather than assuming older files were replaced.

## Debug a specific phase

Use a fixture when the fault is in your worker logic. Include the same external sync unit, resolved sync window and connector-owned state needed to reproduce it. Use the live server when investigating credential verification, platform mapping or installation behavior. Add a unit test for a reproduced fault, particularly missing mapper records, rate limits and continuation.

Never log the entire event: it contains connection credentials. Redact credentials from captured events before sharing them or committing fixtures. See [troubleshooting](faq.md), [authentication](authentication.md) and [deployment](deploy-to-organization.md).

## Receive live platform events

Use a test organization and the public template server to debug real events locally.

Prerequisites are a working connector, an external test account, permission to install snap-ins in a DevRev organization, the [public DevRev CLI](../snapin-development/references/cli-install.md) and an [ngrok](https://ngrok.com/docs/) account/tunnel. Chef is not required.

Authenticate the CLI to your organization:

```bash
devrev profiles authenticate --org YOUR_ORG_SLUG
```

Start the development server from `code/` and leave it running:

```bash
AIRSYNC_LOCAL_DEVELOPMENT=1 npm run test:server
```

In another terminal, expose port 8000:

```bash
ngrok http 8000
```

From the project root, create a testing version using the HTTPS forwarding URL, then draft and activate that version:

```bash
devrev snap_in_version create-one --manifest ./manifest.yaml --create-package --testing-url https://YOUR_TUNNEL_HOST
devrev snap_in draft --snap_in_version YOUR_VERSION_ID
devrev snap_in activate YOUR_SNAP_IN_ID
```

Take IDs from the commands' responses. The testing URL must remain reachable while a sync runs; restarting the tunnel with another URL requires a version configured for that URL. The development server is for testing; deploy a built version for ongoing operation.

In DevRev, install/configure the connector, create its external connection and start an AirSync import. Validate sync-unit discovery, metadata, mappings, records and attachments using [live validation](validation.md#live-initial-and-incremental-sync). An HTTP acknowledgement from the local server does not mean the asynchronous worker finished successfully.

Related: [local fixtures](local-development.md), [deployment](deploy-to-organization.md).

Next: [Test worker inputs and outputs](fixture-testing.md).
