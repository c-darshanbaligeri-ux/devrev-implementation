# API-to-scope reference

Source: <https://developer.devrev.ai/snapin-development/references/scope-reference>
Scraped: 2026-11-03

Each row shows the HTTP method, API path, and the scope(s) that a snap-in's service account must hold to call that endpoint. For context on how to declare scopes in your manifest, see [Snap-in scopes](scopes.md).

Endpoints that need no scopes show **None** in the Required scope column.

## Other

| Method | API path | Required scope |
| ------ | -------- | -------------- |
| `GET`  | `/ping`  | None           |
| `POST` | `/ping`  | None           |

***

## Accounts

| Method | API path           | Required scope                           |
| ------ | ------------------ | ---------------------------------------- |
| `POST` | `/accounts.create` | `account:write,account:all`              |
| `POST` | `/accounts.delete` | `account:all`                            |
| `GET`  | `/accounts.export` | `account:read,account:write,account:all` |
| `POST` | `/accounts.export` | `account:read,account:write,account:all` |
| `GET`  | `/accounts.get`    | `account:read,account:write,account:all` |
| `POST` | `/accounts.get`    | `account:read,account:write,account:all` |
| `GET`  | `/accounts.list`   | `account:read,account:write,account:all` |
| `POST` | `/accounts.list`   | `account:read,account:write,account:all` |
| `POST` | `/accounts.merge`  | `account:all`                            |
| `POST` | `/accounts.update` | `account:write,account:all`              |

***

## Articles

| Method | API path           | Required scope                           |
| ------ | ------------------ | ---------------------------------------- |
| `POST` | `/articles.create` | `article:write,article:all`              |
| `POST` | `/articles.delete` | `article:all`                            |
| `GET`  | `/articles.get`    | `article:read,article:write,article:all` |
| `POST` | `/articles.get`    | `article:read,article:write,article:all` |
| `GET`  | `/articles.list`   | `article:read,article:write,article:all` |
| `POST` | `/articles.list`   | `article:read,article:write,article:all` |
| `POST` | `/articles.update` | `article:write,article:all`              |

***

## Artifacts

| Method | API path                      | Required scope                                   |
| ------ | ----------------------------- | ------------------------------------------------ |
| `GET`  | `/artifacts.download`         | `artifact:read`                                  |
| `POST` | `/artifacts.download`         | `artifact:read`                                  |
| `GET`  | `/artifacts.get`              | `artifact:read` — Also needs parent read access. |
| `POST` | `/artifacts.get`              | `artifact:read` — Also needs parent read access. |
| `GET`  | `/artifacts.list`             | `artifact:read` — Also needs parent read access. |
| `POST` | `/artifacts.list`             | `artifact:read` — Also needs parent read access. |
| `GET`  | `/artifacts.locate`           | `artifact:read` — Also needs parent read access. |
| `POST` | `/artifacts.locate`           | `artifact:read` — Also needs parent read access. |
| `POST` | `/artifacts.prepare`          | `artifact:create`                                |
| `POST` | `/artifacts.versions.delete`  | `artifact:create`                                |
| `POST` | `/artifacts.versions.prepare` | `artifact:create`                                |

***

## Atoms

| Method | API path     | Required scope                                                                            |
| ------ | ------------ | ----------------------------------------------------------------------------------------- |
| `GET`  | `/atoms.get` | `{object_type}:read` (derived from `id` field — for example, `issue:read`, `ticket:read`) |
| `POST` | `/atoms.get` | `{object_type}:read` (derived from `id` field — for example, `issue:read`, `ticket:read`) |

***

## Auth connections

| Method | API path                            | Required scope                               |
| ------ | ----------------------------------- | -------------------------------------------- |
| `POST` | `/dev-orgs.auth-connections.create` | None — Cannot be called via service account. |
| `POST` | `/dev-orgs.auth-connections.delete` | None — Cannot be called via service account. |
| `GET`  | `/dev-orgs.auth-connections.get`    | `Cannot be called via service account.`      |
| `POST` | `/dev-orgs.auth-connections.get`    | `Cannot be called via service account.`      |
| `GET`  | `/dev-orgs.auth-connections.list`   | None — Cannot be called via service account. |
| `POST` | `/dev-orgs.auth-connections.list`   | None — Cannot be called via service account. |
| `POST` | `/dev-orgs.auth-connections.toggle` | None — Cannot be called via service account. |
| `POST` | `/dev-orgs.auth-connections.update` | None — Cannot be called via service account. |

