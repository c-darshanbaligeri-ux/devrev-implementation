#!/usr/bin/env python3
"""Make skill bodies resolvable when the toolkit is installed as a plugin. Idempotent. Standard library only.

    python3 -I scripts/rewrite_plugin_paths.py            # write
    python3 -I scripts/rewrite_plugin_paths.py --check    # exit 1 if any SKILL.md still needs rewriting

An installed plugin lives in a cache directory, not in the user's project, so a path like
`skills/8-devrev-api/references/00_API_Catalog.md` would not resolve from the working directory. Claude Code
substitutes `${CLAUDE_PLUGIN_ROOT}` in a skill's text when it loads the skill, so in every skills/*/SKILL.md this
script rewrites `skills/<N>-<name>/...`, `skills/devrev-start/...` and `docs/LEARNINGS.md` to
`${CLAUDE_PLUGIN_ROOT}/<path>`.

It deliberately leaves two things alone:
  * the front-matter (no substitution happens there), and
  * fenced code blocks: a shell snippet is copied verbatim, and in a plain checkout `${CLAUDE_PLUGIN_ROOT}` is an
    unset shell variable that would silently expand to nothing. Run `devrev-find --root` for the toolkit root.
In a checkout of the repo, read `${CLAUDE_PLUGIN_ROOT}` as the repo root (CLAUDE.md says so).
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH_RE = re.compile(
    r"(?<![\w/.<>${}-])((?:skills/(?:\d+-[a-z0-9-]+|devrev-start)(?:/[A-Za-z0-9_.\-]+)*)|docs/LEARNINGS\.md)(?![\w\-<*])"
)
PREFIX = "${CLAUDE_PLUGIN_ROOT}/"


def rewrite(text: str) -> str:
    lines = text.split("\n")
    start = 0
    if lines and lines[0] == "---":
        start = next((i for i in range(1, len(lines)) if lines[i] == "---"), 0) + 1
    out, fence = lines[:start], False
    for line in lines[start:]:
        if line.lstrip().startswith("```"):
            fence = not fence
            out.append(line)
        elif fence:
            out.append(line)
        else:
            out.append(PATH_RE.sub(lambda m: PREFIX + m.group(1), line))
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    stale = []
    for p in sorted((ROOT / "skills").glob("*/SKILL.md")):
        old = p.read_text(encoding="utf-8")
        new = rewrite(old)
        if new != old:
            stale.append(p.relative_to(ROOT).as_posix())
            if not a.check:
                p.write_text(new, encoding="utf-8")
    if a.check:
        for s in stale:
            print("needs rewriting:", s)
        print(f"{len(stale)} SKILL.md file(s) need rewriting" if stale else "all SKILL.md paths are plugin-ready")
        return 1 if stale else 0
    print(f"rewrote {len(stale)} SKILL.md file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
