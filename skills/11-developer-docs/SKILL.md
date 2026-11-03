---
name: developer-docs
description: Offline mirror of the official DevRev developer docs (developer.devrev.ai, scraped 2026-11-03) — the public AND beta API reference with a field-level request table, required scopes, response codes and cURL example for every endpoint; the Guides (webhooks, object customization, custom objects, restricted timeline messages); the PLuG Web SDK and Android/iOS/React Native/Cordova/Flutter SDKs; snap-in development (concepts, manifest, CLI, functions, keyrings, testing, debugging, quotas); AirSync (data model, object types, extraction/loading); and the changelogs. Use when the user asks what the official docs say about something, needs a request field list or a beta endpoint that skills/8-devrev-api does not carry, SDK install/quickstart steps, snap-in or AirSync reference material, or webhook event/signature details. Reference-only — never calls the live API, and never overrides facts that were live-verified in another skill.
---

# Developer docs mirror — developer.devrev.ai

A local, greppable copy of the DevRev developer documentation: **980 sitemap URLs → 323 Markdown
files (~5.8 MB)**, scraped **2026-11-03**. Every file starts with the same header the rest of this repo
uses for scraped pages (`Source: <url>` / `Scraped: <date>`), so you can always jump to the live page.

The content is DevRev's documentation, mirrored here for offline reference with a source link on every
page. Read the live page (the `Source:` line) when you need the authoritative, current version.

## Precedence — read this first

1. **This mirror records what the vendor docs *say*. Live-verified facts in this repo win.** If a domain
   skill's *Field notes*, `docs/LEARNINGS.md` or the root `CLAUDE.md` disagrees with a mirror page, trust
   the repo — the documentation is known to lag reality (see the corrections already recorded for rate
   limits, stage deprecation, `objects.bulk-upgrade`, etc.).
2. **Never write a learning into a mirror file.** `scripts/build_docs.py` deletes and regenerates every
   generated file, so a hand edit is silently lost on the next refresh. Capture discrepancies with
   `.claude/skills/capture-learnings` into the *owning skill* (e.g. `skills/8-devrev-api`), as usual.
3. **Public first.** Use `api-reference/` by default. `beta/` documents early-access endpoints; how beta is
   selected on the wire is in `skills/10-api-conventions/references/versioning.md`.

## When to use / when not to use

| Use this skill for | Use something else for |
| --- | --- |
| "What does the official doc say about `X`?" | Making the call → `skills/8-devrev-api` (live-verified payloads, DON ids, scope gotchas) |
| The complete request-field table for an endpoint, or a **beta** endpoint | Cross-cutting auth / pagination / rate-limit / error rules → `skills/10-api-conventions` |
| Webhook event payloads, signature/echo-challenge verification | Designing the solution → `skills/0-solution-architecture` |
| PLuG / mobile SDK install, init, identity, events | Building a snap-in or AirSync connector end to end → `skills/9-snapin-development` (the plugin pipeline); read the reference pages here |
| Snap-in manifest, functions, keyrings, CLI, quotas; AirSync data model & object types | Custom objects / fields in a live org → `skills/1-object-schema-customization` |

## Layout

| Path | What is in it | Files |
| --- | --- | --- |
| `INDEX.md` | Every page → local file → source URL, grouped by site section, with totals | 1 |
| `COVERAGE.md` | Public/beta endpoints on the site vs. the names in `skills/8-devrev-api/references/00_API_Catalog.md` | 1 |
| `about/` | Authentication, pagination, versioning, rate limits, errors, for-developers | 6 |
| `guides/` | `webhooks`, `object-customization`, `custom-objects`, `timeline-entries` | 4 |
| `changelog/` | Public API changelog entries | 10 |
| `api-reference/` | `getting-started.md`; **one file per resource** (`accounts.md`, `works.md`, `webhooks.md` …) holding every endpoint of that resource; concept pages in resource sub-folders (`tags/concepts.md`, `webhooks/event-responses.md` …) | 49 |
| `sdks.md`, `sdks/` | `web/` (PLuG), `android/`, `ios/`, `react-native/`, `cordova/`, `flutter/`, `push-notifications.md` | 31 |
| `snapin-development/` | `concepts`, `best-practices`, `locally-testing-snap-ins`, `debugging`, `quotas-limits`, `upgrade-snap-ins`, `references/` (manifest, functions, hooks, event sources, CLI, keyrings, scopes …), `tutorials/` | 37 |
| `airsync.md`, `airsync/` | Connector development: extraction, loading, attachments, state, testing, deployment; `data-model/`; `object-types/` (35 DevRev object pages) | 112 |
| `beta/` | The same shape for the beta API: `about/`, `guides/` (account creation, agents async API, links), `changelog/`, `api-reference/` (57 resource files) | 72 |
| `scripts/` | `fetch_docs.py`, `build_docs.py` — how this mirror is produced and refreshed | 2 |

