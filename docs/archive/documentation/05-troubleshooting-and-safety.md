# 05 — Troubleshooting & Safety

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Session starts but nothing auto-configures; a one-line "create .env" message appears | `.env` missing | `cp .env.example .env`, add your PAT, restart the session |
| `command not found: dashboard-sync` right after adding `.env` | Background install still running, or PATH not refreshed | Check `.claude/.auto-setup/install.log`; if it ends with "install finished OK", start a **new** session so PATH picks up `~/.local/bin` |
| `/plugin` doesn't show `dashboard-dev` / `dataset-builder` | Workspace-trust prompt not accepted, or plugins not reloaded | Accept the trust prompt; restart Claude Code or run `/plugin marketplace update devrev-aai-plugins`. If the GitHub-source marketplace can't authenticate against the private repo, register the local clone once: `/plugin marketplace add ./repos/aai-skills` |
| 401 Unauthorized on API calls | Missing/expired PAT | Verify `.env`; test with `curl -X POST https://api.devrev.ai/ping -H "Authorization: Bearer $DEVREV_PAT" -d '{}'` |
| 403 on a specific call | Token lacks the endpoint's scope | The agent reports the missing scope from the API catalog — regenerate the PAT with that scope rather than retrying |
| Clone failures in `docs/CLONE_RESULTS.md` | No GitHub read access to the `devrev` org | `gh auth status`; ensure the account has org read access, then rerun the update-repos skill |
| A custom field write "succeeded" but the field is empty | Wrong `tnt__`/`ctype__` prefix — this **fails silently** | Check the aggregated schema (`schemas.aggregated.get`) for the real field name; resend with `custom_schema_spec` |
| Records don't show a newly added schema field | Fragments are versioned; records hold the old version | Re-save affected records via their `*.update` |
| Workflow template import fails | Almost always one of four known causes | `uenum` missing `allowed_values`; `array` missing `base_type`; `for_each` used where a dedicated `loop_over_*` op exists; `invoke_code` value-type mismatch. The workflows skill has the full checklist |
| Workflow trigger returns 400 (`"...is not active"`) | Workflow is still a draft | Publish (Deploy in the Workflows UI) first — triggering a draft returns HTTP 400, not 404 (corrected 2026-07-18; a 404 does occur if the workflow ID itself doesn't exist, but a deleted workflow ID was observed returning HTTP 500 in one test, not a clean 404) |
| `gcloud`/`bq`/`kubectl` errors during dataset work | Ponos-path tools not installed (by design) | Run `/dataset-builder:setup` — only needed for Ponos; PaaS needs nothing extra |
| Agent-building command asks for `ORG_PAT` | Mutating internal-API call needs the optional org token | Add `ORG_PAT=` to `.env`, or stick to read-only/public operations |
| `/devrev:*` snap-in commands don't resolve | Plugin never installed (deliberately not auto-enabled — third-party org) | Run `/plugin install devrev@devrev-qk-agents` once. If the marketplace itself won't resolve, register the local clone: `/plugin marketplace add ./repos/devrev-qk-agents` |
| Snap-in build/update/metadata command reports an MCP server isn't connected | Required MCP servers not opted in (bootstrap doesn't install them; third-party services) | `claude mcp add snapin-builder --transport http -s project https://snapin-builder-mcp.onrender.com/mcp` for build/update/generate-metadata/search; `claude mcp add airsync chef-cli mcp initial-mapping` for `/devrev:generate-metadata` only |
| Snap-in Architect mentions "devrev-sdk MCP" and it isn't set up | Third MCP server referenced by the plugin without a documented setup command | Treat as NOT VERIFIED; ask the plugin's maintainers rather than guessing an install line |
| `/create-dashboard` doesn't resolve but `/dashboard-dev:dashboard-create` does | Plugin command's frontmatter uses the `dashboard-create` name; namespaced form always works | Use `/dashboard-dev:dashboard-create` (same command); same for `/modify-dashboard` → `/dashboard-dev:modify-dashboard` |

