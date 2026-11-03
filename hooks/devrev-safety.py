#!/usr/bin/env python3
"""PreToolUse hook: gate shell commands that call the DevRev API by risk class. Standard library only.

    read         -> "allow"  (only when the WHOLE command is read-only DevRev calls plus harmless filters)
    write        -> "ask"    (the user confirms; the reason names the endpoint)
    destructive  -> "ask"    (the reason says DESTRUCTIVE / hard to reverse)
    anything else (no DevRev endpoint found, unknown host, unparseable) -> no decision: the normal prompt applies.

It also covers the toolkit's own workflow tools, whose API calls happen inside Python where the curl check cannot see
them: `devrev-validate-workflow` (offline) and `devrev-import-workflow --dry-run` (sends nothing) are read; a plain
`devrev-import-workflow` run creates a draft workflow (write, ask); with --publish, --attach-connection or
--override-draft it asks with a HIGH IMPACT reason. A write that changes a live automation (workflows.update-status,
workflow-versions.publish, an import that replaces a draft) says HIGH IMPACT in the prompt.

A hook's "allow" approves the whole tool call, so it is deliberately narrow: `curl .../works.list; rm -rf ~`,
output redirection, `curl ... | sh`, `-o file`, heredocs and most command substitutions are NOT auto-approved.
Any error exits 0 with no output, so the hook can never block the session by crashing.

Registered by hooks/hooks.json (plugin) and .claude/settings.json (this repo). Reads the PreToolUse JSON on stdin.
"""
import json
import re
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import devrev_risk  # noqa: E402

SAFE_COMMANDS = {"jq", "head", "tail", "wc", "cut", "tr", "grep", "echo", "printf"}
FORBIDDEN_CURL = re.compile(r"^-[A-Za-z]*[oOTK][A-Za-z]*$|^--(output|remote-name|upload-file|config|create-dirs)(=.*)?$")
ENV_LOADERS = re.compile(r"^(set [-+]a|(source|\.) (\./)?\.env)$")
ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
OPERATORS = {";", "&&", "||", "|", "&"}
IMPORT_TOOLS = {"devrev-import-workflow", "import_workflow.py"}
VALIDATE_TOOLS = {"devrev-validate-workflow", "validate_template.py"}
PYTHON = re.compile(r"^python[0-9.]*$")
IMPORT_IMPACT = {
    "--publish": "switches the workflow on, or publishes a new version of a live one",
    "--attach-connection": "attaches a connection (credentials) to a workflow step",
    "--override-draft": "replaces the workflow's existing draft",
}


def normalize(command: str) -> str:
    """Drop backslash-newline continuations and turn unquoted newlines into ';' so segments split correctly."""
    command = command.replace("\\\r\n", " ").replace("\\\n", " ")
    out, quote, esc = [], None, False
    for ch in command:
        if esc:
            out.append(ch)
            esc = False
            continue
        if ch == "\\" and quote != "'":
            out.append(ch)
            esc = True
            continue
        if quote:
            if ch == quote:
                quote = None
            out.append(ch)
            continue
        if ch in "'\"":
            quote = ch
        if ch == "\n":
            out.append(" ; ")
            continue
        out.append(ch)
    return "".join(out)


