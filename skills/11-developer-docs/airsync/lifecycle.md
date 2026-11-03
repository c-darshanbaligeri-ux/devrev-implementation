# How synchronization works

Source: <https://developer.devrev.ai/airsync/lifecycle>
Scraped: 2026-11-03

AirSync coordinates synchronization between an external system and DevRev. Your connector implements the external-system operations; the platform schedules the work and transforms data according to the configured mappings.

## Extraction lifecycle

Before an import is configured, the connector discovers the external sync units the connected account can access. The user chooses a project, workspace or other boundary and configures its mapping to DevRev.

A configured extraction run then follows this flow:

1. **Metadata:** describe the external record types, fields and relationships.
2. **Data:** read the selected records and normalize them to that schema.
3. **Attachments:** fetch files associated with the extracted records.
4. **Transformation and import:** AirSync uses the selected mapping to turn uploaded data into DevRev objects.

Your extraction worker supplies external records rather than creating DevRev objects directly. AirSync handles the mapping and import.

## Continuation lifecycle

A phase can take longer than one worker invocation. The connector saves progress, such as a pagination cursor, and returns a result asking AirSync to continue. The next invocation starts a fresh worker with the saved state.

For example, an import of 10,000 tasks may need several invocations of the data phase. It remains one phase of the same run. A rate limit can delay continuation without discarding completed work.

Discovery and state cleanup do not support this continuation model. Implementation details are in [worker results](worker-results.md) and [connector state](connector-state.md).

## Reverse-sync lifecycle

When reverse sync is configured, AirSync prepares DevRev changes in the external data model. A loading worker converts those values into external API requests and creates or updates records. Attachment uploads use a separate worker after their owning records have an external identity.

An object mapper connects the external and DevRev identities so later changes reach the corresponding record. Implement only the operations supported by the external API and advertised by your connector.

## State deletion

State cleanup events remove synchronization state. They do not mean deleting business records from either system. The SDK handles their acknowledgement; a connector can add bounded cleanup when needed.

<span id="verification" />

<span id="terms" />

The [terminology page](terminology.md) defines these concepts. The implementation guides explain how to verify initial imports, continuation and changes in both directions.

Next: [Connector components and responsibilities](getting-started.md).
