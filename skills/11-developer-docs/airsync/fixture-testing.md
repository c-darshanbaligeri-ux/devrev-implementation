# Test worker inputs and outputs

Source: <https://developer.devrev.ai/airsync/fixture-testing>
Scraped: 2026-11-03

## Fixture inputs and observable outputs

The [public template](snap-in-template.md) reads fixtures from `code/fixtures/<name>/`:

| File                    | Contract                                                                                                            |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `event.json`            | Required partial event with a valid `payload.event_type`; include connection and event context needed by the worker |
| `state.json`            | Optional fetched state; a continuation fixture requires the complete captured SDK envelope                          |
| `extraction_scope.json` | Optional requested record-type scope; omitted scope defaults to extracting all in the template runner               |

A minimal data event, using a test credential from the environment:

```json
{
  "payload": {
    "event_type": "START_EXTRACTING_DATA",
    "connection_data": {
      "org_id": "test-workspace",
      "org_name": "Test workspace",
      "key": "${EXTERNAL_API_TOKEN}",
      "key_type": "pat"
    },
    "event_context": {
      "external_sync_unit_id": "test-project"
    }
  }
}
```

Define `EXTERNAL_API_TOKEN` in `code/.env`, or rename it to the variable used by your fixture. Run from `code/`:

```bash
npm start -- --fixturePath start_extracting_external_sync_units
npm start -- --fixturePath start_extracting_data
npm start -- --fixturePath start_extracting_data_selective
npm start -- --fixturePath start_loading_data
```

The template mocks DevRev-side endpoints; your external client can still call real APIs. Review loading fixtures before running them. Inspect artifacts in `code/extracted_files/`, phase outcomes and persisted state, not only the process exit status. Assert IDs, item types and record counts; test a continuation event with the captured state to prove it does not omit or duplicate work. Simply rerunning the original fixture repeats its initial state.

Related: [Validation checklist](validation.md).

Next: [Test continuation and recovery](continuation-testing.md).