def tokens(command: str):
    lex = shlex.shlex(command, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    return list(lex)


def segments(toks):
    seg, out = [], []
    for t in toks:
        if t in OPERATORS:
            if seg:
                out.append(seg)
            seg = []
        else:
            seg.append(t)
    if seg:
        out.append(seg)
    return out


def redirects_ok(toks) -> bool:
    """Only redirections to /dev/null or fd duplication (2>&1) are harmless."""
    for i, t in enumerate(toks):
        if re.fullmatch(r"\d*[<>]+&?|&>+", t):
            nxt = toks[i + 1] if i + 1 < len(toks) else ""
            if t.endswith("&") and nxt.isdigit():
                continue
            if t.startswith(">") or re.match(r"\d>", t):
                if nxt == "/dev/null":
                    continue
            return False
    return True


def tool_of(words):
    """('import' | 'validate', {--flags}) when a segment runs one of the toolkit's workflow tools, else None."""
    words = list(words)
    while words and ASSIGN.match(words[0]) and not words[0].startswith("-"):
        words = words[1:]
    if not words:
        return None
    name, rest = Path(words[0]).name, words[1:]
    if PYTHON.match(name):
        script = next((w for w in rest if not w.startswith("-")), None)
        if script is None:
            return None
        name, rest = Path(script).name, rest[rest.index(script) + 1:]
    kind = "import" if name in IMPORT_TOOLS else "validate" if name in VALIDATE_TOOLS else None
    if kind is None:
        return None
    if "--" in rest:  # after a bare `--` argparse treats everything as positional, never as a flag
        rest = rest[:rest.index("--")]
    return kind, {w.split("=", 1)[0] for w in rest if w.startswith("--")}


def tool_calls(command: str):
    try:
        segs = segments(tokens(normalize(command)))
    except ValueError:
        return []
    return [t for t in (tool_of(s) for s in segs) if t]


def segment_ok(seg) -> bool:
    words = [w for w in seg if not re.fullmatch(r"\d*[<>]+&?|&>+|/dev/null|\d+", w) or w in ("echo", "printf")]
    while words and ASSIGN.match(words[0]) and not words[0].startswith("-"):
        words = words[1:]
    if not words:
        return False
    first = words[0]
    if ENV_LOADERS.match(" ".join(seg)):
        return True
    tool = tool_of(words)
    if tool:
        return tool[0] == "validate" or "--dry-run" in tool[1]
    if first == "curl":
        return not any(FORBIDDEN_CURL.match(w) for w in words[1:] if w.startswith("-"))
    return first in SAFE_COMMANDS


def is_pure_read(command: str, depth: int = 0) -> bool:
    """True only if every part of the command is a harmless step and nothing writes or executes unknown code."""
    cmd = normalize(command).strip()
    if not cmd or "`" in cmd or "<<" in cmd or "<(" in cmd or ">(" in cmd:
        return False
    m = re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=\$\((.*)\)", cmd, re.S)  # VAR=$(inner): verify inner on its own
    if m and depth == 0:
        return is_pure_read(m.group(1), depth + 1)
    if "$(" in cmd:
        return False
    try:
        toks = tokens(cmd)
    except ValueError:
        return False
    if not redirects_ok(toks):
        return False
    segs = segments([t for t in toks])
    return bool(segs) and all(segment_ok(s) for s in segs) and any("curl" in s or tool_of(s) for s in segs)


def decision(kind: str, reason: str) -> dict:
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": kind, "permissionDecisionReason": reason}}


def decide(command: str):
    risk, per = devrev_risk.classify_command(command)
    per, notes = list(per), devrev_risk.impact_notes(command)
    for kind, flags in tool_calls(command):
        if kind == "validate":
            per.append(("devrev-validate-workflow (offline check)", "read"))
        elif "--dry-run" in flags:
            per.append(("devrev-import-workflow --dry-run (sends nothing)", "read"))
        else:
            high = sorted(flags & set(IMPORT_IMPACT))
            per.append((" ".join(["devrev-import-workflow"] + high) + ("" if high else " (creates a draft workflow in the org)"), "write"))
            notes += [f"devrev-import-workflow {f} {IMPORT_IMPACT[f]}" for f in high]
    if not per:
        return None
    order = {"read": 0, "write": 1, "destructive": 2}
    risk = max((r for _, r in per), key=order.__getitem__)
    names = ", ".join(f"{n} [{r}]" for n, r in per)
    if risk == "read":
        return decision("allow", f"DevRev read-only call ({names}).") if is_pure_read(command) else None
    if risk == "destructive":
        return decision("ask", f"DevRev DESTRUCTIVE / hard-to-reverse call ({names}). Confirm the target and that it was snapshotted first.")
    if notes:
        return decision("ask", f"DevRev HIGH IMPACT write ({names}): " + "; ".join(notes) +
                        ". Confirm the target org and that the user approved this in this session.")
    return decision("ask", f"DevRev write call ({names}). This changes data in the organization.")


def main() -> int:
    try:
        data = json.load(sys.stdin)
        if data.get("tool_name") != "Bash":
            return 0
        out = decide(data.get("tool_input", {}).get("command", ""))
        if out:
            print(json.dumps(out))
    except Exception:
        return 0  # never block the session because the hook itself failed
    return 0


if __name__ == "__main__":
    sys.exit(main())
