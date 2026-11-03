#!/usr/bin/env python3
"""Turn the raw cache written by fetch_docs.py into the skill's Markdown mirror.

Stage 2 of 2. Standard library only.

    python3 -I build_docs.py --cache <CACHE_DIR> --out <path to skills/11-developer-docs> \
        [--catalog skills/8-devrev-api/references/00_API_Catalog.md] [--date YYYY-MM-DD]

Inputs  : <CACHE_DIR>/manifest.json + the cached pages (never executed, only parsed).
Outputs : one .md per narrative page (same path layout as the site),
          one .md per API resource (every endpoint of that resource, public and beta),
          INDEX.md (what came from where) and COVERAGE.md (site vs. 00_API_Catalog.md).

Endpoint pages have no Markdown form, so their HTML is parsed structurally (class-name
driven, not regex-on-text). Nested object types are shown by *name only* on the site and
therefore here too. Re-running is idempotent: generated files are removed and rewritten;
SKILL.md and scripts/ are never touched.
"""
import argparse
import datetime
import gzip
import html.parser
import json
import os
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

BASE = "https://developer.devrev.ai"
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "wbr", "area", "base", "col", "embed", "param", "track"}
SKIP = {"script", "style", "svg", "template", "noscript", "nav", "aside", "header", "footer"}
METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
MEDIA_RE = re.compile(r"^[a-z]+/[a-z0-9.+*-]+$")
KEEP = {"SKILL.md", "scripts"}  # never deleted by --clean


# --------------------------------------------------------------------------- tiny DOM
class Node:
    __slots__ = ("tag", "attrs", "kids", "parent", "s", "cls")

    def __init__(self, tag, attrs=None, parent=None, s=None):
        self.tag, self.attrs, self.parent, self.s = tag, attrs or {}, parent, s
        self.kids = []
        self.cls = self.attrs.get("class") or ""


