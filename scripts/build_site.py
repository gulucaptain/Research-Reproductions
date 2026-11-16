"""Generate the selected publication homepage from the same registry as README."""
import argparse
import hashlib
import json
import re
import shutil
from datetime import date
from html import escape as esc
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from build_readme import ROOT, load


def article(p, index):
    title, name = esc(p['title']), esc(p['name'])
    repo_link = f'<a href="{esc(p["repo"])}">Implementation ↗</a>' if p['repo'] else '<span>Implementation not published</span>'
    evidence_repo = p.get('evidence_repo') or p['repo']
    evidence_commit = p.get('evidence_commit') or p['commit']
    evidence = ''.join(f'<li><a href="{esc(e["url"])}">{esc(e["path"])} ↗</a><br><code>SHA-256: {esc(e["sha256"])}</code></li>' for e in p['evidence'])
    return f'''<article id="{esc(p['id'])}" class="study {'lead-study' if index == 1 else ''}" data-category="{esc(p['category'])}" style="--project:{p['color']}">
<div class="study-heading"><span class="folio">{index:02}</span><div><div class="eyebrow"><span class="category">{esc(p['category'])}</span><span>{esc(p['platform'])}</span></div><h2>{title}</h2><div class="state"><span class="square" aria-hidden="true"></span>{esc(p['status'])} <span class="scope">/ {esc(p['progress'])}</span></div></div></div>
<div class="study-content"><figure><button type="button" class="figure-open" data-figure="{esc(p['image'])}" data-name="{name}" data-caption="{esc(p['image_caption'])}" aria-label="Enlarge result figure for {name}"><img src="{esc(p['image'])}" alt="{esc(p['image_caption'])}" {'fetchpriority="high"' if index == 1 else 'loading="lazy"'} decoding="async"></button><figcaption><span>Fig. {index}.</span> {esc(p['image_caption'])}<span class="figure-hint">Select the figure to inspect at full size.</span></figcaption></figure>
<div class="abstract"><p class="result">{esc(p['result'])}</p><div class="finding"><span class="small-label">What remains open</span><p>{esc(p['limitations'])}</p></div>
<details><summary>Implementation &amp; local validation</summary><dl><dt>Implemented</dt><dd>{esc(p['implemented'])}</dd><dt>Locally validated</dt><dd>{esc(p['validation'])}</dd></dl></details>
<nav class="paper-links" aria-label="{name} resources"><a href="{esc(p['paper'])}">Original paper ↗</a>{repo_link}<a href="{esc(p['report'])}">Experiment report ↗</a></nav>
<details class="evidence"><summary>Pinned evidence &amp; provenance</summary><ul>{evidence}</ul><p class="reviewed">Reviewed {esc(p['updated'])} · <a href="{esc(evidence_repo)}/tree/{evidence_commit}">evidence {evidence_commit[:7]} ↗</a></p></details></div></div></article>'''


def render(data, site):
    projects = data['projects']
    count = len(projects)
    categories = list(dict.fromkeys(p['category'] for p in projects))
    when = date.fromisoformat(data['updated']).strftime('%d %B %Y').lstrip('0')
    edition = date.fromisoformat(data['updated']).strftime('%B %Y')
    contents = ''.join(f'<a href="#{esc(p["id"])}"><span>{i:02}</span>{esc(p["name"])}</a>' for i,p in enumerate(projects,1))
    filters = '<button type="button" data-filter="all" aria-pressed="true">All studies</button>' + ''.join(f'<button type="button" data-filter="{esc(c)}" aria-pressed="false">{esc(c)}</button>' for c in categories)
    rows = ''.join(article(p, i) for i,p in enumerate(projects,1))
    repo = 'https://github.com/gulucaptain/Research-Reproductions'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{esc(site['description'])}"><meta name="theme-color" content="#ffffff"><meta property="og:title" content="Research Reproductions — A field journal of implementation"><meta property="og:description" content="{esc(site['description'])}"><meta property="og:type" content="website"><meta property="og:url" content="{esc(site['url'])}/"><link rel="canonical" href="{esc(site['url'])}/"><title>Research Reproductions — A field journal of implementation</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css"><script src="assets/site.js" defer></script></head>
