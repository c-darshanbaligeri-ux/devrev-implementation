# Test continuation and recovery

Source: <https://developer.devrev.ai/airsync/continuation-testing>
Scraped: 2026-11-03

## Capture state for a continuation fixture

The stock template runner executes a single event and its mock server serves static fixture state. Worker state-update requests receive a mock acknowledgement but are not written back to the fixture. It does not automatically continue a run.

For a continuation test, capture the last successful `POST /worker_data_url.update` in your local test harness using the SDK's public `MockServer.getRequests`. Its request body has a `state` **string** containing the complete JSON envelope. Parse that string once, then save the resulting envelope object as the next fixture's `state.json`; do not save the outer HTTP body or only `connectorState`.

This complete helper can be added to a local test harness:

```typescript
import { writeFileSync } from 'node:fs';
import { MockServer } from '@devrev/airsync-sdk';

export function saveContinuationState(server: MockServer, outputPath: string): void {
  const updates = server.getRequests('POST', '/worker_data_url.update');
  const latest = updates[updates.length - 1];
  if (!latest) throw new Error('Worker did not post state');
  const body = latest.body as { state?: unknown };
  if (typeof body.state !== 'string') throw new Error('Expected serialized state');
  const envelope = JSON.parse(body.state);
  writeFileSync(outputPath, JSON.stringify(envelope, null, 2));
}
```

In a copy of the template runner, call this helper with `mockServer` and a new fixture's `state.json` path immediately after `await run([event])`, before stopping the server. Create the output directory first. This is an explicit harness extension; the stock runner does not export captured state. Check that the mock acknowledged the selected update and that the callback requests show a continuation outcome; `getRequests` records attempted requests, including failed ones.

The saved object has `stateVersion: 2`, `connectorState` and `sdkState`. Preserve the entire captured object without constructing or editing SDK bookkeeping. Set the new fixture's event type to the matching continuation event, such as `CONTINUE_EXTRACTING_DATA`, and retain the same sync-unit/run context, scope and relevant event inputs. A new START event can reset phase progress and is not a continuation test.

Run the new fixture and assert resumed cursor/page, artifacts, callback outcome and external call counts. Repeat capture for each continuation. Stock mocks also do not retain uploaded artifact contents; tests that resume loading or download prior artifacts must serve those artifact bodies explicitly, or use a live test sync to validate platform-managed storage.

Related: [Validation checklist](validation.md).

Next: [Test connector logic](unit-testing.md).