***

## Auth tokens

| Method | API path                   | Required scope |
| ------ | -------------------------- | -------------- |
| `POST` | `/auth-tokens.create`      | None           |
| `POST` | `/auth-tokens.delete`      | None           |
| `GET`  | `/auth-tokens.get`         | None           |
| `POST` | `/auth-tokens.get`         | None           |
| `GET`  | `/auth-tokens.info`        | None           |
| `POST` | `/auth-tokens.info`        | None           |
| `GET`  | `/auth-tokens.list`        | None           |
| `POST` | `/auth-tokens.list`        | None           |
| `POST` | `/auth-tokens.self.delete` | None           |
| `POST` | `/auth-tokens.update`      | None           |

***

## Chats

| Method | API path        | Required scope                                  |
| ------ | --------------- | ----------------------------------------------- |
| `POST` | `/chats.create` | None — Access is determined by chat membership. |
| `GET`  | `/chats.get`    | None — Access is determined by chat membership. |
| `POST` | `/chats.get`    | None — Access is determined by chat membership. |
| `POST` | `/chats.update` | None — Access is determined by chat membership. |

***

## Code changes

| Method | API path               | Required scope                                       |
| ------ | ---------------------- | ---------------------------------------------------- |
| `POST` | `/code-changes.create` | `code_change:write,code_change:all`                  |
| `POST` | `/code-changes.delete` | `code_change:all`                                    |
| `GET`  | `/code-changes.get`    | `code_change:read,code_change:write,code_change:all` |
| `POST` | `/code-changes.get`    | `code_change:read,code_change:write,code_change:all` |
| `GET`  | `/code-changes.list`   | `code_change:read,code_change:write,code_change:all` |
| `POST` | `/code-changes.list`   | `code_change:read,code_change:write,code_change:all` |
| `POST` | `/code-changes.update` | `code_change:write,code_change:all`                  |

***

## Commands

| Method | API path           | Required scope                           |
| ------ | ------------------ | ---------------------------------------- |
| `POST` | `/commands.create` | `command:write,command:all`              |
| `GET`  | `/commands.get`    | `command:read,command:write,command:all` |
| `POST` | `/commands.get`    | `command:read,command:write,command:all` |
| `GET`  | `/commands.list`   | `command:read,command:write,command:all` |
| `POST` | `/commands.list`   | `command:read,command:write,command:all` |
| `POST` | `/commands.update` | `command:write,command:all`              |

***

## Conversations

| Method | API path                | Required scope                                          |
| ------ | ----------------------- | ------------------------------------------------------- |
| `POST` | `/conversations.create` | `conversation:write,conversation:all`                   |
| `POST` | `/conversations.delete` | `conversation:all`                                      |
| `GET`  | `/conversations.get`    | `conversation:read,conversation:write,conversation:all` |
| `POST` | `/conversations.get`    | `conversation:read,conversation:write,conversation:all` |
| `GET`  | `/conversations.list`   | `conversation:read,conversation:write,conversation:all` |
| `POST` | `/conversations.list`   | `conversation:read,conversation:write,conversation:all` |
| `POST` | `/conversations.update` | `conversation:write,conversation:all`                   |

***

## Customization