class TreeBuilder(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.cur = self.root
        self.skip_tag, self.skip_depth = None, 0

    def handle_starttag(self, tag, attrs):
        if self.skip_depth:
            if tag == self.skip_tag:
                self.skip_depth += 1
            return
        if tag in SKIP:
            self.skip_tag, self.skip_depth = tag, 1
            return
        n = Node(tag, dict(attrs), self.cur)
        self.cur.kids.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        if self.skip_depth or tag in SKIP:
            return
        self.cur.kids.append(Node(tag, dict(attrs), self.cur))

    def handle_endtag(self, tag):
        if self.skip_depth:
            if tag == self.skip_tag:
                self.skip_depth -= 1
            return
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n is not self.root:
            self.cur = n.parent

    def handle_data(self, d):
        if not self.skip_depth:
            self.cur.kids.append(Node(None, parent=self.cur, s=d))


def parse_html(raw):
    tb = TreeBuilder()
    tb.feed(raw)
    return tb.root


def read_gz(path):
    return gzip.open(path, "rt", encoding="utf-8", errors="replace").read()


# --------------------------------------------------------------------------- text helpers
def inline(n):
    """Inline Markdown for the content of node n."""
    out = []
    for k in n.kids:
        if k.tag is None:
            out.append(re.sub(r"\s+", " ", k.s))
        elif k.tag == "code":
            t = inline(k).strip()
            out.append(f"`{t}`" if t else "")
        elif k.tag in ("strong", "b"):
            t = inline(k).strip()
            out.append(f"**{t}**" if t else "")
        elif k.tag in ("em", "i"):
            t = inline(k).strip()
            out.append(f"*{t}*" if t else "")
        elif k.tag == "a":
            t = inline(k).strip()
            href = k.attrs.get("href", "")
            out.append(f"[{t}]({href})" if t and href.startswith(("http", "/")) else t)
        elif k.tag == "br":
            out.append("\n")
        elif k.tag in ("ul", "ol", "pre", "table"):
            continue
        else:
            out.append(inline(k))
    return re.sub(r" *\n *", "\n", "".join(out))


def all_text(n):
    return "".join(k.s if k.tag is None else all_text(k) for k in n.kids)


def descendants(n):
    for k in n.kids:
        if k.tag is not None:
            yield k
            yield from descendants(k)


def first(n, pred):
    for d in descendants(n):
        if pred(d):
            return d
    return None


def list_md(n, depth=0):
    lines = []
    for i, li in enumerate([k for k in n.kids if k.tag == "li"], 1):
        bullet = f"{i}." if n.tag == "ol" else "-"
        lines.append("  " * depth + f"{bullet} {inline(li).strip()}")
        for sub in li.kids:
            if sub.tag in ("ul", "ol"):
                lines.append(list_md(sub, depth + 1))
    return "\n".join(lines)


def table_md(t):
    """<table> -> GitHub-flavored Markdown table (first row is the header)."""
    rows, header_flags = [], []
    for tr in (d for d in descendants(t) if d.tag == "tr"):
        cells = [c for c in tr.kids if c.tag in ("th", "td")]
        rows.append([cell(inline(c).strip()) for c in cells])
        header_flags.append(any(c.tag == "th" for c in cells))
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    if header_flags[0]:
        head, body = rows[0], rows[1:]
    else:
        head, body = [""] * width, rows
    lines = ["| " + " | ".join(head) + " |", "| " + " | ".join(["---"] * width) + " |"]
    lines += ["| " + " | ".join(r) + " |" for r in body]
    return "\n".join(lines)


def pre_lines(pre):
    code = first(pre, lambda d: d.tag == "code") or pre
    spans = [k for k in code.kids if k.tag == "span" and "line" in k.cls.split()]
    if spans:
        return [all_text(s).rstrip() for s in spans]
    return all_text(code).rstrip("\n").split("\n")


def blocks(n):
    """Block-level Markdown paragraphs inside n (skips the small 'chip' badges)."""
    res = []
    for k in n.kids:
        if k.tag is None:
            t = re.sub(r"\s+", " ", k.s).strip()
            if t:
                res.append(t)
        elif "bg-fd-secondary" in k.cls:
            continue
        elif k.tag == "p":
            res.append(inline(k).strip())
        elif k.tag in ("ul", "ol"):
            res.append(list_md(k))
        elif k.tag == "table":
            res.append(table_md(k))
        elif k.tag == "pre":
            res.append("```\n" + "\n".join(pre_lines(k)) + "\n```")
        elif k.tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            res.append("#" * int(k.tag[1]) + " " + inline(k).strip())
        else:
            res.extend(blocks(k))
    return [b for b in res if b]


# --------------------------------------------------------------------------- endpoint pages
def is_field(n):
    return n.tag == "div" and "border-t" in n.cls and "text-sm" in n.cls and ("py-4" in n.cls or "my-4" in n.cls)


RESP_PANEL_RE = re.compile(r"-content-(\d{3})$")


def is_panel(n):
    """One variant panel of a oneOf schema tab group (Fern: id contains '-content-#/components/schemas/')."""
    return n.tag == "div" and "-content-#/" in n.attrs.get("id", "")


def is_group(n):
    """A tab group: a node whose children include variant panels."""
    return any(is_panel(c) for c in n.kids)


def panel_name(p):
    return p.attrs.get("id", "").rsplit("#/components/schemas/", 1)[-1]


def find_fields(n, out):
    """Top-level field blocks under n; does not descend into fields or variant groups."""
    for k in n.kids:
        if k.tag is None:
            continue
        if is_field(k):
            out.append(k)
        elif not is_group(k):
            find_fields(k, out)
    return out


def find_groups(n, out):
    for k in n.kids:
        if k.tag is None or is_field(k):
            continue
        if is_group(k):
            out.append(k)
        else:
            find_groups(k, out)
    return out


def parse_variants(group, prefix=""):
    """[(variant schema name, [fields])] for every panel of a tab group (recursing into nested groups)."""
    res = []
    for p in group.kids:
        if not is_panel(p):
            continue
        name = prefix + panel_name(p)
        res.append((name, [parse_field(f) for f in find_fields(p, [])]))
        for g in find_groups(p, []):
            res.extend(parse_variants(g, prefix=name + " / "))
    return res


def chip_tokens(c):
    toks = [inline(k).strip() for k in c.kids if k.tag is not None and inline(k).strip()]
    if not toks:
        t = all_text(c).strip()
        toks = [t] if t else []
    return toks


def parse_field(n):
    f = {"name": "", "marker": "", "type": "", "desc": [], "chips": [], "children": [], "variants": [],
         "deprecated": False}
    header = next((k for k in n.kids if k.tag == "div" and "flex-wrap" in k.cls and "items-center" in k.cls), None)
    if header is not None:
        spans = [k for k in header.kids if k.tag is not None]
        name_el = next((s for s in spans if "text-fd-primary" in s.cls), None)
        if name_el is not None:
            f["name"] = "".join(k.s for k in name_el.kids if k.tag is None).strip()
            mark = first(name_el, lambda d: d.tag == "span")
            f["marker"] = all_text(mark).strip() if mark is not None else ""
            spans = [s for s in spans if s is not name_el]
        if spans:
            f["type"] = re.sub(r"\s+", " ", all_text(spans[0])).strip()
            for extra in spans[1:]:
                t = re.sub(r"\s+", " ", all_text(extra)).strip()
                if t:
                    f["chips"].append([t])
    nested_roots = []
    for k in n.kids:
        if k is header or k.tag is None:
            continue
        if "prose-no-margin" in k.cls:
            f["desc"] = blocks(k)
            for c in descendants(k):
                if c.tag == "div" and "bg-fd-secondary" in c.cls:
                    f["chips"].append(chip_tokens(c))
        else:
            groups = [k] if is_group(k) else find_groups(k, [])
            has_fields = is_field(k) or bool(find_fields(k, []))
            for g in groups:
                f["variants"].extend(parse_variants(g))
            if has_fields:
                nested_roots.append(k)
            if not groups and not has_fields:
                f["desc"].extend(blocks(k))  # unknown extra content: keep it rather than drop it
    nested = []
    for k in nested_roots:
        nested.append(k) if is_field(k) else nested.extend(find_fields(k, []))
    f["children"] = [parse_field(x) for x in nested]
    f["deprecated"] = any(len(c) == 1 and c[0].lower() == "deprecated" for c in f["chips"])
    return f


class EndpointState:
    def __init__(self):
        self.title = ""
        self.method = ""
        self.api_path = ""
        self.desc = []
        self.section = None
        self.sections = []  # [{"name", "fields", "variants": [(schema name, [fields])]}]
        self.media = {}
        self.responses = []  # [(status, media)]
        self.resp_panels = {}  # status -> (plain text e.g. "Empty", [code-block lines])
        self.pres = []


def parse_endpoint(root):
    st = EndpointState()

    def scan(n):
        for k in n.kids:
            if k.tag is None:
                if st.section and st.section.startswith("Request Body") and "Request Body" not in st.media:
                    t = k.s.strip()
                    if MEDIA_RE.match(t):
                        st.media["Request Body"] = t
                continue
            if k.tag == "h1" and not st.title:
                st.title = inline(k).strip()
                continue
            if k.tag == "h2":
                st.section = re.sub(r"\s+", " ", all_text(k)).strip()
                st.sections.append({"name": st.section, "fields": [], "variants": []})
                continue
            m = RESP_PANEL_RE.search(k.attrs.get("id", "")) if k.tag == "div" else None
            if m:  # one response status panel: either plain text ("Empty") or example JSON
                pres = [pre_lines(p) for p in descendants(k) if p.tag == "pre"]
                st.resp_panels[m.group(1)] = ("" if pres else " ".join(blocks(k)).strip(), pres)
                continue
            if is_group(k):  # oneOf tab group: one panel per variant schema
                if st.sections:
                    st.sections[-1]["variants"].extend(parse_variants(k))
                continue
            if is_field(k):
                if st.sections:
                    st.sections[-1]["fields"].append(parse_field(k))
                continue
            if k.tag == "h3" and st.section == "Response Body":
                btn = first(k, lambda d: d.tag == "button")
                code = re.sub(r"\s+", " ", all_text(btn if btn else k)).strip()
                m = first(k, lambda d: d.tag == "code")
                st.responses.append((code, all_text(m).strip() if m else ""))
                continue
            if k.tag == "pre":
                st.pres.append(pre_lines(k))
                continue
            if (k.tag == "span" and not st.method and "font-mono" in k.cls and "font-medium" in k.cls
                    and all_text(k).strip() in METHODS):
                st.method = all_text(k).strip()
                row = k.parent
                parts = []
                for sib in row.kids:
                    if sib is k or sib.tag in (None, "button"):
                        continue
                    parts.append(re.sub(r"\s+", "", all_text(sib)))
                st.api_path = "".join(parts)
                continue
            if st.title and st.section is None and k.tag in ("p", "ul", "ol", "table"):
                st.desc.extend(_blocks_of(k))
                continue
            scan(k)

    scan(root)
    return st


def _blocks_of(node):
    holder = Node("holder")
    holder.kids = [node]
    return blocks(holder)


def cell(s):
    return s.replace("|", "\\|").replace("\n", "<br>").strip()


def field_rows(fields, prefix=""):
    rows = []
    for f in fields:
        name = prefix + f["name"]
        req = {"*": "yes", "?": "no"}.get(f["marker"], "")
        desc = []
        if f["deprecated"]:
            desc.append("**Deprecated.**")
        desc.extend(f["desc"])
        for chip in f["chips"]:
            if len(chip) == 1 and chip[0].lower() == "deprecated":
                continue
            desc.append("*" + (": ".join(chip) if len(chip) > 1 else chip[0]) + "*")
        typ = f"`{f['type']}`" if f["type"] else ""
        rows.append(f"| `{cell(name)}` | {req} | {cell(typ)} | {cell('<br>'.join(desc))} |")
        rows.extend(field_rows(f["children"], prefix=name + "."))
        for vname, vfields in f["variants"]:
            rows.append(f"| *{cell(name)}: variant* `{cell(vname)}` | | | |")
            rows.extend(field_rows(vfields, prefix=name + "."))
    return rows


def pretty_json(lines):
    txt = "\n".join(lines)
    try:
        return json.dumps(json.loads(txt), indent=2, ensure_ascii=False)
    except ValueError:
        return txt


def render_endpoint(st, url, slug_):
    h = f"{st.method} {st.api_path}".strip() or st.title
    out = [f'<a id="{slug_}"></a>', "", f"## `{h}`", ""]
    if st.title and st.title not in h:
        out += [f"**{st.title}**", ""]
    out += [f"Source: <{url}>", ""]
    if st.desc:
        out += ["\n\n".join(st.desc), ""]
    head = ["| Field | Required | Type | Description |", "| --- | --- | --- | --- |"]
    for sec in st.sections:
        name = sec["name"]
        if name in ("Authorization", "Response Body") or not (sec["fields"] or sec["variants"]):
            continue
        label = name + (f" (`{st.media[name]}`)" if name in st.media else "")
        out += [f"### {label}", ""]
        if sec["fields"]:
            out += head + field_rows(sec["fields"]) + [""]
        if sec["variants"]:
            out += ["The site presents this body as alternative variant schemas (tabs); each table below is one variant.", ""]
        for vname, vfields in sec["variants"]:
            out += [f"#### Variant `{vname}`", ""] + head + field_rows(vfields) + [""]
    if st.responses:
        out += ["### Response codes", ""]
        for c, m in st.responses:
            note = ""
            if c in st.resp_panels and st.resp_panels[c][0]:
                note = f" — {st.resp_panels[c][0].lower()} body" if st.resp_panels[c][0].lower() == "empty" else f" — {st.resp_panels[c][0]}"
            out.append(f"- `{c}`" + (f" — `{m}`" if m else "") + note)
        out += [""]
    curl = next((p for p in st.pres if p and p[0].lstrip().startswith("curl")), None)
    if curl:
        out += ["### cURL example", "", "```bash", "\n".join(curl), "```", ""]
    ok = next((c for c, _ in st.responses if c.startswith("2")), None)
    resp = None
    if ok and ok in st.resp_panels and st.resp_panels[ok][1]:
        resp = st.resp_panels[ok][1][0]
    elif not st.resp_panels:  # page without per-status panels: fall back to the first JSON block
        resp = next((p for p in st.pres if p and p[0].lstrip()[:1] in "{["), None)
    if resp:
        out += [f"<details><summary>Example {ok or 'success'} response</summary>", "", "```json", pretty_json(resp), "```", "", "</details>", ""]
    return "\n".join(out)


# --------------------------------------------------------------------------- narrative pages
FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.S)
IMG_RE = re.compile(r"<img\b[^>]*?>", re.I)
ALT_RE = re.compile(r'alt="([^"]*)"')
EMPTY_LINK_RE = re.compile(r"\[([^\]]*)\]\(\s*\)")
LINK_RE = re.compile(r"(\[[^\]]*\]\()([^)\s]+)((?:\s+\"[^\"]*\")?\))")
HREF_RE = re.compile(r'(href=")(/[^"]*)(")')


