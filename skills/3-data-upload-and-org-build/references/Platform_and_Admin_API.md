# Platform & admin — DevRev API

Infrastructure and admin objects: artifacts (files), webhooks, jobs, keyrings,
schedules, vistas (views), observability sessions, web-crawler jobs, snap
widgets / snap-kit, commands, code changes, and auth tokens/connections.

| Field | Detail |
| --- | --- |
| Base URL | https://api.devrev.ai |
| Auth | `Authorization: Bearer <TOKEN>` |

---

## 1. Artifacts (files & attachments)

Uploading is a two-step prepare-then-upload flow.

```bash
# 1) Prepare an upload — returns a URL + form fields
curl -X POST 'https://api.devrev.ai/artifacts.prepare' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "file_name": "screenshot.png", "file_type": "image/png" }'

# 2) POST the file to the returned URL (multipart), then reference the artifact id.

# Download / read
curl -X POST 'https://api.devrev.ai/artifacts.download' \
-H 'Authorization: Bearer <TOKEN>' -d '{ "id": "<ARTIFACT_ID>" }'
```

| Endpoint | Scope |
| --- | --- |
| `artifacts.prepare` | `artifact:create` |
| `artifacts.versions.prepare` / `.delete` | `artifact:create` |
| `artifacts.download` | `artifact:read` |
| `artifacts.get` / `.list` / `.locate` | `artifact:read` (+ parent read) |

---

## 2. Webhooks

```bash
curl -X POST 'https://api.devrev.ai/webhooks.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "url": "https://example.com/hook",
      "event_types": [ "work_created", "work_updated" ] }'
```

`webhooks.get/list/update/delete/event` — no explicit scope (default scopes N/A).
**Delivery model, verification and security** (doc-cited 2026-11-03 from
`developer.devrev.ai/guides/webhooks`; mirrored at `skills/11-developer-docs/guides/webhooks.md` — not
live-verified here, and the guide leaves one detail open, flagged below):

- **Registration handshake.** `webhooks.create` returns the webhook with a `secret` and
  `status: "unverified"`. DevRev then POSTs a `type: "verify"` event carrying `verify.challenge`; the
  endpoint must answer `200 {"challenge": "<same value>"}` **within 3 minutes** of the create call, after
  which the webhook becomes active.
- **Event envelope.** Every delivery is a `POST` of one schema: `id`, `webhook_id`, `timestamp`, `type`, and a
  field named after the type that holds the object (e.g. `work_created: {...}`). Events are object
  create/update/delete mutations; object payloads use the same schemas as the REST API.
- **Verify every request.** The `X-DevRev-Signature` header is an HMAC-SHA256 with the webhook `secret` as the
  key and the **raw request body** as the message; discard on mismatch. HMAC does not stop replays — also
  reject a stale `timestamp`. *Open point:* the guide does not state the header's encoding (hex vs. base64);
  inspect a real delivery before hard-coding the comparison.
- **Respond fast, tolerate duplicates.** Reply within **3 seconds** (do real work asynchronously) or the
  delivery is aborted and retried — 3 attempts: immediately, after 30 s, after 3 min. Deliveries are
  concurrent and only semi-ordered, and the endpoint must handle duplicates of the same event; use object
  timestamps/versions to order events per object.
- **Degraded state.** Sustained failures mark the endpoint degraded: queued events are failed without
  delivery attempts until verify requests succeed again and the webhook is promoted back to active.

---

## 3. Jobs

Async job status (e.g. exports, bulk operations).

- `jobs.get` — status of one job (`job:read`).
- `jobs.list` — list jobs (`job:read`).

---

## 4. Keyrings

Stored credentials for integrations.

- `keyrings.authorize` — begin an authorization flow (`keyring:read`).

---

## 5. Schedules (business hours / on-call)

Org schedules model working hours and rotations; fragments are versioned pieces.

| Endpoint | Scope |
| --- | --- |
| `org-schedules.create` / `.update` / `.transition` / `.set-future` | `org_schedule:write` / `:all` |
| `org-schedules.get` / `.list` / `.evaluate` | `org_schedule:read` … |
| `org-schedule-fragments.create` / `.transition` | `org_schedule_fragment:write` / `:all` |
| `org-schedule-fragments.get` | `org_schedule_fragment:read` … |

`org-schedules.evaluate` answers "is it working hours now?" for SLA math.

---

## 6. Vistas (saved views)

```bash
curl -X POST 'https://api.devrev.ai/vistas.list' \
-H 'Authorization: Bearer <TOKEN>' -d '{}'
```

| Endpoint | Scope |
| --- | --- |
| `vistas.get` / `.list` | `vista:read` … |
| `vistas.delete` | `vista:all` |
| `vistas.groups.get` / `.list` | `vista:read` … (none for default vistas) |
| `vistas.groups.delete` | `vista:all` |

---

## 7. Observability (sessions)

Session-level telemetry; all endpoints require no scope.

- `observability.sessions.get` / `.list` / `.aggregate`
- `observability.sessions.data.get`
- `observability.sessions.developer-info.get`

---

## 8. Web crawler jobs

Crawl external sites to ingest content (e.g. for knowledge).

- `web-crawler-jobs.create` — start a crawl (`web_crawler_job:all`).
- `web-crawler-jobs.control` — pause/resume/stop.
- `web-crawler-jobs.get` / `.list` — status.

---

## 9. Snap widgets & snap-kit

- `snap-widgets.create` — create a snap widget (`snap_widget:write`/`:all`).
- `snap-kit-action.execute.deferred` — execute a deferred snap-kit action
  (`snap_widget:write`/`:all`).

---

## 10. Commands

Slash/command definitions used by snap-ins and the command bar.

- `commands.create` / `.update` — `command:write`/`:all`.
- `commands.get` / `.list` — `command:read` …

---

## 11. Code changes

Represent commits/PRs linked to work.

- `code-changes.create` / `.update` — `code_change:write`/`:all`.
- `code-changes.delete` — `code_change:all`.
- `code-changes.get` / `.list` — `code_change:read` …

---

## 12. Auth tokens & connections

- `auth-tokens.create/update/delete/self.delete` — manage tokens (no scope).
- `auth-tokens.get/list/info` — inspect tokens.
- `dev-orgs.auth-connections.*` — configure org auth connections; user auth only,
  not callable via a service-account token.

---

## 13. Health

- `ping` — liveness check, no scope. Handy first call to confirm your token works.

---

## 14. Pitfalls

- Artifacts: you can't POST bytes to `artifacts.create` — always `prepare` first,
  upload to the returned URL, then reference the artifact id on the parent object.
- Webhooks: verify the signature on inbound events; `webhooks.event` is the
  delivery endpoint, not something you poll.
- Schedules: SLA calculations depend on `org-schedules.evaluate` — an unset or
  wrong schedule skews SLA timers.
