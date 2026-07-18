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
│   ├── settings.json             # SessionStart hook + committed plugin marketplace registration (2 marketplaces)
│   ├── hooks/bootstrap-workspace.sh
│   └── skills/
│       ├── implementation-router/    # Master intent router
│       ├── capture-learnings/        # Self-learning protocol (routes discoveries to owning files + docs/LEARNINGS.md)
│       └── update-repos/             # Explicit-request-only repo refresh
├── skills/                       # The 10 domains, numbered in implementation-flow order (0 = design, 1–9 = build)
│   ├── 0-solution-architecture/         SKILL.md + references/ + templates/ + examples/
│   ├── 1-object-schema-customization/   SKILL.md + references/
│   ├── 2-stage-lifecycle-customization/ SKILL.md + references/
│   ├── 3-data-upload-and-org-build/     SKILL.md + references/
│   ├── 4-dashboards-and-widgets/        SKILL.md + references/ (router into dashboard-dev plugin)
│   ├── 5-datasets/                      SKILL.md (router into dataset-builder plugin)
│   ├── 6-workflows/                     SKILL.md + operations/ + references/ + examples/ + scripts/
│   ├── 7-agent-building/                SKILL.md + README.md + commands/ + knowledge/ + references/ + scripts/
│   ├── 8-devrev-api/                    SKILL.md + references/ (full API catalog + domain docs)
│   └── 9-snapin-development/            SKILL.md (external-plugin router into devrev-qk-agents)
├── repos/                        # Cloned toolchains (gitignored; never hand-edited)
├── docs/                         # ARCHITECTURE.md, SUMMARY.md (provenance), LEARNINGS.md (journal), CLONE_RESULTS.md
└── documentation/                # This user-facing docs folder
```

## Why the numbering: implementation-flow order

The numbers encode the order the agent reasons in — design before build, foundation before consumers:

0. **Design first** (skill 0): greenfield or cross-domain requests start here. Produces a 20-section
   solution blueprint that hands off section-by-section to the build skills. Never calls the live API.
1. **Customization first** (skills 1–2): records need schemas, subtypes, and stage diagrams to exist
   before data can reference them.
2. **Data second** (skill 3): parts, Trails, accounts, rev-orgs, rev-users, work items — loaded onto
   the customized foundation.
3. **Analytics third** (skills 4–5): dashboards and datasets need records to visualize.
4. **Automation and intelligence next** (skills 6–7): workflows and AI agents consume everything
   built in the earlier layers.
5. **Skill 8 is horizontal**: the raw REST API foundation every other skill's calls are grounded in.
6. **Extensibility last** (skill 9): snap-in / AirSync connector development. Independent of the
   other build layers (a snap-in can be planned/built without any of skills 1–7 in place), but its
   Architect output often produces connectors that feed the object model skills 1–3 manage.

## Four species of skill

- **Design skill** (0): a full `SKILL.md` + inline `references/`/`templates/`/`examples/`, but
  distinct from the knowledge-owners below because it never calls the live API — it's pure design
  reasoning that hands off to the others. Its references cross-reference skills 1, 2, 6, 7, 8 for
  exact API mechanics rather than duplicating them.
- **Knowledge-owning skills** (1, 2, 3, 6, 7, 8): carry their full domain knowledge inline —
  `references/` with the exact API docs, `operations/` catalogs, worked `examples/`, and runnable
  `scripts/`. Self-contained; nothing to install.
- **Native-plugin router skills** (4, 5): deliberately thin. The real domain knowledge (widget JSON
  schema, OASIS SQL, validation pipeline, Oasis/Serengeti APIs, Ponos vs PaaS) lives inside the
  `dashboard-dev` and `dataset-builder` plugins in `repos/aai-skills` (marketplace `devrev-aai-plugins`,
  auto-enabled). These SKILL.md files only route to the right plugin command and enforce
  preconditions.
- **External-plugin router skill** (9): also thin, but delegates to a plugin from a **different
  marketplace and a different GitHub org** (`QK-SnapIn/devrev-qk-agents`). The marketplace is
  registered in `.claude/settings.json` but the plugin is **not auto-enabled** — third-party org,
  manual `/plugin install`. Also excludes half of the routed plugin's surface (the dashboard
  vertical, which hand-writes widget JSON and violates skill 4's hard rule).

## The four cloned toolchains (`repos/`)

| Repo | Role |
| --- | --- |
| `repos/aai-skills` | Plugin marketplace `devrev-aai-plugins` — source of the `dashboard-dev` and `dataset-builder` plugins (auto-enabled) |
| `repos/dashboard-sync-cli` | Python CLI the dashboard plugin shells out to for all platform I/O (installed via pipx by the bootstrap) |
| `repos/api-specs` | DevRev OpenAPI contracts (`specs/next/openapi-internal.yaml`) — grounding for agent-building internal API calls |
| `repos/devrev-qk-agents` | Third-party plugin source (marketplace `devrev-qk-agents`) — powers skill 9's PM/Architect/Tester snap-in pipeline; plugin **not auto-enabled** — user runs `/plugin install devrev@devrev-qk-agents` once |

Rules: `repos/` is a **clone target, never a source of truth** — gitignored, never hand-edited,
refreshed only when you explicitly ask (see [04 — Maintenance](04-maintenance.md)). If a
`/devrev:improve-skill` command patches something under `repos/devrev-qk-agents/`, the patch is
disposable (an `update-repos` refresh overwrites it) — record the same fix in skill 9's Field notes so
it survives.

Deliberately excluded (documented in `docs/CLONE_RESULTS.md`): `devrev/devrev-snap-ins` (snap-in
*source* is out of scope — skill 9 covers snap-in *building* via the routed plugin) and
`devrev/mcp-server` (archived — the hosted MCP in `.mcp.json` replaces it). `devrev/auto-annotations`
is auto-cloned on demand by the agent-building annotation checker.

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
