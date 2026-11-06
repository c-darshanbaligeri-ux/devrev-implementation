# DevRev Computer through the API

## Contents
<!-- toc -->
- [Before you start](#before-you-start)
- [Step 1: your org id and user id](#step-1-your-org-id-and-user-id)
- [Step 2: find the Computer agent](#step-2-find-the-computer-agent)
- [Step 3: read Computer's skills and system prompt](#step-3-read-computers-skills-and-system-prompt)
- [Step 4: send a prompt and read the reply](#step-4-send-a-prompt-and-read-the-reply)
- [Step 5: stop a run, and see every step](#step-5-stop-a-run-and-see-every-step)
- [Fallback: capture the calls from the web app](#fallback-capture-the-calls-from-the-web-app)
- [Pitfalls and safety](#pitfalls-and-safety)
- [Quick reference](#quick-reference)
<!-- /toc -->

Computer (the in-app assistant) is an ordinary DevRev AI agent. This reference gets you, in any org, its agent and
service-account ids, its skills and system prompt, the calls that send it a prompt (with or without a file), how to
read the answer, how to stop a run and where its full step log is.

There is no "run skill" endpoint: you post a chat message and Computer picks the skill itself.

> **Status: captured, not documented.** Almost every call here is under `/internal/`, which DevRev does not
> document. The calls were captured from the DevRev web app in October 2026 (as of 2026-10-28) and checked in one
> US-region org. They can change without notice; if one stops working, re-capture it ([Fallback](#fallback-capture-the-calls-from-the-web-app)).

## Before you start

- **Access.** Sign in to the target org as a dev user and check that Computer opens in the web app.
- **Token.** A personal access token: DevRev → Settings → Account → Personal Access Token, or the DevRev CLI
  (`devrev profiles authenticate -o <org-slug> -u <your-email>`, then `devrev profiles get-token`). Load it into
  `DEVREV_PAT`; never paste it into a chat, ticket or file that is committed.
- **Check it.** `GET /dev-users.self` must return your user.
- **Headers.** Every call goes to `https://api.devrev.ai` with `Authorization: Bearer $DEVREV_PAT` and
  `Content-Type: application/json` (`skills/devrev-start/references/global-api-rules.md`). One org was seen
  accepting only the bare form `Authorization: <token>` on `/internal/` (see `references/computer-data-tools.md`):
  on a 401 from an `/internal/` call, retry once with the bare form before concluding the token is wrong.
- **The token is you.** Everything Computer does from your API calls is done as your user, with your permissions,
  including the records it creates.
- **Region.** Every id carries a region code such as `dvrv-us-1`. If the org is not in the US region, confirm the
  API host in the web app's network calls first.

## Step 1: your org id and user id

`GET /auth-tokens.info` returns both:

```json
{"organization": {"id": "don:identity:<region>:devo/<org>", "display_id": "DEV-<org>"},
 "user": {"id": "don:identity:<region>:devo/<org>:devu/<n>", "display_id": "DEVU-<n>"}}
```

| Placeholder | Meaning | Where to read it |
| --- | --- | --- |
| `<region>` | the org's data region, e.g. `dvrv-us-1` | between `don:identity:` and `:devo/` |
| `<org>` | the org's short code | after `devo/` |
| `<my user id>` | your dev-user id | `user.id` (also `dev_user.id` from `dev-users.self`) |

Agent and chat ids start with `don:core:<region>:devo/<org>` — note `core`, not `identity`.

## Step 2: find the Computer agent

Ask which agent sits behind the in-app assistant; do not search by name (an org can hold more than one agent called
"Computer").

`GET /internal/ai-assistants.surfaces.get?surface_id=2`

`surface_id=2` is the "Global" assistant surface, where Computer lives. It is a surface type, not an org-specific
number, so the same URL should work in every org (checked in one so far).

```json
{"ai_assistant_surface": {
  "surface": {"id": 2, "label": "Global"},
  "ai_agents": [{
    "id": "don:core:<region>:devo/<org>:ai_agent/<a>",
    "display_id": "ai_agent-<a>",
    "default_version_id": {"display_id": "ai_agent_version-<a>.<v>"},
    "service_account": {"id": "don:identity:<region>:devo/<org>:svcacc/<s>", "display_id": "SVCACC-<s>",
                        "display_name": "Computer"}}]}}
```

From `ai_agents[0]` keep `<computer agent id>` (`id`) and `<computer service account id>` (`service_account.id`).

If the list is empty or holds several agents, call `POST /internal/ai-agents.list` with `{}`, keep the agents whose
slug is `computer`, and pick the live one:

| Check | Live Computer | Leftover Computer |
| --- | --- | --- |
| Version state (`POST /internal/ai-agents.versions.list` with `{"agent": "<agent id>"}`) | published | draft only |
| `ai_agent_config` on the agent | a Computer config, e.g. `devrev.computer-agent-common-v1` | empty |
| The org's own skills in `skills[]` | present | missing |

DevRev can leave an older Computer behind after an upgrade. Do not change or delete it; ask the org's DevRev admin.

## Step 3: read Computer's skills and system prompt

`POST /internal/ai-agents.get` with:

```json
{"id": "<computer agent id>", "resolve_config": true, "apply_config_policy": true}
```

Keep both flags. Without them you get only what is stored on the agent itself and miss the skills and settings it
inherits from DevRev's base config.

| Field | What it tells you |
| --- | --- |
| `default_version_id` | the version in use |
| `guidance` | the system prompt the org added (empty if none) |
| `skills[]` | every skill Computer can use |
| `service_account` | the account shown as the author of Computer's replies and records |
| `memory_config` | whether Computer remembers past chats (`recall_chats_enabled`) |

Each skill's trigger says what kind it is: **operation** (a built-in tool such as web search or SQL), **plan** (a skill
package or instruction skill; org-uploaded skills appear here with a `plan.id`) or **workflow** (a DevRev workflow,
which can call outside systems).

Download a skill package:

1. `POST /internal/ai-agents-plans.get` with `{"id": "<plan id>"}`; keep `plan.skill_artifact.id`.
2. `GET /internal/artifacts.locate?id=<artifact id>&prefer_download=true`; it returns a short-lived `url`.
3. Download the zip from that `url` (no token needed).

Org-uploaded skills keep their instructions in the zip and have an empty `guidance`; DevRev's built-in skills carry
theirs in `guidance`. Trust the agent's `skills[]` over `POST /internal/ai-agents-plans.list`, which returns every skill
package in the org, including old ones no longer attached to Computer.

## Step 4: send a prompt and read the reply

Computer answers asynchronously: you post a message into a chat, then poll until the reply is finished.

**4a. Open a chat** — `POST /internal/chats.create`:

```json
{"agent_chat_type": "session", "agent_members": [{"agent": "<computer agent id>"}], "is_default": false,
 "type": "dm", "users": ["<my user id>", "<computer service account id>"]}
```

Keep `chat.id` as `<chat id>` and send follow-ups in the same chat.

**4b. Upload a file (optional)**

1. `POST /internal/artifacts.prepare` with `{"file_name": "spec.pdf", "file_type": "application/pdf", "configuration_set": "default"}`; keep `id`, `url` and `form_data`.
2. POST the file to `url` as `multipart/form-data`: every `form_data` key and value as a field, then the file last as
   the field `file`. No DevRev token on this call; 200, 201 or 204 means it worked.
3. Put the `id` from step 1 in the message's `artifacts` list (4c).

**4c. Send the prompt** — `POST /internal/timeline-entries.create`:

```json
{"object": "<chat id>", "type": "timeline_comment", "body": "Your prompt here", "body_type": "text",
 "client_ref": "<a new random UUID>", "visibility": "internal", "labels": ["display:discussions"],
 "agent_execution_options": {"execution_runtime": "container"}, "artifacts": ["<artifact id from 4b>"]}
```

- Leave out `artifacts` when there is no file.
- Keep `execution_runtime: "container"`: it lets Computer run skills in its remote sandbox. A prompt sent this way
  runs in DevRev's remote container, not in anyone's Computer desktop app (which is why the desktop app cannot be
  "driven" from outside: API prompts never run there).
- Save your `client_ref` and the response's `timeline_entry.id`; you need them to find the reply and to stop the run.

**4d. Wait for the reply.** Poll about every 20 seconds:

1. `POST /internal/ai-agent.sessions.list` with `{"parent": ["<chat id>"]}`. Computer is still working while
   `agent_sessions[0].execution_state.state` is `running`, `queued`, `pending` or `in_progress`.
2. `POST /internal/timeline-entries.list` with `{"object": "<chat id>", "limit": 50}`, following `next_cursor`. The
   reply is the entry whose `client_ref` is `response:<your client_ref>`.

The run is done when the reply exists and the session is no longer running. A skill run can take from a few minutes
to over half an hour.

**4e. Read the reply** from the reply entry's `snap_widget_body[0]`:

| Field | What it holds |
| --- | --- |
| `message` | Computer's answer (also in the entry's `body`) |
| `thoughts[]` | one item per tool step, with `skill.name`, `skill.explanation` and `progress` |
| `todos` | Computer's task list |
| `state`, `status` | where the run stands |

**Follow-ups.** If Computer asks something (many skills ask for approval before they write records), answer with 4c
in the same chat.

## Step 5: stop a run, and see every step

**Stop a run** — `POST /internal/ai-agents.events.signal`:

```json
{"agent": "<computer agent id>", "parent": "<chat id>", "request_id": "<timeline_entry.id of your message>", "signal": "cancel"}
```

**See every step.** Each chat has two file areas. List one with `POST /internal/filesystems.get` and
`{"parent_id": "<chat id>", "type": "private"}` (or `"shared"`); `snapshot.entries[]` gives each file's `path` and
`artifact_id`.

| Area | What it holds |
| --- | --- |
| `private` | `/.agent/<session>.jsonl`: Computer's full log, one JSON line per message or tool call (Claude Agent SDK transcript format) |
| `shared` | files a skill produced during the chat |

Download any of them with `GET /internal/artifacts.locate?id=<artifact_id>&prefer_download=true`, then fetch the `url`.

**Why the log matters.** When DevRev's model service fails, the reply says only "Something went wrong. Please try
again." The real error is in the log: an assistant line with `"isApiErrorMessage": true`, or with the model
`<synthetic>`. For chats run in the Computer **desktop app**, the same transcript also exists on the user's machine;
`references/computer-session-trace.md` turns it into an audit bundle.

## Fallback: capture the calls from the web app

If a call above stops working, record what the DevRev web app sends; it uses the same API.

1. Open the DevRev web app in Chrome, sign in, open DevTools (F12 / Cmd+Option+I) → **Network**, tick **Preserve log**.
2. Leave the filter empty: the app's calls go to `app.devrev.ai/api/gateway/...`, so a filter such as `api.devrev.ai` hides them.
3. Do the thing to capture (for example open a new Computer chat, attach a file, send a short prompt, wait for the answer).
4. Export the requests as a HAR with the **sanitized** export (no cookies or login headers). Never share a HAR exported with sensitive data.
5. Open the HAR (JSON) and find the requests under `/api/gateway/internal/`; their request bodies are the JSON to send.

To call a captured URL yourself, replace `app.devrev.ai/api/gateway` with `api.devrev.ai`
(`https://app.devrev.ai/api/gateway/internal/chats.create` → `https://api.devrev.ai/internal/chats.create`) and send
your own PAT, not the browser session. A re-captured call that differs from this page is a learning: fix this file
and record it (`.claude/skills/capture-learnings/SKILL.md`).

## Pitfalls and safety

Computer works on real data, as you; treat every API prompt like a prompt typed in the app.

- **Records are real.** Skills create and change real records under your name. Test in a sandbox or UAT org where
  you can, and never ask Computer to act on a colleague's work.
- **Approval questions pause the run.** Nothing is written until you answer in the same chat.
- **Watch skills that leave DevRev.** A workflow skill can send data to an outside system; check `skills[]` first and
  keep prompts away from skills you do not mean to run.
- **Run at most two chats at once.** Four concurrent Computer chats all hit HTTP 429; on a 429 wait the `Retry-After`
  seconds before retrying.
- **"Something went wrong" is DevRev's error, not Computer's answer.** Check the log (Step 5). To recover, wait about
  two minutes, then send "Please continue from where you stopped." in the same chat.
- **A new chat is not a clean slate** when `memory_config.recall_chats_enabled` is true: Computer can recall earlier chats.
- **Protect the token.** Never commit, print or share it; revoke it when finished, and at once if it appears in a chat or log.
- **`/internal/` paths can change.** Re-capture with the Fallback steps.

## Quick reference

All calls go to `https://api.devrev.ai` with `Authorization: Bearer $DEVREV_PAT`.

| Step | What it does | Call |
| --- | --- | --- |
| 1 | Your org and user ids | `GET /auth-tokens.info` |
| 2 | Find Computer | `GET /internal/ai-assistants.surfaces.get?surface_id=2` |
| 2 | List all agents | `POST /internal/ai-agents.list` |
| 2 | An agent's versions | `POST /internal/ai-agents.versions.list` |
| 3 | Computer's skills and system prompt | `POST /internal/ai-agents.get` |
| 3 | One skill | `POST /internal/ai-agents-plans.get` |
| 3 | All skill packages in the org | `POST /internal/ai-agents-plans.list` |
| 3, 5 | Download link for a file | `GET /internal/artifacts.locate` |
| 4a | Open a chat | `POST /internal/chats.create` |
| 4b | Prepare a file upload | `POST /internal/artifacts.prepare` |
| 4c | Send a prompt | `POST /internal/timeline-entries.create` |
| 4d | Is Computer still working? | `POST /internal/ai-agent.sessions.list` |
| 4d | Find the reply | `POST /internal/timeline-entries.list` |
| 5 | Stop a run | `POST /internal/ai-agents.events.signal` |
| 5 | List the chat's files and log | `POST /internal/filesystems.get` |
