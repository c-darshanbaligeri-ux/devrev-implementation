# External record loading example

Source: <https://developer.devrev.ai/airsync/data-loading-example>
Scraped: 2026-11-03

Save this worker under `code/src/functions/loading/workers/load-data.ts` in the [public template](snap-in-template.md). Read [loading inputs](load-data.md) and [callback results](load-data.md#loading-callback-results) first.

<span id="v2-data-worker" />

## Data worker

The following worker uses the template's connector-owned helper paths. Implement the helpers against your external API; the template methods are examples, not a working task-service integration.

```typescript
import {
  ExternalSystemItem,
  ExternalSystemItemLoadingParams,
  ExternalSystemItemLoadingResponse,
  processLoadingTask,
} from '@devrev/airsync-sdk';
import { HttpClient } from '../../external-system/http-client';
import { denormalizeTodo } from '../../external-system/data-denormalization';
import type { LoaderState } from '../index';

async function createTodo({ item, event }: ExternalSystemItemLoadingParams<ExternalSystemItem>): Promise<ExternalSystemItemLoadingResponse> {
  const client = new HttpClient(event);
  return client.createTodo(denormalizeTodo(item));
}

async function updateTodo({ item, mappers, event }: ExternalSystemItemLoadingParams<ExternalSystemItem>): Promise<ExternalSystemItemLoadingResponse> {
  const lookup = await mappers.getByTargetId({
    sync_unit: event.payload.event_context.sync_unit,
    target: item.id.devrev,
  });
  const externalId = lookup?.sync_mapper_record.external_ids[0];
  if (!externalId) {
    return { status: 'error', error: { message: 'External task identity is missing.' } };
  }
  const client = new HttpClient(event);
  return client.updateTodo({ ...denormalizeTodo(item), id: externalId });
}

processLoadingTask<LoaderState>({
  task: async ({ adapter }) => adapter.loadItemTypes({
    itemTypesToLoad: [{ itemType: 'todos', create: createTodo, update: updateTodo }],
  }),
});
```

Helper contracts are shown in the public template's [HTTP client](https://github.com/devrev/airsync-template/blob/main/code/src/functions/external-system/http-client.ts) and [denormalization module](https://github.com/devrev/airsync-template/blob/main/code/src/functions/external-system/data-denormalization.ts). Replace their placeholder behavior with API calls, input validation and rate-limit handling.

Related: [Data loading](load-data.md).

Next: [Write related records in dependency order](reverse-sync-ordering.md).
