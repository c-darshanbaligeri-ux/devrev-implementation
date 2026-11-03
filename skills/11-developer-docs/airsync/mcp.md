# Create mappings with an agent

Source: <https://developer.devrev.ai/airsync/mcp>
Scraped: 2026-11-03

An agent can prepare initial domain mappings from external domain metadata and the public mapping contracts. The result is a mapping JSON file used by the connector, not an automatically deployed integration.

## Required inputs and output

Provide the agent with:

* The exact external domain metadata emitted by metadata extraction.
* Representative normalized records for each record type, including nulls, collections and references.
* The connector's intended DevRev target types and supported sync directions.
* The [initial domain mapping contract](initial-domain-mapping.md) and [supported object types](supported-object-types.md).

The agent should produce or modify `initial_domain_mapping.json`, preserving its format version and using only declared external types/fields and supported transformation methods. Mapping a reverse direction does not implement a loader; [reverse sync](loading-phases.md) needs its own code and validation.

## Public workflow

Use the metadata and default mapping files in the [public template](snap-in-template.md) as structural references. Edit the mapping JSON in your repository. Review required target fields, identity fields, references, enum choices, fallback behavior and reversible mappings against the canonical reference.

Run a metadata/extraction fixture and compare the actual records with the schema. Then deploy to a test organization and inspect the offered mapping choices in AirSync. Verify that a new import uses the expected defaults and that required target fields resolve correctly. A JSON parser proves syntax only; it does not prove mapping semantics.

## Suggested agent task

```text
Read the AirSync initial domain mapping and supported object type references.
Use external_domain_metadata.json and representative normalized records.
Update initial_domain_mapping.json for the connector's declared capabilities.
For every target field, identify its source, transformation and missing-value behavior.
Check reference types and required fields. Do not invent schema fields or supported methods.
List ambiguous business choices for review.
Validate the mapping with a new import in a test organization.
```

## MCP scope

A mapping MCP integration, when available in your environment, can expose schema/type lookup, record-type mapping, field mapping and mapping validation. Discover the server's actual tools and parameter schemas before calling them. Always inspect the resulting file and verify it against real metadata and the platform's mapping choices.

MCP access is optional. A mapping server is not required to build a connector. Keep the mapping file in version control and verify it in a test import.

See [metadata extraction](metadata-extraction.md), [initial domain mapping](initial-domain-mapping.md) and [validation](validation.md).
