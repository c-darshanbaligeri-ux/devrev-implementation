#!/usr/bin/env python3
"""PreToolUse hook: gate shell commands that call the DevRev API by risk class. Standard library only.

    read         -> "allow"  (only when the WHOLE command is read-only DevRev calls plus harmless filters)
    write        -> "ask"    (the user confirms; the reason names the endpoint)
    destructive  -> "ask"    (the reason says DESTRUCTIVE / hard to reverse)
    anything else (no DevRev endpoint found, unknown host, unparseable) -> no decision: the normal prompt applies.

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


def segment_ok(seg) -> bool:
    words = [w for w in seg if not re.fullmatch(r"\d*[<>]+&?|&>+|/dev/null|\d+", w) or w in ("echo", "printf")]
    while words and ASSIGN.match(words[0]) and not words[0].startswith("-"):
        words = words[1:]
    if not words:
        return False
    first = words[0]
    if ENV_LOADERS.match(" ".join(seg)):
        return True
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
    return bool(segs) and all(segment_ok(s) for s in segs) and any("curl" in s for s in segs)


def decision(kind: str, reason: str) -> dict:
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": kind, "permissionDecisionReason": reason}}


def decide(command: str):
    risk, per = devrev_risk.classify_command(command)
    if risk is None:
        return None
    names = ", ".join(f"{n} [{r}]" for n, r in per)
    if risk == "read":
        return decision("allow", f"DevRev read-only call ({names}).") if is_pure_read(command) else None
    if risk == "destructive":
        return decision("ask", f"DevRev DESTRUCTIVE / hard-to-reverse call ({names}). Confirm the target and that it was snapshotted first.")
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
