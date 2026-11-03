#!/usr/bin/env python3
"""Build the machine-readable index that `bin/devrev-find` searches. Standard library only.

    python3 -I scripts/build_index.py            # (re)write index/endpoints.json, playbooks.json, learnings.json, operations.json
    python3 -I scripts/build_index.py --check    # exit 1 if the committed index is stale (used by tests)

Inputs  : the generated developer-docs mirror (skills/11-developer-docs/{,beta/}api-reference/*.md), the catalog
          skills/8-devrev-api/references/00_API_Catalog.md, the internal workflow-API table in
          skills/6-workflows/references/manage-workflows-api.md, the workflow operations catalog
          (skills/6-workflows/operations/*.md, schemas/*.md, examples/*.json), every skills/*/SKILL.md,
          docs/LEARNINGS.md and the hand-written index/synonyms.json.
Outputs : index/endpoints.json   one record per endpoint name: methods, public/beta, scopes, required fields,
                                  risk, doc anchor, catalog row, repo notes (file + line + snippet)
          index/playbooks.json   one record per skill: id, name, description, headings, "when to use" bullets
          index/learnings.json   one record per journal row / standing note, keyed to the endpoints it mentions
          index/operations.json  one record per workflow operation (trigger / action / control / blocking): slug,
                                  namespace, tags, scopes, port fields, schema file, example templates that use it

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
WF_API = "skills/6-workflows/references/manage-workflows-api.md"
OPS_DIR = "skills/6-workflows/operations"
EXAMPLES_DIR = "skills/6-workflows/examples"
OP_KINDS = (("trigger", "triggers.md"), ("action", "actions.md"), ("control", "controls.md"), ("blocking", "blockings.md"))
OP_HDR = re.compile(r"^## (\d+)\. (.+?)\s*$")
OP_META = re.compile(r"^- \*\*(Slug|Namespace|ID|Tags|Scopes):\*\*\s*(.*?)\s*$")
OP_PORT = re.compile(r"^### (Input|Output) \(`([^`]+)`\)")
OP_INLINE = re.compile(r"^- `([^`]+)` \(([^)]*)\)( \*\*\(required\)\*\*)?")
SCHEMA_PORT = re.compile(r"^## (Input|Output) Port: `([^`]+)`")
SCHEMA_FIELD = re.compile(r"^- \*\*`([^`]+)`\*\* \(`([^`]+)`\)( \*\*REQUIRED\*\*)?")


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
    internal = parse_internal_workflow_api()
    refs = scan_notes(set(by_name) | set(catalog) | set(internal))
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
    for name in sorted(set(catalog) - set(by_name) - set(internal)):
        out.append({"name": name, "resource": name.split(".")[0], "methods": [], "channels": [], "title": "", "summary": "",
                    "scopes": [], "scopes_text": "", "required": [], "fields": [], "has_variants": False,
                    "risk": devrev_risk.classify(name), "doc": None, "beta_doc": None, "catalog": catalog[name],
                    "notes": refs.get(name, [])})
    # internal workflow routes (documented only in this repo's skill 6): a name the public mirror already has keeps its
    # public record
    for name in sorted(set(internal) - set(by_name)):
        r = internal[name]
        out.append({"name": name, "resource": name.split(".")[0], "methods": [r["method"]], "channels": ["internal"],
                    "title": "", "summary": r["summary"], "scopes": r["scopes"], "scopes_text": "", "required": [],
                    "fields": [], "has_variants": False, "risk": devrev_risk.classify(name),
                    "doc": WF_API, "beta_doc": None, "catalog": catalog.get(name),
                    "internal_path": r["path"], "purpose": r["purpose"], "notes": refs.get(name, [])})
    return out


# --------------------------------------------------------------------------- internal workflow API
def parse_internal_workflow_api():
    """The "Endpoints" table of manage-workflows-api.md: workflow routes that the public docs mirror does not cover."""
    out, in_section = {}, False
    for line in read(ROOT / WF_API).split("\n"):
        if line.startswith("## "):
            in_section = line.strip() == "## Endpoints"
            continue
        m = re.match(r"^\| (.+?) \| (GET|POST) \| (.+?) \| (.*) \|\s*$", line) if in_section else None
        if not m:
            continue
        names = re.findall(r"`([a-z][a-z0-9-]*(?:\.[a-z0-9-]+)+)`", m.group(1))
        paths = re.findall(r"`(/[^`]+)`", m.group(3))
        purpose = re.sub(r"\s+", " ", m.group(4)).strip()
        plain = re.sub(r"\*\*", "", purpose).replace("`", "")
        for i, name in enumerate(names):
            name = devrev_risk.normalize(name)
            path = paths[i] if len(paths) == len(names) else (paths[0] if paths else "")
            out[name] = {"method": m.group(2), "path": path, "purpose": purpose[:900],
                         "summary": first_sentence([plain]), "scopes": SCOPE_TOKEN.findall(purpose)}
    return out


# --------------------------------------------------------------------------- workflow operations
def anchor_of(num, title):
    return re.sub(r"[^a-z0-9 _-]", "", f"{num}. {title}".lower()).replace(" ", "-")


def parse_operation_lists():
    ops = []
    for kind, fname in OP_KINDS:
        path = ROOT / OPS_DIR / fname
        rel = path.relative_to(ROOT).as_posix()
        cur, port = None, None
        for i, line in enumerate(read(path).split("\n"), 1):
            m = OP_HDR.match(line)
            if m:
                if cur:
                    ops.append(cur)
                cur = {"kind": kind, "title": m.group(2), "line": i, "doc": f"{rel}#{anchor_of(m.group(1), m.group(2))}",
                       "slug": "", "namespace": "", "id": "", "tags": [], "scopes": [], "desc": "", "inline": {"in": {}, "out": {}}}
                port = None
                continue
            if cur is None:
                continue
            mm = OP_META.match(line)
            if mm:
                key, val = mm.group(1), mm.group(2)
                if key == "Slug":
                    cur["slug"] = val.strip("`")
                elif key == "Namespace":
                    cur["namespace"] = val.strip("`")
                elif key == "ID":
                    cur["id"] = val.strip("`")
                elif key == "Tags":
                    cur["tags"] = [t.strip() for t in val.split(",") if t.strip()]
                elif key == "Scopes":
                    cur["scopes"] = SCOPE_TOKEN.findall(val)
                continue
            pm = OP_PORT.match(line)
            if pm:
                port = ("in" if pm.group(1) == "Input" else "out", pm.group(2))
                cur["inline"][port[0]].setdefault(port[1], [])
                continue
            if line.startswith("### ") or line.startswith("## ") or line.strip() == "---":
                port = None
                continue
            if port:
                fm = OP_INLINE.match(line)
                if fm:
                    cur["inline"][port[0]][port[1]].append(f"{fm.group(1)}:{fm.group(2)}{'*' if fm.group(3) else ''}")
            elif not cur["desc"] and line.strip() and not line.startswith(("-", ">", "|")):
                cur["desc"] = re.sub(r"\s+", " ", line.strip())[:300]
        if cur:
            ops.append(cur)
    return ops


def parse_schema(path: Path):
    """Top-level port fields of operations/schemas/<slug>.md, as 'name:type' ('*' marks required)."""
    ports, desc, port, title_seen = {"in": {}, "out": {}}, "", None, False
    for line in read(path).split("\n"):
        if line.startswith("# ") and not title_seen:
            title_seen = True
            continue
        pm = SCHEMA_PORT.match(line)
        if pm:
            port = ("in" if pm.group(1) == "Input" else "out", pm.group(2))
            ports[port[0]].setdefault(port[1], [])
            continue
        if line.startswith("## "):
            port = None
            continue
        if port:
            fm = SCHEMA_FIELD.match(line)
            if fm:
                ports[port[0]][port[1]].append(f"{fm.group(1)}:{fm.group(2)}{'*' if fm.group(3) else ''}")
        elif title_seen and not desc and line.strip() and not line.startswith(("#", "-", ">", "|", "<!--")):
            desc = re.sub(r"\s+", " ", line.strip())[:300]
    return ports, desc


def example_usage():
    """slug -> (example template files (basename) whose steps run that operation, input field names they set).

    The field names matter: the port schemas in operations/schemas/ lag the product (ask_ai's `model` and
    `output_format` are absent there but appear in templates that imported fine), so the template validator accepts
    any field an example template already uses.
    """
    use, seen = {}, {}
    for p in sorted((ROOT / EXAMPLES_DIR).glob("*.json")):
        try:
            d = json.loads(read(p))
            inner = json.loads(d["data"]) if isinstance(d.get("data"), str) else d
        except (ValueError, AttributeError):
            continue
        for st in inner.get("steps", []) if isinstance(inner, dict) else []:
            op = st.get("operation") if isinstance(st, dict) else None
            if isinstance(op, dict) and op.get("slug"):
                if p.name not in use.setdefault(op["slug"], []):
                    use[op["slug"]].append(p.name)
                names = seen.setdefault(op["slug"], set())
                for iv in st.get("input_values") or []:
                    for f in (iv.get("fields") or []) if isinstance(iv, dict) else []:
                        if isinstance(f, dict) and isinstance(f.get("name"), str):
                            names.add(f["name"])
    return use, {k: sorted(v) for k, v in seen.items()}


def build_operations():
    used, seen_fields = example_usage()
    schemas = {p.stem: p for p in sorted((ROOT / OPS_DIR / "schemas").glob("*.md"))}
    out, seen = [], set()
    for o in parse_operation_lists():
        slug = o["slug"]
        if not slug or slug in seen:
            continue
        seen.add(slug)
        sp = schemas.get(slug)
        ports = o.pop("inline")
        src = "catalog"
        if sp:
            sports, sdesc = parse_schema(sp)
            if sports["in"] or sports["out"]:
                ports, src = sports, "schema"
            o["desc"] = o["desc"] or sdesc
        o.update({"ports": ports, "ports_source": src,
                  "schema": sp.relative_to(ROOT).as_posix() if sp else None, "examples": used.get(slug, []),
                  "seen_fields": seen_fields.get(slug, [])})
        out.append(o)
    # schemas for operations the four lists do not carry (workflow-node / agent-skill extras) are still real slugs
    for slug, sp in schemas.items():
        if slug in seen:
            continue
        ports, desc = parse_schema(sp)
        out.append({"kind": "other", "title": slug.replace("_", " ").title(), "line": 1,
                    "doc": f"{OPS_DIR}/schema-index.md", "slug": slug, "namespace": "", "id": "", "tags": [], "scopes": [],
                    "desc": desc, "ports": ports, "ports_source": "schema", "schema": sp.relative_to(ROOT).as_posix(),
                    "examples": used.get(slug, []), "seen_fields": seen_fields.get(slug, [])})
    return sorted(out, key=lambda o: (o["kind"], o["slug"]))


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
    files += [ROOT / CATALOG, ROOT / WF_API] + sorted((ROOT / "skills").glob("*/SKILL.md")) + [ROOT / "index" / "synonyms.json"]
    files += sorted((ROOT / OPS_DIR).glob("*.md")) + sorted((ROOT / OPS_DIR / "schemas").glob("*.md"))
    files += sorted((ROOT / EXAMPLES_DIR).glob("*.json"))
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
    operations = build_operations()
    kinds = {k: sum(1 for o in operations if o["kind"] == k) for k in ("trigger", "action", "control", "blocking", "other")}
    dump(ROOT / "index" / "operations.json",
         {"meta": {"count": len(operations), "kinds": kinds, "with_schema": sum(1 for o in operations if o["schema"])},
          "operations": operations})
    risk = {r: sum(1 for e in endpoints if e["risk"] == r) for r in ("read", "write", "destructive")}
    print(f"endpoints={len(endpoints)} (risk {risk}) playbooks={len(playbooks)} learnings={len(learnings)} "
          f"operations={len(operations)} {kinds} core_hash={h}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
