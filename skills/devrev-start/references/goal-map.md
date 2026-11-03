# Common goals and where to start

`devrev-find "<goal>"` is the general tool; this table is a quick sanity check for frequent goals. Every endpoint named here is checked against the index by `tests/test_goal_map.py`. Steps use only facts documented in the skills.

## Plain API operations (skill 8 owns them)

| Goal | Start with | Endpoints, in order |
| --- | --- | --- |
| File a ticket from a report | `skills/8-devrev-api` | `works.create` (type ticket), `timeline-entries.create` for context, `links.create` to relate it to an issue |
| Find or count work items | `skills/8-devrev-api` | `works.list`, `works.count` |
| Change, assign or close work | `skills/8-devrev-api` | `works.update` |
| Add a comment or note | `skills/8-devrev-api` | `timeline-entries.create` |
| Onboard a customer | `skills/3-data-upload-and-org-build` | `accounts.create`, then `rev-orgs.create`, then `rev-users.create` |
| Merge duplicate accounts | `skills/8-devrev-api` | `accounts.merge` (destructive) |
| Attach a file | `skills/3-data-upload-and-org-build` | `artifacts.prepare`, upload the bytes to the returned URL, then reference the artifact id on the parent object |
| Publish knowledge-base content | `skills/8-devrev-api` | `articles.create` (draft), review, `articles.update` (published) |
| Set up support metrics | `skills/8-devrev-api` | `metric-definitions.create`, `slas.create`, `slas.assign`, then check `sla-trackers.get` |
| Search across objects | `skills/8-devrev-api` | `search.hybrid`, `search.core` |
| Get notified of events | `skills/11-developer-docs` (guides/webhooks) | `webhooks.create`, answer the verify challenge, then handle events |
| List conversations | `skills/8-devrev-api` | `conversations.list` |
| Create a product part | `skills/8-devrev-api` | `parts.create` |
| Check who the token belongs to | `skills/10-api-conventions` | `dev-users.self`, `ping` |

## Work that has its own playbook

| Goal | Playbook |
| --- | --- |
| Design a solution for a business problem | `skills/0-solution-architecture` |
| Add a field to a stock object, create a custom object or subtype | `skills/1-object-schema-customization` (`schemas.custom.set`, `custom-objects.create`) |
| Customize stages, states or lifecycles | `skills/2-stage-lifecycle-customization` (`states.custom.create`, `stages.custom.create`, `stage-diagrams.create`) |
| Load files or migrate data, build an org from scratch | `skills/3-data-upload-and-org-build` |
| Build or change a dashboard | `skills/4-dashboards-and-widgets` |
| Create a reporting dataset | `skills/5-datasets` |
| Automate something, or give an AI agent a skill | `skills/6-workflows` |
| Build, debug or test an AI agent | `skills/7-agent-building` |
| Build a snap-in or AirSync connector | `skills/9-snapin-development` |
| Auth, pagination, rate limits, error shapes | `skills/10-api-conventions` |
| "What does the official doc say…", SDK setup, beta endpoints | `skills/11-developer-docs` |
