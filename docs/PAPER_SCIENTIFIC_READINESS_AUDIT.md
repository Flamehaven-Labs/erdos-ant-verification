# Paper Scientific Readiness Audit

Status: suitable as a reproducibility-artifact paper, not as an original
mathematics paper.

This audit covers `paper/main.tex`, `paper/references.bib`,
`paper/README.md`, and the section files under `paper/sections/`.

## Fit to Paper Type

The paper is scientifically appropriate if read as an executable
reproduction artifact for one published numerical expression:
equation (2.2) of the remarks PDF. It is not positioned as a new proof,
a formal proof verification, or a peer-reviewed mathematical result.

That positioning is consistent across:

- the title and abstract in `paper/main.tex`;
- the scope boundary in `sections/01_background.tex`;
- the finite Phase 1 / 2 / 3 descriptions;
- the central eq. (2.2) reproduction in `sections/05_eq22.tex`;
- the explicit non-claims in `sections/06_limits.tex`;
- the reproducibility table and scanner framing in
  `sections/07_reproducibility.tex`.

## Content Integrity

The paper's central claim is narrow and traceable:

> Given the constants from remarks PDF section 2.1, the repository
> evaluates the elementary eq. (2.2) expression at high precision and
> reproduces the published `6.24e-38` exponent excess within source
> rounding.

This claim matches the implemented code. The manuscript does not claim
to prove Theorem 1.1, construct the infinite Golod-Shafarevich tower, or
verify Sawin's later `delta ~ 0.014` refinement.

## Bibliography

`paper/references.bib` contains the required source classes:

- primary proof PDF;
- primary remarks PDF;
- Erdős 1946;
- Golod-Shafarevich;
- Cox for genus theory background;
- Hajir-Maire for tower-cutting background;
- `mpmath` for the high-precision numerical evaluation;
- Kalai blog as explicitly labelled secondary coverage.

The bibliography is adequate for a reproducibility artifact. It would
not be sufficient for a full survey paper on unit-distance bounds, but
that is outside the claimed scope.

## CI/CD PDF Path

`.github/workflows/paper.yml` is the intended PDF production path. The
workflow:

- runs on `main` pushes that touch `paper/**`;
- runs on `v*` tag pushes;
- supports manual `workflow_dispatch`;
- scans for overclaiming language before compilation;
- compiles `paper/main.tex` via `xu-cheng/latex-action`;
- validates that `paper/main.pdf` exists and is non-empty;
- uploads the PDF as `openai-erdos-eq22-reproduction-paper`.

Local PDF compilation is not required for scientific validity, but the
tagged release should not be treated as paper-final until the CI artifact
is produced and inspected.

## Remaining Publication Risk

The remaining risk is not mathematical overclaim. The main operational
risk is stale-PDF confusion: if a tracked `paper/main.pdf` differs from
the current LaTeX source, readers may inspect the wrong artifact.
Therefore, for release communication, prefer the CI-produced PDF
artifact for `v0.2.1` and treat the repository LaTeX source as the
source of truth.
