# Create a project from the public template

Source: <https://developer.devrev.ai/airsync/snap-in-template>
Scraped: 2026-11-03

The [public AirSync template](https://github.com/devrev/airsync-template) supplies an AirSync SDK connector, fixture runner and development server. Use it as the starting point for a new connector. Its Todo implementation uses demonstration data; cloning it does not create an integration with your external API.

## Runtime and dependency requirements

Use Node.js 20 or newer, npm and Git. Always install the latest stable release within SDK major version 2. The major selector below excludes a future v3 and prereleases; the lockfile records the exact version resolved for validation.

```bash
git clone https://github.com/devrev/airsync-template.git my-connector
cd my-connector/code
npm ci
npm install --save-exact '@devrev/airsync-sdk@2'
npm ls @devrev/airsync-sdk
cp .env.example .env
```

Alternatively, use GitHub's **Use this template** action to create a repository with your own history. Commit the resulting `package.json` and lockfile together. Keep `.env` and real tokens out of Git. The template's SDK dependency may lag the latest stable release; verify its compatibility after upgrading.

## Connector file ownership

| File or directory, relative to the project root                    | Responsibility                                                                                    |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| `manifest.yaml`                                                    | Import identity, extraction/loading function names, connections and DevRev service-account scopes |
| `code/src/function-factory.ts`                                     | Export the function names declared by the manifest                                                |
| `code/src/functions/extraction/index.ts`                           | Route extraction events to workers                                                                |
| `code/src/functions/extraction/workers/`                           | Discover sync units; emit metadata, normalized records and attachments                            |
| `code/src/functions/loading/index.ts` and `workers/`               | Route reverse-sync events and write to the external API                                           |
| `code/src/functions/external-system/http-client.ts`                | Replace in-memory Todo methods with authenticated API requests and pagination                     |
| `code/src/functions/external-system/types.ts`                      | External API and normalized data types                                                            |
| `code/src/functions/external-system/data-normalization.ts`         | Convert API records into the declared external domain model                                       |
| `code/src/functions/external-system/data-denormalization.ts`       | Convert reverse-sync records into external API write payloads                                     |
| `code/src/functions/external-system/external_domain_metadata.json` | Record types, field types and reference relationships                                             |
| `code/src/functions/external-system/initial_domain_mapping.json`   | Default choices for mapping the external domain to DevRev                                         |
| `code/fixtures/` and `code/src/test-runner/`                       | Local events, state and extraction scope; mocked DevRev-side execution                            |
| `code/test/`                                                       | Development HTTP server for receiving live platform events                                        |

## Project layout and entry point

The public template separates extraction and loading function directories. Each contains `workers/` and its entry point. External schema, initial domain mapping and normalization live under `code/src/functions/external-system/`; `manifest.yaml` declares the snap-in package.

Save this extraction entry point under `code/src/functions/extraction/index.ts`, alongside the template's `external-system/initial_domain_mapping.json`. Package workers whose compiled paths match the default routing. Stateful SDK initialization requires a valid initial domain mapping when its version state is missing or changes.

```typescript
import { spawn, type AirSyncEvent } from '@devrev/airsync-sdk';
import initialDomainMapping from '../external-system/initial_domain_mapping.json';

type State = { cursor: string | null };

export default async function extraction(events: AirSyncEvent[]): Promise<void> {
  for (const event of events) {
    await spawn<State>({
      event,
      initialState: { cursor: null },
      initialDomainMapping,
      baseWorkerPath: __dirname,
    });
  }
}
```

## Required replacements

Replace the external-system client, API types, normalization, metadata and initial mapping as one consistent change. A field emitted by normalization must match its metadata type. A default mapping must refer to declared fields and valid DevRev targets. Scope discovery must return real external sync units that the connection can access.

Replace the template's keyring verification URL with an authenticated external endpoint; a successful request to a public favicon does not validate a token. Decide whether reverse sync is supported. If it is not, remove both `loader_function` and the loading function from the [manifest](manifest.md).

Implement pagination, continuation, time windows and error handling for your API. The demonstration client's in-memory lists are not durable storage and its simulated pagination is not a production cursor implementation. Attachment fixtures can still fetch a real URL.

## Verify the starting project

Run these commands from `code/`. The current template provides the Jest script but no matching unit tests; add connector tests before expecting `npm test` to pass:

```bash
npm run build
npm run lint
npm test -- --runInBand
npm start -- --fixturePath start_extracting_external_sync_units
npm start -- --fixturePath start_extracting_data
```

Inspect `code/extracted_files/` and the returned worker outcomes. A successful process exit alone does not establish correct record counts or mappings. Use the [validation contracts](validation.md) for observable pass conditions, [local development](local-development.md) for test environments and the [Asana code map](snap-in-examples.md) for a larger integration example.

Next: [Configure connections and authentication](authentication.md).
