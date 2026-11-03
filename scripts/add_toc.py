#!/usr/bin/env python3
"""Add (or refresh) a `## Contents` table of contents in every long hand-written reference. Idempotent. Standard library only.

    python3 -I scripts/add_toc.py            # write
    python3 -I scripts/add_toc.py --check    # exit 1 if any long reference lacks a current TOC

Why: Anthropic's skill guidance says a reference over 100 lines should open with a table of contents, because an
agent often reads only the first lines of a file; the TOC tells it what the rest contains and where to jump.

Targets: skills/**/*.md longer than 100 lines, except SKILL.md files (they are entry points), the generated
developer-docs mirror, and the raw knowledge articles. The TOC lists `##` headings and, when the file has at most
40 of them, `###` headings too. It sits between `<!-- toc -->` markers right after the first `# ` heading.
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIRROR = "skills/11-developer-docs/"
MIRROR_GENERATED = ("api-reference", "beta", "airsync", "snapin-development", "sdks", "guides", "about", "changelog")
START, END = "<!-- toc -->", "<!-- /toc -->"


def targets():
    for p in sorted((ROOT / "skills").rglob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        if p.name == "SKILL.md" or "/knowledge/" in rel:
            continue
        if rel.startswith(MIRROR) and (rel[len(MIRROR):].split("/")[0] in MIRROR_GENERATED or rel.endswith(("INDEX.md", "COVERAGE.md"))):
            continue
        if len(p.read_text(encoding="utf-8").splitlines()) > 100:
            yield p


def slug(heading, seen):
    s = unicodedata.normalize("NFKD", heading.strip().lower())
    s = re.sub(r"[`*_~]", "", s)
    s = re.sub(r"[^\w\s-]", "", s, flags=re.U).strip()
    s = re.sub(r"\s", "-", s)
    n = seen.get(s, 0)
    seen[s] = n + 1
    return s if n == 0 else f"{s}-{n}"


def headings(lines):
    out, fence = [], False
    for l in lines:
        if l.lstrip().startswith("```"):
            fence = not fence
            continue
        m = None if fence else re.match(r"^(#{2,3})\s+(.+?)\s*#*$", l)
        if m:
            out.append((len(m.group(1)), m.group(2).strip()))
    return out


def build(lines):
    hs = [(lvl, h) for lvl, h in headings(lines) if h.lower() != "contents"]
    h2 = sum(1 for lvl, _ in hs if lvl == 2)
    use_h3 = h2 <= 40 and len(hs) <= 90
    seen, out = {}, []
    for lvl, h in headings(lines):  # slugs must count every heading, including "Contents"
        s = slug(h, seen)
        if h.lower() == "contents" or (lvl == 3 and not use_h3):
            continue
        text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", h)
        out.append(f"{'  ' if lvl == 3 else ''}- [{text}](#{s})")
    return out


def apply(text):
    lines = text.split("\n")
    # drop an existing generated block first, so slugs are computed against the real headings only
    if START in text and END in text:
        a = next(i for i, l in enumerate(lines) if l.strip() == START)
        b = next(i for i, l in enumerate(lines) if l.strip() == END)
        # the block is preceded by a '## Contents' heading line (and a blank line)
        s = a - 1
        while s >= 0 and lines[s].strip() == "":
            s -= 1
        if s >= 0 and lines[s].strip().lower() == "## contents":
            a = s
        lines = lines[:a] + lines[b + 1:]
        while a < len(lines) and lines[a].strip() == "" and a > 0 and lines[a - 1].strip() == "":
            del lines[a]
    entries = build(lines)
    # place after the first H1 (skipping front-matter); else at the very top
    pos = 0
    if lines and lines[0] == "---":
        end = next((i for i in range(1, len(lines)) if lines[i] == "---"), 0)
        pos = end + 1
    h1 = next((i for i in range(pos, min(len(lines), pos + 15)) if lines[i].startswith("# ")), None)
    ins = (h1 + 1) if h1 is not None else pos
    block = ["", "## Contents", START] + entries + [END, ""]
    lines[ins:ins] = block
    # re-slug with the Contents heading present so anchors stay right (it is skipped in the list, but counted)
    new = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", new)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    stale = []
    for p in targets():
        old = p.read_text(encoding="utf-8")
        new = apply(old)
        if new != old:
            if a.check:
                stale.append(p.relative_to(ROOT).as_posix())
            else:
                p.write_text(new, encoding="utf-8")
                stale.append(p.relative_to(ROOT).as_posix())
    if a.check:
        for s in stale:
            print("stale or missing TOC:", s)
        print(f"{len(stale)} file(s) need a TOC" if stale else "all long references have a current TOC")
        return 1 if stale else 0
    print(f"updated {len(stale)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
