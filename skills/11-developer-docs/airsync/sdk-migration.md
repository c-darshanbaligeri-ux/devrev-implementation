# Migrate from SDK v1 to v2

Source: <https://developer.devrev.ai/airsync/sdk-migration>
Scraped: 2026-11-03

## Upgrade sequence

1. Establish a passing baseline on the current supported v1 release, recording existing failures.
2. Finish active syncs and review state compatibility before changing the running connector.
3. Install the latest stable major 2 release from `code/`:

```bash
npm uninstall @devrev/ts-adaas
npm install --save-exact '@devrev/airsync-sdk@2'
npm ls @devrev/airsync-sdk
```

4. Read `code/node_modules/@devrev/airsync-sdk/docs/MIGRATION.md` from the project root. That installed version's guide takes precedence over this summary. Remove stale dependency overrides/resolutions, migrate imports and apply the guide across source and tests.
5. Run type checking, lint, build and tests. Verify fixture and live behavior against an existing import and a fresh import.

The manifest schema version and SDK major version are separate. Modern AirSync event names remain compatible, but v2 does not support the old `EXTRACTION_*` event-name aliases.

## Contract changes to inspect

| Area                    | V2 contract                                                                                     |
| ----------------------- | ----------------------------------------------------------------------------------------------- |
| Worker factories        | `processExtractionTask` and `processLoadingTask` replace the shared v1 factory                  |
| Adapters                | `ExtractionAdapter` and `LoadingAdapter` expose the appropriate phase operations                |
| Worker completion       | Return `TaskResult`; the SDK sends the callback once                                            |
| Outcomes                | Use `status: 'success'`, `'progress'`, `'delay'` or `'error'`; delays use `delaySeconds`        |
| Loader/stream callbacks | Return the callback's explicit status union; successful creates/updates need a real external ID |
| External sync units     | Push to `AirSyncDefaultItemTypes.EXTERNAL_SYNC_UNITS` repo rather than inline event data        |
| Repo options            | Spell `overriddenOptions` correctly; remove `skipConfirmation`                                  |
| External HTTP           | Own your external client/dependencies; do not deep-import the SDK's internal client             |
| Mapper lookup           | Returns an unwrapped value or `null`; missing records do not throw a 404                        |
| State                   | `adapter.state` contains connector-owned state; SDK bookkeeping is internal                     |
| Sync window             | Read resolved event-context `extract_from` and `extract_to`                                     |
| Local execution         | Set `AIRSYNC_LOCAL_DEVELOPMENT=1`; remove legacy local positional arguments                     |
| Test adapters           | Use root `createTestExtractionAdapter` / `createTestLoadingAdapter` and valid mocked events     |

Migrate nested helper results as well as workers. A helper that emits in v1 must return its result to the caller in v2. Mapper existence checks deserve explicit tests: `try { lookup(); return true; } catch { return false; }` treats a v2 `null` lookup as success unless rewritten.

## Migration acceptance

Record source and target versions, applied guide sections, ambiguous behavior choices and check results. Validate interruption/resumption, empty incremental windows, mapper misses, rate limits, attachments and reverse sync when supported. Type-check development runners excluded from the main build.

Keep v1 APIs confined to migration material. Current implementation examples must use SDK v2. See [runtime](runtime.md), [validation](validation.md) and [deployment upgrades](deploy-to-organization.md#upgrade-an-existing-connector).

## Persisted state and rollback

Plan how existing synchronization state will be read after an SDK upgrade and after a rollback.

V2 stores connector state and SDK state separately in a versioned envelope and automatically migrates known v1 SDK keys. After a v2 worker persists state, rolling back to v1 against that state is unsupported.

Audit top-level v1 keys before upgrading. Keys named `connectorState` or `sdkState` can collide with envelope detection. Rename and migrate those persisted keys in a staged v1 deployment, or explicitly reset/reinitialize and reimport. If the connector owns a cursor named `lastSuccessfulSyncStarted`, migrate its value into a distinct connector key before upgrading; a source-only rename can lose the cursor when the old name moves into SDK state.

When the old value came from SDK bookkeeping, replace its reads with the resolved sync window rather than copying it into connector state. Connector-owned nested cursors remain your responsibility. Record uncertain classifications and test actual persisted state; compilation does not prove a correct migration.

Drain attachment runs that rely on v1 workarounds before upgrading. Remove code that mutates internal upload bookkeeping to carry attachments between phases; v2 owns that behavior. Plan rollback using verified saved compatible state, or a deliberate reset/reimport, rather than assuming an older package restores it.
