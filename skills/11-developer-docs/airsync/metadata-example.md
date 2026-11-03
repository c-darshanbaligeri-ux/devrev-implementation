# External schema example

Source: <https://developer.devrev.ai/airsync/metadata-example>
Scraped: 2026-11-03

## Complete EDM example

This example describes the connector's normalized records; replace the model with your external system's schema.

```typescript
import type { ExternalDomainMetadata } from '@devrev/airsync-sdk';

export const metadata: ExternalDomainMetadata = {
  schema_version: 'v0.2.0',
  record_types: {
    users: {
      fields: {
        id: { type: 'text', is_identifier: true, is_required: true },
        name: { type: 'text', is_required: true },
      },
    },
    tasks: {
      is_loadable: true,
      attachments: { is_extractable: true, is_loadable: true },
      fields: {
        id: { type: 'text', is_identifier: true, is_required: true },
        title: { type: 'text', is_required: true },
        owner: {
          type: 'reference',
          reference: { refers_to: { '#record:users': {} } },
        },
        status: {
          type: 'enum',
          enum: { values: [{ key: 'open' }, { key: 'done' }] },
        },
      },
    },
  },
};
```

Related: [External domain metadata](external-domain-metadata.md).

Next: [Describe categories, conditions and stages](metadata-advanced.md).
