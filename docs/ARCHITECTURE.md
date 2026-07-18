# Architecture

## Repository Structure

```
devrev-implementation/
├── CLAUDE.md                       (Global rules and routing)
├── README.md                       (Setup walkthrough)
├── .env.example                    (Template for credentials)
├── .gitignore                      (Excludes .env, repos/, logs/, etc.)
├── .mcp.json                       (Hosted DevRev MCP server config)
├── repos.txt                       (Toolchain repos to clone)
├── .devrev/repo.yml                (Non-deployable marker)
├── .claude/
│   ├── settings.json               (SessionStart hook, plugin marketplace)
│   ├── hooks/bootstrap-workspace.sh (Auto-setup: repos clone, CLI install)
│   └── skills/
│       ├── implementation-router/SKILL.md   (Master routing skill)
│       ├── capture-learnings/SKILL.md       (Self-learning protocol)
│       └── update-repos/{SKILL.md, update_repos.sh}  (Explicit refresh)
├── skills/
│   ├── 1-object-schema-customization/{SKILL.md, references/}
│   ├── 2-stage-lifecycle-customization/{SKILL.md, references/}
│   ├── 3-data-upload-and-org-build/{SKILL.md, references/}
│   ├── 4-dashboards-and-widgets/SKILL.md
│   ├── 5-datasets/SKILL.md
│   ├── 6-workflows/{SKILL.md, operations/, references/, examples/, scripts/}
│   ├── 7-agent-building/{SKILL.md, commands/, knowledge/, references/, scripts/}
│   └── 8-devrev-api/{SKILL.md, references/}
├── repos/.gitkeep                  (Clone target, gitignored after population)
└── docs/{ARCHITECTURE.md, SUMMARY.md, CLONE_RESULTS.md}
```

## Design Rationale

### Numbered Flow Order

The skills are numbered to reflect the natural dependency order of DevRev implementation work:

**Foundation Layer (1–3)**: Customization and data must come first
- **1-object-schema-customization**: Custom objects, tenant fields, subtypes, custom link types must be defined before records can be created
- **2-stage-lifecycle-customization**: Custom states, stages, and stage diagrams must exist before work items can flow through them
- **3-data-upload-and-org-build**: Artifacts, org structure (parts, trails, accounts, rev-orgs, rev-users), and bulk data loads depend on schemas and stages being in place

**Analytics Layer (4–5)**: Consumes data
- **4-dashboards-and-widgets**: Visualizations require existing records to query and chart
- **5-datasets**: Custom datasets aggregate and transform data from the platform

**Automation and Intelligence Layer (6–7)**: Highest-level capabilities
- **6-workflows**: Automations and agent-callable skills act on work items, which require the full foundation stack
- **7-agent-building**: AI agent configuration depends on workflows (for agent-callable skills), datasets (for grounding), and the complete object model

**Horizontal Foundation (8)**: The REST API layer
- **8-devrev-api**: Direct API knowledge base, used by all other skills when they need to make raw API calls

### Two Skill Species

**Router skills** (4, 5): Minimal SKILL.md files that delegate to plugins in `repos/aai-skills`
- `skills/4-dashboards-and-widgets`: Routes to `/dashboard-planner`, `/create-dashboard`, `/modify-dashboard`, and the `dashboard-dev` plugin's skills
- `skills/5-datasets`: Routes to `/dataset-builder:*` commands and the `dataset-builder` plugin's skills
- Domain knowledge lives in the plugin repos; these routers only handle preconditions, routing logic, and guardrails

**Knowledge-owner skills** (1, 2, 3, 6, 7, 8): Full SKILL.md files with inline `references/` directories
- Contain complete API reference docs, playbooks, schemas, examples, and scripts
- Self-contained: everything needed to execute is present in the skill folder
- No external plugin dependencies

### `repos/` Directory

- **Clone target**: Populated on first session by `.claude/hooks/bootstrap-workspace.sh` (background)
- **Never edited in place**: Clones are read-only reference material
- **Explicit refresh only**: Updated via the `update-repos` skill when user explicitly requests; never automatic
- **Gitignored**: The `repos/*/` pattern in `.gitignore` excludes all cloned content; only `repos/.gitkeep` is tracked

### Environment Variable Strategy

A single `.env` file at the repo root serves all consumers:
- **API scripts**: Source via `set -a; source .env; set +a`
- **Plugins**: `dashboard-dev` and `dataset-builder` read `DEVREV_PAT` directly
- **CLI tools**: `dashboard-sync` uses environment vars set by the bootstrap hook
- **Hosted MCP**: `.mcp.json` interpolates `${DEVREV_PAT}` from the environment

**Token naming**: `DEVREV_PAT` is canonical; synonyms and aliases:
- `DEVREV_API_KEY` ≡ `DEVREV_PAT` (interchangeable)
- `DEVREV_TOKEN` = alias for inherited scripts (set via `export DEVREV_TOKEN="$DEVREV_PAT"`)

### Determinism-First Execution Model

The repo enforces deterministic, validator-driven workflows:

**Dashboards**: Strict generate → validate → deploy → verify pipeline
- Parallel widget-generator agents produce JSON from requirements
- 3-stage validation: structure → semantic → live API (with auto-fix retries)
- Dashboard assembly and `dashboard-sync dashboard create` deploy
- Playwright visual verification
- **Never hand-write widget JSON**; never bypass validation

**Workflows**: Schema-checked template JSON
- 130 operation schemas in `skills/6-workflows/operations/schemas/`
- `templateVersion: "2.0.0"` envelope with stringified `data` field
- Validated examples in `skills/6-workflows/examples/`

**Org Builds**: Idempotent scripted loops with DON scratchpad persistence
- Phase ordering: auth → customization → parts → trails → custom links → work items → customer data
- `unique_key` for custom objects; check-before-create for stock objects
- Re-runs safe: same input → same output; failures loud

**Datasets**: SQL dry-run and integration tests before deploy
- BigQuery syntax validation via `bq query --dry_run`
- Ponos integration tests via `make int-test` (port-forwarded to dev/qa)
- Schema design follows published patterns (partition columns must be `TIMESTAMP`-typed)

**General principle**: Model reasoning produces plans; deterministic scripts/templates/validators execute them. If it's not in a reference file or a tool result, look it up — never fabricate API fields, DON ids, tokens, or file contents.