def front_matter(md):
    m = FRONT_RE.match(md)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip("\"'")
        md = md[m.end():]
    return fm, md


class Linker:
    def __init__(self, page_map):
        self.map = page_map  # site path -> (relative file, optional #anchor)

    def rewrite(self, href, from_file):
        if href.startswith(BASE):
            href = href[len(BASE):] or "/"
        if not href.startswith("/"):
            return href
        path, _, frag = href.partition("#")
        key = path.rstrip("/") or "/"
        hit = self.map.get(key)
        if hit:
            target, anchor = hit
            rel = os.path.relpath(target, os.path.dirname(from_file) or ".")
            return rel + (("#" + frag) if frag else anchor)
        return BASE + href

    def _prose(self, s, from_file):
        """Apply link/image rewrites to a prose block (may span lines: link text can wrap)."""
        s = EMPTY_LINK_RE.sub(r"\1", s)
        s = IMG_RE.sub(lambda m: "*[image: %s — see source page]*" % ((ALT_RE.search(m.group(0)) or [None, "figure"])[1] or "figure"), s)
        s = LINK_RE.sub(lambda m: m.group(1) + self.rewrite(m.group(2), from_file) + m.group(3), s)
        return HREF_RE.sub(lambda m: m.group(1) + self.rewrite(m.group(2), from_file) + m.group(3), s)

    def text(self, md, from_file):
        """Rewrite prose only; fenced code blocks pass through untouched."""
        out, buf, in_fence = [], [], False

        def flush():
            if buf:
                out.append(self._prose("\n".join(buf), from_file))
                buf.clear()

        for line in md.split("\n"):
            if line.lstrip().startswith("```"):
                if not in_fence:
                    flush()
                in_fence = not in_fence
                out.append(line)
            elif in_fence:
                out.append(line)
            else:
                buf.append(line)
        flush()
        return "\n".join(out)