### Question → file

| Question | Open |
| --- | --- |
| Webhook payload shape, signature verification, echo challenge, retries | `guides/webhooks.md` |
| Object / field customization, tenant vs. subtype fragments | `guides/object-customization.md` |
| Custom objects end to end | `guides/custom-objects.md` |
| Restricted (private/internal) timeline messages | `guides/timeline-entries.md` |
| Add the PLuG widget to a site, identify users, track events | `sdks/web/installation.md`, `user-identity.md`, `track-events.md`, `methods.md` |
| Mobile SDK quickstart | `sdks/<android\|ios\|react-native\|cordova\|flutter>/quickstart.md` |
| Snap-in manifest, functions, hooks, event sources | `snapin-development/references/manifest.md`, `functions.md`, `hooks.md`, `event-sources.md` |
| `devrev` CLI | `snapin-development/references/cli.md`, `cli-install.md`, `commands.md` |
| Snap-in limits / debugging / local testing | `snapin-development/quotas-limits.md`, `debugging.md`, `locally-testing-snap-ins.md` |
| AirSync: what to build, in which order | `airsync.md`, `airsync/getting-started.md`, `airsync/connector-checklist.md` |
| AirSync field mapping, domain metadata | `airsync/external-domain-metadata.md`, `airsync/initial-domain-mapping.md`, `airsync/data-model/` |
| What fields a DevRev object type exposes to AirSync | `airsync/object-types/<object>.md` |

## Finding an endpoint

Run these from the repo root.

```bash
# every endpoint of a resource (method, path, anchor)
sed -n '/^## Endpoints/,/^<a id=/p' skills/11-developer-docs/api-reference/works.md

# one endpoint's full section
awk '/^## `POST \/works.create`/{f=1} f&&/^<a id=/{exit} f' skills/11-developer-docs/api-reference/works.md

# which resource mentions a field
grep -rln 'external_refs' skills/11-developer-docs/api-reference/

# beta-only resources
ls skills/11-developer-docs/beta/api-reference/
```

Endpoint pages that exist as both `GET` and `POST` appear as two sections (anchors `list` and
`list-post`). The anchor is the last segment of the source URL.

## Endpoint section format

Each endpoint in `api-reference/<resource>.md` / `beta/api-reference/<resource>.md` has:

- a heading `## \`METHOD /path\``, the page title, and `Source:` link
- the description and **Required scopes** (a list, or a type → scope table for polymorphic endpoints
  such as `works.*`)
- one table per parameter group (**Request Body**, **Query Parameters**, …): field | required | type |
  description, with `Format`/`Value in`/`Deprecated` notes. Nested fields use dotted names
  (`issue.priority`).
- for `oneOf` bodies (e.g. `parts.create`): one `#### Variant` table per tab the site shows
- **Response codes** (with *empty body* where the site says so), a **cURL example**, and a collapsed
  example success response

## Limits of this mirror — know what is *not* here

- **Nested object types appear by name only** (e.g. `custom-schema-spec`, `set-tag-with-value`) — that is
  all the endpoint page shows. For their shape use the matching `*.get`/schema endpoints live
  (`skills/1-object-schema-customization`, `skills/8-devrev-api`) or another mirror page.
- **Responses are examples, not schemas**: status codes plus one example 2xx body whose values are
  placeholders (`"string"`, `0`).
