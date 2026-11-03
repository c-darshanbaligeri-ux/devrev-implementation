# Custom attachment iterator example

Source: <https://developer.devrev.ai/airsync/attachment-processing-example>
Scraped: 2026-11-03

Read [processor inputs and outputs](customize-attachment-processing.md) before using this example.

<span id="v2-custom-continuation-example" />

## Custom continuation example

This complete worker groups by parent and uses connector state to avoid repeating successful transfers after a continuation. It treats individual errors as phase failures. Source URLs must remain usable; replace `stream` with authenticated URL refresh when required by your source API.

```typescript
import axios from 'axios';
import {
  ExternalSystemAttachmentIteratorFunction,
  ExternalSystemAttachmentReducerFunction,
  ExternalSystemAttachmentStreamingFunction,
  NormalizedAttachment,
  processExtractionTask,
} from '@devrev/airsync-sdk';

type State = { attachmentRunId: string; completedAttachments: string[] };
type Groups = Map<string, NormalizedAttachment[]>;

const reducer: ExternalSystemAttachmentReducerFunction<
  NormalizedAttachment[], Groups, State
> = ({ attachments }) => {
  const groups: Groups = new Map();
  for (const attachment of attachments) {
    const group = groups.get(attachment.parent_id) ?? [];
    group.push(attachment);
    groups.set(attachment.parent_id, group);
  }
  return groups;
};

const stream: ExternalSystemAttachmentStreamingFunction = async ({ item }) => {
  try {
    const response = await axios.get(item.url, {
      responseType: 'stream',
      timeout: 30_000,
      headers: { 'Accept-Encoding': 'identity' },
    });
    return { status: 'success', httpStream: response };
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 429) {
      return { status: 'delay', delaySeconds: 30 };
    }
    return { status: 'error', error: { message: 'Source attachment download failed' } };
  }
};

const iterator: ExternalSystemAttachmentIteratorFunction<Groups, State> = async ({
  reducedAttachments, adapter, stream,
}) => {
  const completed = new Set(adapter.state.completedAttachments);
  for (const attachments of reducedAttachments.values()) {
    for (const attachment of attachments) {
      if (adapter.isTimeout) return { status: 'success' };
      const key = JSON.stringify([attachment.id, attachment.parent_id]);
      if (completed.has(key)) continue;
      const result = await adapter.processAttachment(attachment, stream);
      if (result.status !== 'success') return result;
      if (adapter.isTimeout) return { status: 'success' };
      completed.add(key);
      adapter.state.completedAttachments.push(key);
    }
  }
  return { status: 'success' };
};

processExtractionTask<State>({
  task: async ({ adapter }) => {
    const runId = adapter.event.payload.event_context.run_id;
    if (adapter.state.attachmentRunId !== runId) {
      adapter.state = { attachmentRunId: runId, completedAttachments: [] };
    }
    return adapter.streamAttachments({
      stream,
      processors: { reducer, iterator },
    });
  },
});
```

Seed the same state shape in `spawn`. This example uses a list suitable for a bounded number of attachments; large integrations should use compact cursors or connector-owned artifact references. The custom iterator is sequential: it controls its own concurrency, and the `batchSize` argument does not create a pool around it.

The iterator returns success when it notices timeout because `ProcessAttachmentReturnType` has no progress variant. `streamAttachments` checks `isTimeout` and returns progress without consuming the current descriptor artifact. Do not mark the interrupted item complete. Unlike the built-in pool, custom processors must maintain their own processed-item cursor; SDK deduplication for the default pool does not supply a public custom-iterator cursor.

Related: [Custom attachment processing](customize-attachment-processing.md).

Optional reverse sync: [How reverse sync works](loading-phases.md).

If these optional capabilities are outside your connector's scope, continue to [Run connector events locally](local-development.md).
