# Test connector logic

Source: <https://developer.devrev.ai/airsync/unit-testing>
Scraped: 2026-11-03

## Unit-test contracts

Test worker logic as a function returning `TaskResult`, and use SDK root exports `createTestExtractionAdapter` or `createTestLoadingAdapter` when a real adapter is useful. Test adapters still call the URLs in their event: pair them with `MockServer`/`createMockEvent` rather than a production event.

Use plain doubles for timeout branches and external clients. Cover:

* Success, `progress`, `delay` with seconds, and `error` outcomes; propagation from nested helpers.
* Empty responses, multiple pages, missing/expired cursors and resumption after partial output.
* API 429/retry-after, transient server failures, invalid credentials and unavailable sync units.
* Resolved `extract_from`/`extract_to`, boundaries and historical completion.
* Selected versus excluded record types, including dependencies needed for references.
* Missing mapper records as `null`, existing mappers and API lookup failures.
* Attachment download failures, streaming delays, parent identity and custom processing when implemented.
* Reverse-sync create/update outcomes, relationship ordering and prevention of repeated writes.

Check emitted artifacts, external write counts and worker results. A test that only checks the worker exists provides little evidence of correctness.

Related: [Validation checklist](validation.md).

Next: [Deploy to a test organization](deploy-to-organization.md).