| Method | API path                           | Required scope               |
| ------ | ---------------------------------- | ---------------------------- |
| `GET`  | `/custom-objects.count`            | None                         |
| `POST` | `/custom-objects.count`            | None                         |
| `POST` | `/custom-objects.create`           | `custom_type_fragment:write` |
| `POST` | `/custom-objects.delete`           | `custom_type_fragment:write` |
| `GET`  | `/custom-objects.get`              | None                         |
| `POST` | `/custom-objects.get`              | None                         |
| `GET`  | `/custom-objects.list`             | None                         |
| `POST` | `/custom-objects.list`             | None                         |
| `POST` | `/custom-objects.update`           | `custom_type_fragment:write` |
| `GET`  | `/schemas.aggregated.get`          | None                         |
| `POST` | `/schemas.aggregated.get`          | None                         |
| `GET`  | `/schemas.custom.get`              | None                         |
| `POST` | `/schemas.custom.get`              | None                         |
| `GET`  | `/schemas.custom.list`             | None                         |
| `POST` | `/schemas.custom.list`             | None                         |
| `POST` | `/schemas.custom.set`              | `custom_type_fragment:write` |
| `GET`  | `/schemas.stock.get`               | None                         |
| `POST` | `/schemas.stock.get`               | None                         |
| `GET`  | `/schemas.stock.list`              | None                         |
| `POST` | `/schemas.stock.list`              | None                         |
| `POST` | `/schemas.subtypes.prepare-update` | `custom_type_fragment:write` |
| `POST` | `/stage-diagrams.create`           | `stage_diagram:write`        |
| `GET`  | `/stage-diagrams.get`              | None                         |
| `POST` | `/stage-diagrams.get`              | None                         |
| `GET`  | `/stage-diagrams.list`             | None                         |
| `POST` | `/stage-diagrams.list`             | None                         |
| `POST` | `/stage-diagrams.update`           | `stage_diagram:write`        |
| `POST` | `/stages.custom.create`            | `custom_stage:write`         |
| `GET`  | `/stages.custom.get`               | None                         |
| `POST` | `/stages.custom.get`               | None                         |
| `GET`  | `/stages.custom.list`              | None                         |
| `POST` | `/stages.custom.list`              | None                         |
| `POST` | `/stages.custom.update`            | `custom_stage:write`         |
| `POST` | `/states.custom.create`            | `custom_state:write`         |
| `GET`  | `/states.custom.get`               | None                         |
| `POST` | `/states.custom.get`               | None                         |
| `GET`  | `/states.custom.list`              | None                         |
| `POST` | `/states.custom.list`              | None                         |
| `POST` | `/states.custom.update`            | `custom_state:write`         |

***

## Organizations

| Method | API path        | Required scope               |
| ------ | --------------- | ---------------------------- |
| `GET`  | `/dev-orgs.get` | `dev_org:read,dev_org:write` |
| `POST` | `/dev-orgs.get` | `dev_org:read,dev_org:write` |

***

## Users

| Method | API path                       | Required scope                                  |
| ------ | ------------------------------ | ----------------------------------------------- |
| `POST` | `/dev-users.activate`          | `dev_user:write,dev_user:all`                   |
| `POST` | `/dev-users.create`            | `dev_user:write,dev_user:all`                   |
| `POST` | `/dev-users.deactivate`        | `dev_user:all`                                  |
| `GET`  | `/dev-users.get`               | `dev_user:read,dev_user:write,dev_user:all`     |
| `POST` | `/dev-users.get`               | `dev_user:read,dev_user:write,dev_user:all`     |
| `POST` | `/dev-users.identities.link`   | `dev_user:write,dev_user:all`                   |
| `POST` | `/dev-users.identities.unlink` | `dev_user:write,dev_user:all`                   |
| `GET`  | `/dev-users.list`              | `dev_user:read,dev_user:write,dev_user:all`     |
| `POST` | `/dev-users.list`              | `dev_user:read,dev_user:write,dev_user:all`     |
| `POST` | `/dev-users.merge`             | `dev_user:all`                                  |
| `GET`  | `/dev-users.self`              | None — Default Scopes unavailable for this API. |
| `POST` | `/dev-users.self`              | None — Default Scopes unavailable for this API. |
| `POST` | `/dev-users.self.update`       | None — Default Scopes unavailable for this API. |
| `POST` | `/dev-users.update`            | `dev_user:write,dev_user:all`                   |

***

## Directory

| Method | API path              | Required scope                                 |
| ------ | --------------------- | ---------------------------------------------- |
| `GET`  | `/directories.count`  | `directory:read,directory:write,directory:all` |
| `POST` | `/directories.count`  | `directory:read,directory:write,directory:all` |
| `POST` | `/directories.create` | `directory:write,directory:all`                |
| `POST` | `/directories.delete` | `directory:all`                                |
| `GET`  | `/directories.get`    | `directory:read,directory:write,directory:all` |
| `POST` | `/directories.get`    | `directory:read,directory:write,directory:all` |
| `GET`  | `/directories.list`   | `directory:read,directory:write,directory:all` |
| `POST` | `/directories.list`   | `directory:read,directory:write,directory:all` |
| `POST` | `/directories.update` | `directory:write,directory:all`                |

***

## Groups

