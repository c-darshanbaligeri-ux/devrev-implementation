# Snap-in scopes

Source: <https://developer.devrev.ai/snapin-development/references/scopes>
Scraped: 2026-11-03

Snap-ins support **scopes**, a permissions framework for controlling access during execution. Declare the permissions needed by the snap-in's own service account separately from the permissions requested by each operation when a workflow or agent uses it. This lets each component request only the access it needs.

Declare both `service_account.scopes` and `operations[].static_scopes` in the manifest if your snap-in defines operations. The snap-in service account receives its declared permissions at installation; an operation's requested permissions come from its own scope declaration, not from the snap-in service account.

During installation, users review and grant the permissions requested for the snap-in service account. An operation requests its own permissions when a workflow or agent uses it. Installation proceeds only after the required snap-in permissions have been accepted.

***

## Scope format

Each scope follows an `object:permission` syntax. You specify the object type you need access to, followed by a colon, followed by the permission level.

### Permission levels

Most objects support three standard permission levels:

| Scope          | What it grants                                 |
| -------------- | ---------------------------------------------- |
| `object:read`  | Read-only access (get, list, count)            |
| `object:write` | Read, create, and update access                |
| `object:all`   | Full access — read, create, update, and delete |

Some objects use more granular permissions like `object:update` (grants create and update but not broader write access). When in doubt, refer to the [API-to-scope reference](scope-reference.md).

### Examples

| Scope               | Meaning                                   |
| ------------------- | ----------------------------------------- |
| `ticket:read`       | Read-only access to tickets               |
| `ticket:write`      | Read, create, and update tickets          |
| `rev_user:write`    | Read, create, and update customer details |
| `article:update`    | Read and update articles                  |
| `conversation:read` | Read access to conversations              |
| `command:write`     | Create and update commands                |
| `tag:write`         | Create or modify tags                     |

***

## Add scopes to a snap-in

### 1. Identify the APIs your snap-in uses

Review your snap-in's code and identify all DevRev API calls it makes. For example, if your snap-in creates timeline entries and updates customers, note the endpoints: `timeline-entries.create`, `rev-users.get`, `rev-users.update`.

### 2. Determine the required scopes

Map each API endpoint to its corresponding scope using these general rules:

* **GET/list operations** → `object:read`
* **Create and update operations** → `object:write`
* **Delete operations** → `object:all`

For `timeline-entries.create` and `timeline-entries.update`, the required scope is the **parent object's read permission** — if the timeline entry belongs to an issue, you need `issue:read`; if it belongs to a ticket, you need `ticket:read`.

**Referenced DON IDs require read scope.** Any DevRev object reference (DON ID) passed in a request payload requires the corresponding `:read` scope on that object type, in addition to the scope required for the operation itself.

For example, calling `works.create` to create an issue with a `tags` field that references existing tag DON IDs requires both:

* `issue:write` — to create the issue
* `tag:read` — to resolve and validate each tag DON ID passed in the payload

This applies to every endpoint and every field that accepts a DON ID — owners, parts, accounts, custom object references, and so on. Audit each request payload for DON ID fields and add a `:read` scope for every referenced object type.

Refer to the [API-to-scope reference](scope-reference.md) for the complete mapping.

### 3. Add scopes to the manifest

Declare the scopes in the `service_account` section of your snap-in's manifest file:

```yaml
service_account:
  display_name: DevRev Bot
  scopes:
    self:
      - scope: conversation:read
        optional: false
        reason: "Allow read access to conversations."
      - scope: rev_user:write
        optional: false
        reason: "Allow read and update customer details."
      - scope: comment:write
        optional: false
        reason: "Allow creation and updating of timeline entries."
```

Each scope entry includes:

| Field      | Description                                                                   |
| ---------- | ----------------------------------------------------------------------------- |
| `scope`    | The permission being requested, in `object:permission` format                 |
| `optional` | Whether the scope is required (`false`) or optional (`true`) for installation |
| `reason`   | A human-readable explanation shown to users during installation               |