Diagnostic quick kit:

```bash
cat .claude/.auto-setup/install.log     # bootstrap install/clone progress
cat docs/CLONE_RESULTS.md               # per-repo clone status + SHAs
gh auth status                          # GitHub access
curl -s -X POST 'https://api.devrev.ai/ping' -H "Authorization: Bearer $DEVREV_PAT" -d '{}'   # token
```

## Safety model

These rules are wired into the repo's `CLAUDE.md` and every skill — the agent enforces them, and
they're worth knowing as the human in the loop.

### Destructive operations always require your explicit confirmation

Before any of the following, the agent states the impact and waits for your yes:

- any `*.delete`, any `*.merge` — **confirmed live and genuinely working** (not stubs) for `works.delete`, `custom-objects.delete`, `tags.delete`, `links.delete`, and `workflows.delete` (2026-07-18/19): each returns a clean success and the object then 404s on `.get`. By contrast, `schemas.custom.delete`, `stages.custom.delete`, `states.custom.delete`, and artifact deletes all genuinely don't exist (404 route-not-found) — confirm before running any delete, but don't assume it's a no-op just because some object types have no delete path.
- deprecations (custom link types via `deprecated: true` or `is_deprecated: true` — both accepted as input, confirmed working). **Corrected 2026-07-18**: stage-node `is_deprecated: true` inside a diagram, previously listed here as a working option, is confirmed REJECTED at both create and update (`HTTP 400`) — there is no known working mechanism to retire a stage anywhere in a diagram via the public API; treat every stage as permanent once added. (Attaching a diagram to a subtype/leaf type in the first place is a separate, unrelated operation that IS confirmed working as of 2026-07-19 — see skill 2's Field notes; only *retiring* a stage inside an existing diagram is the blocked operation.)
- `objects.bulk-upgrade` — **confirmed live 2026-07-18**: real, exists at `/internal/objects.bulk-upgrade` (not the public root). Still treat with caution — it affects ALL records of a type org-wide via an async job.
- `web-crawler-jobs.control` with `stop` or `reset`
- dataset / PaaS job deletion, workflow deletion
- `devrev snap_in_version delete-one` (only one non-published version per package; required before creating a new version, but destroys the deleted version's state)

### Verify-after-change

Every mutation is followed by the matching read (`*.get` / `*.list` / `schemas.aggregated.get`) to
confirm it actually landed — no fire-and-forget.

### Credential hygiene

- `.env` (gitignored) is the **only** place a real token lives. Never committed, never echoed into
  files or logs; tokens in documentation are always redacted.
- If a token is missing, the agent tells you exactly what to put in `.env` and **stops** — it never
  fabricates or proceeds without credentials.

### Grounding — never fabricate

Every API field, endpoint, scope, enum value, and DON id the agent uses comes from a reference file
in this repo or a live API response. If a fact isn't in either, the agent looks it up or stops. DON
ids are always used in full (`don:core:dvrv-us-1:devo/0:ticket/456`) — never display IDs.

### Controlled automation surface

The only unattended network operations are the two you pre-approved in the bootstrap: the one-time
`pipx` install of dashboard-sync and the one-time `repos.txt` clone — both idempotent, both logged.
Nothing else auto-installs or auto-updates; `repos/` refreshes only on your explicit request.

### The dashboard validation loop is non-negotiable

New dashboards go through generate → validate (structure → semantic → live API) → deploy → verify.
Hand-written widget JSON bypasses all of it, so the agent will decline to shortcut — the loop is what
makes output reliably valid.

## A note on the known upstream security issue

During the build, two real JWT PATs were found committed in the *source* repo
`devrev/aai-custom-computer-capabilities` (in the agent-building toolkit's `.env.example`). They were
**not** copied into `devrev-implementation`, but they remain in that upstream repo's git history.
If you haven't already: revoke/rotate those tokens (DevRev → Settings → Personal Access Tokens) and
consider having the upstream file scrubbed.
