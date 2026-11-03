# DevRev operator toolkit for Claude Code

Tell Claude Code what you want done in DevRev, in plain words, and it finds the right playbook and API in this toolkit and does the work against your organization.

> "Onboard Acme and open a ticket for them." · "Add a priority field to tickets." · "Build me a support dashboard." · "Let the AI agent look up order status." · "Why did I get a 429?"

## Install

```bash
claude plugin marketplace add c-darshanbaligeri-ux/devrev-implementation
claude plugin install devrev-operator@devrev-implementation
```

Give it a DevRev personal access token (DevRev → Settings → Account → Personal Access Token), either exported or in a `.env` in your project:

```bash
export DEVREV_PAT=<your token>
```

Then just ask. The toolkit installs disabled nowhere and enabled only where you install it; nothing in this repo turns it on for you.

## What you get

- **An entry skill** (`devrev-start`) that Claude follows for any DevRev goal: check the token, find the right playbook or endpoint, read only the files that matter, act, then verify.
- **`devrev-find`**, a command Claude runs to search 300+ API endpoints, 400 workflow operations, 12 domain playbooks and the notes of what was verified live. It prints the risk of each call and the exact files to read.
- **Workflow tools**: `devrev-validate-workflow` checks a workflow template offline, and `devrev-import-workflow` imports it as a draft, validates it in your org and, only when you agree, publishes it.
- **Twelve playbooks**: solution design, custom fields and objects, stages, data loading, dashboards, datasets, workflows, AI agents, the REST API, snap-ins and AirSync, API conventions, and an offline copy of the official developer docs.
- **A safety hook.** Read-only DevRev calls run without a prompt. Anything that writes asks you first, destructive calls (deletes, merges, bulk upgrades, permanent schema changes) ask loudly, and publishing a workflow is flagged as high impact because it switches live automation on.

## Optional plugins

Dashboards and datasets (skills 4 and 5) route into DevRev's own `dashboard-dev` and `dataset-builder` plugins; snap-ins and AirSync connectors (skill 9) route into the third-party `devrev-qk-agents` plugin, which you must install yourself. Claude tells you when one is needed.

## Where things are

| Path | What it is |
| --- | --- |
| `skills/` | The entry skill and the domain playbooks (skill 8 holds the API reference docs; skill 11 mirrors developer.devrev.ai) |
| `bin/`, `index/` | The commands (`devrev-find`, `devrev-validate-workflow`, `devrev-import-workflow`) and the generated index |
| `hooks/` | The safety hook |
| `docs/LEARNINGS.md` | Corrections to the vendor docs that were verified live |
| `tests/`, `evals/`, `scripts/` | Quality gates: `python3 -m unittest discover -s tests` |

Working on this repo itself (maintainers, or Claude Code inside a checkout): read `CLAUDE.md`. Older onboarding and design docs are kept in `docs/archive/`.
