# Research Reproductions — design brief

Audience: researchers browsing independent algorithm implementations and their evidence. Primary actions: explore projects, view original paper, open repository, inspect experiment report.

Confirmed visual context: the six existing repositories. Centered full paper titles with [Reproduction], flat-square badges, paper/GitHub/report navigation, status tables and real experiment figures. Accent colors: blue #2563eb, magenta #db2777, green #059669, violet #7c3aed, cyan #0891b2, orange #ea580c. Use these as project identities, not large decorative gradients.

Working collection name: Research Reproductions. Public GitHub repo: gulucaptain/Research-Reproductions. The README can be published now; website concepts remain drafts pending selection.

Content source: data/projects.json; six real previews in assets/previews with provenance data/preview-sources.json. Display all six complete paper titles, links, status, local validation, outcomes and remaining limitations. No fabricated benchmark values, completion percentages, institutional affiliations, author portraits or endorsements. No full reproduction success claim; all six remain partial. Counts of experiments across projects are not directly comparable and must not be added together.

Look: formal, clear, distinctive academic portfolio; imagery is real experiment evidence. Body >=14px, labels >=12px, readable contrast. Desktop and mobile layouts. Use self-contained HTML/CSS and tiny vanilla JS in design-demos. Local images reference ../assets/previews/… . Do not fetch fonts/scripts at runtime. System serif display and legible sans/monospace are acceptable local fallbacks; original badges use existing project accents. GitHub is a link, not an endorsement.

The content motif is the chain: paper → implementation → experiment → evidence → unresolved gaps. Each concept must express that chain differently, with a real hero anchor and coherent project browsing. A single homepage with hero + exactly six copy-paste cards is insufficient without thoughtful navigation and evidence context.

Direction A: quiet white gallery, large serif headline, a curated image sheet and editorial project list; roulette style 20 (19 mod 20 + 1).
Direction B: reference-led research publication, inspired by Distill’s content-first scientific explanation; validate reference separately.
Direction C: designer-led archive, using Pentagram-style identity/index thinking to make each project distinct within one system; dark graphite, index navigation and clear evidence ledger.

All three are first drafts for choosing a direction, not final deployments. They must use independent layout structures. Do not register hosting, publish, add final production routing or choose a winning design.
