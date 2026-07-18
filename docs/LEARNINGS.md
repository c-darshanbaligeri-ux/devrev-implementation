# Learnings journal

Append-only log of discoveries made while operating this repo — errors hit, restrictions found,
undocumented behaviors, corrections. Each entry here has a matching edit in the *owning* file
(the specific SKILL.md, reference doc, or checklist) — this journal is the audit trail, the owning
file is where the knowledge actually works. Protocol: `.claude/skills/capture-learnings/SKILL.md`.

Rules: append rows at the bottom; never rewrite or delete old rows; no secrets or real customer
DON ids (redact to `<REDACTED>`); one learning per row.

| Date | What happened | Fact learned / root cause | Files updated |
| --- | --- | --- | --- |
| 2026-07-18 | Repo built; journal initialized | — | — |
| 2026-07-18 | Build audit: skill 2 frontmatter had an unquoted `: ` in description — YAML parse failure would break skill loading | Quote SKILL.md descriptions containing colons | `skills/2-*/SKILL.md` |
| 2026-07-18 | Build audit: API catalog claimed full endpoint coverage but had no Parts section; `parts.create/list` + per-type scopes were invisible to catalog-first lookup | Catalog must cover parts; scope tracks part type (product/capability/feature) | `skills/8-*/references/00_API_Catalog.md`, `skills/8-*/SKILL.md` (routing row) |
| 2026-07-18 | Build audit: references document `is_deprecated` only on stage nodes INSIDE a diagram — whole-diagram and state deprecation are not documented anywhere | Don't claim diagram/state deprecation; verify against live API before attempting | `skills/2-*/SKILL.md`, `CLAUDE.md` safety list |
| 2026-07-18 | Build audit: several citations pointed at wrong sections/files (customer build order lives in Customers doc §8, not the org-build doc; `unique_key` is §1.5 not §1.2; toolkit commands cited a CLAUDE.md that no longer carries those sections) | Citations must be verified against the actual reference text, not assumed | `skills/3-*/SKILL.md` (+ copied Customers reference), `skills/7-*/commands/*`, `skills/7-*/references/*` |
| 2026-07-18 | Build audit: `${VAR}` in `.mcp.json` reads the process environment, not `.env` — MCP auth can fail even with a correct `.env` | Export DEVREV_PAT (or source .env) in the shell launching Claude Code for MCP | `README.md` (self-configures table) |
| 2026-07-18 | Solution-architecture merge: adding `skills/0-solution-architecture/templates/solution-blueprint.md` silently failed `git add` — the file never appeared staged | Root `.gitignore` had bare (unanchored) patterns `templates/`, `dashboards/`, `datasets/`, `plans/` meant only for the repo-root workspace dirs the bootstrap hook creates; unanchored, they match at ANY depth and swallowed the new skill's own `templates/` folder | `.gitignore` (anchored all 4 with a leading `/`) |
| 2026-07-18 | Snap-in merge: `repos/aai-skills/.claude-plugin/marketplace.json` (already-cloned SHA 57b8a5f) declares a `connector-dev` plugin at `./plugins/connector-dev`, but that directory does not exist in the clone | Upstream `devrev/aai-skills` drift — a plugin can be listed in the marketplace manifest without its source existing at a given pinned commit; don't trust manifest listings without confirming the directory | `docs/ARCHITECTURE.md` ("A known upstream gap"), `skills/9-*/SKILL.md` |
| 2026-07-18 | Snap-in merge: the `devrev-qk-agents` plugin's `/devrev:improve-skill` self-learning command patches files under what becomes `repos/devrev-qk-agents/` once cloned here — this repo's own rule says never edit `repos/` | A third-party plugin's self-improvement design can conflict with a host repo's clone-hygiene rule; resolve by treating the in-`repos/` patch as disposable and duplicating the same fact into the host skill's own Field notes | `skills/9-*/SKILL.md` ("Self-learning is plugin-scoped"), `.claude/skills/capture-learnings/SKILL.md` (routing row) |
