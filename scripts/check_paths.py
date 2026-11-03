#!/usr/bin/env python3
"""Fail if a hand-written repo file points at a repo path that does not exist.

What it checks (high-signal only, so a failure is always a real dangling pointer):
  * fully-qualified paths: `skills/<N>-<name>/...`, `skills/devrev-start/...` and `docs/<file>`
  * skill-relative paths used inside a skill folder: `references/...`, `scripts/...`, `examples/...`,
    `operations/...`, `commands/...`, `knowledge/...`, `templates/...` — resolved against the skill that
    contains the file (falling back to the repo root)
What it skips: prose shorthand (`skills/9`, `agents/skills`), glob prefixes (`working-`), placeholders
(`FILE.json`, `<name>`), gitignored generated files, the generated developer-docs mirror and the
append-only docs/LEARNINGS.md journal.

    python3 -I scripts/check_paths.py [--root <repo>]

Exit status 1 plus a `file:line: missing path` list when anything dangles. Standard library only.
"""
import argparse
import re
import sys
from pathlib import Path

LEFT = r"(?<![\w/.<>${}-])"
RIGHT = r"(?![\w\-<*])"  # a match that is cut short by `-`, `<` or `*` is a glob/placeholder prefix, not a path
ABS_RE = re.compile(LEFT + r"((?:skills/(?:\d+-[a-z0-9-]+|devrev-start)(?:/[A-Za-z0-9_.\-]+)*)|(?:docs/[A-Za-z0-9_\-]+(?:/[A-Za-z0-9_\-]+)*\.(?:md|json|txt)))" + RIGHT)
REL_RE = re.compile(LEFT + r"((?:references|scripts|examples|operations|commands|knowledge|templates)/[A-Za-z0-9_.\-/]*[A-Za-z0-9_])" + RIGHT)
GENERATED_IGNORED = {"docs/CLONE_RESULTS.local.md"}  # gitignored, written by the bootstrap hook
EXTERNAL = {"scripts/check_prerequisites.sh"}  # lives in the dataset-builder plugin (repos/aai-skills), not this repo
MIRROR = "skills/11-developer-docs/"
MIRROR_GENERATED = ("api-reference", "beta", "airsync", "snapin-development", "sdks", "guides", "about", "changelog")
PLACEHOLDER = re.compile(r"FILE|NAME|<|\*|\{|\.\.\.|^\s*$")


def scan_files(root: Path):
    for name in ("CLAUDE.md", "README.md"):
        if (root / name).exists():
            yield root / name
    if (root / ".claude").exists():
        yield from (root / ".claude").rglob("*.md")
    for p in (root / "skills").rglob("*.md"):
        rel = p.relative_to(root).as_posix()
        if rel.startswith(MIRROR) and rel[len(MIRROR):].split("/")[0] in MIRROR_GENERATED:
            continue
        if rel in (MIRROR + "INDEX.md", MIRROR + "COVERAGE.md"):
            continue
        yield p


def skill_dir_of(root: Path, f: Path):
    rel = f.relative_to(root).parts
    return root / rel[0] / rel[1] if len(rel) > 2 and rel[0] == "skills" else None


def check_one(root: Path, f: Path, line: str, missing: list, n: int) -> int:
    checked = 0
    line = line.replace("${CLAUDE_PLUGIN_ROOT}/", "")  # plugin-ready paths are checked like any repo path
    sdir = skill_dir_of(root, f)
    for m in ABS_RE.finditer(line):
        path = m.group(1).rstrip("/.,;:)")
        if path.endswith("-") or path in GENERATED_IGNORED or PLACEHOLDER.search(path):
            continue
        checked += 1
        if not (root / path).exists():
            missing.append(f"{f.relative_to(root)}:{n}: missing path {path}")
    if sdir is not None:
        for m in REL_RE.finditer(line):
            path = m.group(1).rstrip("/.,;:)")
            if path.endswith("-") or path in EXTERNAL or PLACEHOLDER.search(path):
                continue
            checked += 1
            if not ((sdir / path).exists() or (root / path).exists()):
                missing.append(f"{f.relative_to(root)}:{n}: missing path {path} (relative to {sdir.name}/)")
    return checked


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    root = Path(ap.parse_args().root).resolve()
    missing, checked = [], 0
    for f in sorted(set(scan_files(root))):
        for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            checked += check_one(root, f, line, missing, n)
    print(f"checked {checked} path references")
    for m in missing:
        print("  " + m)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
