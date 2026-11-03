# Notices

## Workflow import API

The endpoint names and request shapes in `skills/6-workflows/scripts/import_workflow.py` and
`skills/6-workflows/references/manage-workflows-api.md` ("Process: importing a template via the API") come from a
live import run reported by this repo's maintainer on 2026-11-03 and were cross-checked against DevRev's
`workflow-skill` (`scripts/api.py` in `devrev/aai-custom-computer-capabilities`, folder
`3-computer-capabilities-nxt/workflow-skill`), which is MIT licensed. The script itself is written for this repo; the
licence is reproduced here because that project was consulted.

```
MIT License

Copyright (c) 2024-2026 DevRev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Workflow operation catalog and example templates

`skills/6-workflows/operations/` (the operation catalog and field schemas) and `skills/6-workflows/examples/` (the
example templates) were assembled when this repo was built (see `docs/archive/SUMMARY.md`). A public community copy of
the same skill (`shashankcube/computer-skill`, folder `create-workflow-template`) carries no licence file, and its
README says it is based on `devrev/computer-skills`. This repo takes nothing from that copy: its files were compared
against `skills/6-workflows` on 2026-11-03 and are identical to ours or a subset of them.

If you hold rights to any of this content and want it removed or credited differently, open an issue.

## Developer documentation mirror

`skills/11-developer-docs/` is a generated offline copy of https://developer.devrev.ai, kept for reference. See
`skills/11-developer-docs/INDEX.md` for how it is produced. The site's content belongs to DevRev.