If the snap-in defines operations, declare the permissions each one requests separately under `operations[].static_scopes`. These are the permissions requested for the workflow or agent using the operation, not additional permissions granted to the snap-in service account. For example, a snap-in that reads tickets in its own automation and exposes an operation that reads issues declares `ticket:read` under `service_account.scopes` and `issue:read` under that operation's `static_scopes`. If both need `issue:read`, declare it in both places.

Each operation declares its own `static_scopes`. Use `static_scopes.impersonation` if the operation needs to act on behalf of a user; the corresponding field under `service_account.scopes` is named `impersonate`. See [Snap-in operations](operations.md) for the operation format and a handler example.

### 4. Publish your snap-in

The snap-in creation and draft process remains the same. In the UI, installers grant the service account's required permissions. Operation scopes are requested separately when a workflow or agent uses the operation.

### 5. Upgrade an existing snap-in

For existing snap-ins, add the scopes to the manifest and republish. The upgrade flow remains the same. For DevRev snap-ins, ensure the `marketplace.yaml` file is present alongside `manifest.yaml`.

***

## Scope types: self vs. impersonate

Scopes are organized into two categories under the `service_account` section.

### Self scopes

Self scopes define the permissions the service account has when operating on its own behalf. This is the most common type.

```yaml
service_account:
  scopes:
    self:
      - scope: ticket:read
        optional: false
        reason: "Read ticket details."
```

### Impersonate scopes

Impersonate scopes define the permissions the service account has when acting on behalf of another entity (a customer or user). The effective permissions are the **intersection** of the service account's impersonate scopes and the impersonated user's own permissions—so the snap-in can never exceed what the user themselves could do.

```yaml
service_account:
  scopes:
    impersonate:
      - act_as: all_devusers
        scopes:
          - scope: ticket:read
            optional: false
            reason: "Read tickets on behalf of the user."
```

***

## Scopes for manifest-defined objects

If your snap-in's manifest creates objects like commands, tags, imports, event sources, or dashboards, include the corresponding scopes as well, since these objects are created via the service account.

For example, if your manifest defines tags and commands:

```yaml
service_account:
  display_name: Example Snap-in
  scopes:
    self:
      - scope: command:write
        reason: "For command creation."
      - scope: tag:write
        reason: "For tag creation."
      - scope: event_source:write
        reason: "For event source creation."

tags:
  - name: exampleTag
    description: Example description

commands:
  - name: exampleCommand
    namespace: devrev
    description: Example description
    surfaces:
      - surface: discussions
        object_types:
          - snap_in
    usage_hint: ""
    function: init_category_import

event_sources:
  organization:
    - name: devrev-webhook
      description: Event coming from DevRev
      display_name: DevRev
      type: devrev-webhook
      config:
        event_types:
          - work_created
```

***

## Custom object scopes

For snap-ins that work with custom objects, scopes follow this format:

```
custom_object:<leaf_type>:<permission>
```

**Example:** `custom_object:asset:read` grants read access to the custom object type `asset`.

Custom object scopes are created automatically when a custom object is defined via the consumer.

