# Snap-in manifest

Source: <https://developer.devrev.ai/snapin-development/references/manifest>
Scraped: 2026-11-03

> **Note:**
>   The following section is for version 2 of the manifest specification. For the previous version, see [Manifest V1](v1-manifest.md).

The snap-in manifest is what the developers write to define a snap-in. The manifest has the following sections:

## Version

The version specifies the manifest version. The following documentation is for version 2 of the manifest. In the manifest, specify the following:

```yaml
version: 2
```

## Keyrings

Keyrings are secret tokens used to make calls to external systems. They can be categorized either as organization-scoped or user-scoped. Keyrings are specified in the manifest with the following syntax:

```yaml
keyrings:
  organization:
    - name: <The name of the keyring that should be used for the snap-in.>
      description: <A description of the functions of this keyring.>
      display_name: <The name shown to the user.>
      types: <List of all keyring types that can be selected by the end-user.>

    - name: <The name of the keyring that should be used for the snap-in.>
      description: <A description of the functions of this keyring.>
      display_name: <The name shown to the user.>
      types: <List of all keyring types that can be selected by the end-user.>
  user:
    - name: <The name of the keyring that should be used for the snap-in.>
      description: <A description of the functions of this keyring.>
      display_name: <The name shown to the user.>
      types: <List of all keyring types that can be selected by the end-user.>

    - name: <The name of the keyring that should be used for the snap-in.>
      description: <A description of the functions of this keyring.>
      display_name: <The name shown to the user.>
      types: <List of all keyring types that can be selected by the end-user.>
```

For example:

```yaml
keyrings:
  organization:
    - name: my-org-secret-token
      description: The secret tokens stores the keys to the kingdom
      types:
        - snap_in_secret
      display_name: Organization secret token
  user:
    - name: my-secret-token
      description: The secret tokens stores the keys to the kingdom
      types:
        - snap_in_secret
      display_name: Your secret token
```

Keyrings defined in the manifest can be provided in the snap-in configuration screens and are made available to the function. The keyring type is used to determine the type of the keyring and restricts selection on the configuration screen to valid types.

Organization keyrings are common to the organization, while user keyrings are set per user. User keyrings are optional, so the developer must correctly handle cases where the keyring isn't found.

To view the supported connection types, see [Keyrings](keyrings/keyring-intro.md).

## Developer keyrings

Developer keyrings are provided by the snap-in version developer. They're available across all installations and hidden from the installer. Only the secret string type can be used as developer keyrings.

```yaml
developer_keyrings:
  - name: <The name of the keyring that should be used for the snap-in.>
    description: <A description of the functions of this keyring.>
    display_name: <The name shown to the developer.>

  - name: <The name of the keyring that should be used for the snap-in.>
    description: <A description of the functions of this keyring.>
    display_name: <The name shown to the developer.>
```

For example:

```yaml
developer_keyrings:
  - name: mongodb
    description: Store usage statistics
    display_name: MongoDB PAT

  - name: discord
    description: Access additional discord's API
    display_name: Discord PAT
```

Select the developer connection while creating `snap_in_version`. The DevRev CLI automatically detects such keyrings in the manifest and asks for them:

```bash
devrev snap_in_version create-one --manifest manifest.yaml
Please provide mapping for the developer keyrings:
Use the arrow keys to navigate: ↓ ↑ → ←
? mongodb:
  ▸ mongodb
    discord
```

> **Note:**
>   Developer keyrings can only be created in the UI. They're of the `Snap-in Secret` type.

## Event sources

Event sources can be categorized as "organization" level and "user" level. Event sources are specified in the manifest with the following syntax:

```yaml
    event_sources:
      organization:
        - name: <The name of the event-source that should be used for the snap-in.>
          description: <A description of the functions of this event-source.>
          display_name: <The name shown to the user.>
          type: <An enum specifying the type of source to create.>
          setup_instructions: <Instructions shown to the end user as an option.>
          config:
      <An object containing event source configuration.>

        - name: <The name of the event-source that should be used for the snap-in.>
          description: <A description of the functions of this event-source.>
          display_name: <The name shown to the user.>
          type: <An enum specifying the type of source to create.>
      user:
        - name: <The name of the event-source that should be used for the snap-in.>
          description: <A description of the functions of this event-source.>
          display_name: <The name shown to the user.>
          type: <An enum specifying the type of source to create.>
          setup_instructions: <Instructions shown to the end user as an option.>
          config:
      <An object containing event source configuration.>

        - name: <The name of the event-source that should be used for the snap-in.>
          description: <A description of the functions of this event-source.>
          display_name: <The name shown to the user.>
          type: <An enum specifying the type of source to create.>

```

