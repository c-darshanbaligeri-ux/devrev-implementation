#!/usr/bin/env python3
"""Build the machine-readable index that `bin/devrev-find` searches. Standard library only.

    python3 -I scripts/build_index.py            # (re)write index/endpoints.json, playbooks.json, learnings.json
    python3 -I scripts/build_index.py --check    # exit 1 if the committed index is stale (used by tests)

Inputs  : the generated developer-docs mirror (skills/11-developer-docs/{,beta/}api-reference/*.md), the catalog
          skills/8-devrev-api/references/00_API_Catalog.md, every skills/*/SKILL.md, docs/LEARNINGS.md and the
          hand-written index/synonyms.json.
Outputs : index/endpoints.json   one record per endpoint name: methods, public/beta, scopes, required fields,
                                  risk, doc anchor, catalog row, repo notes (file + line + snippet)
          index/playbooks.json   one record per skill: id, name, description, headings, "when to use" bullets
          index/learnings.json   one record per journal row / standing note, keyed to the endpoints it mentions

Line numbers in `notes` / `learnings` are as of generation; they drift as docs are edited (each record also carries
a snippet, so a grep always finds the place). `--check` only tracks the inputs that define *what exists*.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import devrev_risk  # noqa: E402

MIRROR = "skills/11-developer-docs"
MIRROR_GENERATED = ("api-reference", "beta", "airsync", "snapin-development", "sdks", "guides", "about", "changelog")
CATALOG = "skills/8-devrev-api/references/00_API_Catalog.md"
HDR = re.compile(r"^## `([A-Z]+) /(\S+)`\s*$")
ANCHOR = re.compile(r'^<a id="([^"]+)"></a>\s*$')
SCOPE_TOKEN = re.compile(r"`([a-z][a-z_]*:[a-z]+)`")
ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*(yes|no|)\s*\|")
NAME_RE = re.compile(r"\b([a-z][a-z0-9-]*(?:\.[a-z0-9-]+)+)\b")
PARAM_SECTIONS = ("request body", "query parameters", "path parameters", "header parameters")


def is_generated_mirror(rel: str) -> bool:
    if rel in (f"{MIRROR}/INDEX.md", f"{MIRROR}/COVERAGE.md"):
        return True
    return rel.startswith(MIRROR + "/") and rel[len(MIRROR) + 1:].split("/")[0] in MIRROR_GENERATED


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


# --------------------------------------------------------------------------- endpoints
def parse_resource_file(path: Path, channel: str):
    rel = path.relative_to(ROOT).as_posix()
    recs, cur, anchor, section, in_scopes, desc_open = [], None, None, "", False, False
    for i, line in enumerate(read(path).split("\n"), 1):
        m = ANCHOR.match(line)
        if m:
            if cur:
                recs.append(cur)
                cur = None
            anchor = m.group(1)
            continue
        m = HDR.match(line)
        if m:
            if cur:
                recs.append(cur)
            name = devrev_risk.normalize(m.group(2))
            cur = {"name": name, "method": m.group(1), "channel": channel, "doc": f"{rel}#{anchor}" if anchor else rel,
                   "title": "", "desc": [], "scopes": [], "scopes_text": "", "required": [], "fields": [], "variants": False}
            section, in_scopes, desc_open = "head", False, True
            continue
        if cur is None:
            continue
        if line.startswith("**Required scopes:**"):
            in_scopes, desc_open = True, False
            rest = line[len("**Required scopes:**"):].strip()
            cur["scopes_text"] = re.sub(r"\s+", " ", SCOPE_TOKEN.sub("", rest).replace("`", "")).strip(" :")[:160]
            cur["scopes"] += SCOPE_TOKEN.findall(rest)
            continue
        if line.startswith("### ") or line.startswith("#### "):
            in_scopes, desc_open = False, False
            if line.startswith("#### Variant"):
                cur["variants"] = True  # variant tables belong to the parameter section they sit under
                continue
            section = line.lstrip("# ").strip().lower()
            continue
        if section == "head":
            if not cur["title"] and re.match(r"^\*\*(.+)\*\*$", line) and not line.startswith("**Required"):
                cur["title"] = line.strip("*").strip()
            elif desc_open and line.strip() and not line.startswith("Source:") and not line.startswith("**"):
                cur["desc"].append(line.strip())
            if in_scopes:
                cur["scopes"] += SCOPE_TOKEN.findall(line)
            continue
        if any(section.startswith(s) for s in PARAM_SECTIONS):
            rm = ROW.match(line)
            if rm:
                fname, req = rm.group(1), rm.group(2)
                if fname not in cur["fields"]:
                    cur["fields"].append(fname)
                if req == "yes" and fname not in cur["required"]:
                    cur["required"].append(fname)
    if cur:
        recs.append(cur)
    # scopes can also sit in the table that follows "Depends on the object type": collect from the head block
    return recs


def first_sentence(parts, limit=240):
    text = re.sub(r"\s+", " ", " ".join(parts)).strip()
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)  # keep link text, drop the URL
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    return (m.group(1) if m else text)[:limit]


def parse_catalog():
    cat, last = {}, None
    for n, line in enumerate(read(ROOT / CATALOG).split("\n"), 1):
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        last = None
        for tok in re.findall(r"`([^`]+)`", cells[0]):
            tok = tok.strip()
            if re.fullmatch(r"[a-z][a-z0-9-]*(?:\.[a-z0-9-]+)+|ping", tok):
                name, last = tok, tok
            elif last and re.fullmatch(r"(?:\.[a-z0-9-]+)+", tok):
                name = last.rsplit(".", 1)[0] + tok
            else:
                continue
            cat[name] = {"line": n, "row": re.sub(r"\s+", " ", " | ".join(cells))[:240]}
    return cat


def scan_notes(known):
    """Where the repo's own (non-mirror) docs mention each endpoint: up to 8 refs, at most 2 per file."""
    refs = {n: [] for n in known}
    for p in sorted((ROOT / "skills").rglob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        if is_generated_mirror(rel) or rel == CATALOG:
            continue
        for i, line in enumerate(read(p).split("\n"), 1):
            for m in NAME_RE.finditer(line):
                n = m.group(1)
                r = refs.get(n)
                if r is not None and len(r) < 8 and sum(1 for x in r if x["file"] == rel) < 2:
                    r.append({"file": rel, "line": i, "snippet": line.strip()[:110]})
    return refs


def build_endpoints():
    by_name = {}
    for channel, base in (("public", ROOT / MIRROR / "api-reference"), ("beta", ROOT / MIRROR / "beta" / "api-reference")):
        for p in sorted(base.glob("*.md")):
            if p.name == "getting-started.md":
                continue
            for rec in parse_resource_file(p, channel):
                by_name.setdefault(rec["name"], []).append(rec)
    catalog = parse_catalog()
    refs = scan_notes(set(by_name) | set(catalog))
    out = []
    for name in sorted(by_name):
        recs = by_name[name]
        recs_sorted = sorted(recs, key=lambda r: (r["channel"] != "public", r["method"] != "POST"))
        prim = recs_sorted[0]
        channels = sorted({r["channel"] for r in recs}, reverse=True)  # public before beta
        scopes = []
        for r in recs:
            for s in r["scopes"]:
                if s not in scopes:
                    scopes.append(s)
        rec = {
            "name": name,
            "resource": name.split(".")[0],
            "methods": sorted({r["method"] for r in recs}),
            "channels": channels,
            "title": prim["title"],
            "summary": first_sentence(prim["desc"]),
            "scopes": scopes,
            "scopes_text": prim["scopes_text"],
            "required": prim["required"],
            "fields": prim["fields"][:80],
            "has_variants": any(r["variants"] for r in recs),
            "risk": devrev_risk.classify(name),
            "doc": next((r["doc"] for r in recs_sorted if r["channel"] == "public"), prim["doc"]),
            "beta_doc": next((r["doc"] for r in recs_sorted if r["channel"] == "beta"), None) if "public" in channels else None,
            "catalog": catalog.get(name),
            "notes": refs.get(name, []),
        }
        out.append(rec)
    # catalog-only names (internal / undocumented on the public site) are still real endpoints for this repo
    for name in sorted(set(catalog) - set(by_name)):
        out.append({"name": name, "resource": name.split(".")[0], "methods": [], "channels": [], "title": "", "summary": "",
                    "scopes": [], "scopes_text": "", "required": [], "fields": [], "has_variants": False,
                    "risk": devrev_risk.classify(name), "doc": None, "beta_doc": None, "catalog": catalog[name],
                    "notes": refs.get(name, [])})
    return out


# --------------------------------------------------------------------------- playbooks
def parse_frontmatter(text):
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if not m:
        return fm, text
    lines = m.group(1).split("\n")
    i = 0
    while i < len(lines):
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", lines[i])
        if km:
            key, val = km.group(1), km.group(2).strip()
            if val in (">", "|", ">-", "|-", ">+", "|+"):
                chunk = []
                i += 1
                while i < len(lines) and (lines[i].startswith(" ") or not lines[i].strip()):
                    chunk.append(lines[i].strip())
                    i += 1
                fm[key] = " ".join(c for c in chunk if c)
                continue
            fm[key] = val.strip("\"'")
        i += 1
    return fm, text[m.end():]


def build_playbooks():
    out = []
    for p in sorted((ROOT / "skills").glob("*/SKILL.md")):
        fm, body = parse_frontmatter(read(p))
        lines = body.split("\n")
        headings = [l.lstrip("# ").strip() for l in lines if l.startswith(("## ", "### "))][:50]
        when, grab = [], False
        for l in lines:
            if l.startswith("## When to use"):
                grab = True
                continue
            if grab and l.startswith("## "):
                break
            if grab and l.lstrip().startswith("- "):
                when.append(re.sub(r"\s+", " ", l.strip()[2:])[:220])
        out.append({"id": p.parent.name, "name": fm.get("name", p.parent.name),
                    "description": re.sub(r"\s+", " ", fm.get("description", "")).strip(),
                    "headings": headings, "when_to_use": when[:12], "path": p.relative_to(ROOT).as_posix(),
                    "lines": len(lines)})
    return out


# --------------------------------------------------------------------------- learnings
def build_learnings(known):
    p = ROOT / "docs" / "LEARNINGS.md"
    if not p.exists():
        return []
    rows = []
    for i, line in enumerate(read(p).split("\n"), 1):
        m = re.match(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|(.*)\|\s*$", line)
        kind = "row"
        files = ""
        if m:
            date, rest = m.group(1), m.group(2).strip()
            cells = re.split(r"\s\|\s", rest, maxsplit=2)
            text = " ".join(cells[:2])
            files = cells[2] if len(cells) > 2 else ""
        else:
            m = re.match(r"^- \*\*(\d{4}-\d{2}-\d{2})\b(.*)$", line)
            if not m:
                continue
            date, text, kind = m.group(1), m.group(2), "standing"
        text = re.sub(r"\s+", " ", text).strip()
        rows.append({"line": i, "date": date, "kind": kind, "text": text[:700],
                     "endpoints": sorted({n for n in NAME_RE.findall(text) if n in known}), "files": files[:200]})
    return rows


# --------------------------------------------------------------------------- freshness
def core_hash():
    """Hash of the inputs that define *what exists* (not of line numbers)."""
    h = hashlib.sha256()
    files = []
    for base in ("api-reference", "beta/api-reference"):
        files += sorted((ROOT / MIRROR / base).glob("*.md"))
    files += [ROOT / CATALOG] + sorted((ROOT / "skills").glob("*/SKILL.md")) + [ROOT / "index" / "synonyms.json"]
    for p in files:
        if p.exists():
            h.update(p.relative_to(ROOT).as_posix().encode())
            h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()[:16]


def dump(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="exit 1 if the committed index is stale")
    args = ap.parse_args()
    h = core_hash()
    idx = ROOT / "index" / "endpoints.json"
    if args.check:
        if not idx.exists():
            print("index/endpoints.json is missing; run scripts/build_index.py")
            return 1
        cur = json.loads(idx.read_text(encoding="utf-8")).get("meta", {}).get("core_hash")
        if cur != h:
            print(f"index is stale (committed {cur}, sources {h}); run: python3 -I scripts/build_index.py")
            return 1
        print(f"index is current ({h})")
        return 0
    endpoints = build_endpoints()
    known = {e["name"] for e in endpoints}
    dump(idx, {"meta": {"core_hash": h, "count": len(endpoints)}, "endpoints": endpoints})
    playbooks = build_playbooks()
    dump(ROOT / "index" / "playbooks.json", {"meta": {"count": len(playbooks)}, "playbooks": playbooks})
    learnings = build_learnings(known)
    dump(ROOT / "index" / "learnings.json", {"meta": {"count": len(learnings)}, "learnings": learnings})
    risk = {r: sum(1 for e in endpoints if e["risk"] == r) for r in ("read", "write", "destructive")}
    print(f"endpoints={len(endpoints)} (risk {risk}) playbooks={len(playbooks)} learnings={len(learnings)} core_hash={h}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
