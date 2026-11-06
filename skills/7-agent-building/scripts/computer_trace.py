#!/usr/bin/env python3
"""DevRev Computer session tracer.

Turns one DevRev Computer desktop chat into a traceability bundle:

  TRACE_REPORT.md        stage-by-stage trace of every turn (input -> runtime prep ->
                         injected context -> reasoning/tool loop -> output -> delivery)
  raw/                   verbatim copies of every source file (secret patterns redacted,
                         original hash recorded when anything was redacted)
  run-data-<chat>.json   the same session in agent-evals run-data format
                         (agent_evals/agent.py Turn schema)
  MANIFEST.sha256        sha256 of every file in the bundle (verify: shasum -a 256 -c)

Sources, all opened read-only:
  ~/.devrev/computer/<identity>/agent/projects/<workdir-slug>/<session>.jsonl
        Claude Agent SDK transcript (the app embeds @anthropic-ai/claude-agent-sdk)
  .../<session>/subagents/agent-<id>.jsonl (+ .meta.json)    subagent transcripts
  .../<session>/tool-results/*                               large tool outputs
  ~/.devrev/computer/<identity>/chats/<chat>/{metadata.json,events.ndjson,todos.json,
        session-approvals.json}
  ~/.devrev/computer/<identity>/chats/<chat>/debug/{debug.log,computer-agent-sdk-debug.log}
        Written only for turns that run LOCALLY in the desktop app. Turns that run in DevRev's
        remote sandbox (cwd /home/devrev/agentcore/...) are synced into the transcript but
        leave no local runtime log. `watch` archives these files during a session as insurance.
  ~/Library/Application Support/Computer/logs/{combined*,error*}.log   (local time)

Subcommands:
  list     recent chats across identities
  watch    archive a chat's per-run files while a session is in progress
  export   build the bundle

Never calls any DevRev API and never writes under ~/.devrev or the app's folders.
Run with:  python3 -I computer_trace.py <subcommand> ...
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import plistlib
import re
import signal
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

__version__ = "1.0.0"

HOME = Path.home()
ROOT = HOME / ".devrev" / "computer"
APP_LOGS = HOME / "Library" / "Application Support" / "Computer" / "logs"
APP_PLIST = Path("/Applications/Computer.app/Contents/Info.plist")
HERE = Path(__file__).resolve().parent

CHAT_FILES = ("metadata.json", "events.ndjson", "todos.json", "session-approvals.json")
DEBUG_FILES = ("debug.log", "computer-agent-sdk-debug.log")
WATCHED = CHAT_FILES + tuple(f"debug/{n}" for n in DEBUG_FILES)
CONTROL_TYPES = {"queue-operation", "last-prompt", "mode", "atis-latch", "summary",
                 "file-history-snapshot", "custom-title", "tag"}
BIG = 2000           # bodies longer than this go inside <details> (never truncated)
BLOB_MIN = 4000      # base64 strings at least this long are moved to raw/blobs/

UTC = timezone.utc


# ───────────────────────── small helpers ─────────────────────────

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_ts(s: Any) -> Optional[datetime]:
    """ISO-8601 (with Z) or 'YYYY-MM-DD HH:MM:SS' local time -> aware UTC datetime."""
    if not isinstance(s, str) or not s:
        return None
    t = s.strip()
    if t.endswith("Z"):
        t = t[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(t)
    except ValueError:
        return None
    if dt.tzinfo is None:          # app logs are naive local time
        dt = dt.astimezone()       # interpret with the machine's local rules
    return dt.astimezone(UTC)


def fmt_ts(dt: Optional[datetime]) -> str:
    if not dt:
        return "—"
    loc = dt.astimezone()
    return (f"{dt:%Y-%m-%d %H:%M:%S}.{dt.microsecond // 1000:03d}Z "
            f"({loc:%H:%M:%S} {loc.tzname()})")


def fmt_secs(sec: Optional[float]) -> str:
    if sec is None:
        return "—"
    if sec < 1:
        return f"{sec * 1000:.0f} ms"
    if sec < 60:
        return f"{sec:.2f} s"
    m, s = divmod(sec, 60)
    if m < 60:
        return f"{int(m)}m {s:.1f}s"
    h, m = divmod(m, 60)
    return f"{int(h)}h {int(m)}m {s:.0f}s"


def delta(a: Optional[datetime], b: Optional[datetime]) -> Optional[float]:
    if a and b:
        return (b - a).total_seconds()
    return None


def slugify(path: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "-", path)


def pjson(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False, default=str)


def fence(text: str, lang: str = "") -> str:
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    f = "`" * max(3, longest + 1)
    return f"{f}{lang}\n{text}\n{f}"


def html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cell(s: Any) -> str:
    """Make a value safe for a Markdown table cell (content kept in full)."""
    t = s if isinstance(s, str) else json.dumps(s, ensure_ascii=False, default=str)
    return html_escape(t).replace("|", "\\|").replace("\r", "").replace("\n", "<br>")


def body(title: str, text: str, lang: str = "text", details: Optional[bool] = None) -> str:
    """Render a verbatim body; long ones collapse into <details>, never truncated."""
    use_details = len(text) > BIG if details is None else details
    if use_details:
        return (f"<details><summary>{html_escape(title)} — {len(text):,} chars</summary>\n\n"
                f"{fence(text, lang)}\n\n</details>")
    return f"**{title}**\n\n{fence(text, lang)}"


# ───────────────────────── redaction ─────────────────────────

REDACTIONS = [
    (re.compile(r"(?i)(bearer\s+)(?!\[REDACTED)[A-Za-z0-9._~+/=-]{8,}"), r"\1[REDACTED]"),
    (re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{4,}"), "[REDACTED_JWT]"),
    (re.compile(r'(?i)("?authorization"?\s*[:=]\s*"?)(?!\[REDACTED)'
                r'(?=[^"\s,}\\]*\d)([^"\s,}\\]{16,})'), r"\1[REDACTED]"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9_-]{10,}"), "[REDACTED_KEY]"),
    (re.compile(r"\b(?:ghp|gho|ghs|github_pat)_[A-Za-z0-9_]{20,}"), "[REDACTED_KEY]"),
    (re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}"), "[REDACTED_KEY]"),
    (re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), "[REDACTED_KEY]"),
    # Pre-signed S3 URLs: the signature and session token grant time-limited access.
    (re.compile(r"(?i)(X-Amz-(?:Signature|Security-Token|Credential)=)(?!\[REDACTED)[^&\s\"'\\]+"),
     r"\1[REDACTED]"),
]


def redact(text: str) -> tuple[str, int]:
    total = 0
    for rx, rep in REDACTIONS:
        text, n = rx.subn(rep, text)
        total += n
    return text, total


# ───────────────────────── locating chats ─────────────────────────

ID_RX = re.compile(r"^don_identity_(dvrv-[a-z]+-\d+)_devo_([^_]+)_(.+)$", re.I)


def identity_label(name: str) -> str:
    m = ID_RX.match(name)
    return f"region={m.group(1)} org={m.group(2)} user={m.group(3)}" if m else name


@dataclass
class Chat:
    identity_dir: Path
    chat_dir: Path

    @property
    def name(self) -> str:
        return self.chat_dir.name

    @property
    def key(self) -> str:
        return self.name.split("_")[-1]

    @property
    def workdir(self) -> Path:
        return self.chat_dir / "workdir"

    @property
    def project_dir(self) -> Path:
        projects = self.identity_dir / "agent" / "projects"
        exact = projects / slugify(str(self.workdir))
        if exact.is_dir():
            return exact
        cands = sorted(projects.glob(f"*{slugify(self.name)}-workdir"))
        return cands[0] if cands else exact

    def transcripts(self) -> list[Path]:
        p = self.project_dir
        return sorted(x for x in p.glob("*.jsonl") if x.is_file()) if p.is_dir() else []

    def last_activity(self) -> float:
        ts = [x.stat().st_mtime for x in self.transcripts()]
        return max(ts) if ts else self.chat_dir.stat().st_mtime

    def metadata(self) -> dict:
        try:
            return json.loads((self.chat_dir / "metadata.json").read_text())
        except (OSError, ValueError):
            return {}

    @property
    def don(self) -> str:
        return self.metadata().get("chatId") or self.name


def iter_identities() -> list[Path]:
    if not ROOT.is_dir():
        sys.exit(f"ERROR: {ROOT} not found — is the DevRev Computer app installed and used?")
    return [d for d in sorted(ROOT.iterdir())
            if d.is_dir() and (d / "chats").is_dir() and (d / "agent").is_dir()]


def iter_chats(include_background: bool) -> list[Chat]:
    out = []
    for ident in iter_identities():
        for c in sorted((ident / "chats").iterdir()):
            if c.is_dir() and (include_background or not c.name.startswith("background-")):
                out.append(Chat(ident, c))
    return out


def resolve_chat(query: str) -> Chat:
    q = re.sub(r"[:/]", "_", query.strip())      # accept a chat DON too
    chats = iter_chats(include_background=True)
    exact = [c for c in chats if c.name == q]
    if exact:
        return exact[0]
    hits = [c for c in chats if c.name.endswith(q) or q in c.name]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        sys.exit(f"ERROR: no chat matches {query!r}. Run `list` to see chat ids.")
    sys.exit("ERROR: ambiguous chat id; matches:\n  " + "\n  ".join(
        f"{c.name}  ({c.identity_dir.name})" for c in hits))


def latest_chat() -> Chat:
    chats = [c for c in iter_chats(False) if c.transcripts()]
    if not chats:
        sys.exit("ERROR: no chats with transcripts found.")
    return max(chats, key=lambda c: c.last_activity())


def first_line_ts(data: bytes) -> str:
    m = re.match(rb"(\d{4}-\d\d-\d\dT[\d:.]+Z)", data[:64])
    return m.group(1).decode() if m else ""


# ───────────────────────── list ─────────────────────────

def prompt_summary(c: Chat) -> tuple[int, str]:
    n, first = 0, ""
    for t in c.transcripts():
        data = t.read_bytes()
        n += data.count(b'"promptSource":"sdk"')
        if not first:
            for line in data.splitlines():
                if b'"promptSource":"sdk"' in line:
                    try:
                        first = prompt_text(json.loads(line)) or ""
                    except ValueError:
                        pass
                    break
    return n, " ".join(first.split())[:60]


def cmd_list(a: argparse.Namespace) -> None:
    t0 = time.time()
    rows = sorted(((c.last_activity(), c) for c in iter_chats(a.include_background)),
                  key=lambda r: r[0], reverse=True)
    print(f"{'last activity (local)':<20} {'prompts':>7} {'size':>8}  chat id  /  identity  /  first prompt")
    for mtime, c in rows[: a.limit]:
        n, first = prompt_summary(c)
        size = sum(t.stat().st_size for t in c.transcripts())
        print(f"{datetime.fromtimestamp(mtime):%Y-%m-%d %H:%M:%S} {n:>7} {size / 1024:>7.0f}K  "
              f"{c.name}\n{'':>38}{identity_label(c.identity_dir.name)}\n{'':>38}{first!r}")
    print(f"\n{len(rows)} chats scanned in {time.time() - t0:.1f}s "
          f"(showing {min(a.limit, len(rows))}; --include-background to see background jobs)")


# ───────────────────────── watch ─────────────────────────

def snapshot_key(rel: str, data: bytes) -> str:
    """One snapshot file per run: debug logs keyed by their first-line timestamp (a new run
    that rewrites the file gets a new key; an appended file keeps one key), metadata.json by
    its createdAt, other files by a hash of their first line."""
    if rel.startswith("debug/"):
        return "run_" + (re.sub(r"[^0-9TZ]", "", first_line_ts(data)) or "nots")
    if rel == "metadata.json":
        try:
            return "created_" + (re.sub(r"[^0-9TZ]", "", json.loads(data).get("createdAt") or "") or "none")
        except (ValueError, AttributeError):
            return "invalid"
    return "first_" + sha256(data.split(b"\n", 1)[0])[:12]


def cmd_watch(a: argparse.Namespace) -> None:
    out = Path(a.out) if a.out else HERE / "watch" / datetime.now().strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True, exist_ok=True)
    stop = {"flag": False}

    def _stop(*_: Any) -> None:
        stop["flag"] = True
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    def say(msg: str) -> None:
        print(f"[watch {datetime.now():%H:%M:%S}] {msg}", flush=True)

    watched: dict[Path, dict] = {}

    def start(c: Chat) -> None:
        d = out / c.name
        (d / "snapshots").mkdir(parents=True, exist_ok=True)
        (d / "watch.json").write_text(pjson({
            "chat_folder": c.name, "identity": c.identity_dir.name, "chat_dir": str(c.chat_dir),
            "started_at": datetime.now(UTC).isoformat(), "interval_s": a.interval}))
        watched[c.chat_dir] = {"chat": c, "dir": d, "hash": {}, "size": {}, "updates": 0,
                               "log": open(d / "watch-log.jsonl", "a")}
        say(f"watching {c.name} ({identity_label(c.identity_dir.name)}) -> {d}")

    known: set[Path] = set()
    if a.chat:
        start(resolve_chat(a.chat))
    else:
        known = {c.chat_dir for c in iter_chats(True)}
        say(f"waiting for NEW Computer chats ({len(known)} existing chats ignored); every new chat "
            f"folder is archived in its own subfolder of {out}")
    last_change, last_beat = time.time(), time.time()
    while not stop["flag"]:
        if not a.chat:
            for c in iter_chats(False):
                if c.chat_dir not in known and c.chat_dir not in watched:
                    start(c)
        for st in watched.values():
            c, d = st["chat"], st["dir"]
            for rel in WATCHED:
                p = c.chat_dir / rel
                try:
                    data = p.read_bytes()
                except OSError:
                    continue
                h = sha256(data)
                if st["hash"].get(rel) == h:
                    continue
                st["hash"][rel], last_change = h, time.time()
                key = f"{rel}|{snapshot_key(rel, data)}"
                n = 1
                while key in st["size"] and len(data) < st["size"][key]:   # never overwrite with less
                    n += 1
                    key = f"{rel}|{snapshot_key(rel, data)}__v{n}"
                action = "update" if key in st["size"] else "new"
                st["size"][key] = len(data)
                dest = d / "snapshots" / rel.replace("/", "__") / f"{key.split('|', 1)[1]}{p.suffix}"
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
                st["updates"] += 1
                stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S.%f")[:-3] + "Z"
                st["log"].write(json.dumps({"captured_at": stamp, "action": action, "file": rel,
                                            "bytes": len(data), "sha256": h,
                                            "first_line_ts": first_line_ts(data),
                                            "snapshot": str(dest.relative_to(d))}) + "\n")
                st["log"].flush()
                if action == "new":
                    say(f"{c.key}: new snapshot {rel} -> {dest.name} ({len(data):,} B)")
        if time.time() - last_beat > 60 and watched:
            last_beat = time.time()
            say("heartbeat: " + ", ".join(f"{s['chat'].key}={s['updates']} updates, "
                                          f"{len(s['size'])} files" for s in watched.values()))
        if a.idle_stop and watched and time.time() - last_change > a.idle_stop:
            say(f"no changes for {a.idle_stop}s — stopping")
            break
        time.sleep(a.interval)
    for st in watched.values():
        st["log"].close()
        say(f"done: {st['chat'].name}: {st['updates']} updates kept as {len(st['size'])} per-run files")
    if not watched:
        say("stopped before any new chat appeared")


# ───────────────────────── transcript model ─────────────────────────

@dataclass
class Rec:
    label: str
    line: int
    data: dict
    ts: Optional[datetime]

    @property
    def key(self) -> tuple[str, int]:
        return (self.label, self.line)

    @property
    def type(self) -> str:
        return str(self.data.get("type"))


def load_jsonl(path: Path, label: str) -> tuple[list[Rec], int]:
    recs, errors = [], 0
    for i, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        try:
            d = json.loads(line)
        except ValueError:
            d, errors = {"type": "__unparseable__", "raw": line}, errors + 1
        if not isinstance(d, dict):
            d = {"type": "__non_object__", "raw": d}
        recs.append(Rec(label, i, d, parse_ts(d.get("timestamp"))))
    return recs, errors


def content_of(d: dict) -> Any:
    m = d.get("message")
    return m.get("content") if isinstance(m, dict) else None


def is_tool_result_user(d: dict) -> bool:
    c = content_of(d)
    return isinstance(c, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c)


def prompt_text(d: dict) -> Optional[str]:
    c = content_of(d)
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
    return None


@dataclass
class Step:
    kind: str                      # text|tool|thinking|context|system|orphan_result|unknown
    rec: Rec
    block: Optional[dict] = None
    first_of_msg: bool = False
    result: Optional[tuple[Rec, dict]] = None
    num: str = ""


@dataclass
class LogLine:
    ts: Optional[datetime]
    source: str
    level: str
    cid: Optional[str]
    component: str
    text: str
    kv: dict = field(default_factory=dict)

    def dedup_key(self) -> tuple:
        return (self.source, self.ts, self.level, self.component, self.text)

    def render(self) -> str:
        cid = " [cid]" if self.cid else ""
        comp = f" [{self.component}]" if self.component else ""
        return f"{fmt_ts(self.ts)[:24]}  {self.source:<14} [{self.level}]{cid}{comp} {self.text}"


@dataclass
class Run:
    cid: str
    start: datetime
    end: datetime
    lines: list[LogLine]
    replies: list[str]


@dataclass
class Turn:
    k: int
    prompt: Rec
    records: list[Rec]
    steps: list[Step] = field(default_factory=list)
    run: Optional[Run] = None
    win_start: Optional[datetime] = None
    logs: list[LogLine] = field(default_factory=list)
    location: str = "unknown"       # local | remote | unknown  (from the records' cwd)
    location_detail: str = ""


# ───────────────────────── log parsing ─────────────────────────

LINE_RX = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z) \[(\w+)\] ?(.*)$")


def parse_stamped_log(text: str, source: str) -> list[LogLine]:
    out: list[LogLine] = []
    for raw in text.splitlines():
        m = LINE_RX.match(raw)
        if not m:
            if out:
                out[-1].text += "\n" + raw
            elif raw.strip():
                out.append(LogLine(None, source, "", None, "", raw))
            continue
        ts, level, rest = m.groups()
        cid, comp = None, ""
        m2 = re.match(r"\[timeline_comment_id=([^\]]*)\] ?(.*)$", rest)
        if m2:
            cid, rest = m2.group(1) or None, m2.group(2)
        m3 = re.match(r"\[([^\]]+)\] ?(.*)$", rest)
        if m3:
            comp, rest = m3.groups()
        kv = dict(re.findall(r"(\w+)=(\S+)", rest)) if comp == "metric" else {}
        out.append(LogLine(parse_ts(ts), source, level, cid, comp, rest, kv))
    return out


def parse_json_log(lines: list[str], source: str) -> list[LogLine]:
    out = []
    for raw in lines:
        try:
            o = json.loads(raw)
        except ValueError:
            m = re.match(r"^(\S+ \S+|\S+)\s+(.*)$", raw)
            out.append(LogLine(parse_ts(m.group(1)) if m else None, source, "", None, "", raw))
            continue
        if not isinstance(o, dict):
            out.append(LogLine(None, source, "", None, "", raw))
            continue
        extra = {k: v for k, v in o.items() if k not in ("message", "timestamp", "level", "service")}
        out.append(LogLine(parse_ts(o.get("timestamp")), source, str(o.get("level", "")),
                           o.get("timelineCommentId") or None, str(o.get("service", "")),
                           str(o.get("message", "")) + (" " + json.dumps(extra, ensure_ascii=False) if extra else ""),
                           extra))
    return out


def parse_events(text: str) -> list[LogLine]:
    out = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        try:
            o = json.loads(raw)
        except ValueError:
            out.append(LogLine(None, "events.ndjson", "", None, "", raw))
            continue
        hi = o.get("hookInput") if isinstance(o, dict) else None
        label = hi.get("hook_event_name", "event") if isinstance(hi, dict) else "event"
        out.append(LogLine(parse_ts(o.get("timestamp")) if isinstance(o, dict) else None,
                           "events.ndjson", "event", None, str(label), raw))
    return out


# ───────────────────────── bundle writer ─────────────────────────

class Bundle:
    def __init__(self, root: Path):
        self.root = root
        self.entries: list[dict] = []
        self.redactions = 0

    def add(self, rel: str, data: bytes, source: str, redact_text: bool = True) -> str:
        dest = self.root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        orig = sha256(data)
        n = 0
        if redact_text:
            try:
                txt = data.decode("utf-8")
            except UnicodeDecodeError:
                txt = None
            if txt is not None:
                new, n = redact(txt)
                if n:
                    data = new.encode("utf-8")
        dest.write_bytes(data)
        self.entries.append({"path": rel, "source": source, "bytes": len(data), "sha256": sha256(data),
                             "redactions": n, "original_sha256": orig if n else None})
        self.redactions += n
        return rel

    def add_file(self, rel: str, src: Path) -> str:
        return self.add(rel, src.read_bytes(), str(src))


# ───────────────────────── export ─────────────────────────

class Exporter:
    def __init__(self, chat: Chat, out_root: Path, runs_dir: Optional[Path], include_workdir: bool):
        self.chat = chat
        self.runs_dir = runs_dir
        self.include_workdir = include_workdir
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.root = out_root / f"{chat.name}_{stamp}"
        self.root.mkdir(parents=True, exist_ok=False)
        self.b = Bundle(self.root)
        self.rendered: set[tuple[str, int]] = set()
        self.records_total: dict[str, int] = {}
        self.parse_errors = 0
        self.usage: dict[str, dict] = {}
        self.models: Counter = Counter()
        self.block_types: Counter = Counter()
        self.unknown: Counter = Counter()
        self.thinking = 0
        self.control: list[Rec] = []
        self.calls: dict[str, Step] = {}
        self.subagents: dict[str, dict] = {}
        self.tool_result_files: dict[str, tuple[Path, str]] = {}
        self.blob_seq = 0
        self.api_errors: list[Rec] = []
        self.md: list[str] = []
        self._ct_cache: dict[int, tuple[str, list[str]]] = {}

    # ---------- loading ----------
    def load(self) -> None:
        c = self.chat
        transcripts = c.transcripts()
        if not transcripts:
            sys.exit(f"ERROR: no transcript found for {c.name} (looked in {c.project_dir})")
        self.main: list[Rec] = []
        for t in transcripts:
            recs, err = load_jsonl(t, t.name)
            self.parse_errors += err
            self.records_total[t.name] = len(recs)
            self.main.extend(recs)
            self.b.add_file(f"raw/transcripts/{t.name}", t)
        first = {}
        for r in self.main:
            if r.ts and r.label not in first:
                first[r.label] = r.ts
        order = sorted(first, key=lambda k: first[k])
        self.main.sort(key=lambda r: (order.index(r.label) if r.label in order else 99, r.line))

        pd = c.project_dir
        for f in sorted(pd.iterdir()):
            if f.is_file() and f.suffix != ".jsonl":
                self.b.add_file(f"raw/transcripts/{f.name}", f)
        for sess_dir in sorted(x for x in pd.iterdir() if x.is_dir()):
            for meta in sorted((sess_dir / "subagents").glob("*.meta.json")):
                jl = meta.with_name(meta.name.replace(".meta.json", ".jsonl"))
                try:
                    m = json.loads(meta.read_text())
                except ValueError:
                    m = {}
                label = f"{sess_dir.name}/subagents/{jl.name}"
                recs, err = load_jsonl(jl, label) if jl.exists() else ([], 0)
                self.parse_errors += err
                self.records_total[label] = len(recs)
                self.subagents[m.get("toolUseId") or label] = {"meta": m, "recs": recs, "label": label}
                self.b.add_file(f"raw/transcripts/{sess_dir.name}/subagents/{meta.name}", meta)
                if jl.exists():
                    self.b.add_file(f"raw/transcripts/{label}", jl)
            for orphan in sorted((sess_dir / "subagents").glob("*.jsonl")):
                label = f"{sess_dir.name}/subagents/{orphan.name}"
                if label not in self.records_total:
                    recs, err = load_jsonl(orphan, label)
                    self.parse_errors += err
                    self.records_total[label] = len(recs)
                    self.subagents[label] = {"meta": {}, "recs": recs, "label": label}
                    self.b.add_file(f"raw/transcripts/{label}", orphan)
            tr = sess_dir / "tool-results"
            if tr.is_dir():
                for f in sorted(tr.iterdir()):
                    if f.is_file():
                        rel = self.b.add_file(f"raw/transcripts/{sess_dir.name}/tool-results/{f.name}", f)
                        self.tool_result_files[f.name] = (f, rel)

        for name in CHAT_FILES:
            p = c.chat_dir / name
            if p.is_file():
                self.b.add_file(f"raw/chat/{name}", p)
        for name in DEBUG_FILES:
            p = c.chat_dir / "debug" / name
            if p.is_file():
                self.b.add_file(f"raw/chat/debug/{name}", p)
        self.meta = c.metadata()
        self.load_logs()
        self.load_config_evidence()

    def load_logs(self) -> None:
        c = self.chat
        self.log_sources: list[str] = []
        texts: dict[str, list[str]] = {n: [] for n in DEBUG_FILES}
        events_texts: list[str] = []
        self.meta_versions: list[dict] = []
        self.snapshot_count = 0
        if self.runs_dir:
            rd = self.runs_dir / c.name if (self.runs_dir / c.name).is_dir() else self.runs_dir
            snaps = rd / "snapshots"
            if not snaps.is_dir():
                sys.exit(f"ERROR: no snapshots/ in {rd} — is --runs the folder written by `watch`?")
            wj = rd / "watch.json"
            if wj.is_file() and json.loads(wj.read_text()).get("chat_folder") not in (None, c.name):
                sys.exit(f"ERROR: {rd} is the watch archive of another chat, not {c.name}")
            for name in ("watch.json", "watch-log.jsonl"):
                p = rd / name
                if p.is_file():
                    self.b.add_file(f"raw/watch/{name}", p)
            for snap in sorted(snaps.glob("*/*")):
                if not snap.is_file():
                    continue
                self.snapshot_count += 1
                self.b.add_file(f"raw/watch/snapshots/{snap.parent.name}/{snap.name}", snap)
                fname = snap.parent.name.replace("__", "/").split("/")[-1]
                txt = snap.read_text(errors="replace")
                if fname in texts:
                    texts[fname].append(txt)
                elif fname == "events.ndjson":
                    events_texts.append(txt)
                elif fname == "metadata.json":
                    try:
                        captured = datetime.fromtimestamp(snap.stat().st_mtime, UTC).isoformat()
                        self.meta_versions.append({"captured_at": captured, "data": json.loads(txt)})
                    except ValueError:
                        pass
            self.log_sources.append(f"`watch` archive {rd} ({self.snapshot_count} per-run snapshot files)")
        for name in DEBUG_FILES:
            p = c.chat_dir / "debug" / name
            if p.is_file():
                texts[name].append(p.read_text(errors="replace"))
        ev = c.chat_dir / "events.ndjson"
        if ev.is_file():
            events_texts.append(ev.read_text(errors="replace"))
        if not self.meta_versions and self.meta:
            self.meta_versions.append({"captured_at": "current", "data": self.meta})
        self.log_sources.append("current per-chat debug logs (debug.log, computer-agent-sdk-debug.log)")

        seen: set = set()
        self.logs: list[LogLine] = []

        def add_lines(lines: list[LogLine]) -> None:
            for ln in lines:
                k = ln.dedup_key()
                if k not in seen:
                    seen.add(k)
                    self.logs.append(ln)
        for name, versions in texts.items():
            src = "sdk-debug" if name.startswith("computer") else "debug.log"
            for t in versions:
                add_lines(parse_stamped_log(t, src))
        for t in events_texts:
            add_lines(parse_events(t))

        key = self.chat.key.encode()
        self.app_log_hits: dict[str, int] = {}
        if APP_LOGS.is_dir():
            files = sorted(APP_LOGS.glob("combined*.log")) + sorted(APP_LOGS.glob("error*.log"))
            for f in files:
                with open(f, "rb") as fh:
                    hits = [ln.decode("utf-8", "replace").rstrip("\n") for ln in fh if key in ln]
                self.app_log_hits[f.name] = len(hits)
                if hits:
                    self.b.add(f"raw/app-logs/{f.name}.chat-lines.log", ("\n".join(hits) + "\n").encode(),
                               f"{f} (lines containing {self.chat.key!r})")
                    add_lines(parse_json_log(hits, f.name.replace(".log", "")))
        self.logs.sort(key=lambda ln: ln.ts or datetime.max.replace(tzinfo=UTC))

        by_cid: dict[str, list[LogLine]] = {}
        for ln in self.logs:
            if ln.cid and ln.source == "sdk-debug":
                by_cid.setdefault(ln.cid, []).append(ln)
        self.runs = []
        for cid, lines in by_cid.items():
            tss = [x.ts for x in lines if x.ts]
            if not tss:
                continue
            replies = []
            for x in lines:
                m = re.search(r"Created response entry (\S+)", x.text)
                if m:
                    replies.append(m.group(1))
            self.runs.append(Run(cid, min(tss), max(tss), lines, replies))
        self.runs.sort(key=lambda r: r.start)
        txt = "\n".join(ln.text for ln in self.logs if ln.source == "sdk-debug")
        m = re.search(r"agentId=(don:[^\s,]+)", txt)
        self.agent_id = m.group(1) if m else None
        m = re.search(r"Gateway model resolved: ?(.*)", txt)
        self.gateway = m.group(1).strip() if m else None

    def load_config_evidence(self) -> None:
        agent = self.chat.identity_dir / "agent"
        self.config_rel = None
        st = agent / "settings.json"
        if st.is_file():
            self.config_rel = self.b.add_file("raw/agent-config/settings.json", st)
        self.skills: list[tuple[str, int, str]] = []
        sk = agent / "skills"
        if sk.is_dir():
            for f in sorted(sk.rglob("*")):
                if f.is_file() and not f.is_symlink():
                    data = f.read_bytes()
                    self.skills.append((str(f.relative_to(sk)), len(data), sha256(data)))
        self.workdir_files: list[tuple[str, int, str]] = []
        wd = self.chat.workdir
        if wd.is_dir():
            for dp, _dns, fns in os.walk(wd, followlinks=False):
                for fn in sorted(fns):
                    f = Path(dp) / fn
                    if f.is_symlink() or not f.is_file():
                        continue
                    size = f.stat().st_size
                    digest = sha256(f.read_bytes()) if size <= 200 * 1024 * 1024 else "not hashed (>200 MB)"
                    rel = str(f.relative_to(wd))
                    self.workdir_files.append((rel, size, digest))
                    if self.include_workdir:
                        self.b.add(f"raw/workdir/{rel}", f.read_bytes(), str(f), redact_text=False)

    # ---------- blobs / images ----------
    def save_blob(self, data_b64: str, hint: str, media: str = "") -> str:
        self.blob_seq += 1
        ext = {"image/png": "png", "image/jpeg": "jpg", "image/gif": "gif", "image/webp": "webp",
               "application/pdf": "pdf"}.get(media, "bin")
        folder = "images" if media.startswith("image/") else "blobs"
        try:
            raw = base64.b64decode(data_b64, validate=False)
        except (ValueError, TypeError):
            raw = data_b64.encode()
            ext = "b64.txt"
        safe = re.sub(r"[^A-Za-z0-9_-]", "_", hint)[:40]
        return self.b.add(f"raw/{folder}/{self.blob_seq:03d}_{safe}.{ext}", raw,
                          f"base64 embedded in transcript ({hint})", redact_text=False)

    def deblob(self, obj: Any, hint: str) -> Any:
        """Copy of obj with long base64 strings moved to files (referenced, not inlined)."""
        if isinstance(obj, dict):
            if obj.get("type") == "base64" and isinstance(obj.get("data"), str) and len(obj["data"]) >= 200:
                rel = self.save_blob(obj["data"], hint, str(obj.get("media_type", "")))
                return {**obj, "data": f"<{len(obj['data']):,} base64 chars saved to {rel}>"}
            return {k: self.deblob(v, hint) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self.deblob(v, hint) for v in obj]
        if isinstance(obj, str) and len(obj) >= BLOB_MIN and re.fullmatch(r"[A-Za-z0-9+/=\r\n]+", obj):
            rel = self.save_blob(obj, hint)
            return f"<{len(obj):,} base64 chars saved to {rel}>"
        return obj

    def content_text(self, content: Any, hint: str) -> tuple[str, list[str]]:
        """tool_result / prompt content -> (verbatim text, image links). Cached per object
        so images are saved once even though the report and run-data both ask."""
        if isinstance(content, str):
            return content, []
        if not isinstance(content, list):
            return pjson(content), []
        if id(content) in self._ct_cache:
            return self._ct_cache[id(content)]
        result = self._content_text(content, hint)
        self._ct_cache[id(content)] = result
        return result

    def _content_text(self, content: list, hint: str) -> tuple[str, list[str]]:
        parts, images = [], []
        for b in content:
            if isinstance(b, dict) and b.get("type") == "text":
                parts.append(b.get("text", ""))
            elif isinstance(b, dict) and b.get("type") == "image":
                src = b.get("source") or {}
                if src.get("type") == "base64" and isinstance(src.get("data"), str):
                    rel = self.save_blob(src["data"], hint, str(src.get("media_type", "")))
                    images.append(rel)
                    parts.append(f"[image saved to {rel}]")
                else:
                    parts.append(pjson(b))
            else:
                parts.append(pjson(self.deblob(b, hint)))
        return "\n".join(parts), images

    # ---------- steps ----------
    def build_steps(self, recs: list[Rec]) -> list[Step]:
        steps: list[Step] = []
        seen_msg: set = set()
        for r in recs:
            d, t = r.data, r.type
            self.rendered.add(r.key)
            if t in CONTROL_TYPES:
                self.control.append(r)
                continue
            if d.get("isApiErrorMessage") or d.get("apiErrorStatus"):
                self.api_errors.append(r)
            if t == "assistant":
                m = d.get("message") if isinstance(d.get("message"), dict) else {}
                mid = m.get("id") or f"{r.label}:{r.line}"
                first = mid not in seen_msg
                seen_msg.add(mid)
                u = m.get("usage")
                if isinstance(u, dict):
                    prev = self.usage.get(mid)
                    if prev is None or (u.get("output_tokens") or 0) >= (prev.get("output_tokens") or 0):
                        self.usage[mid] = u
                if m.get("model"):
                    self.models[m["model"]] += 1 if first else 0
                blocks = m.get("content") if isinstance(m.get("content"), list) else []
                if not blocks:
                    steps.append(Step("unknown", r))
                    self.unknown[f"assistant without content list"] += 1
                for b in blocks:
                    bt = b.get("type") if isinstance(b, dict) else type(b).__name__
                    self.block_types[bt] += 1
                    if bt == "text":
                        steps.append(Step("text", r, b, first))
                    elif bt == "tool_use":
                        s = Step("tool", r, b, first)
                        self.calls[b.get("id", "")] = s
                        steps.append(s)
                    elif bt in ("thinking", "redacted_thinking"):
                        self.thinking += 1
                        steps.append(Step("thinking", r, b, first))
                    else:
                        self.unknown[f"assistant block:{bt}"] += 1
                        steps.append(Step("unknown", r, b, first))
                    first = False
            elif t == "user":
                c = content_of(d)
                if is_tool_result_user(d):
                    for b in c:
                        if isinstance(b, dict) and b.get("type") == "tool_result":
                            s = self.calls.get(b.get("tool_use_id", ""))
                            if s is not None and s.result is None:
                                s.result = (r, b)
                            else:
                                steps.append(Step("orphan_result", r, b))
                        else:
                            steps.append(Step("context", r, b if isinstance(b, dict) else {"value": b}))
                else:
                    steps.append(Step("context", r))
            elif t == "attachment":
                steps.append(Step("context", r))
            elif t == "system":
                steps.append(Step("system", r))
            else:
                self.unknown[f"record:{t}"] += 1
                steps.append(Step("unknown", r))
        return steps

    # ---------- turns ----------
    def segment(self) -> tuple[list[Rec], list[Turn]]:
        strict = any(r.data.get("promptSource") == "sdk" for r in self.main)

        def is_prompt(r: Rec) -> bool:
            d = r.data
            if r.type != "user" or d.get("isMeta") or d.get("isSidechain") or is_tool_result_user(d):
                return False
            return d.get("promptSource") == "sdk" if strict else True
        pre: list[Rec] = []
        turns: list[Turn] = []
        for r in self.main:
            if is_prompt(r):
                turns.append(Turn(len(turns) + 1, r, []))
            elif turns:
                turns[-1].records.append(r)
            else:
                pre.append(r)
        self.prompt_rule = ("user records with promptSource='sdk' that are not isMeta / tool results"
                            if strict else "user text records that are not isMeta / tool results "
                                           "(no promptSource field in this transcript)")
        return pre, turns

    def locate(self, turns: list[Turn]) -> None:
        """Where each turn executed, from the `cwd` its records carry: the local chat workdir on
        this Mac, or a DevRev remote sandbox (/home/devrev/agentcore/sessions/...)."""
        for t in turns:
            cw: Counter = Counter()
            for r in [t.prompt, *t.records]:
                cwd = r.data.get("cwd")
                if isinstance(cwd, str) and cwd:
                    cw["local" if cwd.startswith(str(HOME)) else cwd] += 1
            local = cw.pop("local", 0)
            remote = sum(cw.values())
            if not local and not remote:
                continue
            if remote > local:
                top = cw.most_common(1)[0][0]
                t.location = "remote"
                t.location_detail = (f"DevRev remote sandbox `{top}` ({remote} records"
                                     + (f"; {local} with the local workdir" if local else "") + ")")
            else:
                t.location = "local"
                t.location_detail = (f"this Mac, chat workdir ({local} records"
                                     + (f"; {remote} with a remote sandbox cwd" if remote else "") + ")")

    def missing_cause(self, t: Turn) -> str:
        if t.location == "remote":
            return (f"Turn {t.k} ran in a {t.location_detail}. Its transcript was synced to this Mac, but no "
                    f"runtime log lines for it were found here. Remote runs most likely log on DevRev's side.")
        if not (self.chat.chat_dir / "debug").is_dir() and not self.snapshot_count:
            return f"Turn {t.k} ran locally, but this chat has no per-chat `debug/` folder."
        first = min((ln.ts for ln in self.logs if ln.ts and ln.source in ("sdk-debug", "debug.log")), default=None)
        return (f"Turn {t.k} ran locally, but the surviving debug logs do not cover it"
                + (f" (they start at {fmt_ts(first)})" if first else "")
                + ", and no `watch` archive covered it.")

    def attach_logs(self, turns: list[Turn]) -> None:
        for t in turns:
            p = t.prompt.ts
            if not p:
                continue
            cands = [r for r in self.runs if r.start <= p + timedelta(seconds=5) and p <= r.end + timedelta(seconds=5)]
            t.run = max(cands, key=lambda r: r.start) if cands else None
            t.win_start = min(t.run.start, p) if t.run else p - timedelta(seconds=5)
        timed = [t for t in turns if t.win_start]
        self.unassigned_logs: list[LogLine] = []
        for ln in self.logs:
            if ln.cid and ln.source == "sdk-debug":
                owner = next((t for t in timed if t.run and t.run.cid == ln.cid), None)
                if owner:
                    owner.logs.append(ln)
                    continue
            owner = None
            if ln.ts:
                for t in timed:
                    if t.win_start and ln.ts >= t.win_start:
                        owner = t
            if owner:
                owner.logs.append(ln)
            else:
                self.unassigned_logs.append(ln)

    # ---------- rendering ----------
    def w(self, s: str = "") -> None:
        self.md.append(s)

    def usage_line(self, u: dict) -> str:
        return (f"in {u.get('input_tokens', 0):,} · out {u.get('output_tokens', 0):,} · "
                f"cache read {u.get('cache_read_input_tokens', 0):,} · "
                f"cache write {u.get('cache_creation_input_tokens', 0):,}"
                + (f" · thinking {u['output_tokens_details'].get('thinking_tokens', 0):,}"
                   if isinstance(u.get("output_tokens_details"), dict) else ""))

    def render_steps(self, steps: list[Step], prefix: str, start_ts: Optional[datetime]) -> None:
        prev = start_ts
        n = 0
        for s in steps:
            n += 1
            s.num = f"{prefix}.{n}"
            r, d = s.rec, s.rec.data
            gap = delta(prev, r.ts)
            when = f"{fmt_ts(r.ts)}" + (f" · +{fmt_secs(gap)}" if gap is not None else "")
            prev = r.ts or prev
            lineage = f"`{d.get('uuid', '—')}` ← `{d.get('parentUuid') or 'root'}`"
            side = " · sidechain" if d.get("isSidechain") else ""
            if s.kind in ("text", "tool", "thinking") or (s.kind == "unknown" and r.type == "assistant"):
                m = d.get("message") or {}
                meta = (f"- **API message:** `{m.get('id', '—')}` · **model:** `{m.get('model', '—')}` · "
                        f"**stop reason:** `{m.get('stop_reason')}` · **effort:** `{d.get('effort', '—')}`{side}")
                usage = self.usage.get(m.get("id")) if s.first_of_msg else None
            else:
                meta, usage = None, None
            if s.kind == "text":
                self.w(f"#### Step {s.num} · 💬 Agent text — {when}")
                self.w(meta)
                if usage:
                    self.w(f"- **Tokens for this model call:** {self.usage_line(usage)}")
                self.w(f"- **Lineage:** {lineage}")
                self.w()
                self.w(body("Text (verbatim)", s.block.get("text", ""), "markdown"))
            elif s.kind == "thinking":
                self.w(f"#### Step {s.num} · 🧠 Model thinking block ({s.block.get('type')}) — {when}")
                self.w(meta)
                self.w(f"- **Lineage:** {lineage}")
                self.w()
                self.w(body("Thinking (verbatim)", s.block.get("thinking") or s.block.get("data") or "", "text"))
            elif s.kind == "tool":
                self.render_tool(s, when, meta, usage, lineage)
            elif s.kind == "context":
                self.render_context(s, when, lineage)
            elif s.kind == "system":
                self.w(f"#### Step {s.num} · ⚙️ System record `{d.get('subtype', '')}` — {when}")
                self.w(f"- **Lineage:** {lineage}")
                self.w()
                self.w(body("Record (verbatim JSON)", pjson(self.deblob(d, s.num)), "json"))
            elif s.kind == "orphan_result":
                self.w(f"#### Step {s.num} · ⚠️ Tool result with no matching call in this scope — {when}")
                self.w(f"- **tool_use_id:** `{s.block.get('tool_use_id')}` · **Lineage:** {lineage}")
                txt, _ = self.content_text(s.block.get("content"), s.num)
                self.w()
                self.w(body("Result (verbatim)", txt))
            else:
                self.w(f"#### Step {s.num} · ❓ Unrecognised record/block `{r.type}` — {when}")
                self.w("Rendered raw so nothing is dropped.")
                self.w()
                self.w(body("Raw (verbatim JSON)", pjson(self.deblob(s.block or d, s.num)), "json"))
            if s.kind in ("text", "thinking", "tool") and d.get("isApiErrorMessage"):
                self.w(f"> ⚠️ **API error message** — status `{d.get('apiErrorStatus')}` "
                       f"transient=`{d.get('apiErrorIsTransient')}` error=`{d.get('error')}`")
            self.w()

    def render_tool(self, s: Step, when: str, meta: Optional[str], usage: Optional[dict], lineage: str) -> None:
        b = s.block or {}
        name, tid = b.get("name", "?"), b.get("id", "")
        self.w(f"#### Step {s.num} · 🔧 Tool call `{name}` — {when}")
        self.w(f"- **Call id:** `{tid}`")
        if meta:
            self.w(meta)
        if usage:
            self.w(f"- **Tokens for this model call:** {self.usage_line(usage)}")
        self.w(f"- **Lineage:** {lineage}")
        self.w()
        self.w(body("Input (verbatim JSON)", pjson(b.get("input")), "json"))
        self.w()
        if s.result is None:
            self.w("**Result:** ⚠️ no `tool_result` with this id was recorded "
                   "(turn interrupted, still running, or result lost).")
            return
        rr, rb = s.result
        lat = delta(s.rec.ts, rr.ts)
        txt, _ = self.content_text(rb.get("content"), tid)
        status = "❌ error" if rb.get("is_error") else "✅ ok"
        self.w(f"**Result:** {status} · returned {fmt_ts(rr.ts)} · latency {fmt_secs(lat)} · "
               f"{len(txt):,} chars · record `{rr.data.get('uuid')}`")
        self.w()
        self.w(body("Tool output as the model received it (verbatim)", txt))
        for m in sorted(set(re.findall(r"tool-results/([A-Za-z0-9_-][A-Za-z0-9._-]*\.[A-Za-z0-9]+)(?![A-Za-z0-9_-])", txt))):
            if m in self.tool_result_files:
                f, rel = self.tool_result_files[m]
                full = f.read_text(errors="replace")
                self.w()
                self.w(f"Full output persisted by the SDK → `{rel}`")
                self.w()
                self.w(body(f"Persisted tool output {m}", full, details=True))
        tur = rr.data.get("toolUseResult")
        if tur is not None:
            self.w()
            self.w(body("Structured tool result (toolUseResult, verbatim JSON)",
                        pjson(self.deblob(tur, tid)), "json", details=True))
        sub = self.subagents.get(tid)
        if sub and not sub.get("rendered"):
            self.render_subagent(sub, s.num, s.rec.ts, under_call=True)

    def render_subagent(self, sub: dict, num: str, ts: Optional[datetime], under_call: bool = False) -> None:
        m = sub["meta"]
        sub["rendered"] = "call" if under_call else "unlinked"
        self.w()
        self.w(f"#### ↳ Subagent of step {num}: `{m.get('agentType', '?')}` — {m.get('description', '')}")
        self.w(f"- **Transcript:** `raw/transcripts/{sub['label']}` · **spawn depth:** {m.get('spawnDepth', '—')} "
               f"· **records:** {len(sub['recs'])}")
        self.w()
        self.render_steps(sub["steps"], f"{num}", ts)
        self.w(f"#### ↲ End of subagent for step {num}")

    def render_context(self, s: Step, when: str, lineage: str) -> None:
        d = s.rec.data
        if s.rec.type == "attachment":
            a = d.get("attachment") or {}
            kind = a.get("type", "?")
            self.w(f"#### Step {s.num} · 🔔 Context injected into the model — attachment `{kind}` — {when}")
            extra = f" · from hook `{a.get('hookName')}` ({a.get('hookEvent')}) for tool `{a.get('toolUseID')}`" \
                if a.get("hookName") else ""
            self.w(f"- **Lineage:** {lineage}{extra}")
            self.w()
            self.w(body("Attachment (verbatim JSON)", pjson(self.deblob(a, s.num)), "json"))
        else:
            src = d.get("sourceToolUseID")
            why = (f"content returned by tool `{src}` (e.g. a loaded skill body)" if src
                   else "synthetic/meta message added by the runtime" if d.get("isMeta")
                   else "non-prompt user message")
            self.w(f"#### Step {s.num} · 🔔 Context injected into the model — {why} — {when}")
            self.w(f"- **isMeta:** `{d.get('isMeta')}` · **promptSource:** `{d.get('promptSource')}` · "
                   f"**Lineage:** {lineage}")
            self.w()
            if s.block is not None:
                self.w(body("Content block (verbatim JSON)", pjson(self.deblob(s.block, s.num)), "json"))
            else:
                txt, _ = self.content_text(content_of(d), s.num)
                self.w(body("Content (verbatim)", txt))

    def render_log_table(self, lines: list[LogLine]) -> None:
        if not lines:
            self.w("_No runtime log lines in this window._")
            return
        self.w("| Time (UTC) | Source | Level | Component | Message |")
        self.w("|---|---|---|---|---|")
        for ln in lines:
            self.w(f"| {fmt_ts(ln.ts)[:23]} | {ln.source} | {ln.level} | {cell(ln.component)} | {cell(ln.text)} |")

    def turn_tokens(self, steps: list[Step]) -> dict:
        tot: Counter = Counter()
        ids = set()

        def walk(ss: list[Step]) -> None:
            for s in ss:
                if s.rec.type == "assistant":
                    ids.add((s.rec.data.get("message") or {}).get("id"))
        walk(steps)
        for mid in ids:
            u = self.usage.get(mid) or {}
            for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"):
                tot[k] += u.get(k) or 0
        tot["model_calls"] = len(ids)
        return tot

    # ---------- main ----------
    def run(self) -> Path:
        self.load()
        pre, turns = self.segment()
        self.locate(turns)
        self.attach_logs(turns)
        pre_steps = self.build_steps(pre)
        for t in turns:
            self.rendered.add(t.prompt.key)
            t.steps = self.build_steps(t.records)
        # Subagents are parsed up front so coverage, token and tool totals include them.
        for sub in self.unique_subagents():
            sub["steps"] = self.build_steps(sub["recs"])
        self.link_subagents()
        self.render(pre_steps, turns)
        report, n = redact("\n".join(self.md).replace("{{SUBAGENT_STATUS}}", self.subagent_status()))
        report = report.replace("{{REPORT_REDACTIONS}}", str(n))
        (self.root / "TRACE_REPORT.md").write_text(report)
        rd, _ = redact(pjson(self.run_data(turns)))
        (self.root / f"run-data-{self.chat.name}.json").write_text(rd)
        (self.root / "raw" / "SOURCES.json").write_text(pjson(self.b.entries))
        lines = []
        for f in sorted(self.root.rglob("*")):
            if f.is_file() and f.name != "MANIFEST.sha256":
                lines.append(f"{sha256(f.read_bytes())}  {f.relative_to(self.root)}")
        (self.root / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
        return self.root

    def unique_subagents(self) -> list[dict]:
        return list({id(s): s for s in self.subagents.values()}.values())

    def link_subagents(self) -> None:
        """Link each subagent transcript to the tool call that spawned it.

        Newer SDKs write meta.toolUseId. Older ones (e.g. 2.1.141) do not, so fall back to
        the parent call's toolUseResult.agentId matching the file name agent-<agentId>.jsonl,
        then to an identical `description`."""
        by_agent = {}
        for sub in self.unique_subagents():
            m = re.search(r"agent-([A-Za-z0-9]+)\.jsonl$", sub["label"])
            if m:
                by_agent[m.group(1)] = sub
            if sub["meta"].get("toolUseId") in self.calls:
                sub["linked"] = sub["meta"]["toolUseId"]
                sub["link_how"] = "meta.toolUseId"
        for tid, s in self.calls.items():
            if tid in self.subagents or s.result is None:
                continue
            tur = s.result[0].data.get("toolUseResult")
            aid = tur.get("agentId") if isinstance(tur, dict) else None
            sub, how = (by_agent.get(aid), "toolUseResult.agentId") if aid else (None, "")
            if sub is None and (s.block or {}).get("name") in ("Agent", "Task"):
                desc = ((s.block or {}).get("input") or {}).get("description")
                sub = next((x for x in self.unique_subagents()
                            if not x.get("linked") and desc and x["meta"].get("description") == desc), None)
                how = "matching description"
            if sub is not None and not sub.get("linked"):
                self.subagents[tid] = sub
                sub["linked"], sub["link_how"] = tid, how

    def subagent_status(self) -> str:
        subs = self.unique_subagents()
        if not subs:
            return "none in this chat"
        under = [s for s in subs if s.get("rendered") == "call"]
        hows = Counter(s.get("link_how") for s in under)
        txt = (f"{len(under)} of {len(subs)} rendered under their spawning tool call"
               + (f" (linked by {', '.join(f'{k}×{v}' for k, v in hows.items())})" if under else ""))
        if len(under) < len(subs):
            txt += (f"; ⚠️ {len(subs) - len(under)} could not be linked and are rendered in "
                    f"“Subagents not linked to a tool call”")
        return txt

    def render(self, pre_steps: list[Step], turns: list[Turn]) -> None:
        c, meta = self.chat, self.meta
        all_ts = [r.ts for r in self.main if r.ts]
        start, end = (min(all_ts), max(all_ts)) if all_ts else (None, None)
        tools = Counter(s.block.get("name") for s in self.calls.values() if s.block)
        unmatched = [tid for tid, s in self.calls.items() if s.result is None]
        totals: Counter = Counter()
        for u in self.usage.values():
            for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"):
                totals[k] += u.get(k) or 0
        try:
            app_ver = plistlib.loads(APP_PLIST.read_bytes()).get("CFBundleShortVersionString")
        except (OSError, ValueError):
            app_ver = None
        fields = lambda key: sorted({str(r.data[key]) for r in self.main if r.data.get(key)})  # noqa: E731
        cids = sorted({r.cid for r in self.runs})
        with_runtime = [t.k for t in turns if t.run]

        w = self.w
        w(f"# DevRev Computer — session trace: `{c.don}`")
        w()
        w(f"_Generated {fmt_ts(datetime.now(UTC))} by `computer_trace.py export` from local files only "
          f"(no DevRev API calls). Every value below is copied from a source file listed in "
          f"[Appendix F](#appendix-f--evidence-files); nothing is summarised away._")
        w()
        w("## How a turn flows through the Computer (the six stages used below)")
        w()
        w(fence(
            "You type in Computer.app ─► DevRev timeline comment ─► Computer app AgentRunner ─► Claude Agent SDK ─► gateway model\n"
            "        A. input received            B. runtime preparation        C. context injected   D. reasoning ⇄ tool loop\n"
            "                                                                                                 │\n"
            "DevRev timeline reply ◄─ Computer app (final response) ◄─ E. final answer ◄────────────────────────┘\n"
            "        F. delivery", "text"))
        w()
        w("## 1. Session header")
        w()
        rows = [
            ("Chat (DevRev DON)", c.don),
            ("Agent session (DevRev)", meta.get("agentSessionId", "—")),
            ("SDK session id(s)", ", ".join(fields("sessionId")) or "—"),
            ("Identity", identity_label(c.identity_dir.name)),
            ("Agent id", self.agent_id or "— (not in surviving logs)"),
            ("Gateway model config", self.gateway or "— (not in surviving logs)"),
            ("Model(s) in transcript", ", ".join(f"{k} ({v} calls)" for k, v in self.models.items()) or "—"),
            ("Computer app version (installed at export time, not necessarily the one that ran the chat)",
             app_ver or "—"),
            ("Agent SDK version(s)", ", ".join(fields("version")) or "—"),
            ("Entrypoint / permission mode / effort",
             f"{', '.join(fields('entrypoint')) or '—'} / {', '.join(fields('permissionMode')) or '—'} / "
             f"{', '.join(fields('effort')) or '—'}"),
            ("Working directory", ", ".join(fields("cwd")) or "—"),
            ("Started → ended", f"{fmt_ts(start)} → {fmt_ts(end)} ({fmt_secs(delta(start, end))})"),
            ("Prompts (turns)", str(len(turns))),
            ("Execution location per turn", "; ".join(f"turn {t.k}: {t.location}" for t in turns) or "—"),
            ("Model calls (unique API messages)", f"{len(self.usage):,}"),
            ("Tokens (sum over unique API messages)",
             f"in {totals['input_tokens']:,} · out {totals['output_tokens']:,} · cache read "
             f"{totals['cache_read_input_tokens']:,} · cache write {totals['cache_creation_input_tokens']:,}"),
            ("Tool calls", f"{len(self.calls)} — " + ", ".join(f"{k}×{v}" for k, v in tools.most_common())),
            ("API error records", str(len(self.api_errors))),
        ]
        w("| Field | Value |")
        w("|---|---|")
        for k, v in rows:
            w(f"| {k} | {cell(v)} |")
        w()
        if self.meta_versions:
            w("**App-reported usage (`metadata.json`).** The app rewrites this file on every run, so each "
              "version covers one run only:")
            w()
            w("| Captured | Run created | Turns | Input tok | Output tok | Cost (USD) | Duration |")
            w("|---|---|---|---|---|---|---|")
            seen = set()
            for mv in self.meta_versions:
                u = mv["data"].get("usage") or {}
                key = (mv["data"].get("createdAt"), json.dumps(u, sort_keys=True))
                if key in seen:
                    continue
                seen.add(key)
                w(f"| {mv['captured_at']} | {mv['data'].get('createdAt', '—')} | {u.get('numTurns', '—')} | "
                  f"{u.get('inputTokens', '—')} | {u.get('outputTokens', '—')} | {u.get('totalCostUsd', '—')} | "
                  f"{fmt_secs((u.get('durationMs') or 0) / 1000) if u.get('durationMs') else '—'} |")
            w()

        w("## 2. Coverage and limits")
        w()
        total = sum(self.records_total.values())
        ok = "✅" if len(self.rendered) == total else "⚠️"
        w(f"- {ok} **Transcript records rendered:** {len(self.rendered):,} of {total:,} "
          f"(across {len(self.records_total)} file(s); {self.parse_errors} unparseable line(s), rendered raw).")
        w(f"- **Record types:** " + ", ".join(f"`{k}`×{v}" for k, v in
                                              Counter(r.type for r in self.main).most_common()))
        w(f"- **Content block types (assistant):** " + (", ".join(f"`{k}`×{v}" for k, v in self.block_types.most_common()) or "—"))
        w(f"- {'✅' if not self.unknown else '⚠️'} **Unrecognised types:** "
          + (", ".join(f"`{k}`×{v}" for k, v in self.unknown.items()) + " — rendered raw, not dropped"
             if self.unknown else "none"))
        w(f"- {'✅' if not unmatched else '⚠️'} **Tool calls paired with their result by `tool_use_id`:** "
          f"{len(self.calls) - len(unmatched)} of {len(self.calls)}"
          + (f" — unmatched: {', '.join(f'`{x}`' for x in unmatched)}" if unmatched else ""))
        w(f"- **Subagents:** {{{{SUBAGENT_STATUS}}}}")
        w(f"- **Model thinking blocks:** {self.thinking}. "
          + ("The model did **not** emit extended-thinking blocks in this session, so there is no hidden "
             "reasoning to show. The agent's reasoning is visible only as its own text between tool calls "
             "(💬 steps) and the inputs it chose for each tool (🔧 steps)." if not self.thinking
             else "Shown verbatim as 🧠 steps."))
        w("- **System prompt:** not stored in the transcript. The closest local evidence of the agent's "
          "instructions is the skill listing injected as context (🔔 steps), the agent settings and the "
          "skills inventory in [Appendix E](#appendix-e--agent-configuration-evidence).")
        w(f"- **Runtime logs used:** " + "; ".join(self.log_sources) + ".")
        verdict = "✅" if len(cids) == len(turns) and len(with_runtime) == len(turns) else "⚠️"
        w(f"- {verdict} **Turn count cross-check against DevRev:** {len(turns)} prompt(s) in the transcript "
          f"(rule: {self.prompt_rule}); {len(cids)} distinct DevRev `timeline_comment_id`(s) in the runtime logs; "
          f"turns with runtime evidence: {with_runtime or 'none'}.")
        if turns:
            w("  - Turn → DevRev comment mapping: " + "; ".join(
                f"turn {t.k} → `{t.run.cid.split(':')[-1]}`" if t.run else f"turn {t.k} → none"
                for t in turns))
        shared: dict[str, list[Turn]] = {}
        for t in turns:
            if t.run:
                shared.setdefault(t.run.cid, []).append(t)
        for cid, ts_ in shared.items():
            if len(ts_) > 1:
                texts = {" ".join((prompt_text(x.prompt.data) or "").split()) for x in ts_}
                same = "with **identical** prompt text" if len(texts) == 1 else "with different prompt text"
                w(f"  - Turns {', '.join(str(x.k) for x in ts_)} fall inside the same DevRev run "
                  f"`{cid.split(':')[-1]}` {same}. One DevRev message (or one long-lived run) fed several "
                  f"prompts to the agent, for example a retry or resume. The transcript records each delivery "
                  f"separately.")
        for t in turns:
            if not t.run:
                w(f"  - ⚠️ {self.missing_cause(t)} Stages B and F for this turn rely on app-log lines only. "
                  f"Stages A and C–E come from the transcript and are complete.")
        w(f"- **App-log lines mentioning this chat:** " +
          (", ".join(f"`{k}`: {v}" for k, v in self.app_log_hits.items() if v) or "none") + ".")
        w(f"- **Secret redaction:** {self.b.redactions} in raw copies, {{{{REPORT_REDACTIONS}}}} in this report "
          f"(Bearer tokens, JWTs, Authorization values, API keys, AWS pre-signed-URL credentials and "
          f"signatures). Redacted raw files keep the original's SHA-256 in Appendix F.")
        w("- **Timestamps** are UTC with local time in brackets. App logs record local time with no zone and "
          "were converted to UTC.")
        w()

        if pre_steps:
            w("## Session preamble (records before the first prompt)")
            w()
            self.render_steps(pre_steps, "0", start)

        for t in turns:
            self.render_turn(t)

        unlinked = [s for s in self.unique_subagents() if not s.get("rendered")]
        if unlinked:
            w("---")
            w()
            w("## Subagents not linked to a tool call")
            w()
            w("These subagent transcripts have no matching spawning tool call in the main transcript. They are "
              "rendered here so nothing is dropped.")
            w()
            for i, sub in enumerate(unlinked, 1):
                self.render_subagent(sub, f"U{i}", None)
                w()

        w("## Appendix A — Merged runtime timeline (all logs, sorted by time)")
        w()
        w(fence("\n".join(ln.render() for ln in self.logs) or "(no runtime log lines)", "text"))
        w()
        if self.unassigned_logs:
            w(f"_{len(self.unassigned_logs)} line(s) fall outside every turn window, mostly app-level activity "
              f"before the first captured run or with no timestamp. They are included above._")
            w()
        w("## Appendix B — Session-control records")
        w()
        w("| # | File:line | Type | Timestamp | Details |")
        w("|---|---|---|---|---|")
        for i, r in enumerate(self.control, 1):
            det = {k: v for k, v in r.data.items() if k not in ("type", "timestamp", "sessionId")}
            w(f"| {i} | {r.label}:{r.line} | `{r.type}` | {fmt_ts(r.ts)} | {cell(det)} |")
        w()
        w("## Appendix C — Task list, approvals, and metadata versions")
        w()
        for name in ("todos.json", "session-approvals.json", "metadata.json"):
            p = c.chat_dir / name
            if p.is_file():
                w(body(f"{name} (current)", p.read_text(errors="replace"), "json", details=True))
                w()
        if len(self.meta_versions) > 1:
            w(body("metadata.json — every version archived by watch",
                   pjson(self.meta_versions), "json", details=True))
            w()
        w("## Appendix D — Uploaded / working files (chat workdir)")
        w()
        if self.workdir_files:
            w("| Path | Bytes | SHA-256 |")
            w("|---|---|---|")
            for rel, size, h in self.workdir_files:
                w(f"| {cell(rel)} | {size:,} | `{h}` |")
            w()
            w("Contents are " + ("copied to `raw/workdir/`." if self.include_workdir else
                                 "**not** copied (use `--include-workdir`). The hashes identify each file exactly."))
        else:
            w("_No files in the workdir._")
        w()
        w("## Appendix E — Agent configuration evidence")
        w()
        w(f"- Agent settings: `{self.config_rel or 'not found'}`")
        if self.skills:
            w()
            w("| Skill file (under agent/skills) | Bytes | SHA-256 |")
            w("|---|---|---|")
            for rel, size, h in self.skills:
                w(f"| {cell(rel)} | {size:,} | `{h}` |")
        w()
        w("## Appendix F — Evidence files")
        w()
        w("Each file under `raw/` is a byte-for-byte copy of its source, unless the Redactions column is "
          "non-zero; then the original's hash is listed too. `MANIFEST.sha256` covers every file in the "
          "bundle. Run `shasum -a 256 -c MANIFEST.sha256` in the bundle folder to verify.")
        w()
        w("| Bundle path | Source | Bytes | SHA-256 | Redactions | Original SHA-256 |")
        w("|---|---|---|---|---|---|")
        for e in self.b.entries:
            w(f"| `{e['path']}` | {cell(e['source'])} | {e['bytes']:,} | `{e['sha256'][:16]}…` | "
              f"{e['redactions']} | {('`' + e['original_sha256'][:16] + '…`') if e['original_sha256'] else '—'} |")
        w()

    def render_turn(self, t: Turn) -> None:
        w = self.w
        p = t.prompt
        steps = t.steps
        asst = [s for s in steps if s.rec.type == "assistant"]
        first_ai = asst[0].rec.ts if asst else None
        last_ts = max([s.rec.ts for s in steps if s.rec.ts] +
                      [s.result[0].ts for s in steps if s.result and s.result[0].ts] + ([p.ts] if p.ts else []),
                      default=None)
        finals = [s for s in steps if s.kind == "text" and not s.rec.data.get("isSidechain")]
        final = finals[-1] if finals else None
        tok = self.turn_tokens(steps)
        w("---")
        w()
        prompt_txt, _ = self.content_text(content_of(p.data), f"turn{t.k}_prompt")
        w(f"## Turn {t.k} — “{' '.join(prompt_txt.split())[:80]}”")
        w()
        w(f"- **Prompt time:** {fmt_ts(p.ts)} · **last activity:** {fmt_ts(last_ts)} · "
          f"**turn duration:** {fmt_secs(delta(p.ts, last_ts))}")
        w(f"- **Execution location:** {'🖥️ ' if t.location == 'local' else '☁️ ' if t.location == 'remote' else ''}"
          f"{t.location_detail or 'unknown (no cwd on records)'}")
        w(f"- **Model calls:** {tok['model_calls']} · **tokens:** in {tok['input_tokens']:,} · out "
          f"{tok['output_tokens']:,} · cache read {tok['cache_read_input_tokens']:,} · cache write "
          f"{tok['cache_creation_input_tokens']:,}")
        w(f"- **Tool calls:** {sum(1 for s in steps if s.kind == 'tool')} · **steps:** {len(steps)}")
        w()
        w("### A. Input received")
        w()
        w(f"- **DevRev timeline comment:** `{t.run.cid if t.run else '— (run not captured)'}`")
        w(f"- **Transcript record:** `{p.label}:{p.line}` · uuid `{p.data.get('uuid')}` · promptId "
          f"`{p.data.get('promptId')}` · promptSource `{p.data.get('promptSource')}`")
        q = [r for r in self.control if r.type == "queue-operation" and r.ts and p.ts
             and timedelta(0) <= p.ts - r.ts <= timedelta(seconds=30)]
        if q:
            w("- **Queue:** " + ", ".join(f"{r.data.get('operation')} at {fmt_ts(r.ts)}" for r in q))
        w()
        w(body("Prompt as delivered to the agent (verbatim)", prompt_txt, "markdown"))
        w()
        pre_lines = [ln for ln in t.logs if ln.ts and first_ai and ln.ts < first_ai] if first_ai else list(t.logs)
        post_lines = [ln for ln in t.logs if ln.ts and last_ts and ln.ts > last_ts]
        taken = {id(x) for x in pre_lines} | {id(x) for x in post_lines}
        mid_lines = [ln for ln in t.logs if id(ln) not in taken]
        w("### B. Runtime preparation (Computer app → SDK)")
        w()
        if t.run:
            w(f"Run `{t.run.cid}`: {fmt_ts(t.run.start)} → {fmt_ts(t.run.end)}")
            w()
            self.render_log_table(pre_lines)
        else:
            w(f"_{self.missing_cause(t)}_")
            if pre_lines:
                w()
                w("App-log lines in this window:")
                w()
                self.render_log_table(pre_lines)
        w()
        ctx_steps = []
        for s in steps:
            if s.rec.type == "assistant":
                break
            ctx_steps.append(s)
        w("### C. Context injected into the model before its first response")
        w()
        if ctx_steps:
            self.render_steps(ctx_steps, f"{t.k}.C", p.ts)
        else:
            w("_None recorded._")
            w()
        rest = steps[len(ctx_steps):]
        w("### D. Reasoning ⇄ tool loop")
        w()
        w("Numbered steps in time order. 💬 is the agent's own text, which is its visible reasoning. 🔧 is a "
          "tool call with its full input and output. 🔔 is context the runtime injected. The +Δ figure is "
          "the time since the previous step.")
        w()
        self.render_steps(rest, str(t.k), ctx_steps[-1].rec.ts if ctx_steps else p.ts)
        if mid_lines:
            w("<details><summary>Runtime log lines during the loop — "
              f"{len(mid_lines)} lines</summary>\n")
            self.render_log_table(mid_lines)
            w("\n</details>")
            w()
        w("### E. Output (final answer of this turn)")
        w()
        if final:
            w(f"From step {final.num} at {fmt_ts(final.rec.ts)}:")
            w()
            w(body("Final answer (verbatim)", final.block.get("text", ""), "markdown", details=False))
        else:
            w("_The turn ended without a text reply (interrupted, or it ended on a tool call)._")
        w()
        w("### F. Delivery (app → DevRev)")
        w()
        if t.run and t.run.replies:
            w("- **Reply posted to the DevRev timeline as:** " + ", ".join(f"`{x}`" for x in t.run.replies))
        if post_lines:
            self.render_log_table(post_lines)
        elif not (t.run and t.run.replies):
            w("_No delivery log lines captured for this turn._")
        w()

    # ---------- agent-evals run-data ----------
    def run_data(self, turns: list[Turn]) -> dict:
        def iso(dt: Optional[datetime]) -> Optional[str]:
            return dt.isoformat() if dt else None

        out = []
        for t in turns:
            txt, _ = self.content_text(content_of(t.prompt.data), f"turn{t.k}")
            out.append({"type": "user_message", "user_message": {"text": txt}, "created_at": iso(t.prompt.ts)})
            flat: list[Step] = []

            def collect(ss: list[Step]) -> None:
                # Subagent tool calls are flattened in after their spawning call, like
                # agent-evals' convert_traces.py does, so metrics see every tool call.
                for s in ss:
                    flat.append(s)
                    if s.kind == "tool" and s.block and s.block.get("id") in self.subagents:
                        collect(self.subagents[s.block["id"]].get("steps", []))
            collect(t.steps)
            texts = [s for s in t.steps if s.kind == "text" and not s.rec.data.get("isSidechain")]
            final = texts[-1] if texts else None
            thinking = []
            for s in flat:
                if s.kind == "text" and s is not final:
                    thinking.append({"text": s.block.get("text", ""), "first_token_timestamp": iso(s.rec.ts)})
                elif s.kind == "tool":
                    b = s.block
                    out.append({"type": "skill_triggered", "skill_triggered": {
                        "skill_name": b.get("name", ""), "skill_call_id": b.get("id", ""),
                        "args": b.get("input") if isinstance(b.get("input"), dict) else {"input": b.get("input")}},
                        "created_at": iso(s.rec.ts)})
                    if s.result:
                        rr, rb = s.result
                        rtxt, _ = self.content_text(rb.get("content"), b.get("id", ""))
                        out.append({"type": "skill_executed", "skill_executed": {
                            "skill_name": b.get("name", ""), "skill_call_id": b.get("id", ""),
                            "output": {"result": rtxt}, "metadata": {"is_error": bool(rb.get("is_error"))}},
                            "created_at": iso(rr.ts)})
            if final:
                out.append({"type": "ai_message", "ai_message": {
                    "text": final.block.get("text", ""),
                    "metadata": {"first_token_timestamp": iso(final.rec.ts), "thinking_messages": thinking}},
                    "created_at": iso(final.rec.ts)})
        user = ID_RX.match(self.chat.identity_dir.name)
        return {"sessions": [{"original_session_id": self.chat.don, "turns": out,
                              "metadata": {"session_id": self.chat.don,
                                           "user_id": user.group(3) if user else self.chat.identity_dir.name,
                                           "agent_id": self.agent_id},
                              "props": {}}],
                "dataset_path": f"computer_trace:{self.chat.name}"}


def cmd_export(a: argparse.Namespace) -> None:
    chat = latest_chat() if a.latest else resolve_chat(a.chat) if a.chat else None
    if chat is None:
        sys.exit("ERROR: give a chat id or --latest")
    age = time.time() - chat.last_activity()
    if age < 15:
        print(f"WARNING: transcript changed {age:.0f}s ago — the session may still be running.", file=sys.stderr)
    out_root = Path(a.out) if a.out else HERE / "exports"
    out_root.mkdir(parents=True, exist_ok=True)
    root = Exporter(chat, out_root, Path(a.runs) if a.runs else None, a.include_workdir).run()
    print(f"Exported {chat.name} ({identity_label(chat.identity_dir.name)})")
    print(f"  report   : {root / 'TRACE_REPORT.md'}")
    print(f"  bundle   : {root}")
    print(f"  verify   : cd '{root}' && shasum -a 256 -c MANIFEST.sha256")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=f"computer_trace.py {__version__}")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("list", help="list recent chats")
    p.add_argument("--limit", type=int, default=15)
    p.add_argument("--include-background", action="store_true")
    p.set_defaults(fn=cmd_list)
    p = sp.add_parser("watch", help="archive per-run files of a chat while a session runs")
    p.add_argument("--chat", help="existing chat id (default: wait for a NEW chat)")
    p.add_argument("--out", help="archive folder (default: watch/<timestamp> next to this script)")
    p.add_argument("--interval", type=float, default=1.0)
    p.add_argument("--idle-stop", type=float, default=0, help="stop after N idle seconds (0 = never)")
    p.set_defaults(fn=cmd_watch)
    p = sp.add_parser("export", help="build the traceability bundle")
    p.add_argument("chat", nargs="?", help="chat folder name, suffix (e.g. AbCd1234) or DON")
    p.add_argument("--latest", action="store_true", help="most recently active chat")
    p.add_argument("--runs", help="folder written by `watch` for this chat")
    p.add_argument("--out", help="output root (default: exports/ next to this script)")
    p.add_argument("--include-workdir", action="store_true", help="also copy uploaded/working files")
    p.set_defaults(fn=cmd_export)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
