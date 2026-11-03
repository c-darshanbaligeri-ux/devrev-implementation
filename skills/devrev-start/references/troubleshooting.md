# Setup problems and error fixes

Facts an agent needs that used to live only in the human README. Fix the cause; do not retry the same call.

| Symptom | Likely cause | What to do |
| --- | --- | --- |
| No token available | `DEVREV_PAT` unset and no `.env` | Tell the user to create a personal access token (Settings > Account > Personal Access Token), set `DEVREV_PAT` (or put it in `.env` from `.env.example`), then stop. Never invent a token. |
| 401 Unauthorized / `invalid token` | Missing, expired or revoked PAT (PATs cannot be renewed) | Test with `POST /ping`. Inspect the token's claims **locally** (command in `skills/10-api-conventions/SKILL.md`), never on a website. If expired, the user must create a new one. |
| 403 on one call | The token lacks that endpoint's scope | Report the missing scope from `devrev-find --endpoint <name>`; the user must regenerate the PAT with it. Do not retry. |
| A custom-field write "succeeded" but the field is empty | Wrong `tnt__` / `ctype__` prefix (fails silently) | Read `schemas.aggregated.get` for the real field name; resend with `custom_schema_spec`. |
| Records don't show a newly added schema field | Fragments are versioned and the records hold the old version | Re-save affected records via their `*.update`, or run `objects.bulk-upgrade` (destructive-class: confirm first). |
| A list stops after one page | Reading only `next_cursor` | Some operations return `cursor` instead; follow whichever is present (`skills/10-api-conventions`). |
| 429 Too Many Requests | Rate limit | Back off for `Retry-After` seconds; pace from the live `X-Ratelimit-*` headers, not a static number. |
| Workflow import fails | Almost always one of four causes: `uenum` missing `allowed_values`; `array` missing `base_type`; `for_each` used where a dedicated `loop_over_*` operation exists; `invoke_code` value-type mismatch | Full checklist in `skills/6-workflows/SKILL.md`. |
| Workflow trigger returns 400 "is not active" | The workflow is still a draft | Publish it first: `workflows.update-status` with `status: active` (or the UI's Deploy). See skill 6. |
| MCP shows unauthorized although `.env` is correct | `${DEVREV_PAT}` in `.mcp.json` is read from the **process environment**, not `.env` | Export `DEVREV_PAT` (or source `.env`) in the shell that launches Claude Code. |
| `dashboard-dev` / `dataset-builder` plugin commands missing | Plugin marketplace not trusted or not loaded | The user runs `/plugin marketplace update devrev-aai-plugins`; if the GitHub source cannot authenticate, register the local clone once with `/plugin marketplace add ./repos/aai-skills`. |
| `/create-dashboard` does not resolve | The plugin command is named `dashboard-create` | Use `/dashboard-dev:dashboard-create` (same for `/modify-dashboard` → `/dashboard-dev:modify-dashboard`). `/dashboard-planner` is a plugin **skill**, not a slash command. |
| `gcloud` / `bq` / `kubectl` fail during dataset work | Ponos-path tools are not installed (by design) | Only Ponos jobs need them; PaaS datasets need nothing extra (skill 5). |
| An agent-building script asks for `ORG_PAT` | Mutating internal-API calls need the optional org token | Add `ORG_PAT=` to `.env`, or stay with read-only / public operations (skill 7). |
| `/devrev:*` snap-in commands do not resolve, or report an MCP server not connected | Third-party plugin not installed or its MCP servers not opted in | Follow skill 9's preconditions (the install command there needs the local-shim workaround it documents). |
