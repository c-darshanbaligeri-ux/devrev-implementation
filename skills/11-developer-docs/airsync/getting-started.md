# Connector components and responsibilities

Source: <https://developer.devrev.ai/airsync/getting-started>
Scraped: 2026-11-03

An AirSync connector is a snap-in containing code and configuration for one external system. The parts below work together to import data into DevRev and, when supported, send changes back.

## Components and responsibilities

| Component                | Purpose                                                                   | Who implements it                                              |
| ------------------------ | ------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Entry point              | Receives AirSync events and starts the appropriate worker                 | You wire it to the SDK                                         |
| Worker                   | Performs one phase of extraction or reverse sync                          | You write the external-system behavior                         |
| External API client      | Reads and writes data through the provider's API                          | You implement requests and provider-specific behavior          |
| External schema          | Describes the record types, fields and references your connector produces | You define it                                                  |
| Normalization            | Converts API responses into records matching that schema                  | You implement it                                               |
| Domain mapping           | Defines how external records and fields correspond to DevRev objects      | You supply defaults; users choose their import configuration   |
| Denormalization          | Converts reverse-sync input into external API write payloads              | You implement it when supporting reverse sync                  |
| Connector state          | Records progress so a later invocation can continue                       | You track completed work; the SDK stores and reloads it        |
| Manifest and connections | Declares functions, capabilities, permissions and authentication          | You configure it; the platform supplies authorized credentials |

<span id="implementation-boundaries" />

<span id="public-project-shape" />

<span id="capability-dependencies" />

<span id="design-evidence-to-collect" />

The [project setup guide](snap-in-template.md#project-layout-and-entry-point) shows where these components live. [Choose connector capabilities](connector-capabilities.md) explains the implementation required for each supported feature.

Next: [What the AirSync SDK does](sdk-overview.md).
