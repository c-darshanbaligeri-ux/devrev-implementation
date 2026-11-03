# Key concepts and terminology

Source: <https://developer.devrev.ai/airsync/terminology>
Scraped: 2026-11-03

Use these terms to distinguish connector work from platform transformation and scheduling.

| Term                           | Meaning                                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- |
| External system                | The source or destination API, such as Asana                                           |
| External sync unit (ESU)       | A selectable boundary of external data, such as a project or workspace                 |
| Sync unit                      | The configured synchronization of an external boundary with DevRev                     |
| Sync run                       | A coordinated extraction cycle for a sync unit; a run can contain multiple invocations |
| Invocation                     | One incoming event, one worker execution and one phase outcome                         |
| Extraction                     | External system → DevRev                                                               |
| Normalization                  | External API response → connector's declared external record schema                    |
| Domain transformation          | External records → DevRev objects according to domain mapping                          |
| Loading / reverse sync         | DevRev changes → external system                                                       |
| Denormalization                | Loading input → the external API's write payload                                       |
| External domain metadata (EDM) | Record types, fields, references and capability metadata for the external system       |
| Initial domain mapping (IDM)   | Default recipes mapping external record types and fields into DevRev                   |
| Object mapper                  | Persistent identity correspondence between an external record and a DevRev object      |
| Connector state                | Application-owned cursor/progress data persisted by the SDK                            |

## How the terms fit together

A connection gives a connector access to an external system. The connector discovers external sync units, such as Asana projects. A user selects one and configures its synchronization with DevRev as a sync unit.

A sync run processes that unit through several phases. Each phase can require multiple worker invocations. For example, a data extraction worker can fetch one page, save a cursor and continue in a new invocation.

| Term              | Meaning                                                                                      |
| ----------------- | -------------------------------------------------------------------------------------------- |
| Connection        | Authorized credentials and configuration for accessing an external system                    |
| Snap-in           | The installable DevRev package containing the connector's functions and configuration        |
| Phase             | A stage of synchronization, such as metadata extraction or attachment loading                |
| Worker            | Connector code that handles one phase invocation through an SDK adapter                      |
| Adapter           | SDK-provided access to the event, state, repositories and phase-specific helpers             |
| Repository (repo) | SDK buffer and uploader for one kind of extracted output                                     |
| Checkpoint        | Saved progress from which a later invocation can continue                                    |
| Initial sync      | The first extraction of the configured data range                                            |
| Incremental sync  | Extraction of changes in a subsequent resolved time window                                   |
| Historical sync   | Extraction of earlier history in additional windows                                          |
| Recipe            | The mapping configuration selected for a sync unit from the choices offered by the connector |
| Subtype           | A DevRev type specialization used by an import to represent an external record type          |

For example, an Asana task response is normalized into the connector's task schema. A domain mapping then transforms that record into a DevRev object. The object mapper preserves the correspondence between their identities.

Next: [How synchronization works](lifecycle.md).
