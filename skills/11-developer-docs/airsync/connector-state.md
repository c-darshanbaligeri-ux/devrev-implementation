# Save connector state

Source: <https://developer.devrev.ai/airsync/connector-state>
Scraped: 2026-11-03

This applies to stateful extraction and loading workers. See [worker routing](runtime.md) for initialization.

## Connector state and persistence

`adapter.state` stores your connector's JSON data: pagination cursors, phase progress and idempotency intent. The SDK's state envelope and extraction boundaries are internal. Extraction and loading use separate state. A write to extraction state does not appear in a loading worker.

Stateful invocations load state before calling the task. The SDK flushes extraction repos, saves state and emits the result in that order. `initialState` seeds missing state; it is not a reset on every invocation. Reinitialize phase-local progress when a genuinely new run begins, and preserve it for continuations and replayed events within that run.

`postState()` saves immediately and throws on failure. It is useful for recording write intent before an external mutation, but it does not provide atomicity with that mutation. Use source idempotency keys or read-after-write reconciliation to recover an ambiguous outcome. For extraction, avoid persisting a cursor ahead of buffered records that have not uploaded. Large connector-owned datasets can use `uploadArtifact`/`downloadArtifact`; store only their references in state. Such uploads are not reported as extracted output.

Discovery and deletion are stateless. Do not use them for work that requires an SDK-persisted continuation cursor. See [state deletion](data-attachments-deletion.md) for cleanup limitations.

Related: [Worker routing](runtime.md).