| Method | API path                 | Required scope                               |
| ------ | ------------------------ | -------------------------------------------- |
| `POST` | `/groups.create`         | `group:write,group:all`                      |
| `GET`  | `/groups.get`            | `group:read,group:write,group:all`           |
| `POST` | `/groups.get`            | `group:read,group:write,group:all`           |
| `GET`  | `/groups.list`           | `group:read,group:write,group:all`           |
| `POST` | `/groups.list`           | `group:read,group:write,group:all`           |
| `POST` | `/groups.members.add`    | `group_membership:all`                       |
| `GET`  | `/groups.members.list`   | `group_membership:read,group_membership:all` |
| `POST` | `/groups.members.list`   | `group_membership:read,group_membership:all` |
| `POST` | `/groups.members.remove` | `group_membership:all`                       |
| `POST` | `/groups.update`         | `group:write,group:all`                      |

***

## Jobs

| Method | API path     | Required scope |
| ------ | ------------ | -------------- |
| `GET`  | `/jobs.get`  | `job:read`     |
| `POST` | `/jobs.get`  | `job:read`     |
| `GET`  | `/jobs.list` | `job:read`     |
| `POST` | `/jobs.list` | `job:read`     |

***

## Keyrings

| Method | API path              | Required scope |
| ------ | --------------------- | -------------- |
| `GET`  | `/keyrings.authorize` | `keyring:read` |
| `POST` | `/keyrings.authorize` | `keyring:read` |

***

## Links

| Method | API path         | Required scope                                                 |
| ------ | ---------------- | -------------------------------------------------------------- |
| `POST` | `/links.create`  | `link:write,link:all` — Also needs linked objects read access. |
| `POST` | `/links.delete`  | `link:all` — Also needs linked objects read access.            |
| `GET`  | `/links.get`     | `link:read,link:write,link:all`                                |
| `POST` | `/links.get`     | `link:read,link:write,link:all`                                |
| `GET`  | `/links.list`    | `link:read,link:write,link:all`                                |
| `POST` | `/links.list`    | `link:read,link:write,link:all`                                |
| `POST` | `/links.replace` | `link:write,link:all` — Also needs linked objects read access. |

***

## Meetings

| Method | API path           | Required scope                           |
| ------ | ------------------ | ---------------------------------------- |
| `GET`  | `/meetings.count`  | `meeting:read,meeting:write,meeting:all` |
| `POST` | `/meetings.count`  | `meeting:read,meeting:write,meeting:all` |
| `POST` | `/meetings.create` | `meeting:write,meeting:all`              |
| `POST` | `/meetings.delete` | `meeting:all`                            |
| `GET`  | `/meetings.get`    | `meeting:read,meeting:write,meeting:all` |
| `POST` | `/meetings.get`    | `meeting:read,meeting:write,meeting:all` |
| `GET`  | `/meetings.list`   | `meeting:read,meeting:write,meeting:all` |
| `POST` | `/meetings.list`   | `meeting:read,meeting:write,meeting:all` |
| `POST` | `/meetings.update` | `meeting:write,meeting:all`              |

***

## Observability

| Method | API path                                     | Required scope |
| ------ | -------------------------------------------- | -------------- |
| `POST` | `/observability.sessions.aggregate`          | None           |
| `GET`  | `/observability.sessions.data.get`           | None           |
| `POST` | `/observability.sessions.data.get`           | None           |
| `GET`  | `/observability.sessions.developer-info.get` | None           |
| `POST` | `/observability.sessions.developer-info.get` | None           |
| `GET`  | `/observability.sessions.get`                | None           |
| `POST` | `/observability.sessions.get`                | None           |
| `GET`  | `/observability.sessions.list`               | None           |
| `POST` | `/observability.sessions.list`               | None           |

***

## Parts

