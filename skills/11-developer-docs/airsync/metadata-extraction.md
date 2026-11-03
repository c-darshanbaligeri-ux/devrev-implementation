# Extract and upload schema metadata

Source: <https://developer.devrev.ai/airsync/metadata-extraction>
Scraped: 2026-11-03

## Before implementing the worker

Define the [external schema](external-domain-metadata.md) and its [fields and references](metadata-fields.md) first. Record-type keys must match the repositories and normalized records your data worker emits.

<span id="metadata-structure" />

<span id="complete-bounded-v2-example" />

## Complete bounded example

This static example describes `tasks`; a production schema must also declare its references, custom fields and other emitted record types.

```typescript
import {
  AirSyncDefaultItemTypes,
  ExternalDomainMetadata,
  processExtractionTask,
} from '@devrev/airsync-sdk';

const metadata: ExternalDomainMetadata = {
  schema_version: 'v0.2.0',
  record_types: {
    tasks: {
      name: 'Tasks',
      fields: {
        title: { type: 'text', is_required: true },
        item_url_field: { type: 'text' },
      },
    },
  },
};

processExtractionTask<Record<string, never>>({
  task: async ({ adapter }) => {
    const itemType = AirSyncDefaultItemTypes.EXTERNAL_DOMAIN_METADATA;
    adapter.initializeRepos([{ itemType }]);
    const repo = adapter.getRepo(itemType);
    if (!repo) throw new Error('Metadata repo is missing');
    await repo.push([metadata]);
    return { status: 'success' };
  },
});
```

Metadata output goes through the repo without data normalization. Workers return `TaskResult`; the SDK emits `METADATA_EXTRACTION_DONE`, `*_PROGRESS`, `*_DELAYED` or `*_ERROR`. If dynamic discovery requires continuation, persist its cursor in connector state and emit complete coherent schema output. Do not return success while required field discovery is incomplete.

## Counts and schema validation

Optionally set `adapter.preExtractionItemCounts` during metadata extraction. Each entry contains `record_type`, `count` and `model_input_type: ItemInputType.MAIN` or `ItemInputType.USERS`. The SDK attaches counts to metadata-done for duration estimation. Report trustworthy counts; omit them when unavailable instead of expensive enumeration merely for estimation.

Validate EDM against the [public JSON schema](https://github.com/devrev/airsync-sdk/blob/main/src/tests/external-domain-metadata/external_domain_metadata_schema.json), then verify semantic consistency with the [mapping workflow](mcp.md). Validate extracted records and mappings together: JSON schema validation alone cannot prove that source references resolve or target mappings satisfy DevRev requirements.

Verification must include every repo type, required field, enum key, category and reference target, plus changes to dynamic fields between runs. Test missing metadata worker and schema-download failures explicitly. Related: [data extraction](data-extraction.md), [supported objects](supported-object-types.md), [template metadata](https://github.com/devrev/airsync-template/blob/main/code/src/functions/external-system/external_domain_metadata.json).

<span id="field-types-and-references" />

Related:

* [Metadata field types](metadata-fields.md#field-types-and-references).

Next: [Map external records to DevRev objects](initial-domain-mapping.md).
