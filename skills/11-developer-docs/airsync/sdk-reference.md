# SDK API reference

Source: <https://developer.devrev.ai/airsync/sdk-reference>
Scraped: 2026-11-03

```bash
npm install @devrev/airsync-sdk@2
npm ls @devrev/airsync-sdk
```

Commit the resolved lockfile. The SDK major version, metadata version and manifest control-protocol version are separate. Deep package imports are unsupported.

## Entry points and result contract

| Export                                                        | Purpose                                                   |
| ------------------------------------------------------------- | --------------------------------------------------------- |
| `spawn(params)`                               | Main-thread routing, worker creation and timeout handling |
| `processExtractionTask({ task, onTimeout? })` | Extraction worker entry point                             |
| `processLoadingTask({ task, onTimeout? })`    | Loading worker entry point                                |
| `ExtractionAdapter`, `LoadingAdapter`, `BaseAdapter`          | Type-only exports for SDK-created adapters                |
| `TaskResult`, `ProcessTaskInterface`, `TaskAdapterInterface`  | Worker callback contracts                                 |
| `EventType`, `AirSyncEvent`                                   | Incoming event constants and payload                      |
| `AirSyncErrorCode`, `AirSyncHttpError`                        | Recognized error codes and platform-call failures         |

Pass the bundled `initialDomainMapping` to both extraction and loading `spawn()` entry points. Stateful initialization installs it when the stored snap-in version is missing or changes; omitting it then fails initialization before the task runs. See [mapping installation](mapping-installation.md) for the lifecycle and [initial domain mapping](initial-domain-mapping.md) for the file contract and [runtime routing](runtime.md) for entry-point configuration.

`task` and `onTimeout` receive `{ adapter }` and return `Promise`. The public result union is:

```typescript
type TaskResult =
  | { status: 'success' }
  | { status: 'progress' }
  | { status: 'delay'; delaySeconds: number }
  | { status: 'error'; error: { message: string; code?: AirSyncErrorCode } };
```

This is a contract excerpt; `TaskResult` and `AirSyncErrorCode` are exported by the package. Workers return results instead of calling an emitter. See [runtime](runtime.md) for valid outcomes by phase.

## Shared adapter surface

The SDK constructs adapters and passes them to workers. Do not construct them or access internal SDK state.

| Member                                                    | Contract                                                                                     |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `event: AirSyncEvent`                                     | Incoming event, including source connection and resolved event context                       |
| `state: ConnectorState`                                   | JSON-serializable connector-owned state; readable and replaceable                            |
| `isTimeout: boolean`                                      | Read-only signal to stop acquiring work and return                                           |
| `extractionScope`                                         | Parsed source record-type selection                                                          |
| `mappers`                                                 | Sync identity lookup/create/update operations; see [object mappers](object-mappers.md) |
| `postState(): Promise<void>`                              | Save state immediately; throws on failure                                                    |
| `uploadArtifact(itemType, data): Promise<{ id: string }>` | Store connector-owned object arrays as gzipped JSONL; not an extraction-output repo          |
| `downloadArtifact(id): Promise<T[]>`                   | Read such an artifact; throws on failure                                                     |

Do not construct adapters, access internal SDK state, set `isTimeout` or call internal emit methods. State and artifact helpers do not make an external write transactional; persist intent and use source idempotency where available.

## Extraction adapter and repos

Initialize repositories once per invocation, then use them to write extraction output.

| Member                                                                        | Contract                                                                                             |
| ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `initializeRepos(RepoInterface[])`                                            | Create this invocation's repositories; initialize once before extraction                             |
| `getRepo(itemType): Repo \| undefined`                                        | Retrieve an initialized repo; treat missing required repos as configuration errors                   |
| `shouldExtract(itemType): boolean`                                            | Whether that type is enabled; missing scope entries default to `true`                                |
| `preExtractionItemCounts: ItemTypeCount[] \| undefined`                       | Metadata-phase counts for duration estimation                                                        |
| `streamAttachments({ stream, batchSize?, processors? }): Promise` | Consume queued attachment descriptors with SDK continuation                                          |
| `processAttachment(attachment, stream)`                                       | Process one descriptor; see [custom attachment processing](customize-attachment-processing.md) |

`RepoInterface` contains `itemType`, optional `normalize(record: object)` and optional `overriddenOptions: { batchSize?: number }`. A normalizer returns `NormalizedItem` or `NormalizedAttachment`. `repo.push(items)` buffers and uploads full batches; `repo.upload()` flushes the remainder. Both throw on upload failure. Default repo batch size is 2,000 items. Attachment streaming `batchSize` means concurrent streams and is a separate option.

`AirSyncDefaultItemTypes` names `EXTERNAL_DOMAIN_METADATA`, `EXTERNAL_SYNC_UNITS` and `ATTACHMENTS`. Metadata repos bypass normalization. Sync-unit upload confirmation is handled by the SDK; it is not a public repo option.

<span id="loading-and-test-support" />
