# AirSync

Source: <https://developer.devrev.ai/airsync>
Scraped: 2026-11-03

AirSync connects data in an external system with DevRev. A connector imports records, attachments and supported access rules. It can also send DevRev changes back to the external system when you implement reverse sync.

These docs explain the complete connector development flow: understand AirSync, set up a project, implement the required capabilities, test the integration and publish it.

## Start here

Read the sections in this order when building your first connector:

| Section                                                      | What you will learn or build                                            |
| ------------------------------------------------------------ | ----------------------------------------------------------------------- |
| [Understand AirSync](airsync/terminology.md)                   | The terms, synchronization flow and connector responsibilities          |
| [Set up your connector](airsync/snap-in-template.md)           | A project with connections and declared capabilities                    |
| [Import data into DevRev](airsync/extraction-phases.md)        | Discovery, schema, mappings, records and attachments                    |
| [Add optional capabilities](airsync/data-model/permissions.md) | Access rules, teams, formatted content and custom attachment processing |
| [Sync changes back](airsync/loading-phases.md)                 | External record and attachment writes                                   |
| [Test and publish](airsync/local-development.md)               | Local checks, deployment, live validation and marketplace publication   |

Implement the capabilities your integration needs. The optional sections can be skipped when those capabilities are outside its scope. Use Reference for API details, target fields and troubleshooting as you work.

## Public starting points

Start your implementation from the [AirSync template](https://github.com/devrev/airsync-template). The [Asana connector](https://github.com/devrev/airdrop-asana-snap-in) is a complete public integration example.

<span id="find-a-topic" />

Next: [Key concepts and terminology](airsync/terminology.md).