FLIGHT_RE = re.compile(r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)')
CHART_RE = re.compile(r'"chart":"((?:[^"\\]|\\.)*)"')
DANGLING_RE = re.compile(r"(?m)^/>\s*$")


def extract_charts(raw_html):
    """Mermaid sources in document order, recovered from the page's streamed (RSC) payload."""
    chunks = []
    for m in FLIGHT_RE.finditer(raw_html):
        try:
            chunks.append(json.loads('"' + m.group(1) + '"'))
        except ValueError:
            continue
    charts = []
    for m in CHART_RE.finditer("".join(chunks)):
        try:
            charts.append(json.loads('"' + m.group(1) + '"'))
        except ValueError:
            continue
    return charts


def restore_diagrams(body, charts, url, warnings):
    """Replace each garbled diagram remnant (it ends with a lone '/>' line) by its full ```mermaid source.

    The Markdown endpoint drops the head of the diagram (up to the first '>' of its source) and keeps the
    tail; the remnant is the run of non-blank lines directly above the '/>'. Pairing the n-th remnant with
    the n-th recovered source is only accepted when the two agree on their last line (after normalizing
    quotes, spaces and HTML entities). Otherwise nothing is guessed: a visible placeholder is written and a
    warning is raised."""
    lines = body.split("\n")
    ends = [i for i, l in enumerate(lines) if DANGLING_RE.match(l)]
    if not ends:
        return body
    ok = len(ends) == len(charts)
    if not ok:
        warnings.append(f"{url}: {len(ends)} garbled diagram(s) but {len(charts)} chart source(s) found in the HTML")
    for n in range(len(ends) - 1, -1, -1):
        end = ends[n]
        start = end
        while start > 0 and lines[start - 1].strip() != "":
            start -= 1
        if ok and start < end and _same_tail(lines[end - 1], charts[n]):
            lines[start:end + 1] = ["```mermaid", charts[n].rstrip("\n"), "```"]
        else:
            if ok:
                warnings.append(f"{url}: diagram remnant at line {start + 1} does not match the recovered source")
            lines[start:end + 1] = ["*[diagram: source could not be recovered — see source page]*"]
    return "\n".join(lines)