Refer to [Event sources](event-sources.md) for a checklist of supported event sources and their corresponding event types.

Refer to the webhook event-request example for a list of supported webhooks:

```json
{
  "account_created": {
    "account": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "display_name": "string",
      "description": "string",
      "domains": [
        null
      ],
      "external_refs": [
        null
      ],
      "owned_by": [
        {}
      ],
      "tier": "string"
    }
  },
  "account_deleted": {
    "id": "ACC-12345"
  },
  "account_updated": {
    "account": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "display_name": "string",
      "description": "string",
      "domains": [
        null
      ],
      "external_refs": [
        null
      ],
      "owned_by": [
        {}
      ],
      "tier": "string"
    }
  },
  "conversation_created": {
    "conversation": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "description": "string",
      "group": {},
      "members": [
        {}
      ],
      "messages": [
        {}
      ],
      "metadata": {},
      "owned_by": [
        {}
      ],
      "stage": {},
      "tags": [
        {}
      ],
      "title": "string"
    }
  },
  "conversation_deleted": {
    "id": "string"
  },
  "conversation_updated": {
    "conversation": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "description": "string",
      "group": {},
      "members": [
        {}
      ],
      "messages": [
        {}
      ],
      "metadata": {},
      "owned_by": [
        {}
      ],
      "stage": {},
      "tags": [
        {}
      ],
      "title": "string"
    }
  },
  "dev_user_created": {
    "dev_user": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "display_name": "string",
      "display_picture": {},
      "email": "string",
      "full_name": "string",
      "phone_numbers": [
        null
      ],
      "state": "active",
      "external_identities": [
        {}
      ]
    }
  },
  "dev_user_deleted": {
    "id": "string"
  },
  "dev_user_updated": {
    "dev_user": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "display_name": "string",
      "display_picture": {},
      "email": "string",
      "full_name": "string",
      "phone_numbers": [
        null
      ],
      "state": "active",
      "external_identities": [
        {}
      ]
    }
  },
  "id": "string",
  "part_created": {
    "part": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "artifacts": [
        null
      ],
      "description": "string",
      "name": "string",
      "owned_by": [
        {}
      ],
      "tags": [
        {}
      ]
    }
  },
  "part_deleted": {
    "id": "PROD-12345"
  },
  "part_updated": {
    "part": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "artifacts": [
        null
      ],
      "description": "string",
      "name": "string",
      "owned_by": [
        {}
      ],
      "tags": [
        {}
      ]
    }
  },
  "rev_org_created": {
    "rev_org": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "display_name": "string",
      "description": "string",
      "domain": "string",
      "external_ref": "string"
    }
  },
  "rev_org_deleted": {
    "id": "REV-AbCdEfGh"
  },
  "rev_org_updated": {
    "rev_org": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "display_name": "string",
      "description": "string",
      "domain": "string",
      "external_ref": "string"
    }
  },
  "rev_user_created": {
    "rev_user": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "display_name": "string",
      "display_picture": {},
      "email": "string",
      "full_name": "string",
      "phone_numbers": [
        null
      ],
      "state": "active",
      "description": "string",
      "external_ref": "string",
      "rev_org": {}
    }
  },
  "rev_user_deleted": {
    "id": "string"
  },
  "rev_user_updated": {
    "rev_user": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "display_name": "string",
      "display_picture": {},
      "email": "string",
      "full_name": "string",
      "phone_numbers": [
        null
      ],
      "state": "active",
      "description": "string",
      "external_ref": "string",
      "rev_org": {}
    }
  },
  "sla_tracker_created": {
    "sla_tracker": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z"
    }
  },
  "sla_tracker_deleted": {
    "id": "string"
  },
  "sla_tracker_updated": {
    "sla_tracker": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z"
    }
  },
  "tag_created": {
    "tag": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "allowed_values": [
        null
      ],
      "description": "string",
      "name": "string"
    }
  },
  "tag_deleted": {
    "id": "TAG-12345"
  },
  "tag_updated": {
    "tag": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "allowed_values": [
        null
      ],
      "description": "string",
      "name": "string"
    }
  },
  "timeline_entry_created": {
    "entry": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "object": "string",
      "object_display_id": "string",
      "object_type": "capability",
      "visibility": "external",
      "artifacts": [
        null
      ],
      "body": "string",
      "body_type": "snap_kit",
      "snap_kit_body": {
        "body": {}
      },
      "snap_widget_body": [
        {}
      ]
    }
  },
  "timeline_entry_deleted": {
    "id": "don:core:<partition>:devo/<dev-org-id>:ticket/123:timeline_event/<timeline-event-id>"
  },
  "timeline_entry_updated": {
    "entry": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "object": "string",
      "object_display_id": "string",
      "object_type": "capability",
      "visibility": "external",
      "artifacts": [
        null
      ],
      "body": "string",
      "body_type": "snap_kit",
      "snap_kit_body": {
        "body": {}
      },
      "snap_widget_body": [
        {}
      ]
    }
  },
  "timestamp": "2023-01-01T12:00:00.000Z",
  "type": "account_created",
  "verify": {
    "challenge": "string"
  },
  "webhook_created": {
    "webhook": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "event_types": [
        null
      ],
      "secret": "string",
      "status": "active",
      "url": "string"
    }
  },
  "webhook_deleted": {
    "id": "don:integration:<partition>:devo/<dev-org-id>:webhook/<webhook-id>"
  },
  "webhook_id": "don:integration:<partition>:devo/<dev-org-id>:webhook/<webhook-id>",
  "webhook_updated": {
    "webhook": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "event_types": [
        null
      ],
      "secret": "string",
      "status": "active",
      "url": "string"
    }
  },
  "work_created": {
    "work": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "applies_to_part": {},
      "artifacts": [
        null
      ],
      "body": "string",
      "owned_by": [
        {}
      ],
      "reported_by": [
        {}
      ],
      "stage": {},
      "tags": [
        {}
      ],
      "target_close_date": "2023-01-01T12:00:00.000Z",
      "title": "string",
      "developed_with": [
        {}
      ],
      "priority": "p0"
    }
  },
  "work_deleted": {
    "id": "ISS-12345"
  },
  "work_updated": {
    "work": {
      "created_by": {},
      "created_date": "2023-01-01T12:00:00.000Z",
      "display_id": "string",
      "id": "string",
      "modified_by": {},
      "modified_date": "2023-01-01T12:00:00.000Z",
      "applies_to_part": {},
      "artifacts": [
        null
      ],
      "body": "string",
      "owned_by": [
        {}
      ],
      "reported_by": [
        {}
      ],
      "stage": {},
      "tags": [
        {}
      ],
      "target_close_date": "2023-01-01T12:00:00.000Z",
      "title": "string",
      "developed_with": [
        {}
      ],
      "priority": "p0"
    }
  }
}
```

