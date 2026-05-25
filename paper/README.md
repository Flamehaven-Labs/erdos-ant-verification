# paper/

LaTeX source of the accompanying reproduction paper.

## Compile locally

```bash
# Requires: TeX Live (or MiKTeX), biber, latexmk
cd paper
latexmk -pdf main.tex
# Output: main.pdf
```

## Compile via Overleaf

Upload the `paper/` directory contents to a new Overleaf project. Set
the main document to `main.tex` and the compiler to `pdfLaTeX` with
`biber` for the bibliography.

## Compile via CI

Every push to `main` that touches `paper/**`, every `v*` tag push, and
manual `workflow_dispatch` run triggers `.github/workflows/paper.yml`.
The workflow compiles `paper/main.tex`, checks that `paper/main.pdf`
exists and is non-empty, and uploads the compiled PDF as a workflow
artifact named `erdos-ant-verification-paper`.

## Honesty scan

The CI workflow runs a `grep`-based scan that fails the build if any of
the following appear:

- `we prove`, `we have proved`, `we proof` (the paper does NOT prove
  any new result; use "reproduce", "compute", or "pin against the
  published source" instead).
- `revolutionary`, `unprecedented`, `state-of-the-art` (banned
  marketing language).

## Structure

```
paper/
├── main.tex                 Document skeleton + title + abstract
├── references.bib           BibLaTeX bibliography
├── sections/
│   ├── 01_background.tex    Background and scope
│   ├── 02_phase1.tex        h(K)=1 lattices
│   ├── 03_phase2.tex        Q(sqrt(-5)) with genus theory
│   ├── 04_phase3.tex        Sawin multi-quadratic finite parts
│   ├── 05_eq22.tex          Numerical reproduction of eq (2.2) (central)
│   ├── 06_limits.tex        Limits and non-claims
│   ├── 07_reproducibility.tex   Reproducibility
│   └── 08_acknowledgements.tex
└── README.md                this file
```

## Release-time substitutions

As of v0.1.4 there are no `<COMMIT_HASH>` or `<ZENODO_DOI>` placeholders
left in the paper sources — both are filled in with the v0.1.3 release
values:

- Commit hash: `c8fe529` (v0.1.3 release tag)
- Zenodo DOI: [10.5281/zenodo.20377950](https://doi.org/10.5281/zenodo.20377950) (v0.1.3 deposit)

For future paper-bearing releases that need to refer to a new release
tag or DOI, edit `paper/main.tex` (abstract footnote) and
`paper/sections/07_reproducibility.tex` (reproducibility table) in the
same commit that closes the new release; do not reintroduce placeholder
syntax.

Do not retag a paper source as a numbered release until the
corresponding code, report evidence, and CI-produced PDF artifact are
frozen together.
