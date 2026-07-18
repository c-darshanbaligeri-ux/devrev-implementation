# 02 — Repository Tour

## Layout

```
devrev-implementation/
├── CLAUDE.md                     # Top router: routing table, global API rules, safety, guardrails
├── README.md                     # Quick setup + plug-and-play acceptance summary
├── .env.example                  # Template for the one manual step
├── .gitignore                    # .env, repos/*/, logs, workspace outputs — secrets never commit
├── .mcp.json                     # Hosted DevRev MCP (https://api.devrev.ai/mcp/v1, Bearer ${DEVREV_PAT})
├── repos.txt                     # Toolchain repos to clone (+ documented exclusions)
├── .devrev/repo.yml              # deployable: false
├── .claude/
│   ├── settings.json             # SessionStart hook + committed plugin marketplace registration
│   ├── hooks/bootstrap-workspace.sh
│   └── skills/
│       ├── implementation-router/    # Master intent router
│       └── update-repos/             # Explicit-request-only repo refresh
├── skills/                       # The 8 domains, numbered in implementation-flow order
│   ├── 1-object-schema-customization/   SKILL.md + references/
│   ├── 2-stage-lifecycle-customization/ SKILL.md + references/
│   ├── 3-data-upload-and-org-build/     SKILL.md + references/
│   ├── 4-dashboards-and-widgets/        SKILL.md (router into dashboard-dev plugin)
│   ├── 5-datasets/                      SKILL.md (router into dataset-builder plugin)
│   ├── 6-workflows/                     SKILL.md + operations/ + references/ + examples/ + scripts/
│   ├── 7-agent-building/                SKILL.md + commands/ + knowledge/ + references/ + scripts/
│   └── 8-devrev-api/                    SKILL.md + references/ (full API catalog + domain docs)
├── repos/                        # Cloned toolchains (gitignored; never hand-edited)
└── docs/                         # ARCHITECTURE.md, SUMMARY.md (provenance), CLONE_RESULTS.md
```

## Why the numbering: implementation-flow order

The numbers encode the order a fresh DevRev org is built in — and the order the agent reasons in:

1. **Customization first** (skills 1–2): records need schemas, subtypes, and stage diagrams to exist
   before data can reference them.
2. **Data second** (skill 3): parts, Trails, accounts, rev-orgs, rev-users, work items — loaded onto
   the customized foundation.
3. **Analytics third** (skills 4–5): dashboards and datasets need records to visualize.
4. **Automation and intelligence last** (skills 6–7): workflows and AI agents consume everything
   built in the earlier layers.
5. **Skill 8 is horizontal**: the raw REST API foundation every other skill's calls are grounded in.

## Two species of skill

- **Knowledge-owning skills** (1, 2, 3, 6, 7, 8): carry their full domain knowledge inline —
  `references/` with the exact API docs, `operations/` catalogs, worked `examples/`, and runnable
  `scripts/`. Self-contained; nothing to install.
- **Router skills** (4, 5): deliberately thin. The real domain knowledge (widget JSON schema, OASIS
  SQL, validation pipeline, Oasis/Serengeti APIs, Ponos vs PaaS) lives inside the `dashboard-dev` and
  `dataset-builder` plugins in `repos/aai-skills`. These SKILL.md files only route to the right
  plugin command and enforce preconditions — they never duplicate plugin logic.

## The three cloned toolchains (`repos/`)

| Repo | Role |
| --- | --- |
| `repos/aai-skills` | Plugin marketplace `devrev-aai-plugins` — source of the `dashboard-dev` and `dataset-builder` plugins |
| `repos/dashboard-sync-cli` | Python CLI the dashboard plugin shells out to for all platform I/O (installed via pipx by the bootstrap) |
| `repos/api-specs` | DevRev OpenAPI contracts (`specs/next/openapi-internal.yaml`) — grounding for agent-building internal API calls |

Rules: `repos/` is a **clone target, never a source of truth** — gitignored, never hand-edited,
refreshed only when you explicitly ask (see [04 — Maintenance](04-maintenance.md)).

Deliberately excluded (documented in `docs/CLONE_RESULTS.md`): `devrev/devrev-snap-ins` (snap-ins are
out of scope) and `devrev/mcp-server` (archived — the hosted MCP in `.mcp.json` replaces it).
`devrev/auto-annotations` is auto-cloned on demand by the agent-building annotation checker.

## One `.env` serves everything

The single `.env` at repo root feeds:
- **API scripts** (`DEVREV_PAT`, aliased to `DEVREV_TOKEN`/`DEVREV_API_KEY` as needed)
- **The plugins** (dashboard-dev reads `DEVREV_PAT` + `DEVREV_ENDPOINT`; dataset-builder detects your
  dev/qa/prod environment from the PAT itself)
- **The dashboard-sync CLI**
- **The hosted MCP server** (`${DEVREV_PAT}` interpolation in `.mcp.json`)

## Design principle: determinism first

Everywhere a task *can* be deterministic, it *is*: org builds run as an ordered, idempotent,
re-runnable sequence; workflows are authored as schema-checked template JSON and imported (not
improvised step-by-step); dashboards go through a 3-stage validator before deployment; data loads
check-before-create so re-runs converge instead of duplicating. Model reasoning is reserved for
intent parsing and requirement drafting — execution goes through scripts, templates, and validators
that fail loudly. `docs/ARCHITECTURE.md` covers this in depth; `docs/SUMMARY.md` records exactly
which file came from which source project.
