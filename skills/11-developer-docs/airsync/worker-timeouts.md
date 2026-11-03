# Handle worker timeouts

Source: <https://developer.devrev.ai/airsync/worker-timeouts>
Scraped: 2026-11-03

Set the timeout through `spawn({ options: { timeout } })`; the value is in milliseconds.

## Soft timeout, hard timeout and cancellation

`options.timeout` is milliseconds, capped at ten minutes. At the soft timeout, `adapter.isTimeout` becomes true. Check it between source pages, record batches and attachment operations; stop acquiring work and return promptly. A task that blocks the event loop cannot see the signal. Yield CPU-heavy loops with `setImmediate` and use finite source-request timeouts.

`onTimeout` runs after the task returns, not concurrently. Once timed out, a returned `progress` or a `success` in a resumable phase is replaced by `onTimeout`'s result; without that callback the default is progress. A returned error or delay remains that result. Non-resumable success remains success; a non-resumable phase that cannot finish must return an error.

At 1.3 times the soft timeout, the SDK can terminate a worker that has not stopped and emit a phase error. It cannot rely on the killed worker to flush buffered output or save its latest cursor. Design replay-safe source reads and writes instead of treating the hard timeout as a checkpoint.

A large collection of artifact references can also set `isTimeout` before the wall-clock deadline. Treat the signal identically regardless of its cause. Do not manually pack large data arrays into control-event payloads.

## Verify runtime behavior

Run the same source page through start and continuation fixtures with a short timeout. Verify that emitted artifacts cover each selected external ID, state resumes at the next unconsumed page, rate limits preserve that page, upload failures do not silently advance it and a hard interruption can replay safely. Inspect only sanitized IDs/counts in connector logs; never log events, keyrings or source payloads wholesale.

See [SDK API](sdk-reference.md), [data extraction](data-extraction.md), [extraction windows](extraction-scope.md) and [local development](local-development.md).

Related: [Worker routing](runtime.md).