| Method | API path        | Required scope                                                                                                                                                                                                                                                                             |
| ------ | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `POST` | `/parts.create` | **capability**: `capability:write`, `capability:all`**enhancement**: `enhancement:write`, `enhancement:all`**feature**: `feature:write`, `feature:all`**product**: `product:write`, `product:all`                                                                        |
| `POST` | `/parts.delete` | **capability**: `capability:all`**enhancement**: `enhancement:all`**feature**: `feature:all`**product**: `product:all`                                                                                                                                                   |
| `GET`  | `/parts.get`    | **capability**: `capability:read`, `capability:write`, `capability:all`**enhancement**: `enhancement:read`, `enhancement:write`, `enhancement:all`**feature**: `feature:read`, `feature:write`, `feature:all`**product**: `product:read`, `product:write`, `product:all` |
| `POST` | `/parts.get`    | **capability**: `capability:read`, `capability:write`, `capability:all`**enhancement**: `enhancement:read`, `enhancement:write`, `enhancement:all`**feature**: `feature:read`, `feature:write`, `feature:all`**product**: `product:read`, `product:write`, `product:all` |
| `GET`  | `/parts.list`   | **capability**: `capability:read`, `capability:write`, `capability:all`**enhancement**: `enhancement:read`, `enhancement:write`, `enhancement:all`**feature**: `feature:read`, `feature:write`, `feature:all`**product**: `product:read`, `product:write`, `product:all` |
| `POST` | `/parts.list`   | **capability**: `capability:read`, `capability:write`, `capability:all`**enhancement**: `enhancement:read`, `enhancement:write`, `enhancement:all`**feature**: `feature:read`, `feature:write`, `feature:all`**product**: `product:read`, `product:write`, `product:all` |
| `POST` | `/parts.update` | **capability**: `capability:write`, `capability:all`**enhancement**: `enhancement:write`, `enhancement:all`**feature**: `feature:write`, `feature:all`**product**: `product:write`, `product:all`                                                                        |

***

## Workspaces

| Method | API path           | Required scope                           |
| ------ | ------------------ | ---------------------------------------- |
| `POST` | `/rev-orgs.create` | `rev_org:write,rev_org:all`              |
| `POST` | `/rev-orgs.delete` | `rev_org:all`                            |
| `GET`  | `/rev-orgs.get`    | `rev_org:read,rev_org:write,rev_org:all` |
| `POST` | `/rev-orgs.get`    | `rev_org:read,rev_org:write,rev_org:all` |
| `GET`  | `/rev-orgs.list`   | `rev_org:read,rev_org:write,rev_org:all` |
| `POST` | `/rev-orgs.list`   | `rev_org:read,rev_org:write,rev_org:all` |
| `POST` | `/rev-orgs.update` | `rev_org:write,rev_org:all`              |

***

## Customers

| Method | API path            | Required scope                              |
| ------ | ------------------- | ------------------------------------------- |
| `POST` | `/rev-users.create` | `rev_user:write,rev_user:all`               |
| `POST` | `/rev-users.delete` | `rev_user:all`                              |
| `GET`  | `/rev-users.get`    | `rev_user:read,rev_user:write,rev_user:all` |
| `POST` | `/rev-users.get`    | `rev_user:read,rev_user:write,rev_user:all` |
| `GET`  | `/rev-users.list`   | `rev_user:read,rev_user:write,rev_user:all` |
| `POST` | `/rev-users.list`   | `rev_user:read,rev_user:write,rev_user:all` |
| `POST` | `/rev-users.merge`  | `rev_user:all`                              |
| `GET`  | `/rev-users.scan`   | `rev_user:read,rev_user:write,rev_user:all` |
| `POST` | `/rev-users.scan`   | `rev_user:read,rev_user:write,rev_user:all` |
| `POST` | `/rev-users.update` | `rev_user:write,rev_user:all`               |

***

## Schedules

| Method | API path                             | Required scope                                                                     |
| ------ | ------------------------------------ | ---------------------------------------------------------------------------------- |
| `POST` | `/org-schedule-fragments.create`     | `org_schedule_fragment:write,org_schedule_fragment:all`                            |
| `GET`  | `/org-schedule-fragments.get`        | `org_schedule_fragment:read,org_schedule_fragment:write,org_schedule_fragment:all` |
| `POST` | `/org-schedule-fragments.get`        | `org_schedule_fragment:read,org_schedule_fragment:write,org_schedule_fragment:all` |
| `POST` | `/org-schedule-fragments.transition` | `org_schedule_fragment:write,org_schedule_fragment:all`                            |
| `POST` | `/org-schedules.create`              | `org_schedule:write,org_schedule:all`                                              |
| `GET`  | `/org-schedules.evaluate`            | `org_schedule:read,org_schedule:write,org_schedule:all`                            |
| `POST` | `/org-schedules.evaluate`            | `org_schedule:read,org_schedule:write,org_schedule:all`                            |
| `GET`  | `/org-schedules.get`                 | `org_schedule:read,org_schedule:write,org_schedule:all`                            |
| `POST` | `/org-schedules.get`                 | `org_schedule:read,org_schedule:write,org_schedule:all`                            |
| `GET`  | `/org-schedules.list`                | `org_schedule:read,org_schedule:write,org_schedule:all`                            |
| `POST` | `/org-schedules.list`                | `org_schedule:read,org_schedule:write,org_schedule:all`                            |
| `POST` | `/org-schedules.set-future`          | `org_schedule:write,org_schedule:all`                                              |
| `POST` | `/org-schedules.transition`          | `org_schedule:write,org_schedule:all`                                              |
| `POST` | `/org-schedules.update`              | `org_schedule:write,org_schedule:all`                                              |

