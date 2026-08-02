---
name: api-conventions
description: Base cross-cutting conventions that every DevRev REST endpoint follows — authentication tokens (PAT/AAT/SUT/session), cursor-based pagination, API versioning header, rate-limit headers and 429 handling, standard error response shape and HTTP status codes. Use when writing or debugging any DevRev API client, when a call returns a status code or header you need to interpret, or when picking up an API version / beta scope. Applies before/underneath every domain skill (1–9); does not itself define any endpoint payloads.
---

# API conventions — the base rules every DevRev REST call follows

These are the cross-cutting rules the DevRev "About" section of developer.devrev.ai
documents: tokens, pagination, versioning, rate limits, and error shape. Every
domain skill in this repo (1–9) sits on top of these rules. Read the repo root
`CLAUDE.md` first for global operating rules; use this skill when you're
building or debugging the *plumbing* around any endpoint call.

## When to use

Trigger when the user or your own workflow needs:

- The exact `Authorization` / version / scope header value to send
- The cursor field name for paginating any `.list` endpoint
- The meaning of a specific HTTP status code (401 vs 403, 429, 409, 503, ...)
- The meaning of a rate-limit response header (`X-Ratelimit-*`, `Retry-After`)
- Rules for opting into beta APIs
- The default and current public API version
- The JSON shape of an error body

## When not to use

- Specific endpoint payloads or scopes → `skills/8-devrev-api`
- Schema/subtype/custom-object shape → `skills/1-object-schema-customization`
- Stage/state lifecycle → `skills/2-stage-lifecycle-customization`
- Workflow/agent authoring → `skills/6-workflows`, `skills/7-agent-building`
- Snap-in build/deploy → `skills/9-snapin-development`
- Anything that isn't in the six developer.devrev.ai "About" pages listed below

## References — one file per developer.devrev.ai "About" page

| File | What's in it |
| --- | --- |
| `references/for-developers.md` | Landing page: OpenAPI 3.0 spec, Public vs. Beta versions, SDK list (Plug Web + 5 mobile), snap-in framework pointer |
| `references/authentication.md` | The four token types (AAT / SUT / Session / PAT) with example DON subjects; PAT create + revoke workflow; PATs cannot be renewed, revocations are permanent |
| `references/pagination.md` | Cursor-based pagination: response includes `next_cursor` when more pages exist; pass `cursor=<value>` as a query param to advance; absence of `next_cursor` means end-of-results |
| `references/versioning.md` | Current public version `2022-10-20`, override via `X-Devrev-Version` header; opt into beta APIs via `X-Devrev-Scope: beta`; each public version supported for at least 1 year |
| `references/rate-limits.md` | 5-minute rolling window, aggregate per authenticated user; 429 with `Retry-After: <seconds>`; quota headers `X-Ratelimit-Limit` / `X-Ratelimit-Remaining` / `X-Ratelimit-Reset` (Unix epoch seconds); uniform per-endpoint weight |
| `references/errors.md` | Success codes (200/201/204); JSON error shape `{"message":"..."}`; common 4xx/5xx (400/401/403/404/429/500/503); per-endpoint extras (301/404/409) |

## Working rules

These are the concrete rules extracted from the pages above. Every DevRev REST
call in this repo obeys them.

### Auth header

- Every request carries `Authorization: Bearer <token>` — the four token types
  (PAT, AAT, SUT, Session) are all bearer JWTs. For this repo the token is
  always a **PAT** read from `.env` as `DEVREV_PAT` (see repo-root `CLAUDE.md`).
- PATs **cannot be renewed** — generate a new one and update `.env` before the
  old one expires.
- If you see `invalid token`, decode the JWT at `jwt.io` to inspect its
  subject/expiry; do not "retry with a different scope" blindly.

### Version header

- Default (no header) → version `2022-10-20`.
- Override with `X-Devrev-Version: 2022-10-20` (or a later dated version once
  DevRev releases one). Each dated public version is supported ≥ 1 year.
- Opt into beta endpoints with `X-Devrev-Scope: beta`. Beta APIs may change
  without notice — do not build production integrations on them.

### Pagination

- All `.list` endpoints use **cursor-based** pagination.
- Read the response field `next_cursor`. If present, pass it back as the query
  parameter `cursor` (`.../works.list?cursor=<value>`) to fetch the next page.
