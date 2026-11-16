# Collection validation — 2026-11-16

- Six project records were reviewed against the existing project READMEs and result reports. Figures were copied unchanged from tracked files in the corresponding repositories.
- Preview image hashes, required registry fields, pinned evidence URLs and generated README output are checked with the standard-library generator.
- Each of the three website design drafts was loaded in a browser. Desktop screenshots are retained in design-demos. All six source preview files exist locally.
- The three layouts were checked at a 390px viewport. No document-level horizontal overflow remained after fixing the dark archive’s rotated expand icon. The ledger may scroll horizontally within its own container.
- The publication concept’s Rendering filter returned two studies, and All studies restored the collection. The archive concept’s mobile index opened and navigated to the KoalaGS dossier, opening the selected record.
- No browser console errors were observed during the tested interactions. This is draft-level visual and functional QA, not exhaustive production testing.
- The collection checks do not rerun upstream experiments or prove scientific correctness. The production homepage is pending direction selection.

## Selected production page

Direction B was selected by the user. The production page is generated from the shared reviewed registry. Static asset and anchor checks passed; the browser verified Rendering filtering (two studies), combined Bezier search (one study), a no-result query, resetting filters by selecting a paper from the index, the image dialog, and the 390px mobile layout with no document overflow. No console errors were observed in those local checks. Publication source and README generation are checked in CI; deployment status and public access are verified separately.
