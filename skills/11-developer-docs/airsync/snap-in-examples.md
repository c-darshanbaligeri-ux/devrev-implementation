# Find implementation examples in Asana

Source: <https://developer.devrev.ai/airsync/snap-in-examples>
Scraped: 2026-11-03

Use the [public AirSync template](https://github.com/devrev/airsync-template) for runnable SDK scaffolding. Use the [public Asana connector](https://github.com/devrev/airdrop-asana-snap-in) to study a larger integration's API, domain model, normalization and tests.

## Version compatibility

As checked on 16 October 2026, the public template and Asana use `@devrev/airsync-sdk@2.0.0`. Asana's SDK migration is merged into `main`; the code map below uses revision `ee2a31f4e4ef746c7650f9c78e2f67ac430eec19`.

Use the template for a minimal project and Asana for API integration, normalization, reverse sync and tests. Check `code/package.json` at the revision you use, install its dependencies and run its checks before adapting it to another system. Provider-specific behavior still needs your own implementation and validation.

## Asana code map

Paths below are relative to the Asana repository and link to the checked revision.

| Topic                                               | Public source                                                                                                                                                                                                                                                                                                                     |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| External API client and generated API types         | [`code/src/asana/api-client/`](https://github.com/devrev/airdrop-asana-snap-in/tree/ee2a31f4e4ef746c7650f9c78e2f67ac430eec19/code/src/asana/api-client)                                                                                                                                                                           |
| External types and metadata                         | [`code/src/asana/types.ts`](https://github.com/devrev/airdrop-asana-snap-in/blob/ee2a31f4e4ef746c7650f9c78e2f67ac430eec19/code/src/asana/types.ts), [`external_domain_metadata.json`](https://github.com/devrev/airdrop-asana-snap-in/blob/ee2a31f4e4ef746c7650f9c78e2f67ac430eec19/code/src/asana/external_domain_metadata.json) |
| Normalization and tests                             | [`code/src/asana/data-normalization.ts`](https://github.com/devrev/airdrop-asana-snap-in/blob/ee2a31f4e4ef746c7650f9c78e2f67ac430eec19/code/src/asana/data-normalization.ts) and adjacent `.test.ts`                                                                                                                              |
| Default mappings                                    | [`code/src/asana/initial_domain_mapping.json`](https://github.com/devrev/airdrop-asana-snap-in/blob/ee2a31f4e4ef746c7650f9c78e2f67ac430eec19/code/src/asana/initial_domain_mapping.json)                                                                                                                                          |
| Sync-unit, metadata, data and attachment extraction | [`code/src/functions/extraction/workers/`](https://github.com/devrev/airdrop-asana-snap-in/tree/ee2a31f4e4ef746c7650f9c78e2f67ac430eec19/code/src/functions/extraction/workers)                                                                                                                                                   |
| Reverse-sync denormalization                        | [`code/src/asana/data-denormalization.ts`](https://github.com/devrev/airdrop-asana-snap-in/blob/ee2a31f4e4ef746c7650f9c78e2f67ac430eec19/code/src/asana/data-denormalization.ts) and adjacent `.test.ts`                                                                                                                          |
| Loading and attachment loading                      | [`code/src/functions/loading/workers/`](https://github.com/devrev/airdrop-asana-snap-in/tree/ee2a31f4e4ef746c7650f9c78e2f67ac430eec19/code/src/functions/loading/workers)                                                                                                                                                         |
| Rich text, permissions and loading helpers          | [`code/src/utils/`](https://github.com/devrev/airdrop-asana-snap-in/tree/ee2a31f4e4ef746c7650f9c78e2f67ac430eec19/code/src/utils)                                                                                                                                                                                                 |
| Connection and function declarations                | [`manifest.yaml`](https://github.com/devrev/airdrop-asana-snap-in/blob/ee2a31f4e4ef746c7650f9c78e2f67ac430eec19/manifest.yaml)                                                                                                                                                                                                    |

Read workers together with their helpers, metadata and tests. A source file's existence does not prove every edge case is supported. Validate the capabilities you implement against your own API and installation.

<span id="v2-template-examples" />

## Template examples

The template includes extraction and loading worker families, normalized Todo/user records, metadata/default mapping, attachment handling and fixtures. Its external client uses in-memory demonstration data. Replace it with your own API calls, credential verification, pagination and durable continuation.

Run [project setup](snap-in-template.md), inspect the [runtime contract](runtime.md), and use [validation](validation.md) to check the resulting integration. Neither example replaces the supported-object and mapping references.
