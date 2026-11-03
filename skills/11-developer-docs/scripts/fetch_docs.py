#!/usr/bin/env python3
"""Download developer.devrev.ai into a raw cache directory.

Stage 1 of 2 (stage 2 is build_docs.py). Standard library only.

    python3 -I fetch_docs.py --out <EMPTY_OR_RESUMABLE_CACHE_DIR> [--only REGEX] [--concurrency 6]

What it does
  1. Reads https://developer.devrev.ai/sitemap.xml.
  2. Classifies every URL:
       endpoint   /api-reference/<resource>/<endpoint>  (also under /beta/)
                  -> full HTML page, stored gzipped (no Markdown form exists)
       narrative  everything else (guides, SDKs, snap-ins, AirSync, resource
                  landing pages, changelog ...)
                  -> <url>/llms.txt, which the site serves as clean Markdown
       skipped    the site root (its /llms.txt is the whole-site index, not a page)
  3. Writes manifest.json describing the outcome for every URL.

Safe to re-run: URLs already present in the cache are skipped. The cache must live
OUTSIDE the repository: it holds untrusted downloaded content and is large.
Run with `python3 -I` so the interpreter does not import from the current directory.
"""
import argparse
import concurrent.futures as cf
import gzip
import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = "https://developer.devrev.ai"
USER_AGENT = "devrev-implementation-docs-mirror/1.0 (+https://github.com/c-darshanbaligeri-ux/devrev-implementation)"
ENDPOINT_RE = re.compile(r"^/(beta/)?api-reference/[^/]+/[^/]+$")
MAX_ATTEMPTS = 6


def http_get(url, accept=None):
    """GET with retry + exponential backoff. Honors Retry-After on 429/503."""
    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept
    last_err = None
    for attempt in range(MAX_ATTEMPTS):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.status, resp.headers.get("Content-Type", ""), resp.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                retry_after = e.headers.get("Retry-After")
                delay = float(retry_after) if retry_after and retry_after.isdigit() else 2 ** attempt
                last_err = f"HTTP {e.code}"
                time.sleep(min(delay, 60))
                continue
            return e.code, e.headers.get("Content-Type", ""), b""
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_err = repr(e)
            time.sleep(min(2 ** attempt, 60))
    return 0, "", last_err.encode() if last_err else b""


def slug(path):
    """URL path -> flat, filesystem-safe cache name (no directories)."""
    s = path.strip("/") or "index"
    return s.replace("/", "__")


# The site's Markdown endpoint mangles Mermaid diagrams: the diagram source contains "->>", and the first
# ">" ends the <Mermaid chart="..."> component, so the head of the diagram is lost and a lone "/>" line is
# left behind. The full source is still in the page's HTML, so for such pages we also keep the HTML.
DANGLING = re.compile(rb"(?m)^/>\s*$")


def ensure_diagrams(rec, name, out_dir, md_bytes):
    if not DANGLING.search(md_bytes):
        return
    target = out_dir / f"{name}.diagrams.html.gz"
    if not target.exists():
        status, _, body = http_get(rec["url"])
        if status != 200:
            rec["note"] = (rec.get("note", "") + f" diagram HTML HTTP {status}").strip()
            return
        target.write_bytes(gzip.compress(body))
    rec["diagrams"] = target.name


def classify(path):
    if path in ("", "/"):
        return "skipped"
    if ENDPOINT_RE.match(path):
        return "endpoint"
    return "narrative"


