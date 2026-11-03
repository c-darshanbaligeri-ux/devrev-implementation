# docs/archive: historical documents, not for agents

These were written for humans when the repo was first built. They are kept for provenance and may be stale; nothing in the toolkit routes to them, and `.claude/settings.json` denies Claude Code read access to this folder so they do not leak into searches.

| File | What it is |
| --- | --- |
| `documentation/` | The original five-part user guide (getting started, repository tour, using the skills, maintenance, troubleshooting). Replaced by the short `../../README.md` and, for agents, `skills/devrev-start/`. |
| `ARCHITECTURE.md` | Design rationale for the numbered-skill layout. |
| `SUMMARY.md` | Provenance: where each file came from when the repo was assembled, and the fixups applied. |
| `CLONE_RESULTS.md` | A 2026-07-18 snapshot of the cloned toolchains. |

Facts from these documents that an agent needs at run time (setup problems, error fixes, the MCP token rule) now live in `skills/devrev-start/references/troubleshooting.md`.
