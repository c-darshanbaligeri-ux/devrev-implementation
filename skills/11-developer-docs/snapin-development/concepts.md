# Snap-in Platform

Source: <https://developer.devrev.ai/snapin-development/concepts>
Scraped: 2026-11-03

## Snap-in platform

A snap-in platform manages snap-in packages and installs snap-ins. It enables snap-ins to register, validate, and deploy functions, creating other DevRev objects, registering events/webhooks, and triggering actions enriched by context.

## Snap-in

Snap-ins are collections of objects that extend DevRev's core platform value. These objects include automation, event sources, keyrings, custom types, vistas. With snap-ins, developers can develop at "arms-length" and without making any changes to DevRev's core platform.

Snap-in developers interact with DevRev objects through APIs, get updates on DevRev objects through webhooks, and register an event source to subscribe to GitHub/Slack/any external events.

## Snap-in package

A snap-in package is a collection of DevRev objects and their relationships that describe the functionality of the developed snap-in. It doesn't reference an object within the installer's dev org. It's a parent object collecting snap-in package versions.

## Snap-in version

A snap-in version is the definition of a snap-in. It doesn't belong to any dev org. It's equivalent to a snap-in source code. When a snap-in version is installed, it requires certain inputs from the installer, such as a PAT for GitHub, registering a URL on Bitbucket or some configuration.

The snap-in developer can specify some input configurations that the installer can use to customize the snap-in.

## Automation

In automation, the event source is linked to a function, so whenever an event occurs on that event source, the function is triggered and the event payload is passed along. All keyrings configured by the installer are included in the payload passed to the functions, along with developer-level tokens.

## Connection

A connection uses a keyring object to provide authentication, access token refreshment, and secret storage (access token, refresh token, PAT, API key and more). Upon creating the connection, the platform automatically refreshes the OAuth access token whenever necessary. Objects can reference secrets to access external or DevRev-protected APIs. The platform may use a connection to automatically register the webhook URL with an external source. Automations may also use connections to pass secret values to corresponding functions.

## Event source

[Event sources](references/event-sources.md) collect events from webhooks, emails, and timer-based API calls. Events can also be manually published. DevRev supports the ingestion of webhooks from any source. Each event source is assigned to a dev org.

For example, if you want to collect webhook events from an organization's GitHub, create an event source which in turn gives us a URL to subscribe to on GitHub. Webhook events published to this URL are available from this event source.

## Function

The framework for executing code provided by users is [functions](references/functions.md). Currently, Javascript/TypeScript can be taken as input from the user and deployed as a function.

Connection values can be passed to a function at runtime, enabling it to execute API calls to DevRev and to external systems such as GitHub, Slack, Bitbucket, and Discord.

## Keyring

A [keyring](references/keyrings/keyring-intro.md) is a collection of authentication information for external systems. This includes the key (such as a PAT or an API key), its type, the organization ID for which a key is valid,
and in some cases the organization name. A keyring is used by a snap-ins to authenticate to the external system in API calls.

## Imports

Snap-ins that provide an extractor function for an [AirSync](../airsync.md) snap-in responsible for extracting data from an external system need to have an import section defined in their manifest to register their snap-in in the **Imports** section of the DevRev app.

## Globals

Snap-ins can be configured to enable and disable features, based on custom inputs defined by the developer and provided by the installer.

## Commands

A user can trigger [commands](references/commands.md) on different surfaces based on some parameters. Once a command is executed, a function is triggered.

A developer can develop commands to be included in a snap-in Version along with associated functions. These commands are installed when the snap-in is installed.

As part of the snap-in, commands have access to keyrings, global variables, and event sources.

## Hooks

[Hooks](references/hooks.md) enable developers to invoke functions when various events in the lifecycle of a snap-in occur. Hooks can be used to perform various actions based on the event such as validating the snap-in inputs and keyrings when the configuration is updated, registering event-sources and webhooks in external platforms when snap-in is activated, or setting custom fields to be used by the snap-in.

Detailed documentation on hooks can be found in the [hooks reference](references/hooks.md).

## States

The snap-in can have the following states:

* *DRAFT*: The snap-in installation is in progress and the event-sources, automations, and commands aren't created yet.
* *ACTIVATING*: The snap-in is being activated, and the automations, commands, and snap-kit actions are paused. The snap-in can't be updated in this state.
* *ACTIVE*: The snap-in is functioning, and the automations, commands, and snap-kit actions can be invoked.
* *ERROR*: The snap-in isn't functioning, and the automations, commands, and snap-kit actions are paused. This state can be reached in case of any misconfiguration of the snap-in (such as invalid keyrings or inputs) or failure to activate the snap-in.
* *DEACTIVATING*: The snap-in is being deactivated, and the automations, commands, and snap-kit actions are paused. The snap-in can't be updated in this state.
* *INACTIVE*: The snap-in is paused by the user, and the automations, commands, and snap-kit actions are paused.

> **Info:**
>   *ACTIVATING* and *DEACTIVATING* are transitory states and background processes and hooks move the snap-in from these states to a stable state.

The following diagram illustrates the transitions between different states.
*[image: snap-in-lifecycle — see source page]*

## Snap-kit

[Snap-kit](references/snapkit.md) defines UI customization components. It's defined in the snap-in package and used to display developer-defined components. A snap-kit component can display data to a user or collect input for triggering a function.

## Marketplace

The [marketplace](https://marketplace.devrev.ai/marketplace) is a portal where DevRev and external developers can publish snap-ins and other extensions.

Similarly, developers can use private marketplaces to publish their own custom snap-ins that are scoped to their dev org.

## Service account

Every snap-in has a service account—a service identity provisioned when the snap-in is installed. The service account makes API calls on the snap-in's behalf and is subject to access control.

Developers declare the service account's display name and its scopes in the manifest. Scopes are permission strings of the form `<object>:<operation>` (for example, `issue:read` or `workflow:write`) that control exactly which DevRev resources the snap-in can access.

Scopes can be required (the snap-in cannot install without them) or optional (the snap-in can function in a degraded mode without them). Once a snap-in version is published, new required scopes cannot be added in a later version—only optional scopes can be added during an upgrade.

See [Snap-in scopes](references/scopes.md) for the full reference.

## Personas

### Publisher

The developer's dev org is responsible for publishing the snap-in to the marketplace. The publisher is responsible for supporting snap-in users.

### Installer

Installers install the snap-in, provide configuration inputs, set up the necessary keyrings, and configure webhooks for external apps.
