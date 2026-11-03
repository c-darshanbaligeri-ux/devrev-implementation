# Paginated extraction worker example

Source: <https://developer.devrev.ai/airsync/data-extraction-example>
Scraped: 2026-11-03

Use this with [normalized record inputs](data-extraction.md), [selection](extraction-scope.md) and [time windows](extraction-scope.md#resolved-extraction-window).

<span id="bounded-v2-pagination-example" />

## Bounded pagination example

This complete worker demonstrates one source page per invocation. Its example source API returns `{ items, next_cursor }` from `GET /tasks`; replace that API contract with your system's actual endpoint, credentials, response validation and pagination. Supply `EXAMPLE_API_ORIGIN` and `EXAMPLE_API_TOKEN` through your local development environment; deployed code should use its configured connection instead.

```typescript
import {
  NormalizedItem,
  processExtractionTask,
} from '@devrev/airsync-sdk';

type SourceTask = {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
};
type Page = { items: SourceTask[]; next_cursor: string | null };
type State = { runId: string; cursor: string | null; completed: boolean };

function normalize(record: object): NormalizedItem {
  const task = record as SourceTask;
  return {
    id: String(task.id),
    created_date: new Date(task.created_at).toISOString(),
    modified_date: new Date(task.updated_at).toISOString(),
    data: { title: task.title },
  };
}

processExtractionTask<State>({
  task: async ({ adapter }) => {
    const context = adapter.event.payload.event_context;
    if (adapter.state.runId !== context.run_id) {
      adapter.state = { runId: context.run_id, cursor: null, completed: false };
    }
    if (!adapter.shouldExtract('tasks') || adapter.state.completed) {
      return { status: 'success' };
    }
    if (adapter.isTimeout) return { status: 'progress' };

    const origin = process.env.EXAMPLE_API_ORIGIN;
    const token = process.env.EXAMPLE_API_TOKEN;
    if (!origin || !token) throw new Error('Source API configuration is missing');
    const url = new URL('/tasks', origin);
    url.searchParams.set('project_id', context.external_sync_unit_id);
    url.searchParams.set('limit', '100');
    if (adapter.state.cursor) url.searchParams.set('cursor', adapter.state.cursor);
    if (context.extract_from) url.searchParams.set('updated_from', context.extract_from);
    if (context.extract_to) url.searchParams.set('updated_to', context.extract_to);

    const response = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` },
      signal: AbortSignal.timeout(30_000),
    });
    if (response.status === 429) {
      const value = Number(response.headers.get('retry-after'));
      return {
        status: 'delay',
        delaySeconds: Number.isFinite(value) && value > 0 ? value : 30,
      };
    }
    if (!response.ok) {
      return { status: 'error', error: { message: `Source HTTP ${response.status}` } };
    }
    const page = await response.json() as Page;
    if (!Array.isArray(page.items) ||
        !(page.next_cursor === null || typeof page.next_cursor === 'string')) {
      throw new Error('Invalid source page');
    }
    if (page.next_cursor !== null && page.next_cursor === adapter.state.cursor) {
      throw new Error('Source pagination cursor did not advance');
    }

    adapter.initializeRepos([{ itemType: 'tasks', normalize }]);
    const repo = adapter.getRepo('tasks');
    if (!repo) throw new Error('Tasks repo is missing');
    await repo.push(page.items);
    await repo.upload();
    adapter.state.cursor = page.next_cursor;
    adapter.state.completed = page.next_cursor === null;
    return { status: adapter.state.completed ? 'success' : 'progress' };
  },
});
```

The source example assumes numeric `Retry-After`; support HTTP dates if your API sends them. Production code must validate individual source fields before normalizing. Seed the matching state shape in `spawn()`. The run ID prevents a completed prior run's cursor from suppressing a new sync, while continuations reuse it.

Related: [Data extraction](data-extraction.md).

Next: [Fetch multiple pages and resume extraction](pagination.md).