For example:

```yaml
event_sources:
  organization:
    - name: devrev-webhook
      description: Events coming from GitHub
      display_name: DevRev webhook
      type: devrev-webhook
      config:
        event_types:
          - work_created
```

## Inputs

Inputs are implemented using per-object schemas, which is a customization technique to store custom schemas inline with the object. Each input's schema maps to a FieldDescriptor. Inputs, like keyrings and event sources, are organization and user scoped. Organization-scoped inputs are set by the admins of the organization and are common across all users. User inputs are set individually.

Inputs are defined as:

```yaml
inputs:
  organization:
    - name: <The name of the input.>
      description: <A description of the functions of this input.>
      field_type: <The supported input types.>
      id_type: <If the field type is id, so what are the supported object types whose ids this input can store?>
      is_required: <Is this input required?>
      default_value: <The default value for this input>
      ui:
        display_name: <Input field display name.>
  user:
    - name: <The name of the input.>
      description: <A description of the functions of this input.>
      field_type: <The supported input types.>
      id_type: <If the field type is id, so what are the supported object types whose ids this input can store?>
      is_required: <Is this input required?>
      default_value: <The default value for this input>
      ui:
        display_name: <Input field display name.>
```

Inputs of type `timestamp`, `date` and `array` of `booleans` aren't supported.

## Tags

In the manifest, pass the name and description of the tag.

For example:

```yaml
tags:
  - name: github.branch.name
    description: Tag storing github branch name.
```

## Commands

In the manifest, you need to specify the command's name, its namespace, and the surfaces where it can appear, such as comment discussions. It also specifies the UI description, usage hints, and the function to be triggered when the command is invoked.

```yaml
commands:
  - name: summarize
    namespace: turing
    description: Summarizes the conversation
    surfaces:
      - surface: discussions
        object_types:
          - conversation
    usage_hint: "number of tokens to generate"
    function: generate_summary
```

