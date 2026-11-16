# Public project page

The production website uses the selected B research-publication design.

Public URL: https://research-reproductions.gulucaptain666.chatgpt.site

## Source and content

- `data/projects.json`: reviewed project records, evidence and findings, also used by the README.
- `data/preview-sources.json`: unchanged figure sources and hashes.
- `data/site.json`: website metadata and public origin.
- `site/style.css` and `site/app.js`: selected visual system and browser interactions.
- `scripts/build_site.py`: static HTML generation, preview/data copying, sitemap and local-asset checks.
- `.openai/hosting.json`: deployment project identity and static output directory. It contains no credentials.

## Build and preview

```sh
python3 scripts/build_readme.py
python3 scripts/build_readme.py --check
python3 scripts/build_site.py
python3 -m http.server 8000 --directory dist --bind 127.0.0.1
```

Open `http://127.0.0.1:8000`. No third-party Python packages, frontend build dependencies, API keys or database are required. Without JavaScript, all studies and their paper/report links remain present. JavaScript adds category filtering, keyword search, shareable filter URLs, the no-result state, image enlargement and current-section navigation. Images and code are served locally with no external fonts or analytics.

The output `dist/` is generated and ignored by Git. It can be served by a standard static host, including at a repository subpath; only canonical and sitemap URLs should be changed for another public origin.

## Publish changes

Build and verify the source, then use the existing Sites project in `.openai/hosting.json` to synchronize that exact source, package `dist/`, save a version and deploy it publicly. The public GitHub repository and the hosting source are separate destinations; the hosting helper preserves the GitHub `origin`. Push the reviewed source commit to GitHub as well and verify the remote commit.

GitHub Actions validates the registry, generated README and static website. A GitHub push alone does not automatically update the hosted Sites deployment. Deployment credentials are short-lived and are never committed. Request an update of the existing project page when the reviewed registry changes; do not create a new Site.