For certain cases, you might need to allowlist a snap-in to bypass the custom object scopes requirement. Check the [Manage allowlist exceptions](#manage-allowlist-exceptions) section for more details.

***

## Empty scopes

If your snap-in does not call any DevRev APIs and needs no permissions, declare empty scopes to indicate this explicitly:

```yaml
service_account:
  display_name: DevRev Bot
  scopes:
    self:
```

This tells the platform that the service account intentionally requires no permissions. If the snap-in defines operations, also declare `static_scopes` on each operation, even when an operation requests no permissions:

```yaml
static_scopes:
  self: []
```

An empty service-account scope declaration does not make an operation's scope declaration optional, and an empty operation scope declaration does not grant it the snap-in service account's permissions.

***

## Best practices

**Know the default self-permissions.** The snap-in service account has default permission to read and update itself. Any API calls targeting the snap-in itself work without explicitly setting scopes.

**Do not add required scopes after the initial release.** Adding new required scopes on an update can break the snap-in for users who haven't granted the new permission. If you need additional scopes later, add them as `optional: true`. Optional scopes are granted automatically, but this behavior may change—plan your scopes from the start.

**Remove scopes on updates without restriction.** Removing scopes on subsequent updates is supported.

**Request only what you need.** Follow the principle of least privilege. Requesting fewer permissions makes it easier for admins to approve your snap-in and reduces security risk.

**Include clear reasons.** The `reason` field is shown to users during installation. Write descriptions that explain why each permission is needed in plain language.

***

## Allowlist exceptions

In some cases, the scopes framework cannot fully support a snap-in's requirements. For these, the snap-in can be added to the allowlist to bypass scopes and use the older systems group permissions.

### Custom objects created during activation

If a snap-in creates a custom object during its activation hooks and also needs `custom_object:<leaf_type>:<permission>` scopes for that same object, a circular dependency exists. Because the object doesn't exist yet when scopes are evaluated, these snap-ins need to be added to the allowlist.

### Impersonation with agent authorization

If a snap-in uses impersonation scopes with `act_as` and expects permissions to be the intersection of the user's and service account's permissions, it may need to be added to the allowlist until agent impersonation is fully rolled out.

If your snap-in falls into either of these categories, raise a ticket to request allowlisting by snap-in version or package slug.

***

## API-to-scope reference

The table below maps commonly used APIs to their required scopes. For the complete auto-generated reference covering every public endpoint, see the [API-to-scope reference](scope-reference.md).

### Work items (tickets, issues, opportunities)

The `works.*` APIs require scopes for **each work item type** your snap-in interacts with.

| API                                                                     | Required scopes                                    |
| ----------------------------------------------------------------------- | -------------------------------------------------- |
| `works.get`, `works.list`, `works.count`, `works.group`, `works.export` | `ticket:read`, `issue:read`, `opportunity:read`    |
| `works.create`, `works.update`                                          | `ticket:write`, `issue:write`, `opportunity:write` |
| `works.delete`                                                          | `ticket:all`, `issue:all`, `opportunity:all`       |

### Accounts and workspaces

| API                                  | Required scope  |
| ------------------------------------ | --------------- |
| `accounts.get`, `accounts.list`      | `account:read`  |
| `accounts.create`, `accounts.update` | `account:write` |
| `rev-orgs.get`, `rev-orgs.list`      | `rev_org:read`  |
| `rev-orgs.create`, `rev-orgs.update` | `rev_org:write` |

### Users

| API                                                       | Required scope   |
| --------------------------------------------------------- | ---------------- |
| `rev-users.get`, `rev-users.list`                         | `rev_user:read`  |
| `rev-users.create`, `rev-users.update`, `rev-users.merge` | `rev_user:write` |
| `rev-users.delete`                                        | `rev_user:all`   |
| `dev-users.get`, `dev-users.list`                         | `dev_user:read`  |
| `dev-users.create`, `dev-users.update`                    | `dev_user:write` |

### Conversations

| API                                            | Required scope       |
| ---------------------------------------------- | -------------------- |
| `conversations.get`, `conversations.list`      | `conversation:read`  |
| `conversations.create`, `conversations.update` | `conversation:write` |

### Timeline entries

Timeline entries require the **parent object's read scope**. If the entry belongs to a ticket, you need `ticket:read`; if it belongs to an issue, you need `issue:read`.

| API                                                              | Required scope  |
| ---------------------------------------------------------------- | --------------- |
| `timeline-entries.create`, `.update`, `.get`, `.list`, `.delete` | `<parent>:read` |

### Articles

| API                                  | Required scope   |
| ------------------------------------ | ---------------- |
| `articles.get`, `articles.list`      | `article:read`   |
| `articles.create`, `articles.update` | `article:update` |
| `articles.delete`                    | `article:all`    |

### Tags and commands

| API                     | Required scope |
| ----------------------- | -------------- |
| `tags.get`, `tags.list` | `tag:read`     |
| `tags.create`           | `tag:write`    |
| `commands.get`          | `command:read` |

### Links

| API            | Required scope |
| -------------- | -------------- |
| `links.list`   | `link:read`    |
| `links.create` | `link:write`   |
| `links.delete` | `link:all`     |

### Engagements and meetings

| API                                        | Required scope     |
| ------------------------------------------ | ------------------ |
| `engagements.list`                         | `engagement:read`  |
| `engagements.create`, `engagements.update` | `engagement:write` |
| `engagements.delete`                       | `engagement:all`   |
| `meetings.get`, `meetings.list`            | `meeting:read`     |
| `meetings.create`, `meetings.update`       | `meeting:write`    |

### Incidents

| API                                    | Required scope   |
| -------------------------------------- | ---------------- |
| `incidents.get`, `incidents.list`      | `incident:read`  |
| `incidents.create`, `incidents.update` | `incident:write` |

### Surveys

| API                                                                  | Required scope |
| -------------------------------------------------------------------- | -------------- |
| `surveys.get`, `surveys.list`                                        | `survey:read`  |
| `surveys.create`, `surveys.update`, `surveys.send`, `surveys.submit` | `survey:write` |

### Groups and roles

| API                                           | Required scope                          |
| --------------------------------------------- | --------------------------------------- |
| `groups.get`, `groups.list`                   | `group:read`                            |
| `groups.update`                               | `group:update`                          |
| `groups.members.list`                         | `group_membership:read`, `group:read`   |
| `groups.members.add`, `groups.members.remove` | `group_membership:update`, `group:read` |
| `roles.list`                                  | `role:read`                             |
| `roles.create`, `roles.apply`, `roles.update` | `role:update`                           |

### Artifacts and dashboards

| API                                                       | Required scope    |
| --------------------------------------------------------- | ----------------- |
| `artifacts.get`, `artifacts.download`, `artifacts.locate` | `artifact:read`   |
| `artifacts.prepare`                                       | `artifact:create` |
| `dashboards.get`, `dashboards.list`                       | `dashboard:read`  |
| `dashboards.create`, `dashboards.update`                  | `dashboard:write` |

### Workflows

| API                                                   | Required scope   |
| ----------------------------------------------------- | ---------------- |
| `workflows.get`                                       | `workflow:read`  |
| `workflows.create`, `workflows.templates.instantiate` | `workflow:write` |
| `workflows.delete`                                    | `workflow:all`   |

### Custom objects

| API                                                                 | Required scope                    |
| ------------------------------------------------------------------- | --------------------------------- |
| `custom-objects.get`, `custom-objects.list`, `custom-objects.count` | `custom_object:<leaf_type>:read`  |
| `custom-objects.create`, `custom-objects.update`                    | `custom_object:<leaf_type>:write` |
| `custom-objects.delete`                                             | `custom_object:<leaf_type>:all`   |

### Snap widgets

| API                                          | Required scope                     |
| -------------------------------------------- | ---------------------------------- |
| `snap-widgets.get`, `snap-widgets.count`     | `parent:read`, `snap_widget:read`  |
| `snap-widgets.create`, `snap-widgets.update` | `parent:read`, `snap_widget:write` |

### APIs that require no scope

The following APIs do not require explicit scopes: `schemas.aggregated.get`, `schemas.custom.list`, `schemas.stock.list`, `schemas.subtypes.list`, `stage-diagrams.list`, `stages.custom.get`, `stages.custom.list`, `states.custom.get`, `states.custom.list`, `snap-ins.get`, `snap-ins.update`, and `recommendations.*` endpoints.

***

## FAQ

**Does my existing snap-in stop working?**
No. Previously published snap-ins are not affected. Scopes are only required when publishing a new snap-in or republishing an updated version.

**What happens if I don't define scopes?**
Publishing a scope-enforced snap-in is blocked if `service_account.scopes` is missing or any operation lacks `static_scopes`. Declare empty scopes explicitly if no permissions are needed.

**Can I change scopes after publishing?**
You can remove scopes. You can add new scopes as `optional: true`. Adding new required scopes after the initial release is not supported—it can break the snap-in for existing users.

**What if my snap-in doesn't need any permissions?**
Use empty scopes (`self:` with no entries) to explicitly declare that no permissions are required.

**How do custom object scopes work?**
Use the format `custom_object:<leaf_type>:<permission>`. For example, `custom_object:asset:read`. These scopes are created automatically when a custom object is defined.

**Where can I find the full API-to-scope mapping?**
See the [API-to-scope reference](scope-reference.md)—it is auto-generated from the public OpenAPI spec and stays up to date with every spec change.