For commands, the `<name, namespace>` pair should be unique across the Org in which it's installed.

## Functions

In the manifest, pass the name and description of the functions.

```yaml
functions:
  - name: create_work
    description: Function containing logic to create a DevRev work.

  - name: post_message
    description: Function containing logic to post a message on newly created work.
```

For functions, you also need to provide the actual JS/TS code behind this function. Refer to the README in the provided template.

## Operations

An operation exposes a snap-in function as a reusable action in workflows or agents. Define each operation under `operations` with a unique `slug`, a `function` listed under `functions`, and its input and output fields. Declare the permissions the operation requests under its own `static_scopes` block:

```yaml
version: 2
name: Issue lookup
description: Read issues in workflows or agents.

service_account:
  display_name: Example Snap-in
  scopes:
    self:
      - scope: issue:read
        reason: "Read issues from the snap-in function."

functions:
  - name: operation_handler
    description: Handle issue lookup requests.

operations:
  - name: get_issue
    display_name: Get issue
    description: Read an issue for a workflow or agent.
    slug: get_issue
    type: action
    function: operation_handler
    static_scopes:
      self:
        - scope: issue:read
          optional: false
          reason: "Read the issue selected in the workflow or agent."
    inputs:
      fields:
        - name: issue_id
          field_type: id
          id_type:
            - issue
          is_required: true
          ui:
            display_name: Issue
    outputs:
      fields:
        - name: title
          field_type: text
          ui:
            display_name: Title
```

`service_account.scopes` grants permissions to the snap-in's own service account for its runtime. `operations[].static_scopes` declares the permissions requested by the workflow or agent using that specific operation. The operation does not inherit its requested scopes from the snap-in service account. The `issue:read` scope appears in both places in the example because the snap-in function and the operation's consumer each need it. Other operations in the same snap-in declare their own scopes independently.

Operation scopes support `self` entries with `scope`, `optional`, and `reason`. For operations that act on behalf of a user, use `static_scopes.impersonation` with an `act_as` value and nested `scopes`. The corresponding field under `service_account.scopes` is named `impersonate`. Supported `act_as` values are `all_devusers`, `all_revusers`, and `devusers_explicit`. For example:

```yaml
static_scopes:
  impersonation:
    - act_as: all_devusers
      scopes:
        - scope: issue:read
          optional: false
          reason: "Read issues on behalf of the user."
```

Declare `static_scopes` on every operation, even if it requests no permissions. An empty declaration such as `static_scopes: { self: [] }` makes that intent explicit. The same applies to `service_account.scopes` when the snap-in service account needs no permissions. For operation fields, exposure settings, and handler implementation, see [Snap-in operations](operations.md). For scope selection and permission levels, see [Snap-in scopes](scopes.md).

## Automations

Automation refers to linking events from the event sources to your functions.

Automations are defined as:

```yaml
automations:
  - name: <The name of the automation.>
    source: <Name of the event source specified in the manifest from which the events coming in could trigger this automation.>
    event_types:
      - <Event from the source on which you need to run the code.>
    function: <Specifies which function should be run from the manifest.>
```

For custom event sources, whatever event key you emit from your policy, the event name is `custom:<your event key>`.

## Service account

Every snap-in has a service account, a service identity that makes API calls on the snap-in's behalf. Declare the service account's display name and the scopes (permissions) its own runtime needs. These scopes are separate from the `static_scopes` declared on each operation for use in workflows or agents.

```yaml
service_account:
  display_name: <Display name shown in the DevRev UI for this bot>
  scopes:
    self:
      - scope: <scope string, e.g. issue:read>
        optional: <true|false — whether the snap-in can function without this scope>
        reason: <Human-readable explanation shown during installation>
    impersonate:
      - act_as: <group to impersonate, e.g. all_devusers>
        scopes:
          - scope: <scope string>
            optional: <true|false>
            reason: <explanation>
```

For example:

```yaml
service_account:
  display_name: "GitHub Sync Bot"
  scopes:
    self:
      - scope: issue:write
        optional: false
        reason: "Create and update issues from GitHub events"
      - scope: ticket:write
        optional: false
        reason: "Post comments when PRs are linked"
```

> **Note:**
>   The `snap_in_package:read` scope is granted implicitly to every snap-in. Do not declare it.

For the complete reference on scopes—including required vs. optional semantics, impersonation, upgrade constraints, and how to identify the right scope for an API call—see [Snap-in scopes](scopes.md).