***

## Service accounts

| Method | API path                   | Required scope                                                                  |
| ------ | -------------------------- | ------------------------------------------------------------------------------- |
| `POST` | `/service-accounts.create` | None — Not accessible via service account tokens. Requires user authentication. |
| `GET`  | `/service-accounts.get`    | `svcacc:read`                                                                   |
| `POST` | `/service-accounts.get`    | `svcacc:read`                                                                   |

***

## Slas

| Method | API path                     | Required scope                                                         |
| ------ | ---------------------------- | ---------------------------------------------------------------------- |
| `POST` | `/metric-action.execute`     | None                                                                   |
| `POST` | `/metric-definitions.create` | `metric_definition:write,metric_definition:all`                        |
| `POST` | `/metric-definitions.delete` | `metric_definition:all`                                                |
| `GET`  | `/metric-definitions.get`    | `metric_definition:read,metric_definition:write,metric_definition:all` |
| `POST` | `/metric-definitions.get`    | `metric_definition:read,metric_definition:write,metric_definition:all` |
| `GET`  | `/metric-definitions.list`   | `metric_definition:read,metric_definition:write,metric_definition:all` |
| `POST` | `/metric-definitions.list`   | `metric_definition:read,metric_definition:write,metric_definition:all` |
| `POST` | `/metric-definitions.update` | `metric_definition:write,metric_definition:all`                        |
| `GET`  | `/metric-trackers.get`       | None                                                                   |
| `POST` | `/metric-trackers.get`       | None                                                                   |
| `GET`  | `/sla-trackers.get`          | None                                                                   |
| `POST` | `/sla-trackers.get`          | None                                                                   |
| `GET`  | `/sla-trackers.list`         | None                                                                   |
| `POST` | `/sla-trackers.list`         | None                                                                   |
| `POST` | `/slas.assign`               | `sla:write`                                                            |
| `POST` | `/slas.create`               | `sla:write`                                                            |
| `GET`  | `/slas.get`                  | `sla:read,sla:write`                                                   |
| `POST` | `/slas.get`                  | `sla:read,sla:write`                                                   |
| `GET`  | `/slas.list`                 | `sla:read,sla:write`                                                   |
| `POST` | `/slas.list`                 | `sla:read,sla:write`                                                   |
| `POST` | `/slas.transition`           | `sla:write`                                                            |
| `POST` | `/slas.update`               | `sla:write`                                                            |

***

## Snap kit execution

| Method | API path                            | Required scope                      |
| ------ | ----------------------------------- | ----------------------------------- |
| `POST` | `/snap-kit-action.execute.deferred` | `snap_widget:write,snap_widget:all` |

***

## Snap widgets

| Method | API path               | Required scope                      |
| ------ | ---------------------- | ----------------------------------- |
| `POST` | `/snap-widgets.create` | `snap_widget:write,snap_widget:all` |

***

## Surveys

| Method | API path                    | Required scope                                                   |
| ------ | --------------------------- | ---------------------------------------------------------------- |
| `POST` | `/surveys.create`           | `survey:write,survey:all`                                        |
| `POST` | `/surveys.delete`           | `survey:all`                                                     |
| `GET`  | `/surveys.get`              | `survey:read,survey:write,survey:all`                            |
| `POST` | `/surveys.get`              | `survey:read,survey:write,survey:all`                            |
| `GET`  | `/surveys.list`             | `survey:read,survey:write,survey:all`                            |
| `POST` | `/surveys.list`             | `survey:read,survey:write,survey:all`                            |
| `GET`  | `/surveys.responses.list`   | `survey_response:read,survey_response:write,survey_response:all` |
| `POST` | `/surveys.responses.list`   | `survey_response:read,survey_response:write,survey_response:all` |
| `POST` | `/surveys.responses.update` | `survey_response:write,survey_response:all`                      |
| `POST` | `/surveys.send`             | `survey:write,survey:all`                                        |
| `POST` | `/surveys.submit`           | `survey_response:write,survey_response:all`                      |
| `POST` | `/surveys.update`           | `survey:write,survey:all`                                        |

