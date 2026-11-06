# Tracing a DevRev Computer desktop session

`scripts/computer_trace.py` turns one chat from the **DevRev Computer desktop app** (macOS) into a traceability
bundle: every prompt, every model call, every tool call with its full input and output, every subagent, the app's
runtime logs, and a SHA-256 manifest that proves nothing changed after export. Use it for audits, incident reviews,
bug reports, and to see exactly what Computer did in a desktop session.

It only reads files the desktop app already writes on the machine. It calls no API, needs no token, writes nothing
under the app's folders, and uses the Python standard library only (3.9+). Version 1.0.0 (`--version`), tested on
macOS with Python 3.9 and 3.14 against transcripts written by Computer.app 5.1.40.

For a chat that ran through the API or in DevRev's remote sandbox and is **not** on this machine, fetch the same SDK
log from the chat's private file area instead (`references/computer-agent-api.md`, Step 5).

## Where the desktop app keeps a session

The app embeds the Claude Agent SDK. Per signed-in identity (`~/.devrev/computer/<identity>/`):

| Source | What it holds |
| --- | --- |
| `agent/projects/<workdir-slug>/<session>.jsonl` | The SDK transcript: prompts, model calls, tool calls and results, injected context |
| `.../<session>/subagents/agent-<id>.jsonl` + `.meta.json` | Subagent transcripts (older SDK builds write no `toolUseId`; link through `toolUseResult.agentId`) |
| `.../<session>/tool-results/` | Large tool outputs stored outside the transcript |
| `chats/<chat>/{metadata.json,events.ndjson,todos.json,session-approvals.json}` | Chat metadata, app events, task list, approvals |
| `chats/<chat>/debug/{debug.log,computer-agent-sdk-debug.log}` | Runtime logs, written only for turns that run locally |
| `~/Library/Application Support/Computer/logs/{combined*,error*}.log` | App-wide logs (local time); the exporter keeps only the lines that mention the chat |

Each turn runs either **locally** in the app or in DevRev's **remote sandbox** (working directory
`/home/devrev/agentcore/sessions/...`). Remote turns are synced into the local transcript with full tool detail; they
just leave no local runtime log. No extended-thinking blocks have been seen in Computer transcripts, and the system
prompt is not stored locally (read it through the API: `references/computer-agent-api.md`, Step 3).

## Run it

Run from the toolkit root (`devrev-find --root` prints it). **Always pass `--out`** with a local folder outside this
repo and outside iCloud/OneDrive/Dropbox: bundles hold the full conversation, and without `--out` they land next to
the script.

```bash
# 1. Find the chat (newest first; the part after the last _dm_ is the chat suffix)
python3 -I skills/7-agent-building/scripts/computer_trace.py list

# 2. Export it (suffix, chat folder name, or the full DON in quotes; --latest for the newest chat)
python3 -I skills/7-agent-building/scripts/computer_trace.py export <chat-suffix> --out ~/devrev-traces

# 3. Verify the bundle
cd ~/devrev-traces/<chat-folder>_<YYYYMMDD-HHMMSS> && shasum -a 256 -c MANIFEST.sha256
```

`-I` (isolated mode) stops Python from importing stray files from the current folder. `--include-workdir` also copies
the files uploaded to or produced in the chat (verbatim, unredacted). A `WARNING: transcript changed Ns ago` means the
agent is still replying: wait and export again.

**Recording a session as evidence (optional insurance).** Local runtime logs normally build up across runs (one test
chat had runtime logs for all 11 local turns without help). For an audit, start `watch` before the session so every
run's files are snapshotted even if the app later rewrites or cleans them, then export with `--runs`:

```bash
python3 -I skills/7-agent-building/scripts/computer_trace.py watch --out ~/devrev-traces/watch-<stamp>            # new chats
python3 -I skills/7-agent-building/scripts/computer_trace.py watch --chat <chat-suffix> --out ~/devrev-traces/watch-<stamp>
# ... run the session in the desktop app, then Ctrl+C (or start with --idle-stop 600) ...
python3 -I skills/7-agent-building/scripts/computer_trace.py export <chat-suffix> --runs ~/devrev-traces/watch-<stamp> --out ~/devrev-traces
```

`--idle-stop` only counts once a chat is being watched; while it waits for a new chat it never stops by itself.

## What the bundle holds

| File | Contents |
| --- | --- |
| `TRACE_REPORT.md` | The readable trace: session header, a coverage-and-limits section that proves completeness, then per turn **A** input → **B** runtime preparation → **C** injected context → **D** reasoning ⇄ tool loop (every tool call with full input and output, subagents inline) → **E** final answer → **F** delivery, and appendices (merged runtime timeline, control records, todos/approvals, workdir files with hashes, agent config and skills inventory, evidence list) |
| `run-data-<chat>.json` | The same session as structured turns (the `agent-evals` turn schema) |
| `raw/` | Verbatim copies of every source, with `raw/SOURCES.json` giving each file's origin, size, hash and redaction count |
| `MANIFEST.sha256` | SHA-256 of every file in the bundle |

Nothing is truncated (long bodies fold into `<details>`). Secret patterns (Bearer tokens, JWTs, Authorization values,
API keys, AWS pre-signed URL signatures) are redacted in the raw copies and the report; a redacted raw file keeps the
original's hash. Names, customer data and document contents are **not** removed: review the report before sharing,
and share bundles only through an approved channel.

## Limits and troubleshooting

| Symptom | Cause | What to do |
| --- | --- | --- |
| `no chat matches '<id>'` | The chat is not on this machine (it ran in the web app, through the API, or on another computer) | Export on the machine where it ran, or fetch the SDK log through the API (`references/computer-agent-api.md`, Step 5). Opening the chat in this desktop app and sending a follow-up may bring in only the new turn (untested) |
| `no transcript found for <chat>` | No prompt was ever run, or the transcript was later removed from disk (seen on older chats; the cause and retention rule are unknown) | Nothing to recover locally; export important chats soon after they happen |
| Runtime logs missing for a turn | The turn ran in the remote sandbox (the report marks it), or the local logs were removed | Expected for remote turns; use `watch` next time for local ones |
| `ambiguous chat id` | The suffix matches several chats | Use the full folder name from the error |
| `❓ Unrecognised` entries in the report | A newer app or SDK wrote a record type the exporter does not know | They are still rendered raw; record the app version and update the exporter |

Other limits: macOS only (other platforms store app logs elsewhere and are untested); the header's app version is
the one installed at export time, not necessarily the one that ran the chat.
