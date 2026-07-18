# DevRev public API — master catalog

Every public DevRev REST endpoint, grouped by domain, with the HTTP method and
the OAuth scope(s) required. This is the authoritative index for the whole
folder. Source: DevRev auto-generated API-to-scope reference.

Excluded by design (not covered in this folder): AI agents, workflows, and
AirSync connectors.

| Field | Detail |
| --- | --- |
| Base URL | https://api.devrev.ai |
| Auth | `Authorization: Bearer <TOKEN>` on every request |
| Content type | `application/json` |
| Method note | Most endpoints accept both GET (query params) and POST (JSON body). Prefer POST for anything with a non-trivial body. |
| Scope note | "None" means no scope is required, though object-level read/write access still applies. Ranges like `x:read,x:write,x:all` mean any one of those grants access. |

Detailed payloads and examples live in the domain docs — see `CLAUDE.md` for the
routing table. This file is the lookup index; go to the domain doc to build a call.

---

## Works (issue, ticket, task, incident, opportunity)
Scope varies by work type (e.g. `issue:*`, `ticket:*`, `opportunity:*`, `task:*`, `incident:*`).

| Endpoint | Method | Scope (write example) |
| --- | --- | --- |
| `works.create` | POST | `<type>:write` / `<type>:all` |
| `works.update` | POST | `<type>:write` / `<type>:all` |
| `works.delete` | POST | `<type>:all` |
| `works.get` | GET/POST | `<type>:read` … |
| `works.list` | GET/POST | `<type>:read` … |
| `works.count` | GET/POST | `<type>:read` … |
| `works.export` | GET/POST | `<type>:read` … |

## Timeline entries & reactions
Scope = read/write of the parent object's type (e.g. `issue:write` to post on an issue).

| Endpoint | Method |
| --- | --- |
| `timeline-entries.create` | POST |
| `timeline-entries.update` | POST |
| `timeline-entries.delete` | POST |
| `timeline-entries.get` | GET/POST |
| `timeline-entries.list` | GET/POST |
| `reactions.list` | GET/POST |
| `reactions.update` | POST |

## Tags
| Endpoint | Method | Scope |
| --- | --- | --- |
| `tags.create` | POST | `tag:write` / `tag:all` |
| `tags.update` | POST | `tag:write` / `tag:all` |
| `tags.delete` | POST | `tag:all` |
| `tags.get` / `tags.list` | GET/POST | `tag:read` … |

## Links
| Endpoint | Method | Scope |
| --- | --- | --- |
| `links.create` | POST | `link:write` / `link:all` (+ read on both objects) |
| `links.replace` | POST | `link:write` / `link:all` (+ read on both). Atomic only for part-to-part default link types |
| `links.delete` | POST | `link:all` (+ read on both) |
| `links.get` / `links.list` | GET/POST | `link:read` … |

## Custom link types
| Endpoint | Method | Scope |
| --- | --- | --- |
| `link-types.custom.create` | POST | `custom_link_type:write` |
| `link-types.custom.update` | POST | `custom_link_type:write` (also used to deprecate) |
| `link-types.custom.get` / `.list` | GET/POST | none |

Note: custom link types cannot be deleted, only deprecated (`deprecated: true`
via `.update`). There is no `link-types.custom.delete`.

## Atoms (generic object fetch)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `atoms.get` | GET/POST | `<object_type>:read` (derived from the id) |

---

## Parts (product / capability / feature)
The scope tracks the part type (like works). Source: `DevRev_Building_Org_Using_API_v1.md` Phase 2.
| Endpoint | Method | Scope |
| --- | --- | --- |
| `parts.create` | POST | `product:write,product:all` (product) / `capability:write,capability:all` (capability) / `feature:write,feature:all` (feature) |
| `parts.list` | GET/POST | corresponding `<part_type>:read,...` |

