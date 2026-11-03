# Route events to workers

Source: <https://developer.devrev.ai/airsync/runtime>
Scraped: 2026-11-03

## Entry point and worker routing

A CommonJS-oriented extraction entry point under `code/src/functions/extraction/index.ts` uses the public SDK and the bundled template mapping. Stateful initialization requires a valid IDM when its version state is missing or changes:

```typescript
import { AirSyncEvent, spawn } from '@devrev/airsync-sdk';
import initialDomainMapping from '../external-system/initial_domain_mapping.json';

type ConnectorState = { cursor: string | null; completed: boolean };

export async function run(events: AirSyncEvent[]): Promise<void> {
  for (const event of events) {
    await spawn<ConnectorState>({
      event,
      initialState: { cursor: null, completed: false },
      initialDomainMapping,
      baseWorkerPath: __dirname,
      options: { timeout: 60_000, batchSize: 2_000 },
    });
  }
}
```

`baseWorkerPath` is the directory containing `workers/`. Package compiled worker files with the snap-in. `workerPathOverrides` maps incoming `EventType` values to path suffixes (for example `/workers/cleanup.js`) appended to that base when a custom layout or deletion worker is needed. Follow the public [template layout](snap-in-template.md) for bundle and manifest wiring.

| Incoming event family                                             | Default worker                         | Can continue? |
| ----------------------------------------------------------------- | -------------------------------------- | ------------- |
| `START_EXTRACTING_EXTERNAL_SYNC_UNITS`                            | `external-sync-units-extraction.js`    | No            |
| `START_EXTRACTING_METADATA`, `CONTINUE_EXTRACTING_METADATA`       | `metadata-extraction.js`               | Yes           |
| `START_EXTRACTING_DATA`, `CONTINUE_EXTRACTING_DATA`               | `data-extraction.js`                   | Yes           |
| `START_EXTRACTING_ATTACHMENTS`, `CONTINUE_EXTRACTING_ATTACHMENTS` | `attachments-extraction.js`            | Yes           |
| `START_LOADING_DATA`, `CONTINUE_LOADING_DATA`                     | `load-data.js`                         | Yes           |
| `START_LOADING_ATTACHMENTS`, `CONTINUE_LOADING_ATTACHMENTS`       | `load-attachments.js`                  | Yes           |
| State-deletion events                                             | No default worker; SDK acknowledgement | No            |

A missing metadata worker is a configuration error. Do not assume a misspelled or unbundled required worker will complete successfully.

<span id="worker-results-and-rate-limits" />

<span id="connector-state-and-persistence" />

<span id="soft-timeout-hard-timeout-and-cancellation" />

Related:

* [Worker results and errors](worker-results.md).
* [Connector state](connector-state.md).
* [Worker timeouts](worker-timeouts.md).
