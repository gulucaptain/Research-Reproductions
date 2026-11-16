# Add a research reproduction

1. Keep paper-specific code, environments and raw experiments in its own repository. This collection stores a reviewed summary and preview, not another copy of the implementation.
2. Add an entry to `data/projects.json`. Supply the full original paper title, repository and paper links, category, compute platform, precise progress, implementation scope, validation scope, result, limitations and review date.
3. Pin `commit` to the reviewed repository SHA. Add evidence paths, commit-pinned URLs and SHA-256 digests. Summarize both favorable and unfavorable findings. Preserve metric units, seeds, evaluation resolution and distinctions between local and official benchmarks.
4. Copy an appropriate public result figure into `assets/previews/`. Add its original repository path, pinned source URL, SHA-256 and accurate caption to `data/preview-sources.json`. Do not copy raw datasets, private images, model weights or credentials.
5. Run `python3 scripts/build_readme.py`, then `python3 scripts/build_readme.py --check` and `python3 scripts/build_site.py`. Inspect the generated README and the selected website layout on desktop and mobile before publishing.
6. Commit the registry, preview, provenance and generated documentation together. When updating an existing paper, review its new evidence and advance the pinned commit deliberately; upstream changes are not silently accepted.

Project IDs should remain stable. New categories and additional papers should be data changes, not a redesign of the homepage. The production website uses the selected B publication layout. `site/` holds its CSS and browser behavior; `scripts/build_site.py` generates the complete static page from the same reviewed registry. The three initial concepts remain as design history. See `docs/WEBSITE.md` for preview and deployment.