Hierarchy: product (root) → capability (`parent_part` = product) → feature (`parent_part` = capability or feature).
A Trail is **not** a separate object — there is no `trails.create`; it's the rendered part hierarchy plus links.
(Other `parts.*` verbs are not documented in this folder's references — verify against the official API reference before use.)

---

## Accounts
| Endpoint | Method | Scope |
| --- | --- | --- |
| `accounts.create` | POST | `account:write` / `account:all` |
| `accounts.update` | POST | `account:write` / `account:all` |
| `accounts.delete` | POST | `account:all` |
| `accounts.merge` | POST | `account:all` |
| `accounts.get` / `.list` / `.export` | GET/POST | `account:read` … |

## Rev orgs (workspaces / customer orgs)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `rev-orgs.create` | POST | `rev_org:write` / `rev_org:all` |
| `rev-orgs.update` | POST | `rev_org:write` / `rev_org:all` |
| `rev-orgs.delete` | POST | `rev_org:all` |
| `rev-orgs.get` / `.list` | GET/POST | `rev_org:read` … |

## Rev users (customers / contacts)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `rev-users.create` | POST | `rev_user:write` / `rev_user:all` |
| `rev-users.update` | POST | `rev_user:write` / `rev_user:all` |
| `rev-users.delete` | POST | `rev_user:all` |
| `rev-users.merge` | POST | `rev_user:all` |
| `rev-users.get` / `.list` / `.scan` | GET/POST | `rev_user:read` … |

## Dev users (internal users)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `dev-users.create` | POST | `dev_user:write` / `dev_user:all` |
| `dev-users.update` | POST | `dev_user:write` / `dev_user:all` |
| `dev-users.activate` | POST | `dev_user:write` / `dev_user:all` |
| `dev-users.deactivate` | POST | `dev_user:all` |
| `dev-users.merge` | POST | `dev_user:all` |
| `dev-users.identities.link` / `.unlink` | POST | `dev_user:write` / `dev_user:all` |
| `dev-users.get` / `.list` | GET/POST | `dev_user:read` … |
| `dev-users.self` / `.self.update` | GET/POST | None |

## Dev orgs
| Endpoint | Method | Scope |
| --- | --- | --- |
| `dev-orgs.get` | GET/POST | `dev_org:read` / `dev_org:write` |

## Groups & directory
| Endpoint | Method | Scope |
| --- | --- | --- |
| `groups.create` / `.update` | POST | `group:write` / `group:all` |
| `groups.get` / `.list` | GET/POST | `group:read` … |
| `groups.members.add` / `.remove` | POST | `group_membership:all` |
| `groups.members.list` | GET/POST | `group_membership:read` / `:all` |
| `directories.create` / `.update` | POST | `directory:write` / `directory:all` |
| `directories.delete` | POST | `directory:all` |
| `directories.get` / `.list` / `.count` | GET/POST | `directory:read` … |

## Service accounts & system users
| Endpoint | Method | Scope |
| --- | --- | --- |
| `service-accounts.create` | POST | None (user auth only) |
| `service-accounts.get` | GET/POST | `svcacc:read` |
| `sys-users.list` / `.update` | GET/POST | None |

---

## Conversations
| Endpoint | Method | Scope |
| --- | --- | --- |
| `conversations.create` / `.update` | POST | `conversation:write` / `conversation:all` |
| `conversations.delete` | POST | `conversation:all` |
| `conversations.get` / `.list` | GET/POST | `conversation:read` … |

## Chats
| Endpoint | Method | Scope |
| --- | --- | --- |
| `chats.create` / `.get` / `.update` | POST/GET | None (chat membership governs access) |

## Articles (knowledge base)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `articles.create` / `.update` | POST | `article:write` / `article:all` |
| `articles.delete` | POST | `article:all` |
| `articles.get` / `.list` | GET/POST | `article:read` … |

## Surveys
| Endpoint | Method | Scope |
| --- | --- | --- |
| `surveys.create` / `.update` / `.send` | POST | `survey:write` / `survey:all` |
| `surveys.delete` | POST | `survey:all` |
| `surveys.get` / `.list` | GET/POST | `survey:read` … |
| `surveys.submit` | POST | `survey_response:write` / `:all` |
| `surveys.responses.list` | GET/POST | `survey_response:read` … |
| `surveys.responses.update` | POST | `survey_response:write` / `:all` |

## Meetings
| Endpoint | Method | Scope |
| --- | --- | --- |
| `meetings.create` / `.update` | POST | `meeting:write` / `meeting:all` |
| `meetings.delete` | POST | `meeting:all` |
| `meetings.get` / `.list` / `.count` | GET/POST | `meeting:read` … |

## SLAs, metrics & trackers
| Endpoint | Method | Scope |
| --- | --- | --- |
| `slas.create` / `.update` / `.assign` / `.transition` | POST | `sla:write` |
| `slas.get` / `.list` | GET/POST | `sla:read` / `sla:write` |
| `metric-definitions.create` / `.update` | POST | `metric_definition:write` / `:all` |
| `metric-definitions.delete` | POST | `metric_definition:all` |
| `metric-definitions.get` / `.list` | GET/POST | `metric_definition:read` … |
| `metric-action.execute` | POST | None |
| `metric-trackers.get` | GET/POST | None |
| `sla-trackers.get` / `.list` | GET/POST | None |

---

## Artifacts (files)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `artifacts.prepare` | POST | `artifact:create` |
| `artifacts.versions.prepare` / `.delete` | POST | `artifact:create` |
| `artifacts.download` | GET/POST | `artifact:read` |
| `artifacts.get` / `.list` / `.locate` | GET/POST | `artifact:read` (+ parent read) |

## Webhooks
| Endpoint | Method | Scope |
| --- | --- | --- |
| `webhooks.create` / `.update` / `.delete` / `.event` | POST | None (default scopes N/A) |
| `webhooks.get` / `.list` | GET/POST | None |

## Jobs
| Endpoint | Method | Scope |
| --- | --- | --- |
| `jobs.get` / `.list` | GET/POST | `job:read` |

## Keyrings
| Endpoint | Method | Scope |
| --- | --- | --- |
| `keyrings.authorize` | GET/POST | `keyring:read` |

## Schedules (org schedules & fragments)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `org-schedules.create` / `.update` / `.transition` / `.set-future` | POST | `org_schedule:write` / `:all` |
| `org-schedules.get` / `.list` / `.evaluate` | GET/POST | `org_schedule:read` … |
| `org-schedule-fragments.create` / `.transition` | POST | `org_schedule_fragment:write` / `:all` |
| `org-schedule-fragments.get` | GET/POST | `org_schedule_fragment:read` … |

## Vistas (views)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `vistas.get` / `.list` | GET/POST | `vista:read` … |
| `vistas.delete` | POST | `vista:all` |
| `vistas.groups.get` / `.list` | GET/POST | `vista:read` … (none for default vistas) |
| `vistas.groups.delete` | POST | `vista:all` |

## Observability (sessions)
| Endpoint | Method | Scope |
| --- | --- | --- |
| `observability.sessions.get` / `.list` / `.aggregate` | GET/POST | None |
| `observability.sessions.data.get` | GET/POST | None |
| `observability.sessions.developer-info.get` | GET/POST | None |

## Web crawler jobs
| Endpoint | Method | Scope |
| --- | --- | --- |
| `web-crawler-jobs.create` / `.control` | POST | `web_crawler_job:all` |
| `web-crawler-jobs.get` / `.list` | GET/POST | `web_crawler_job:all` |

## Snap widgets & snap-kit
| Endpoint | Method | Scope |
| --- | --- | --- |
| `snap-widgets.create` | POST | `snap_widget:write` / `:all` |
| `snap-kit-action.execute.deferred` | POST | `snap_widget:write` / `:all` |

## Commands
| Endpoint | Method | Scope |
| --- | --- | --- |
| `commands.create` / `.update` | POST | `command:write` / `command:all` |
| `commands.get` / `.list` | GET/POST | `command:read` … |

## Code changes
| Endpoint | Method | Scope |
| --- | --- | --- |
| `code-changes.create` / `.update` | POST | `code_change:write` / `:all` |
| `code-changes.delete` | POST | `code_change:all` |
| `code-changes.get` / `.list` | GET/POST | `code_change:read` … |

## Auth tokens & connections
| Endpoint | Method | Scope |
| --- | --- | --- |
| `auth-tokens.create` / `.update` / `.delete` / `.self.delete` | POST | None |
| `auth-tokens.get` / `.list` / `.info` | GET/POST | None |
| `dev-orgs.auth-connections.*` | POST/GET | None (user auth only; not via service account) |

## Customization (schemas, custom objects, stages, states, diagrams)
See `Stock_Object_Modification_and_Schemas_API.md`, `Custom_Objects_and_Links_API.md`,
and `Stages_States_and_StageDiagrams_API.md` for full detail. Endpoints:
`schemas.custom.set/get/list`, `schemas.stock.get/list`, `schemas.aggregated.get`,
`schemas.subtypes.list`, `schemas.subtypes.prepare-update`,
`custom-objects.create/update/delete/get/list/count`,
`stages.custom.*`, `states.custom.*`, `stage-diagrams.*`.

## Health
| Endpoint | Method | Scope |
| --- | --- | --- |
| `ping` | GET/POST | None |