<body><a class="skip" href="#studies">Skip to studies</a><div class="shell"><header class="masthead" id="top"><a class="wordmark" href="#top">Research Reproductions<span>A field journal of implementation</span></a><nav aria-label="Main navigation"><a href="#studies">The collection</a><a href="#reading-evidence">Reading the evidence</a><a href="{repo}">GitHub ↗</a></nav></header>
<main><section class="intro" aria-labelledby="intro-title"><div><div class="eyebrow">Independent research <span class="edition">Collection / {edition}</span></div><h1 id="intro-title">What survives<br>implementation?</h1><p class="dek">From a paper’s central idea to an experiment you can inspect. {count} independent reproductions, with local results and the questions still open.</p></div><aside class="intro-aside"><span class="small-label">A note on scope</span><p>Implementation, local validation and agreement with the original paper are distinct claims. Each study states its current coverage and remaining gaps.</p><a href="#reading-evidence">How to read this collection →</a></aside></section>
<div class="chain" aria-label="Our evidence process"><b>01 · Paper</b><span aria-hidden="true">→</span><b>02 · Implementation</b><span aria-hidden="true">→</span><b>03 · Experiment</b><span aria-hidden="true">→</span><b>04 · Evidence</b><span aria-hidden="true">→</span><b>05 · Open questions</b></div>
<div class="reading"><aside class="margin"><h2>In this collection</h2><nav class="contents" aria-label="Study index">{contents}</nav><p class="margin-note">{count} studies.<br>{len(categories)} research areas.<br>CPU and Apple Silicon.<br>Reviewed {when}.</p></aside>
<section id="studies" aria-label="Research reproduction studies"><div class="search-row"><label class="search-box"><span aria-hidden="true">⌕</span><span class="visually-hidden">Search studies</span><input type="search" id="search" placeholder="Search papers, methods or results…" autocomplete="off" aria-controls="study-list"></label><button type="button" class="reset" id="reset-filters">Reset</button></div><div class="toolbar"><div class="filters" role="group" aria-label="Filter studies by research area">{filters}</div><span class="count" role="status" aria-live="polite">{count} studies</span></div><div id="study-list">{rows}</div><div class="empty" hidden><h2>No studies found.</h2><p>Try another keyword or research area.</p><button type="button" id="empty-reset">Show all studies</button></div><noscript><p class="source-note">All studies are shown below. Search, filtering and image enlargement require JavaScript; paper, implementation and report links remain available.</p></noscript></section></div>
<section class="closing" id="reading-evidence"><h2>The result is only<br>part of the story.</h2><div><p>Each figure comes from a local experiment, with its evaluation scope stated alongside it. Open the implementation for the algorithm and the experiment report for settings, results and remaining differences. Run counts describe different experiments and are not comparable across projects. Local experiments do not by themselves establish complete paper-level reproduction.</p><p class="source-note"><a href="{repo}/blob/main/docs/EVIDENCE_POLICY.md">Evidence policy ↗</a> · <a href="data/preview-sources.json">Figure provenance ↗</a> · <a href="{repo}/blob/main/docs/ADDING_PROJECT.md">Add a study ↗</a></p></div></section></main><footer><span>Research Reproductions · Independent implementations &amp; evidence<br>Last reviewed {when} · <a href="{repo}">Source &amp; maintenance ↗</a></span><a class="top-link" href="#top">Back to the top ↑</a></footer></div>
<dialog id="figure-dialog" aria-labelledby="figure-title"><div class="dialog-bar"><h2 id="figure-title"></h2><button type="button" class="dialog-close">Close ×</button></div><img alt=""><p id="figure-caption"></p></dialog></body></html>'''


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = set()
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, 'Duplicate DOM ID: ' + attrs['id']
            self.ids.add(attrs['id'])
        for key in ['href', 'src']:
            value = attrs.get(key, '')
            if value.startswith('#'):
                self.anchors.append(value[1:])
            elif value and not urlparse(value).scheme:
                self.refs.append(value)


def validate(output):
    parser = AssetParser()
    parser.feed((output / 'index.html').read_text())
    for value in parser.refs:
        assert (output / value).is_file(), 'Missing deployed asset: ' + value
    assert all(a in parser.ids for a in parser.anchors)
    text = (output / 'index.html').read_text()
    assert 'Draft for review' not in text and 'First design draft' not in text
    data = load()
    assert text.count('class="study ') == len(data['projects'])
    for p in data['projects']:
        for key in ['title', 'result', 'limitations']:
            assert esc(p[key]) in text, (p['id'], key)
    print(f"Website checked: {len(data['projects'])} studies; all local references and evidence fields present.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, default=ROOT / 'dist')
    args = ap.parse_args()
    out = args.out.resolve()
    assert out != ROOT, 'Choose a build output directory, not the source root'
    data = load()
    site = json.loads((ROOT / 'data/site.json').read_text())
    out.mkdir(parents=True, exist_ok=True)
    (out / 'assets').mkdir(exist_ok=True)
    (out / 'data').mkdir(exist_ok=True)
    (out / 'index.html').write_text(render(data, site))
    for src,dest in [('site/style.css','assets/site.css'), ('site/app.js','assets/site.js'), ('site/favicon.svg','assets/favicon.svg')]:
        shutil.copyfile(ROOT / src, out / dest)
    shutil.copytree(ROOT / 'assets/previews', out / 'assets/previews', dirs_exist_ok=True)
    for name in ['projects.json', 'preview-sources.json']:
        shutil.copyfile(ROOT / 'data' / name, out / 'data' / name)
    (out / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + site['url'] + '/sitemap.xml\n')
    (out / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>' + esc(site['url']) + '/</loc><lastmod>' + data['updated'] + '</lastmod></url></urlset>\n')
    validate(out)


if __name__ == '__main__':
    main()
