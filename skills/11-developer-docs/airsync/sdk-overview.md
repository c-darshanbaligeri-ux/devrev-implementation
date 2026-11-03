# What the AirSync SDK does

Source: <https://developer.devrev.ai/airsync/sdk-overview>
Scraped: 2026-11-03

The AirSync SDK is the TypeScript library used by a connector to communicate with the AirSync backend. It implements the event and result protocol and provides helpers for extraction and reverse sync.

You implement the external system's behavior: reading its API, converting responses into your declared schema and writing changes back when reverse sync is supported.

## Where the SDK fits

For an import, the flow is:

1. AirSync sends a phase event to the snap-in function.
2. The SDK selects a worker and supplies an adapter with the event and saved state.
3. Your worker reads the external API and sends normalized records through SDK repositories.
4. The SDK uploads output, saves progress and reports the phase result to AirSync.
5. AirSync transforms the records according to the configured mappings and imports them into DevRev.

For reverse sync, AirSync prepares changes in the external data model. The SDK supplies loading helpers; your callbacks turn the supplied values into external API requests.

## Responsibilities

| SDK and platform                            | Your connector                                              |
| ------------------------------------------- | ----------------------------------------------------------- |
| Event routing and worker startup            | Functions and workers packaged in the snap-in               |
| Adapters, output repositories and uploads   | External API requests and response normalization            |
| State persistence and continuation protocol | Cursors and markers that describe completed work            |
| Phase results and timeout handling          | Returning the appropriate result and stopping work promptly |
| Applying domain mappings                    | External schema and default mapping definitions             |
| Loading progress and identity helpers       | External writes, relationship handling and retry recovery   |

The SDK does not supply a general-purpose HTTP client for the external system. You choose the client and implement authentication headers, provider pagination and rate-limit handling.

The public package is `@devrev/airsync-sdk`. These docs cover its current major version, 2. Installation requirements belong to [project setup](snap-in-template.md); exported APIs are listed in the [SDK reference](sdk-reference.md).

Next: [Create a project from the public template](snap-in-template.md).
