# Troubleshoot data imports

Source: <https://developer.devrev.ai/airsync/extraction-troubleshooting>
Scraped: 2026-11-03

Use these checks when the connector fails during extraction.

## Connection passes verification but extraction is unauthorized

The verification endpoint may not exercise the scopes needed by later API calls. Test discovery, metadata, records and attachment endpoints using the same connection account. Replace unauthenticated placeholder verification URLs. Inspect insufficient scopes, revoked access and differences between organization and project permissions. See [authentication](authentication.md).

## Fixture completes but records are wrong or missing

Inspect the current artifacts under `code/extracted_files/`. Verify the selected fixture, external sync unit, extraction scope and resolved time window. Fixture execution can use a real external client and different account permissions from production. Check artifact counts, normalized IDs and metadata types rather than treating the runner's completion message as semantic validation.

## Only the first API page is imported

Implement pagination in the connector's own external client/worker. Persist the next cursor after durable progress and resume when the runtime requests continuation. Do not return `success` while pages remain. The template's in-memory Todo pagination is illustrative. See [data extraction](data-extraction.md).

## Incremental sync misses records or reimports everything

Read the SDK-resolved `extract_from` and `extract_to` from event context. Verify external timestamp semantics, timezone handling and inclusive/exclusive boundaries. Preserve connector-owned cursors separately from SDK bookkeeping. Ensure an empty window does not mean an unconditional full import. See [runtime](runtime.md) and [SDK migration](sdk-migration.md).

Related: [troubleshooting index](faq.md).
