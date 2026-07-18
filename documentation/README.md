# DevRev Implementation — User Documentation

Documentation for the **`devrev-implementation`** repository — the unified, plug-and-play Claude Code
operating environment for all DevRev implementation work, spanning solution design (skill 0) through
build (skills 1–9, incl. snap-in/AirSync development via a routed third-party plugin at skill 9).

- **Repo (local)**: `/Users/q15137/Documents/The one/devrev-implementation`
- **Repo (GitHub, private)**: https://github.com/c-darshanbaligeri-ux/devrev-implementation

## Reading map

| Read this | When |
| --- | --- |
| [01 — Getting Started](01-getting-started.md) | First time on a machine: setup, the one manual step, first-session walkthrough, how to verify everything self-configured |
| [02 — Repository Tour](02-repository-tour.md) | You want to understand what's in the repo, where things live, and why it's laid out this way |
| [03 — Using the Skills (daily work)](03-using-the-skills.md) | Day-to-day: how to ask for each kind of work (solution design, schemas, stages, data, dashboards, datasets, workflows, agents, raw API, snap-ins) with example prompts and what happens under the hood |
| [04 — Maintenance](04-maintenance.md) | Updating the cloned toolchain repos, reloading plugins, refreshing agent knowledge, the workflow learning loop |
| [05 — Troubleshooting & Safety](05-troubleshooting-and-safety.md) | Something's not working, or you want the safety/credential rules in one place |

## The 60-second version

1. Clone the repo, `cp .env.example .env`, paste your DevRev PAT. **That's the only manual step for skills 0–8.**
2. Start a Claude Code session in the repo folder; accept the workspace-trust prompt.
3. Everything else self-configures in the background (toolchain clones, CLI install, workspace dirs, `dashboard-dev` + `dataset-builder` plugins, MCP).
4. Start a second session (so PATH picks up the installed CLI) and just ask for what you want in plain English —
   "design a support-deflection solution", "add a field to accounts", "build me a support dashboard", "when a ticket comes in, notify the owner",
   "let the agent look up order status". The repo routes your request to the right domain skill automatically.
5. **Snap-in development (skill 9) has one extra opt-in**: `/plugin install devrev@devrev-qk-agents` plus 1–2 MCP servers — see [01 — Getting Started](01-getting-started.md) "Optional: snap-in development".