def load_sitemap():
    status, _, body = http_get(f"{BASE}/sitemap.xml")
    if status != 200:
        sys.exit(f"sitemap fetch failed: HTTP {status}")
    root = ET.fromstring(body)
    urls = []
    for el in root.iter():
        if el.tag.endswith("}loc") or el.tag == "loc":
            u = (el.text or "").strip()
            if u.startswith(BASE):
                urls.append(u)
    # de-dup, keep order
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def fetch_one(url, kind, out_dir):
    path = url[len(BASE):] or "/"
    name = slug(path)
    rec = {"url": url, "path": path, "kind": kind, "file": None, "status": None, "bytes": 0, "note": ""}
    if kind == "skipped":
        rec["note"] = "site root; its /llms.txt is the whole-site index, not mirrored as a page"
        return rec
    if kind == "narrative":
        target = out_dir / f"{name}.md"
        src = url.rstrip("/") + "/llms.txt"
        if target.exists():
            rec.update(file=target.name, status=200, bytes=target.stat().st_size, note="cached")
            ensure_diagrams(rec, name, out_dir, target.read_bytes())
            return rec
        status, ctype, body = http_get(src)
        rec["status"] = status
        if status == 200 and "markdown" in ctype.lower() or (status == 200 and body.lstrip().startswith(b"---")):
            target.write_bytes(body)
            rec.update(file=target.name, bytes=len(body))
            ensure_diagrams(rec, name, out_dir, body)
            return rec
        # Fallback: no Markdown form -> keep the HTML so the builder can still extract text
        rec["note"] = f"llms.txt HTTP {status} ({ctype}); fell back to HTML"
        target = out_dir / f"{name}.html.gz"
        if target.exists():
            rec.update(file=target.name, status=200, bytes=target.stat().st_size, kind="narrative-html")
            return rec
        status, _, body = http_get(url)
        rec["status"] = status
        if status == 200:
            target.write_bytes(gzip.compress(body))
            rec.update(file=target.name, bytes=len(body), kind="narrative-html")
        return rec
    # endpoint-shaped URL. A handful are concept pages (e.g. /api-reference/tags/concepts):
    # those serve llms.txt, real endpoint pages 404 there -- so probe Markdown first.
    md_target = out_dir / f"{name}.md"
    target = out_dir / f"{name}.html.gz"
    for cached, kind_ in ((md_target, "narrative"), (target, "endpoint")):
        if cached.exists():
            rec.update(file=cached.name, status=200, bytes=cached.stat().st_size, kind=kind_, note="cached")
            if cached.suffix == ".md":
                ensure_diagrams(rec, name, out_dir, cached.read_bytes())
            return rec
    status, ctype, body = http_get(url.rstrip("/") + "/llms.txt")
    if status == 200 and "markdown" in ctype.lower():
        md_target.write_bytes(body)
        rec.update(file=md_target.name, status=200, bytes=len(body), kind="narrative", note="concept page under /api-reference/")
        ensure_diagrams(rec, name, out_dir, body)
        return rec
    status, _, body = http_get(url)
    rec["status"] = status
    if status == 200:
        target.write_bytes(gzip.compress(body))
        rec.update(file=target.name, bytes=len(body))
    else:
        rec["note"] = body.decode("utf-8", "replace")[:200]
    return rec


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="cache directory (outside the repo)")
    ap.add_argument("--only", help="regex; only fetch URL paths matching it (for testing)")
    ap.add_argument("--concurrency", type=int, default=6)
    args = ap.parse_args()

    out_dir = Path(args.out).resolve()
    if (out_dir / ".git").exists() or "devrev-implementation" in out_dir.parts[-3:]:
        sys.exit("refusing to cache inside the repo; pass a directory outside it")
    out_dir.mkdir(parents=True, exist_ok=True)

    urls = load_sitemap()
    print(f"sitemap: {len(urls)} URLs")
    jobs = []
    for u in urls:
        path = u[len(BASE):] or "/"
        if args.only and not re.search(args.only, path):
            continue
        jobs.append((u, classify(path)))
    print(f"fetching {len(jobs)} URLs with concurrency {args.concurrency}")

    # Catch case-only collisions now (filesystem is case-insensitive on macOS).
    lowered = {}
    for u, k in jobs:
        key = slug(u[len(BASE):]).lower()
        if key in lowered and lowered[key] != u:
            print(f"WARNING case collision: {lowered[key]} vs {u}", file=sys.stderr)
        lowered[key] = u

    manifest, done = [], 0
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futs = {pool.submit(fetch_one, u, k, out_dir): u for u, k in jobs}
        for fut in cf.as_completed(futs):
            try:
                manifest.append(fut.result())
            except Exception as e:  # keep going; record the failure
                manifest.append({"url": futs[fut], "kind": "error", "status": 0, "note": repr(e)})
            done += 1
            if done % 50 == 0 or done == len(jobs):
                print(f"  {done}/{len(jobs)}  ({time.time() - t0:.0f}s)", flush=True)

    manifest.sort(key=lambda r: r["url"])
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=1))
    bad = [r for r in manifest if r.get("kind") != "skipped" and r.get("status") != 200]
    print(f"done: {len(manifest) - len(bad)} ok, {len(bad)} not ok")
    for r in bad[:20]:
        print(f"  FAIL {r['url']} status={r.get('status')} {r.get('note', '')}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
