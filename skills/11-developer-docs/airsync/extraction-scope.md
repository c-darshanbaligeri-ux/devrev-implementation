# Extract selected record types

Source: <https://developer.devrev.ai/airsync/extraction-scope>
Scraped: 2026-11-03

Use the import's record selection to decide which source types to fetch. For example, a user may choose tasks while excluding comments.

<span id="selective-extraction" />

## Apply record selection

`adapter.extractionScope` is a dictionary of source item types to `{ extract: boolean }`. Use `adapter.shouldExtract(itemType)` before issuing source API calls. It returns true for an empty scope and for an item type absent from the scope; a present entry returns its `extract` value.

This is a worker-body fragment using the [data extraction](data-extraction.md) state contract:

```typescript
if (!adapter.shouldExtract('tasks')) {
  return { status: 'success' };
}
```

Use the exact metadata/repo key, not a display name. For a multi-type worker, skip that type and continue other enabled types. Keep type-specific completion state coherent when selection changes in a new run. Do not skip necessary reference data silently: define which selected types require users, teams or other relationships, and validate the resulting mapping. Disabled primary records must not generate unattached child records or attachment downloads.

## Verify record selection

Confirm disabled record types generate no source calls or attachment downloads. Check that selected records still have the users, teams and other references their mappings need. Test selection changes between runs.

<span id="resolved-extraction-window" />

<span id="source-query-and-timestamp-semantics" />

<span id="initial-incremental-and-historical-runs" />

<span id="verification" />

Date filtering is covered in [Run incremental and historical extraction](extraction-windows.md).

Next: [Run incremental and historical extraction](extraction-windows.md).