***

## System users

| Method | API path            | Required scope                                  |
| ------ | ------------------- | ----------------------------------------------- |
| `GET`  | `/sys-users.list`   | None — Default Scopes unavailable for this API. |
| `POST` | `/sys-users.list`   | None — Default Scopes unavailable for this API. |
| `POST` | `/sys-users.update` | None — Default Scopes unavailable for this API. |

***

## Tags

| Method | API path       | Required scope               |
| ------ | -------------- | ---------------------------- |
| `POST` | `/tags.create` | `tag:write,tag:all`          |
| `POST` | `/tags.delete` | `tag:all`                    |
| `GET`  | `/tags.get`    | `tag:read,tag:write,tag:all` |
| `POST` | `/tags.get`    | `tag:read,tag:write,tag:all` |
| `GET`  | `/tags.list`   | `tag:read,tag:write,tag:all` |
| `POST` | `/tags.list`   | `tag:read,tag:write,tag:all` |
| `POST` | `/tags.update` | `tag:write,tag:all`          |

***

## Timeline entries

| Method | API path                   | Required scope                                                                                                              |
| ------ | -------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `GET`  | `/reactions.list`          | None — Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline). |
| `POST` | `/reactions.list`          | None — Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline). |
| `POST` | `/reactions.update`        | None — Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline). |
| `POST` | `/timeline-entries.create` | None — Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline). |
| `POST` | `/timeline-entries.delete` | None — Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline). |
| `GET`  | `/timeline-entries.get`    | None — Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline). |
| `POST` | `/timeline-entries.get`    | None — Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline). |
| `GET`  | `/timeline-entries.list`   | None — Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline). |
| `POST` | `/timeline-entries.list`   | None — Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline). |
| `POST` | `/timeline-entries.update` | None — Requires the read or write scope of the parent object's type (e.g. issue:write when posting to an issue's timeline). |

***

## Vistas

| Method | API path                | Required scope                                                              |
| ------ | ----------------------- | --------------------------------------------------------------------------- |
| `POST` | `/vistas.delete`        | `vista:all`                                                                 |
| `GET`  | `/vistas.get`           | `vista:read,vista:write,vista:all`                                          |
| `POST` | `/vistas.get`           | `vista:read,vista:write,vista:all`                                          |
| `POST` | `/vistas.groups.delete` | `vista:all` — No scopes required for default vistas.                        |
| `GET`  | `/vistas.groups.get`    | `vista:read,vista:write,vista:all` — No scopes required for default vistas. |
| `POST` | `/vistas.groups.get`    | `vista:read,vista:write,vista:all` — No scopes required for default vistas. |
| `GET`  | `/vistas.groups.list`   | `vista:read,vista:write,vista:all` — No scopes required for default vistas. |
| `POST` | `/vistas.groups.list`   | `vista:read,vista:write,vista:all` — No scopes required for default vistas. |
| `GET`  | `/vistas.list`          | `vista:read,vista:write,vista:all`                                          |
| `POST` | `/vistas.list`          | `vista:read,vista:write,vista:all`                                          |

***

## Web crawler job

| Method | API path                    | Required scope        |
| ------ | --------------------------- | --------------------- |
| `POST` | `/web-crawler-jobs.control` | `web_crawler_job:all` |
| `POST` | `/web-crawler-jobs.create`  | `web_crawler_job:all` |
| `GET`  | `/web-crawler-jobs.get`     | `web_crawler_job:all` |
| `POST` | `/web-crawler-jobs.get`     | `web_crawler_job:all` |
| `GET`  | `/web-crawler-jobs.list`    | `web_crawler_job:all` |
| `POST` | `/web-crawler-jobs.list`    | `web_crawler_job:all` |

***

## Webhooks

