# Install and update connector mappings

Source: <https://developer.devrev.ai/airsync/mapping-installation>
Scraped: 2026-11-03

The initial domain mapping file belongs to the connector package. The SDK makes its options available when the snap-in is initialized or upgraded; users select their mapping configuration for an import.

## Install the bundled mapping

Pass IDM to both extraction and loading `spawn()` entry points:

```typescript
import { AirSyncEvent, spawn } from '@devrev/airsync-sdk';
import initialDomainMapping from '../external-system/initial_domain_mapping.json';

export default async function run(events: AirSyncEvent[]): Promise<void> {
  for (const event of events) {
    await spawn({
      event,
      initialState: {},
      initialDomainMapping,
      baseWorkerPath: __dirname,
    });
  }
}
```

The SDK installs the bundled mapping when its stateful lifecycle detects a snap-in version change. Do not call the underlying installation endpoints or reinstall the mapping in each worker. Supplying `starting_recipe_blueprint` is best-effort: its creation can fail while installation of the additional mappings continues. Verify the resulting user choices rather than assuming a successful task proves the optional blueprint was created.

## Update a mapping

A changed external schema or target metadata revision may require updated mapping options. Package the revised JSON with the new snap-in version and test it with a new import.

An existing sync unit has a selected recipe. Do not assume that updating the bundled mapping changes that recipe. Check existing imports separately, including their field choices and persisted state.

## Verify installation and upgrades

Confirm the expected record and field options appear in a new import. If you include a starting recipe blueprint, verify it was created. Test an upgrade against an existing import before release.

Next: [Extract and normalize records](data-extraction.md).
