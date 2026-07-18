# Provenance Summary

This document tracks the source lineage and adaptations for all artifacts in the `devrev-implementation` repository.

## Source Repositories

- **S1** = `/Users/q15137/Documents/The one/API's` — DevRev REST API knowledge base
- **S2** = `/Users/q15137/Documents/The one/devrev-workflow-admin` — workflow authoring/admin skill
- **S3** = `/Users/q15137/Documents/The one/Dashboard and Widget Creation` — working plug-and-play workspace
- **S4** = `/Users/q15137/Documents/The one/aai-custom-computer-capabilities/3-computer-capabilities-nxt/agent-building-toolkit` — agent-building toolkit
- **S5** = `/Users/q15137/Documents/The one/plan-skill-workspace/devrev-solution-architect` — standalone design-phase skill (2026-07-18 merge; built independently of S1–S4, with zero prior shared authorship)
- **S6** = `/Users/q15137/Documents/The one/devrev-snapins-main` (repo `QK-SnapIn/devrev-qk-agents`) — standalone Claude Code plugin for snap-in/AirSync connector development (2026-07-18 merge; third-party org, not `devrev/aai-skills`)

## Provenance Table

| Destination | Source | Adaptation |
|-------------|--------|------------|
| **Root config files** | | |
| `.gitignore` | Authored new | Combines patterns from S3 with repo-specific exclusions (repos/*, plans/, templates/, dashboards/, datasets/) |
| `.mcp.json` | S3 `.mcp.json` | Verbatim copy; proven hosted DevRev MCP configuration |
| `.env.example` | Authored new | Standardized on `DEVREV_PAT` (canonical) + `DEVREV_ENDPOINT`; added optional `ORG_PAT` for skills/7-agent-building |
| `repos.txt` | Authored new | Lists 4 repos (aai-skills, dashboard-sync-cli, api-specs, devrev-qk-agents — the 4th added 2026-07-18 for skills/9); documents 2 deliberate exclusions |
| `.devrev/repo.yml` | Authored new | Single line: `deployable: false` |
| **`.claude/` infrastructure** | | |
| `.claude/settings.json` | Authored new | SessionStart hook + `extraKnownMarketplaces` (github-source to devrev/aai-skills AND QK-SnapIn/devrev-qk-agents, added 2026-07-18) + `enabledPlugins` (dashboard-dev, dataset-builder — deliberately excludes the `devrev` plugin from devrev-qk-agents; third-party org, manual opt-in only, see skills/9) |
| `.claude/hooks/bootstrap-workspace.sh` | S3 bootstrap hook | Extended with: (1) `.env` gate, (2) workspace dirs creation, (3) repos/ initial clone (background, once, writes to CLONE_RESULTS.md), (4) dashboard-sync CLI install via pipx (background, once) |
| `.claude/skills/update-repos/SKILL.md` | S3 `update-repos/SKILL.md` | Updated post-run note: restart Claude Code or `/plugin marketplace update devrev-aai-plugins` if aai-skills changed; removed clone_repos.sh reference |
| `.claude/skills/update-repos/update_repos.sh` | S3 `update-repos/update_repos.sh` | Verbatim copy; idempotent shallow clone with dirty-check skip |
| `.claude/skills/implementation-router/SKILL.md` | Authored new | Master router with routing table (8 skills + update-repos + capture-learnings); preconditions check (.env, ping); never reconstruct from memory |
| `.claude/skills/capture-learnings/SKILL.md` | Authored new (2026-07-18 refinement) | Self-learning protocol: routes discoveries (errors, restrictions, undocumented behavior) to the specific owning file + docs/LEARNINGS.md journal |
| `docs/LEARNINGS.md` | Authored new (2026-07-18 refinement) | Append-only learnings journal (audit trail for the capture-learnings protocol) |
| **skills/0-solution-architecture** | | |
| `SKILL.md`, `templates/solution-blueprint.md`, `examples/` (3 files) | S5 (verbatim) | No structural change — the unique methodology brain (6-step problem-working process, 20-section blueprint template, 3 worked examples) has no Tree-B equivalent. Added: "Field notes" section, "Handing off to execution" table (blueprint section → execution skill, incl. 2 honestly-flagged gaps: AirSync setup and Security/Permissions have no execution-skill counterpart in this repo), frontmatter `name` changed `devrev-solution-architect` → `solution-architecture` (repo naming convention) |
| `references/{data-model,api-cookbook,workflows-automation,agents,patterns-and-recipes}.md` | S5, trimmed | API-mechanics sections replaced with pointers into skills/1, 2, 6, 7, 8 (which document the same facts at equal-or-greater fidelity, incl. empirically-verified wire formats). Design/conceptual framing kept verbatim. One correction folded in: `ai-agents.plans.get/list` confirmed not to exist (live-verified) |
| `references/{extensibility-and-apis,integrations-channels,decision-frameworks,estimation-and-delivery,case-studies}.md` | S5 (verbatim) | No Tree-B equivalent exists for AirSync/channels/PLuG, analytics concepts, RBAC/permissions model, notifications, case studies, effort estimation, or the master decision-tree framework — kept as-is |
| **skills/8-devrev-api** | | |
| `skills/8-devrev-api/references/` (10 files) | S1 (9 .md files) | Verbatim copies: 00_API_Catalog.md, Work_Items_Timeline_Tags_Links_API.md, Customers_Users_and_Orgs_API.md, Support_Knowledge_and_SLAs_API.md, Platform_and_Admin_API.md, Custom_Objects_and_Links_API.md, Stock_Object_Modification_and_Schemas_API.md, Stages_States_and_StageDiagrams_API.md, DevRev_Building_Org_Using_API_v1.md |
| `skills/8-devrev-api/references/devrev-mcp-claude-code-setup.md` | S1 (same filename) | Copied + PREPENDED superseded notice (hosted MCP via .mcp.json supersedes npx @devrev/mcp-server) |
| `skills/8-devrev-api/SKILL.md` | S1 `SKILL.md` | Path updates (doc references → references/); token guidance updated (DEVREV_PAT from .env, alias DEVREV_TOKEN); added "When not to use" line (workflows/agents/dashboards/datasets → other skills) |
| **skills/9-snapin-development** | | |
| `SKILL.md` | Authored new | Router-only; a fourth species (external-plugin router — see docs/ARCHITECTURE.md). Routes to the `devrev` plugin (`devrev-qk-agents`, S6) for the snap-in vertical only. Documents 2 required MCP servers as manual opt-in (not wired into `.mcp.json`); flags a 3rd MCP ("devrev-sdk MCP") as NOT VERIFIED (setup command undocumented in S6). Explicitly excludes S6's own "Implementation" (dashboard) vertical — it hand-writes widget JSON, violating skills/4's hard rule. Notes the plugin's own self-learning command (`/devrev:improve-skill`) patches `repos/devrev-qk-agents/`, which conflicts with this repo's never-edit-`repos/` rule — resolved by requiring a duplicate Field-notes entry here. Also flags a `connector-dev` plugin gap in the already-cloned `repos/aai-skills` (declared in that repo's own marketplace.json but its source directory doesn't exist at the pinned SHA — upstream drift, not introduced here). |
| **skills/1-object-schema-customization** | | |
| `references/` (2 files) | S1 | Verbatim copies: Custom_Objects_and_Links_API.md, Stock_Object_Modification_and_Schemas_API.md |
| `SKILL.md` | Authored new | Grounded in the 2 reference files; playbooks for custom objects, tenant fields, subtypes, custom link types; every endpoint/scope/field cited from references |
| **skills/2-stage-lifecycle-customization** | | |
| `references/` (1 file) | S1 | Verbatim copy: Stages_States_and_StageDiagrams_API.md |
| `SKILL.md` | Authored new | Grounded in the reference file; playbook for states → stages → stage diagram → subtype assignment → dependent fields |
| **skills/3-data-upload-and-org-build** | | |
| `references/` (2 files) | S1 | Verbatim copies: DevRev_Building_Org_Using_API_v1.md, Platform_and_Admin_API.md |
| `SKILL.md` | Authored new | Grounded in the 2 reference files; playbooks for artifact upload, ordered org build (5 phases), bulk record creation (honest: no bulk endpoint, scripted loops) |
| **skills/4-dashboards-and-widgets** | | |
| `SKILL.md` | Authored new | Router-only; modeled on S3 `.claude/skills/devrev-dashboards/SKILL.md`; routes to /dashboard-planner, /create-dashboard, /modify-dashboard, widget-development/dashboard-development skills in repos/aai-skills; enforces hard rule (never bypass generate→validate→deploy→verify pipeline) |
| **skills/5-datasets** | | |
| `SKILL.md` | Authored new | Router-only; routes to /dataset-builder:* commands; PaaS vs Ponos decision table (from repos/aai-skills/plugins/dataset-builder/README.md); preconditions (DEVREV_PAT for PaaS; +gcloud/bq/AWS/kubectl for Ponos); known gotchas; safety (destructive deletes) |
| **skills/6-workflows** | | |
| `references/`, `operations/`, `examples/`, `scripts/` | S2 (all 4 dirs) | Copied recursively; applied 4 fixups (see below) |
| `SKILL.md` | S2 `SKILL.md` | Fixups: (1) stale path `.claude/skills/devrev-workflow-admin/` → `skills/6-workflows/`; (2) `/tmp/op_schemas/<slug>.json` → `operations/schemas/<slug>.md` (wording adjusted); (3) count "106" → "130" (actual schema count); (4a) token guidance (DEVREV_PAT from .env), (4b) added "When not to use" (snap-in dev out of scope, AI agent config → skills/7), (4c) learning loop path → `skills/6-workflows/examples/` |
| **skills/7-agent-building** | | |
| `commands/`, `knowledge/`, `references/`, `scripts/` | S4 (all 4 dirs) | Copied; EXCLUDED: .env, .env.example (REAL SECRETS), presentations/, agent-instructions-ai_agent-1.md, dependent-objects-bridge-skill-guide.md (client-specific), .claude/, .claude-plugin/, hooks/, LICENSE, .gitignore, references/IMPROVEMENTS.md; secret scan mandatory (eyJ regex) |
| `references/toolkit-guide.md` | S4 `CLAUDE.md` | Renamed on copy; fixed relative links (knowledge/ → ../knowledge/) |
| `SKILL.md` | S4 `SKILL.md` | Fixups: (1) removed `disable-model-invocation: true` frontmatter; (2) path `.cursor/skills/devrev-agent-toolkit/` → `skills/7-agent-building/`, `${CLAUDE_PLUGIN_ROOT}` → `skills/7-agent-building`; (3) env note (DEVREV_PAT for public API, ORG_PAT optional for internal API); (4) article ID updates (old ART-27856/27858/27860 → current ART-30501/30502/30503 per knowledge/INDEX.md) |
| **Top-level docs** | | |
| `CLAUDE.md` | Authored new | Structure from S1 `CLAUDE.md` (global API rules source); plug-and-play phrasing from S3 `CLAUDE.md`; 8 sections: identity, routing table, plug-and-play (one manual step = .env), global API rules (verbatim from S1), execution flow, safety, keeping repos current, guardrails |
| `README.md` | Authored new | Sections: what this is, one-time setup, what self-configures (table), capability map (8 skills), plug-and-play acceptance, troubleshooting |
| `docs/ARCHITECTURE.md` | Authored new | Final tree + design rationale: numbered flow order (customization→data→analytics→automation→API), two skill species (routers vs knowledge-owners), repos/ never-edited, env var strategy (one .env), determinism-first execution model |
| `docs/SUMMARY.md` | Authored new (this file) | Provenance table covering all artifacts; source→destination→adaptation mappings |
| `docs/CLONE_RESULTS.md` | Generated by Chunk J | Created by bootstrap hook's repos/ clone; table with repo/status/branch/SHA; deliberate exclusions section |

## Key Decisions

### Environment Variable Standardization
- **Canonical**: `DEVREV_PAT` in `.env`
- **Synonyms**: `DEVREV_API_KEY` ≡ `DEVREV_PAT` (interchangeable)
- **Aliases**: `DEVREV_TOKEN` = legacy name for inherited scripts; set via `export DEVREV_TOKEN="$DEVREV_PAT"`
- **Rationale**: Single source of truth; scripts/plugins/CLI/MCP all read from the same `.env`

### Hosted MCP Supersedes npx Flow
- `.mcp.json` wires `https://api.devrev.ai/mcp/v1` (hosted DevRev MCP server)
- `references/devrev-mcp-claude-code-setup.md` in skills/8 has PREPENDED superseded notice
- Legacy `npx @devrev/mcp-server` flow kept for reference only (devrev/mcp-server repo is archived)

### Deliberately Excluded Repos
**Not in `repos.txt`**:
1. `devrev/devrev-snap-ins`: Snap-in source development is out of scope for this repo (only tangential reference: `trigger-dashboard-agent` in snap-ins, which is optional/Dev0-only)
2. `devrev/mcp-server`: Archived; superseded by hosted MCP at `https://api.devrev.ai/mcp/v1`

**Cloned on demand**:
- `devrev/auto-annotations`: Not in repos.txt; cloned only when `skills/7-agent-building/scripts/check-annotations.sh` runs

### Workflow-Builder Plugin Not Consolidated
- `workflow-skill` (workflow-builder plugin in S4's parent directory) was NOT consolidated
- **Rationale**: Known upstream alternative to `skills/6-workflows`; user already has S2's devrev-workflow-admin as the canonical workflow skill
- Both approaches valid; S2 chosen for this repo

### Agent-Building Commands as Reference Files
- S4 `.claude/commands/*.md` → `skills/7-agent-building/commands/` (no `.claude/commands/` registration)
- **User decision**: Commands available as reference material only; not registered as slash commands
- **Rationale**: Avoids namespace collision; keeps /commands focused on implementation-router and marketplace-provided commands

## Fixups Applied

### skills/6-workflows (S2 copy)
1. **Stale path prefix**: `grep -rl` then `sed -i ''` to replace `.claude/skills/devrev-workflow-admin/` → `skills/6-workflows/` across all .md files
2. **Stale schema path**: `/tmp/op_schemas/<slug>.json` → `operations/schemas/<slug>.md` (sentence wording adjusted, not just path)
3. **Count drift**: "106" → "130" (actual schema file count in operations/schemas/)
4. **SKILL.md updates**: (a) token from `.env` (DEVREV_PAT), (b) "When not to use" (snap-in dev, AI agent config), (c) learning loop path → `skills/6-workflows/examples/`

### skills/7-agent-building (S4 copy)
1. **Secret exclusion**: Mandatory `grep -rE 'eyJ[A-Za-z0-9_-]{20,}'` scan; .env/.env.example never copied
2. **Path prefix**: `.cursor/skills/devrev-agent-toolkit/` → `skills/7-agent-building/`, `${CLAUDE_PLUGIN_ROOT}` → `skills/7-agent-building` (all .md files and scripts)
3. **Env & auth note**: `DEVREV_PAT` from repo-root `.env` (public API); `ORG_PAT` optional (internal API) — added to SKILL.md
4. **Article ID updates**: ART-27856 → ART-30501, ART-27858 → ART-30502, ART-27860 → ART-30503 (per knowledge/INDEX.md)
5. **Excluded client artifacts**: agent-instructions-ai_agent-1.md, dependent-objects-bridge-skill-guide.md, presentations/
6. **Frontmatter**: Removed `disable-model-invocation: true` (skill must be routable)

### skills/8-devrev-api (S1 copy)
1. **Doc references**: Old paths → `references/<filename>` (checked every table row in SKILL.md)
2. **Token wording**: Lone `$DEVREV_TOKEN` → token from `.env` (`DEVREV_PAT`), alias via `export DEVREV_TOKEN="$DEVREV_PAT"`
3. **When not to use**: Added line routing workflows/agent configs/dashboards/datasets to other skills
4. **MCP setup doc**: PREPENDED superseded notice (hosted MCP via .mcp.json; npx flow legacy)

### Bootstrap Hook (S3 extension)
1. **Gate**: If no `.env` → echo gate message → `exit 0` (no side effects)
2. **Workspace dirs**: `mkdir -p dashboards datasets plans logs templates` (synchronous)
3. **repos/ clone**: Background once; writes per-repo status to `docs/CLONE_RESULTS.md` (table with branch/SHA/notes)
4. **dashboard-sync install**: Background once via pipx (S3 logic verbatim)
5. **Conventions preserved**: `set +e`, fully-detached background subshells, `.claude/.auto-setup/` status dir, always `exit 0`

### Update-Repos Skill (S3 copy)
1. **Post-run note**: If aai-skills changed → restart Claude Code or `/plugin marketplace update devrev-aai-plugins`
2. **Removed reference**: No `clone_repos.sh` (initial clone is bootstrap hook's job)
3. **Script logic**: Unchanged (dirty→SKIPPED, default branch detection, `git reset --hard origin/<branch>`)

## Verification (build-time, 2026-07-18)

| Check | Result |
| --- | --- |
| Secret scan (`eyJ[A-Za-z0-9_-]{20,}`, excluding `repos/`) | CLEAN — no matches; no `.env` files present |
| Stale paths (`/tmp/op_schemas`, `.cursor/`, `CLAUDE_PLUGIN_ROOT`, old skill paths) | CLEAN (provenance mentions in this file excepted) |
| Shell syntax (`bash -n` on hook, update_repos, 7 toolkit scripts) | PASS |
| Python (`py_compile` trigger_manual_workflow.py) | PASS |
| JSON (.mcp.json, .claude/settings.json, 13 workflow example templates incl. stringified `data`) | PASS |
| Tree completeness (8 skills; 130 op schemas; 13 examples; 10 knowledge articles; 8 commands; 7 scripts) | PASS |
| Bootstrap hook dry-run (no `.env` → gate message, exit 0, zero side effects; with `.env` → dirs created, background install + log) | PASS |
| update-repos idempotency + dirty-repo safety (second run "up to date"; dirtied repo SKIPPED, never reset) | PASS |
| Clones | aai-skills main@57b8a5f, dashboard-sync-cli main@451a51d, api-specs main@79cd29e |

**Marketplace registration variant shipped**: GitHub source (`{"source": "github", "repo": "devrev/aai-skills"}`)
in project `.claude/settings.json`, activated by the one-time workspace-trust prompt. Fallback documented in
README troubleshooting: `/plugin marketplace add ./repos/aai-skills` (local clone) if GitHub-source auth to the
private repo fails in a given environment.

**Build-time fixes beyond the plan** (recorded for honesty):
- `skills/6-workflows/SKILL.md` frontmatter `name:` changed `devrev-workflow-admin` → `workflows` (stale name).
- Bootstrap hook `dashboard-sync init` idempotency uses a `.claude/.auto-setup/init.done` marker instead of
  checking `dashboards/` existence (this repo pre-creates that directory, so existence can't signal init state).

## Completeness check vs the four source projects (2026-07-18)

Verified file-by-file. Everything carried over or deliberately excluded:

- **`API's`**: all 10 reference .md files copied (skills/8 + duplicated into skills/1–3 per design);
  CLAUDE.md/SKILL.md adapted into root CLAUDE.md + skills/8 SKILL.md. Excluded:
  `DevRev_Building_Org_Using_API_v1.docx` (exact duplicate of the .md).
- **`devrev-workflow-admin`**: 100% carried (SKILL.md, 3 references, 5 operations files + 130
  schemas, 13 examples, trigger script) with path/count fixups.
- **`Dashboard and Widget Creation`**: mechanics adapted (.mcp.json, .gitignore, settings.json,
  bootstrap hook, update-repos, devrev-dashboards router → skills/4); context/OVERVIEW.md and
  context/API_AND_JSON.md added to `skills/4-dashboards-and-widgets/references/` (completeness
  pass). Excluded: START_HERE.md, SUMMARY.md, CLONE_RESULTS.md, clone_repos.sh, repos.txt
  (project-specific task-package artifacts superseded by this repo's own equivalents), repos/
  clones (re-cloned here).
- **`aai-custom-computer-capabilities`**: agent-building-toolkit fully carried (SKILL.md, 8
  commands, knowledge, references, 7 scripts; CLAUDE.md → references/toolkit-guide.md; README's
  auth table folded into skills/7 README; hooks' knowledge-freshness check documented as a manual
  step in skills/7 README). Excluded by design: `.env`/`.env.example` (real secrets), LICENSE,
  `.claude-plugin/` + `hooks/` (plugin-install machinery — not a plugin here), presentations/
  (slide deck), `agent-instructions-ai_agent-1.md` + `dependent-objects-bridge-skill-guide.md`
  (client-specific artifacts), `references/IMPROVEMENTS.md` (historical changelog), `.claude/`
  command dupes. All snap-in dirs (1-*, 2-*, 4-*) and non-agent nxt skills: out of scope.
  `workflow-skill` (workflow-builder plugin): not consolidated — skills/6 covers the domain;
  known upstream alternative.

## Fifth-source merge: `plan-skill-workspace` (2026-07-18)

Unlike S1–S4, **S5 (`plan-skill-workspace`) was NOT deleted or fully absorbed** — it remains an
independent, standalone skill at its original path (its own CLAUDE.md says to publish it separately
via skill-creation tooling, so nothing there was removed wholesale). What happened instead:

1. **Deduplicated in place at the source** — the 5 reference files with API-mechanics overlap
   (`data-model.md`, `api-cookbook.md`, `workflows-automation.md`, `agents.md`,
   `patterns-and-recipes.md`) were trimmed inside `plan-skill-workspace/devrev-solution-architect/references/`
   itself, replacing exact payloads/schemas/node catalogs with cross-repo pointers into this repo's
   skills 1, 2, 6, 7, 8. The other 5 reference files, the SKILL.md, the blueprint template, and the
   3 examples have no equivalent in this repo and were left untouched.
2. **Embedded here as `skills/0-solution-architecture`** — a copy of the now-deduplicated content,
   with the same 5 files' pointers rewritten to in-repo relative paths, plus two additions specific
   to this repo: a "Field notes" section (wired to `docs/LEARNINGS.md`) and a "Handing off to
   execution" table mapping each blueprint section to the skill that builds it — including two
   honestly-flagged gaps (AirSync connector setup and Security/Permissions/RBAC have no execution
   skill in this repo).
3. **One correction folded in** from this repo's empirically-verified knowledge:
   `ai-agents.plans.get`/`ai-agents.plans.list` do not exist as endpoints (live-verified against the
   internal API), now stated in both copies' `agents.md`.

Net effect: `plan-skill-workspace` stays independently publishable with no duplicate API-mechanics
content, and `devrev-implementation` gains a design phase that precedes its 8 execution skills.

## Sixth-source merge: `devrev-snapins-main` (2026-07-18)

Unlike S1–S5, **S6 (`devrev-snapins-main`, repo `QK-SnapIn/devrev-qk-agents`) is a fully-built Claude
Code plugin**, not reference material — 7 agents, 11 commands, 7 skills across two verticals (snap-in
development; dashboard/widget development). Nothing from S6 was copied into `devrev-implementation`;
the merge is architectural — a new router skill plus repo-level registration:

1. **`skills/9-snapin-development` authored new** — a router in the same spirit as skills 4/5, but a
   distinct fourth species: it delegates to a plugin from a **different marketplace and a different
   GitHub org** than `devrev/aai-skills` (see docs/ARCHITECTURE.md "Four Skill Species").
2. **Only the snap-in vertical is routed to.** S6's "Implementation" vertical (dashboard PM/Architect/
   Tester) is explicitly excluded — its Architect agent generates widget JSON by hand, which is exactly
   what `skills/4-dashboards-and-widgets`'s HARD RULE forbids (that rule exists because hand-authored
   widget JSON produced unreliable output in this repo's own build history — see
   `skills/0-solution-architecture/references/estimation-and-delivery.md` §7). Routing to it would
   silently violate an existing safety rule.
3. **Plugin registered but deliberately not auto-enabled.** `.claude/settings.json` gained a new
   `extraKnownMarketplaces` entry (`devrev-qk-agents` → `QK-SnapIn/devrev-qk-agents`) so the plugin is
   installable, but `enabledPlugins` was NOT extended to include it — auto-activating a third-party
   org's code on every session (unlike DevRev's own `dashboard-dev`/`dataset-builder`) is a trust
   boundary this repo doesn't cross without an explicit, visible `/plugin install` from the user.
   `repos.txt` gained a matching clone entry for reading/grounding only.
4. **Three MCP-server dependencies documented as manual opt-in**, per this repo's existing "no
   unattended network installs beyond the confirmed bootstrap" guardrail — `snapin-builder-mcp` and
   `chef-cli mcp` setup commands are given verbatim in the skill; a third ("devrev-sdk MCP") is flagged
   as NOT VERIFIED because S6 references it without ever documenting its setup command.
5. **A pre-existing upstream gap surfaced during comparison, not introduced by this merge**: the
   already-cloned `repos/aai-skills` declares a `connector-dev` plugin in its own marketplace.json, but
   that plugin's source directory doesn't exist in the clone at the pinned SHA. Recorded in
   `docs/ARCHITECTURE.md` and `skills/9`'s SKILL.md so a future `update-repos` refresh that picks up
   `connector-dev` gets compared against skill 9 rather than assumed redundant or superior.
6. **A design tension named, not silently resolved**: S6's own `/devrev:improve-skill` self-learning
   command patches files inside the plugin, which (once cloned) live under `repos/devrev-qk-agents/` —
   this repo's own rule says never edit `repos/`. Skill 9 resolves this by treating any such patch as
   disposable (it's overwritten on the next `update-repos` refresh) and requiring the same learning to
   also be recorded in skill 9's own Field notes, which does survive a refresh.

Net effect: this repo's Identity line no longer needs to say "apart from snap-in development" — that
gap is now covered, but via routing and manual opt-in, not by building or auto-activating new
first-party tooling for it.