| Method | API path           | Required scope                                  |
| ------ | ------------------ | ----------------------------------------------- |
| `POST` | `/webhooks.create` | None — Default Scopes unavailable for this API. |
| `POST` | `/webhooks.delete` | None — Default Scopes unavailable for this API. |
| `POST` | `/webhooks.event`  | None — Default Scopes unavailable for this API. |
| `GET`  | `/webhooks.get`    | None — Default Scopes unavailable for this API. |
| `POST` | `/webhooks.get`    | None — Default Scopes unavailable for this API. |
| `GET`  | `/webhooks.list`   | None — Default Scopes unavailable for this API. |
| `POST` | `/webhooks.list`   | None — Default Scopes unavailable for this API. |
| `POST` | `/webhooks.update` | None — Default Scopes unavailable for this API. |

***

## Works

| Method | API path        | Required scope                                                                                                                                                                                                                                                                                                              |
| ------ | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GET`  | `/works.count`  | **incident**: `incident:read`, `incident:write`, `incident:all`**issue**: `issue:read`, `issue:write`, `issue:all`**opportunity**: `opportunity:read`, `opportunity:write`, `opportunity:all`**task**: `task:read`, `task:write`, `task:all`**ticket**: `ticket:read`, `ticket:write`, `ticket:all` |
| `POST` | `/works.count`  | **incident**: `incident:read`, `incident:write`, `incident:all`**issue**: `issue:read`, `issue:write`, `issue:all`**opportunity**: `opportunity:read`, `opportunity:write`, `opportunity:all`**task**: `task:read`, `task:write`, `task:all`**ticket**: `ticket:read`, `ticket:write`, `ticket:all` |
| `POST` | `/works.create` | **incident**: `incident:write`, `incident:all`**issue**: `issue:write`, `issue:all`**opportunity**: `opportunity:write`, `opportunity:all`**task**: `task:write`, `task:all`**ticket**: `ticket:write`, `ticket:all`                                                                                |
| `POST` | `/works.delete` | **incident**: `incident:all`**issue**: `issue:all`**opportunity**: `opportunity:all`**task**: `task:all`**ticket**: `ticket:all`                                                                                                                                                                    |
| `GET`  | `/works.export` | **incident**: `incident:read`, `incident:write`, `incident:all`**issue**: `issue:read`, `issue:write`, `issue:all`**opportunity**: `opportunity:read`, `opportunity:write`, `opportunity:all`**task**: `task:read`, `task:write`, `task:all`**ticket**: `ticket:read`, `ticket:write`, `ticket:all` |
| `POST` | `/works.export` | **incident**: `incident:read`, `incident:write`, `incident:all`**issue**: `issue:read`, `issue:write`, `issue:all`**opportunity**: `opportunity:read`, `opportunity:write`, `opportunity:all`**task**: `task:read`, `task:write`, `task:all`**ticket**: `ticket:read`, `ticket:write`, `ticket:all` |
| `GET`  | `/works.get`    | **incident**: `incident:read`, `incident:write`, `incident:all`**issue**: `issue:read`, `issue:write`, `issue:all`**opportunity**: `opportunity:read`, `opportunity:write`, `opportunity:all`**task**: `task:read`, `task:write`, `task:all`**ticket**: `ticket:read`, `ticket:write`, `ticket:all` |
| `POST` | `/works.get`    | **incident**: `incident:read`, `incident:write`, `incident:all`**issue**: `issue:read`, `issue:write`, `issue:all`**opportunity**: `opportunity:read`, `opportunity:write`, `opportunity:all`**task**: `task:read`, `task:write`, `task:all`**ticket**: `ticket:read`, `ticket:write`, `ticket:all` |
| `GET`  | `/works.list`   | **incident**: `incident:read`, `incident:write`, `incident:all`**issue**: `issue:read`, `issue:write`, `issue:all`**opportunity**: `opportunity:read`, `opportunity:write`, `opportunity:all`**task**: `task:read`, `task:write`, `task:all`**ticket**: `ticket:read`, `ticket:write`, `ticket:all` |
| `POST` | `/works.list`   | **incident**: `incident:read`, `incident:write`, `incident:all`**issue**: `issue:read`, `issue:write`, `issue:all`**opportunity**: `opportunity:read`, `opportunity:write`, `opportunity:all`**task**: `task:read`, `task:write`, `task:all`**ticket**: `ticket:read`, `ticket:write`, `ticket:all` |
| `POST` | `/works.update` | **incident**: `incident:write`, `incident:all`**issue**: `issue:write`, `issue:all`**opportunity**: `opportunity:write`, `opportunity:all`**task**: `task:write`, `task:all`**ticket**: `ticket:write`, `ticket:all`                                                                                |
