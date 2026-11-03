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

## Workflows and automations (skill 6 owns them)

| Goal | Start with | Do this |
| --- | --- | --- |
| Build an automation ("when X happens, do Y") | `skills/6-workflows` | `devrev-find "<goal>"` lists matching triggers and steps; `devrev-find --operation <slug>` gives ports and example templates; author the template from the closest example |
| Give an AI agent a callable skill | `skills/6-workflows` | Start from `skills/6-workflows/examples/default-ai-agent-skill-template.json`; follow the agent-skill rules in the skill |
| Import a template and put it live | `skills/6-workflows` | `workflows.templates.instantiate` (creates a draft), `workflow-versions.list`, `workflows.components.validate`, then `workflows.update-status` for a new workflow or `workflow-versions.publish` for an already-published one. The last step switches automation on: confirm with the user first |
| Run a workflow now | `skills/6-workflows` | `workflows.trigger` (the workflow must be active, not a draft) |
| Find or inspect existing workflows | `skills/6-workflows` | `workflows.list`, `workflows.get` |
| Attach a connection to a Code step | `skills/6-workflows` | `keyrings.list`, `workflow-steps.list`, then `workflow-steps.update` with `keyrings` |
| Find out why a template will not import | `skills/6-workflows` | "Debugging a failed import", then `workflows.components.validate` on the draft |

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
