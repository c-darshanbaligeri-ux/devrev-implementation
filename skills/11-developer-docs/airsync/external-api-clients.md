# Call the external API

Source: <https://developer.devrev.ai/airsync/external-api-clients>
Scraped: 2026-11-03

## Client contract

A provider request must identify its expected response shape and classify failures. Handle authentication failures, permission failures, rate limits and transient service errors separately. Do not turn an unreadable page or failed request into an empty successful result.

| Input or outcome           | Required handling                                                                                                                                     |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Provider base URL          | Use the documented endpoint and validate tenant-supplied URLs before sending credentials                                                              |
| Credentials                | Read from the authorized connection; do not hard-code or log tokens                                                                                   |
| Successful response        | Validate required identity/pagination fields before normalization                                                                                     |
| HTTP 401/403               | Explain invalid credentials or missing scope without including secrets                                                                                |
| HTTP 429                   | Read provider retry guidance; return `delaySeconds` in resumable phases, or fail non-resumable discovery without reporting a partial list as complete |
| HTTP 5xx / network failure | Apply bounded provider-specific retries or fail the phase; retain the last completed checkpoint                                                       |
| Request timeout            | Abort the request before the worker's remaining execution budget is exhausted                                                                         |
| Empty response             | Distinguish a valid empty page from an unexpected response schema                                                                                     |

The SDK's `AirSyncHttpError` concerns SDK HTTP operations. Your provider client must define or handle its own errors. Map them to [worker outcomes](runtime.md) at the worker boundary.

<span id="bounded-fetch-example" />

<span id="pagination-and-checkpoints" />

Related:

* [External request example](external-fetch-example.md).
* [Pagination and checkpoints](pagination.md).