def _squash(s):
    return re.sub(r"[\s\"']+", "", html.unescape(s))


def _same_tail(remnant_last, chart):
    """The remnant's last line must be the end of the recovered source's last line (equal when the cut fell
    on an earlier line; a proper suffix when the whole diagram is a single line and the cut fell inside it)."""
    last = [l for l in chart.split("\n") if l.strip()]
    tail = _squash(remnant_last)
    return bool(last) and bool(tail) and _squash(last[-1]).endswith(tail)


def html_fallback_md(raw):
    root = parse_html(raw)
    main = first(root, lambda d: d.tag == "main") or root
    return "\n\n".join(blocks(main))


def header(title, url, date):
    return f"# {title}\n\nSource: <{url}>\nScraped: {date}\n"


# --------------------------------------------------------------------------- catalog diff
FULL_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*(?:\.[a-z0-9-]+)+$")
SHORT_NAME_RE = re.compile(r"^(?:\.[a-z0-9-]+)+$")


def catalog_names(text):
    """Endpoint names in 00_API_Catalog.md. Handles its shorthand: `accounts.get` / `.list` / `.export`
    means accounts.get, accounts.list, accounts.export (suffix replaces the last segment of the previous name)."""
    names = set()
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):  # endpoint rows are table rows; prose mentions are not endpoints
            continue
        last = None
        for tok in re.findall(r"`([^`]+)`", line):
            tok = tok.strip()
            if FULL_NAME_RE.match(tok):
                names.add(tok)
                last = tok
            elif last and SHORT_NAME_RE.match(tok):
                names.add(last.rsplit(".", 1)[0] + tok)
    return names


