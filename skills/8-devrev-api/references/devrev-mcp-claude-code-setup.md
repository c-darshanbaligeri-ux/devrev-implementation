> **SUPERSEDED (2026-07):** This repo wires the **hosted** DevRev MCP server via the root `.mcp.json`
> (`https://api.devrev.ai/mcp/v1`, `Authorization: Bearer ${DEVREV_PAT}`) — no local server needed.
> The npx `@devrev/mcp-server` flow below is the legacy/archived option, kept for reference only.

# Setting up DevRev as an MCP server for Claude Code

A step-by-step guide to connect your DevRev workspace to Claude Code using the
Model Context Protocol (MCP), so Claude Code can search, read, create, and update
DevRev work items directly from your terminal.

---

## 1. What this gives you

MCP lets Claude Code call DevRev's tools directly. Instead of switching to the
DevRev UI, you ask Claude Code in plain language and it invokes the matching
DevRev API under the hood.

You can combine DevRev context with your codebase in one session — e.g. read an
issue, fix the relevant code, and comment back on the issue without leaving the
terminal.

---

## 2. Prerequisites

- Claude Code installed and working (`claude --version` returns a version).
- Node.js 18+ installed (`node --version`). The DevRev MCP server runs via `npx`.
- A DevRev account with permission to generate a Personal Access Token (PAT).

---

## 3. Get a DevRev Personal Access Token (PAT)

1. Log in to DevRev.
2. Go to **Settings -> Account -> Personal Access Tokens** (also called API tokens).
3. Click **New token**, give it a clear name (e.g. `claude-code-mcp`).
4. Copy the token immediately and store it somewhere safe — you cannot view it again.

> Security: treat the PAT like a password. Do not commit it to source control.
> Prefer an environment variable or Claude Code's `--env` flag over hardcoding.

---

## 4. Add the MCP server to Claude Code

### Option A — CLI (recommended)

```bash
claude mcp add devrev \
  --env DEVREV_API_KEY=your_pat_here \
  -- npx -y @devrev/mcp-server
```

- `devrev` is the name the server appears under in Claude Code.
- Replace `your_pat_here` with the PAT from step 3.

### Option B — Manual config

Add to your Claude Code config file. Use `~/.claude.json` for a global setup, or
a project-level `.mcp.json` to share with a repo (never commit real secrets).

```json
{
  "mcpServers": {
    "devrev": {
      "command": "npx",
      "args": ["-y", "@devrev/mcp-server"],
      "env": {
        "DEVREV_API_KEY": "your_pat_here"
      }
    }
  }
}
```

### Scope tip

- Global (`~/.claude.json`): available in every project on your machine.
- Project (`.mcp.json`): shared with the repo. Reference the token via an env var
  (e.g. `"DEVREV_API_KEY": "${DEVREV_API_KEY}"`) and set it in your shell instead
  of committing the literal value.

---

## 5. Verify the connection

1. Restart Claude Code (or reload the session).
2. Run the slash command:

   ```
   /mcp
   ```

3. Confirm the `devrev` server shows as **connected** and lists its tools.

If it fails to connect, see Troubleshooting below.

---

## 6. What you can do once connected

### Read / search
- Search across work items — tickets, issues, enhancements.
- Fetch a specific object by ID and read full detail (description, status, owner, timeline).
- Look up accounts, parts (product areas), and users.
- Run analytical queries ("how many open tickets do I own", "issues in this sprint").

### Write / create
- Create tickets and issues from the terminal.
- Add comments to existing work items.
- Update fields — status, owner, priority, tags.
- Link objects (ticket <-> issue, issue <-> issue).

### Example prompts to Claude Code
- "Here's a stack trace — create an issue and assign it to me."
- "Read ISS-329585 and summarize what's blocking it."
- "I fixed this bug in the code — add a comment to the ticket and mark it resolved."
- "List my P0 issues and draft a status update."

---

## 7. Limitations to be aware of

- **Agent / workflow creation is NOT supported** via the standard DevRev MCP server.
  The MCP surface is built around data and work-item operations. Building AI agents,
  defining agent skills, or authoring workflows on the canvas is done through
  DevRev's own Builder tooling, not through this MCP connection.
- The exact tool list varies by DevRev MCP server version. Newer or org-specific
  snap-ins may expose more than the standard set.
- The authoritative way to see what your install supports is `/mcp` in Claude Code —
  it lists every available tool by name.

---

## 8. Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Server not listed after `/mcp` | Config not loaded | Fully restart Claude Code |
| `command not found: npx` | Node.js not installed | Install Node 18+ and retry |
| Auth / 401 errors | Bad or expired PAT | Regenerate the token, update the env var |
| `@devrev/mcp-server` not found | Package name differs for your org/version | Check DevRev's official MCP docs for the current package/endpoint |
| Tools connect but return no data | Wrong org or insufficient token scope | Verify the PAT belongs to the correct DevRev org and has needed permissions |

---

## 9. Next steps

- Run `/mcp` and note the exact tool names available in your org.
- Try a low-risk read first ("search my open issues") before any create/update action.
- If you need agent or workflow building, use the DevRev Builder UI — that is
  outside the MCP connection.

---

*Note: The exact package name and token steps can change with DevRev releases.
If `@devrev/mcp-server` does not resolve, confirm the current package name and
endpoint in DevRev's official MCP documentation.*
