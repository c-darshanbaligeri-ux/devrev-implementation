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