# --------------------------------------------------------------------------- main
def slug_of(path):
    return path.rstrip("/").rsplit("/", 1)[-1]


def title_from_path(path):
    return slug_of(path).replace("-", " ").title()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cache", required=True)
    ap.add_argument("--out", required=True, help="the skills/11-developer-docs directory")
    ap.add_argument("--catalog", help="path to skills/8-devrev-api/references/00_API_Catalog.md for COVERAGE.md")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--allow-failures", action="store_true")
    args = ap.parse_args()

    cache, out = Path(args.cache).resolve(), Path(args.out).resolve()
    if not (out / "scripts" / "build_docs.py").exists():
        sys.exit("--out must be the skill directory (expected scripts/build_docs.py inside it)")
    manifest = json.loads((cache / "manifest.json").read_text())
    bad = [r for r in manifest if r.get("kind") != "skipped" and r.get("status") != 200]
    if bad and not args.allow_failures:
        sys.exit(f"{len(bad)} URLs failed to download (e.g. {bad[0]['url']}); re-run fetch_docs.py or pass --allow-failures")

    narrative = [r for r in manifest if r["kind"] in ("narrative", "narrative-html") and r.get("status") == 200]
    endpoints = [r for r in manifest if r["kind"] == "endpoint" and r.get("status") == 200]
    skipped = [r for r in manifest if r["kind"] == "skipped"]

    # ---- site path -> output file map (needed for link rewriting)
    page_map = {}
    for r in narrative:
        page_map[r["path"].rstrip("/")] = (r["path"].strip("/") + ".md", "")
    groups = defaultdict(list)  # resource file -> endpoint records
    for r in endpoints:
        parts = r["path"].strip("/").split("/")
        beta = parts[0] == "beta"
        base = parts[1:] if beta else parts
        res_file = ("beta/" if beta else "") + f"api-reference/{base[1]}.md"
        groups[res_file].append(r)
        page_map[r["path"].rstrip("/")] = (res_file, "#" + base[2])
    linker = Linker(page_map)

    # ---- collision check (macOS is case-insensitive)
    seen = {}
    for f in list(groups) + [v[0] for v in page_map.values() if v[0] not in groups]:
        k = f.lower()
        if k in seen and seen[k] != f:
            sys.exit(f"case-only path collision: {seen[k]} vs {f}")
        seen[k] = f

    # ---- clean previous output
    for child in out.iterdir():
        if child.name in KEEP:
            continue
        shutil.rmtree(child) if child.is_dir() else child.unlink()

    written, warnings = {}, []

    def write(rel, text):
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text.rstrip("\n") + "\n", encoding="utf-8")
        written[rel] = len(text)

    # ---- narrative pages (resource landing pages are merged into their resource file later)
    landing = {}
    page_rows = []
    for r in sorted(narrative, key=lambda r: r["path"]):
        rel = r["path"].strip("/") + ".md"
        src = cache / r["file"]
        if r["file"].endswith(".md"):
            fm, body = front_matter(src.read_text(encoding="utf-8", errors="replace"))
        else:
            fm, body = {}, html_fallback_md(read_gz(src))
        title = fm.get("title") or title_from_path(r["path"])
        body = body.strip("\n")
        body = re.sub(r"\A#\s+" + re.escape(title) + r"\s*\n+", "", body)  # avoid duplicate H1
        if DANGLING_RE.search(body):  # mangled Mermaid diagram(s): restore from the HTML copy
            charts = extract_charts(read_gz(cache / r["diagrams"])) if r.get("diagrams") else []
            body = restore_diagrams(body, charts, r["url"], warnings)
        body = linker.text(body, rel)
        if rel in groups:  # resource landing page: merged into the resource file below
            landing[rel] = (title, body, r)
            continue
        write(rel, header(title, r["url"], args.date) + "\n" + body)
        page_rows.append((title, rel, r["url"], "html-fallback" if r["kind"] == "narrative-html" else "markdown"))

    # ---- API resource files
    resource_rows = []
    for rel, recs in sorted(groups.items()):
        parsed = []
        for r in recs:
            raw = read_gz(cache / r["file"])
            st = parse_endpoint(parse_html(raw))
            if not st.method or not st.api_path:
                warnings.append(f"{r['url']}: no method/path found")
            if not st.responses:
                warnings.append(f"{r['url']}: no response codes found")
            if not st.title:
                warnings.append(f"{r['url']}: no title found")
            parsed.append((r, st))
        parsed.sort(key=lambda x: (x[1].api_path, x[1].method, x[0]["path"]))
        res_name = rel.rsplit("/", 1)[-1][:-3]
        if rel in landing:
            title, body, lr = landing[rel]
            url = lr["url"]
        else:
            title, body, url = title_from_path(res_name), "", f"{BASE}/{rel[:-3]}"
        text = [header(title, url, args.date)]
        if body:
            text += [body, ""]
        text += ["## Endpoints", "", "| Method | Path | Page |", "| --- | --- | --- |"]
        for r, st in parsed:
            text.append(f"| {st.method} | `{st.api_path}` | [{slug_of(r['path'])}](#{slug_of(r['path'])}) |")
        text.append("")
        for r, st in parsed:
            text += [render_endpoint(st, r["url"], slug_of(r["path"])), ""]
        write(rel, "\n".join(text))
        resource_rows.append((title, rel, url, parsed))

    # ---- INDEX.md
    def section_of(path):
        parts = path.strip("/").split("/")
        return "/".join(parts[:2]) if parts[0] == "beta" and len(parts) > 1 else parts[0]

    by_section = defaultdict(list)
    for title, rel, url, kind in page_rows:
        by_section[section_of(rel[:-3])].append(f"| {title} | [`{rel}`]({rel}) | <{url}> |")
    for title, rel, url, parsed in resource_rows:
        by_section[section_of(rel[:-3])].append(f"| {title} ({len(parsed)} endpoints) | [`{rel}`]({rel}) | <{url}> |")
    total_urls = len(manifest)
    idx = [f"# Index — developer.devrev.ai mirror\n\nScraped: {args.date} · source: <{BASE}/sitemap.xml>\n",
           "| Source URLs in sitemap | Narrative pages | Endpoint pages | Resource files | Not mirrored |",
           "| --- | --- | --- | --- | --- |",
           f"| {total_urls} | {len(narrative)} | {len(endpoints)} | {len(groups)} | {len(skipped)} |", ""]
    for sec in sorted(by_section):
        idx += [f"## {sec}", "", "| Page | Local file | Source |", "| --- | --- | --- |"] + sorted(by_section[sec]) + [""]
    if skipped:
        idx += ["## Not mirrored", ""] + [f"- <{r['url']}> — {r['note']}" for r in skipped] + [""]
    write("INDEX.md", "\n".join(idx))

    # ---- COVERAGE.md (site endpoints vs. the repo's own API catalog)
    cov = ["# Coverage — site endpoints vs. skills/8-devrev-api catalog\n", f"Scraped: {args.date}\n"]
    site_public = {st.api_path.lstrip("/") for _, _, _, parsed in resource_rows
                   for r, st in parsed if not r["path"].startswith("/beta/") and st.api_path}
    site_beta = {st.api_path.lstrip("/") for _, _, _, parsed in resource_rows
                 for r, st in parsed if r["path"].startswith("/beta/") and st.api_path}
    cov += [f"- Public endpoints on the site: **{len(site_public)}** (unique names; GET/POST pairs counted once)",
            f"- Beta endpoints on the site: **{len(site_beta)}**", ""]
    if args.catalog and Path(args.catalog).exists():
        cat = Path(args.catalog).read_text(encoding="utf-8")
        names = catalog_names(cat)
        resources = {n.split(".")[0] for n in site_public | site_beta}
        names = {n for n in names if n.split(".")[0] in resources}
        missing = sorted(site_public - names)
        extra = sorted(names - site_public)
        cov += [f"- Names found in `{Path(args.catalog).name}`: **{len(names)}**", "",
                f"## On the public site but not in the catalog ({len(missing)})", "",
                "Not listed *by name in a table row* of `00_API_Catalog.md`. Many are documented in other skill "
                "references instead (custom objects, schemas, stage diagrams in skills 1–2; `ping` in the root "
                "`CLAUDE.md`), so `grep -rF '<name>' skills/` before treating one as a real knowledge gap. "
                "Verify live before adding anything to the catalog.", ""]
        cov += [f"- `{n}`" for n in missing] or ["- none"]
        cov += ["", f"## In the catalog but not on the public site ({len(extra)})", "",
                "Internal, beta-only (marked below), renamed or removed endpoints. The catalog is live-verified in "
                "places where the docs are not — do not delete anything from it on this evidence alone.", ""]
        cov += [f"- `{n}`" + (" (beta page exists)" if n in site_beta else "") for n in extra] or ["- none"]
    else:
        cov += ["_No catalog path supplied; pass `--catalog` to diff against it._"]
    write("COVERAGE.md", "\n".join(cov) + "\n")

    (cache / "build_warnings.txt").write_text("\n".join(warnings) + ("\n" if warnings else ""))
    print(f"wrote {len(written)} files; narrative={len(narrative)} endpoints={len(endpoints)} resources={len(groups)} warnings={len(warnings)}")
    for w in warnings[:20]:
        print("  WARN", w)
    return 1 if warnings and not args.allow_failures else 0


if __name__ == "__main__":
    sys.exit(main())