- **Only the cURL sample** is kept; the other language tabs are not present in the page source.
- **Images and diagrams are not downloaded** — they appear as `*[image: <alt text> — see source page]*`.
- **No OpenAPI file**: the site advertises a spec download but publishes no working link
  (`/openapi.*` 404, `api.devrev.ai/openapi.*` 401), so the endpoint tables are rebuilt from page HTML.
- The site root `/` is not mirrored (its `llms.txt` is the whole-site index; `INDEX.md` replaces it).

## Refresh

About 3 minutes, ~980 requests, ~80 MB of cache. The cache **must live outside the repo** (it is
untrusted downloaded content; `fetch_docs.py` refuses a cache inside the repo).

```bash
CACHE="$(mktemp -d)"
python3 -I skills/11-developer-docs/scripts/fetch_docs.py --out "$CACHE"
python3 -I skills/11-developer-docs/scripts/build_docs.py --cache "$CACHE" \
        --out skills/11-developer-docs \
        --catalog skills/8-devrev-api/references/00_API_Catalog.md
git diff --stat skills/11-developer-docs      # review what the docs changed
```

- Both scripts are standard-library Python; run them with `-I` so nothing is imported from the
  current directory. `fetch_docs.py` is resumable and backs off on 429/5xx.
- `build_docs.py` exits non-zero if any endpoint page fails to parse (no method/path/response codes) —
  that is the signal the site markup changed; fix the parser, do not hand-patch output.
- **Commit refreshes with a `docs:` prefix, not `learn:`.** The `learn:` prefix triggers the
  auto-push hook (`.claude/hooks/push-learnings.sh`), which is meant for single self-learning facts.
- After a refresh, re-read the diff of `about/` against `skills/10-api-conventions/references/` (that
  skill keeps its own curated copy of the six About pages) and update it if the docs changed.

## Field notes (live-learned; see docs/LEARNINGS.md)

- **2026-11-03 · How the site can (and cannot) be fetched.** The sitemap lists 980 URLs: 751 endpoint
  pages (311 public + 440 beta), 228 narrative pages (200 public guides/SDK/snap-in/AirSync/changelog
  pages, 13 concept/landing pages under `api-reference/`, 15 beta about/guides/changelog pages), and the
  root. Narrative and concept/landing pages serve clean Markdown at `<page-url>/llms.txt`
  (`text/markdown`; code fences intact; images reduced to `<img alt=…>` with no `src`). Real endpoint
  pages return **404** at `/llms.txt`, and there is no `.md` suffix form, no `/llms-full.txt`, and no
  public OpenAPI file — each endpoint page's HTML (1.2–1.9 MB) is the only source and carries only its own
  schema.
- **2026-11-03 · Eleven URLs shaped like endpoints are concept pages** (`api-reference/tags/concepts`,
  `webhooks/event-responses`, `works/tickets-and-issues`, …): no HTTP method, but they *do* serve
  `llms.txt`. The fetcher therefore probes `llms.txt` first for every endpoint-shaped URL.
- **2026-11-03 · Page structure the parser depends on.** Request fields are `div.text-sm.border-t`
  blocks (name span with a `*`/`?` marker, type span, description block, chip badges for `Format` /
  `Deprecated`); `oneOf` request schemas are tab groups whose panel ids contain `-content-#/components/schemas/`;
  response bodies are per-status panels (`-content-<code>`), where a delete endpoint's `200` panel just
  says "Empty". Treating all `pre` blocks on a page as one pool mislabels an error example as the success
  example — the parser keeps them per status.
- **2026-11-03 · Catalog shorthand.** `00_API_Catalog.md` packs several endpoints into one table cell
  (the first name in full, then bare suffixes such as `.list` and `.export`); `COVERAGE.md` expands that
  shorthand before diffing. 30 public endpoints are not
  named in a catalog table row — all of them are documented in other skill references (custom objects,
  schemas, stage diagrams, `ping`), so they are catalog-listing gaps, not knowledge gaps. The site lists
  `link-types.custom.*` under **beta only**, while this repo's notes record them working on the public root.