- If `next_cursor` is absent, you're on the last page.
- Page-size / `limit` semantics (default, max) are not documented on the About
  page as of scrape date 2026-08-02 — read the specific endpoint doc in
  `skills/8-devrev-api/references/` for that.

### Rate limits

- Aggregate per authenticated user across ALL requests. **Window resets every
  5 minutes** per the docs.
- Read three headers from every response:
  - `X-Ratelimit-Limit` — total units in the current window
  - `X-Ratelimit-Remaining` — units left
  - `X-Ratelimit-Reset` — Unix epoch seconds when the window resets
- On 429: back off for `Retry-After` seconds (integer). All endpoints have
  uniform weight today; DevRev reserves the right to change this.
- The specific numeric ceiling is **org-dependent** and not fixed by the public
  docs (only an example `1000` is shown). Pace off the live headers, not off
  any static table — see `references/rate-limits.md` "Skill-8 field note".

### Error response shape

- Success: 200 (result in body), 201 (created), 204 (no body — common on
  deletes).
- Errors: JSON body with a `message` field, e.g. `{"message":"route not found"}`.
  DevRev's actual APIs also return richer fields like `type`, `field_name`,
  `subtype`, `reason` in practice (observed live in skill-1/skill-8 field
  notes) — those aren't spelled out on the About > Errors page, but they're
  real; script your error-matching off both `message` and `type`.
- Standard 4xx/5xx meanings:
  - `400 Bad Request` — malformed / invalid arguments
  - `401 Unauthorized` — missing or invalid credentials
  - `403 Forbidden` — authenticated but not permitted (often means missing
    scope, or "custom object has zero access by default" — see skill 1)
  - `404 Not Found` — endpoint doesn't exist, or object doesn't exist
  - `409 Conflict` — object already exists (e.g. duplicate group name)
  - `429 Too Many Requests` — rate limited; honour `Retry-After`
  - `500 Internal Server Error` — retry after a short delay; contact support
    if it persists
  - `503 Service Unavailable` — transient; retry after a short delay
- Per-endpoint extras: `301 Moved Permanently` (the resource ID changed; the
  new ID is in the `Location` header — treat as a hint to update stored IDs).

### DON ids, headers, base URL — see repo-root `CLAUDE.md`

The base URL (`https://api.devrev.ai`), the `Content-Type` / `Accept:
application/json` header pair, and the "always use DON ids, never display IDs"
rule are stated in the repo-root `CLAUDE.md` "Global API rules" section, not on
any developer.devrev.ai About page. This skill doesn't restate them — they're
global.

## Verify

```bash
# 1. Auth works (returns HTTP 200 with a small body)
curl -s -X POST 'https://api.devrev.ai/ping' \
  -H "Authorization: Bearer $DEVREV_PAT" \
  -H "Content-Type: application/json" \
  -d '{}' -D -

# 2. Version + rate-limit headers are echoed on any call (inspect -D)
curl -s -X POST 'https://api.devrev.ai/works.list' \
  -H "Authorization: Bearer $DEVREV_PAT" \
  -H "X-Devrev-Version: 2022-10-20" \
  -H "Content-Type: application/json" \
  -d '{ "type": ["ticket"], "limit": 1 }' -D -
# Look for: X-Ratelimit-Limit / X-Ratelimit-Remaining / X-Ratelimit-Reset

# 3. Cursor-based pagination works end-to-end
curl -s -X POST 'https://api.devrev.ai/works.list' \
  -H "Authorization: Bearer $DEVREV_PAT" \
  -H "Content-Type: application/json" \
  -d '{ "type": ["ticket"], "limit": 2 }'
# Response will include "next_cursor":"<value>" if more pages exist; then:
curl -s -G 'https://api.devrev.ai/works.list' \
  -H "Authorization: Bearer $DEVREV_PAT" \
  --data-urlencode 'cursor=<value>'
```

## Field notes (live-learned; see docs/LEARNINGS.md)

Dated facts discovered while operating this domain — errors hit, restrictions
found, behaviors that differ from the references. Add entries via the
`capture-learnings` protocol
(`.claude/skills/capture-learnings/SKILL.md`): one dated bullet per fact, with
evidence. If a fact *corrects* a reference doc, fix the doc in place too — this
section is for knowledge that has no better home or needs domain-level
visibility.

<!-- Empty for now — future learnings about auth headers, cursor edge cases,
rate-limit numeric ceilings observed live, error-body field shapes, or
version-header behavior go here. -->
