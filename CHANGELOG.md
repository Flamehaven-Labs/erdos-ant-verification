# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.3] - 2026-05-25 (paper readability + public-source framing)

Patch release over v0.2.2. No numerical claim, code path, or test-count
change. This release fixes PDF readability defects and removes
project-specific release-check terminology from the public paper/README
surface.

### Changed (0.2.3)

- Shortened the abstract reproduction paragraph so the reader is sent
  to the reproducibility section instead of seeing a long command chain
  in the abstract.
- Replaced the pinned-environment `tabular` with `tabularx`, allowing
  the repository URL and tagged-revision row to wrap inside the PDF
  text block.
- Reframed the supplementary checks section as author-operated local
  source-level checks and stated that those checks are not independent
  review or mathematical peer review.
- Added a precision-budget explanation for the 200-bit `mpmath`
  setting: the `1.31e-18` numerator separation needs roughly 60 bits
  just to resolve the signal, plus guard bits for the `1e-3`
  regression threshold.
- Clarified the difference between the observed `1.4e-4` relative error
  and the `1e-3` regression tolerance.
- Softened the Limits section tone so the artifact's strength is framed
  as deterministic numerical reproduction with explicit scope
  boundaries, not as a list of disclaimers.

### Audit log (0.2.3)

The public paper remains an executable reproduction of remarks PDF
eq. (2.2), not a formal proof verification and not a reproduction of
Sawin's separate explicit lower bound. The eq. (2.2) output remains
`6.2391e-38` with `1.4e-4` relative error against the published
two-significant-figure value.

## [0.2.2] - 2026-05-25 (public naming alignment)

Patch release over v0.2.1. No numerical claim, code path, or test-count
change. This release aligns the public project name with the repository
slug `openai-erdos-eq22-reproduction`.

### Changed (0.2.2)

- README display title changed to `OpenAI Erdős Unit-Distance Disproof:
  Eq. (2.2) Executable Reproduction`.
- README / package description changed to a GitHub-about-ready summary:
  `Independent Python reproduction of equation (2.2) in the 2026
  OpenAI/Sawin Erdős unit-distance disproof remarks PDF. mpmath-200-bit,
  NumPy + mpmath only.`
- Paper title changed to `Executable Reproduction of Equation (2.2) in
  the OpenAI Erdős Unit-Distance Disproof Remarks`.
- Paper subtitle added: `A High-Precision Python Check of the Published
  Eq. (2.2) Calculation`.
- `pyproject.toml`, `CITATION.cff`, README clone commands, paper
  reproducibility commands, paper CI artifact name, and documentation
  links now point to
  `https://github.com/Flamehaven-Labs/openai-erdos-eq22-reproduction`.

### Audit log (0.2.2)

The Python import package remains `erdos_ant` for compatibility with the
existing code, tests, and reports. The distribution/repository name is
the public-facing name; the import namespace is treated as a stable
internal API.

## [0.2.1] - 2026-05-25 (source-alignment audit + paper CI hardening)

Patch release over v0.2.0. The eq (2.2) numerical claim remains
`6.2391e-38` with `1.4e-4` relative error against the published
two-significant-figure value, and the unit-test count remains exactly
`60`. This release tightens the executable reproduction surface and
prepares paper PDF generation to run reliably in CI/CD.

### Changed (0.2.1)

- Hardened the verification CLI's internal pytest subprocess against
  user-environment plugin leakage by setting `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`
  by default and recording a bounded timeout result instead of allowing a hung
  subprocess to block the verification run indefinitely.
- Tightened the eq (2.2) source-match tolerance from `0.5` relative
  error to `1e-3`, matching the deviation-ledger policy and preventing
  an overly loose pass condition from masquerading as reproduction.
- Added `docs/SOURCE_CODE_ALIGNMENT_AUDIT.md`, mapping each executable
  source-PDF claim to its code anchor and documenting where source
  constants end and computed values begin.
- Added `docs/PAPER_SCIENTIFIC_READINESS_AUDIT.md`, documenting that
  the manuscript is suitable as a reproducibility-artifact paper, not
  as an original mathematics paper, and recording the CI/CD PDF
  production boundary.
- Updated `paper/main.tex`, `paper/sections/*`, and `paper/README.md`
  from `v0.2.1-draft` to `v0.2.1`, with the paper positioned as a
  reproduction artifact rather than a proof-verification paper.
- Hardened `.github/workflows/paper.yml` so `v*` tag pushes also build
  the paper, and added an explicit non-empty `paper/main.pdf`
  validation step before uploading the workflow artifact.
- Refreshed tracked verification evidence so the source hash manifest binds to
  the updated `src/erdos_ant/*` implementation.

### Audit log (0.2.1)

The source-code alignment audit found that `6.24e-38` is used as a
published comparison target, not as the generated output. The computed
value is still obtained from the remarks PDF eq (2.2) formula using
`mpmath` at 200-bit precision. Local PDF recompilation was not possible
in this environment because `latexmk` is not installed; paper PDF
generation is therefore delegated to the CI paper workflow and checked
there as a build artifact.

## [0.2.0] - 2026-05-25 (positioning + jargon overhaul)

Documentation-only minor release. **No source-code change** and **no
change to any numerical claim**: the verifier still returns PASS with
21/21 checks, the eq (2.2) exponent excess is still `6.2391e-38`, and
the relative error against the published value is still `1.4e-4`. The
60-test unit suite is unchanged. This release tightens the positioning
language to what an external mathematician audit found defensible and
removes terminology specific to the author's internal tooling.

### Changed (0.2.0)

- **Paper title** (`paper/main.tex`, `CITATION.cff`, `pyproject.toml`):
  `An Executable Verification Artifact for the Sawin et al. Lower Bound
  on the Erdős Unit-Distance Exponent` → `An Executable Reproduction
  Artifact for Equation (2.2) of the Erdős Unit-Distance Disproof
  Remarks Paper`. The new title (i) avoids "verification", which to a
  mathematics reader connotes formal proof verification (Lean / Coq
  kernels), and (ii) avoids "Sawin et al. lower bound", which now
  collides with Sawin's separately published explicit-lower-bound
  preprint (`δ ≈ 0.014`) — a different and out-of-scope result.
- **Theorem-style environment renamed** `verification` → `reproduction`
  in the paper, with a backward-compatible `\let\verification\reproduction`
  alias so existing `\begin{verification}` blocks still render.
- **README rewritten further**: hero paragraph rebound to eq (2.2);
  new section "What this artifact verifies, and what it only cites"
  with a four-row table separating (i) Theorem 1.1 itself, (ii) eq (2.2)
  numerical value (the only claim this artifact reproduces), (iii)
  Sawin's later explicit `δ ≈ 0.014`, and (iv) informal community
  optimisations.
- **Test count corrected to the actual `60`** everywhere. Previous
  states said `59` (paper §6.3 and `TRIPLE_INSPECTION_REPORT.md`) or
  `60+` (README and badge); pytest collects exactly `60` tests, so
  every reference is now the exact number.
- **"Independent inspection" wording softened** in paper §7.3, the
  historical checker report, and the README documentation list:
  the automated checker outputs are now framed as recorded local
  source-level evidence, with the note that none of them performs
  mathematical peer review.
- **Acknowledgements rewritten** to remove internal-tooling vocabulary
  (`Flamehaven-TOE`, `TOE-TEST cell`, `Generative Discovery Charter`)
  that was meaningful inside the author's own workflow but read as
  unexplained jargon to an external mathematics reader. The
  acknowledgement of local release checks is preserved but framed as
  recorded engineering output, not as third-party endorsement.
- **Abstract** explicitly notes that this artifact does *not*
  reproduce or verify Sawin's separately published explicit lower
  bound `δ ≈ 0.014`, and does *not* address informal `0.014` /
  `0.0318` figures in secondary coverage. The bound this artifact
  reproduces is exactly the verbatim `6.24 × 10⁻³⁸` of remarks PDF
  eq (2.2), and nothing larger.

### Audit log (0.2.0)

External two-round audit verdict on v0.1.x was "ACCEPT (code) / HOLD
(publication-surface positioning)". This release closes the four
positioning items the second audit flagged: title scope, "Sawin et
al. lower bound" → eq (2.2) binding, "three independent" → measured
wording, and test-count inconsistency. The reviewer's fifth
suggestion (a "what we verify vs what we only cite" table) is added
to the README. The reviewer's sixth suggestion (GitHub About text
revision) is a UI-level edit on `github.com/Flamehaven-Labs/openai-erdos-eq22-reproduction`
that does not affect this commit; the suggested replacement matches
the new `pyproject.toml` `description` field.

## [0.1.4] - 2026-05-25 (placeholder fill-in)

Patch release over v0.1.3. No source-code, claim, or numerical change;
the verifier still returns PASS with eq (2.2) excess `6.2391e-38`
(rel.err `1.4e-4`). This release exists only to substitute the two
deferred values that became known after v0.1.3 was published:

### Changed (0.1.4)

- `paper/main.tex` abstract footnote: `<COMMIT_HASH>` and `<ZENODO_DOI>`
  placeholders replaced with the actual values — commit `c8fe529`
  (the v0.1.3 tag commit) and DOI [10.5281/zenodo.20377950](https://doi.org/10.5281/zenodo.20377950) (the v0.1.3 Zenodo deposit).
- `paper/sections/07_reproducibility.tex` reproducibility table:
  `Commit hash` row now reads `c8fe529 (v0.1.3 release tag)`; `DOI
  (this release)` row now resolves to the v0.1.3 DOI link.
- `CITATION.cff`: bump `version` to `0.1.4`; add top-level `doi` field
  pointing at `10.5281/zenodo.20377950` (so the GitHub "Cite this
  repository" sidebar and Zenodo cross-link both resolve to a real
  DOI rather than to "issued upon publish").
- `README.md`: Citation section now lists the v0.1.3 DOI as the latest
  paper-bearing DOI alongside the v0.1.1 source-only DOI; the bibtex
  block points at the v0.1.3 DOI.

### Audit log (0.1.4)

This release closes the two placeholder items that v0.1.3's CHANGELOG
explicitly deferred to v0.1.4. With this commit, no `<COMMIT_HASH>` or
`<ZENODO_DOI>` token remains in the paper sources.

## [0.1.3] - 2026-05-25 (release-surface closure)

First release with the accompanying paper compiled, attached, and free
of margin-overflow / pagination defects. Closes the audit-round-2 HOLD
items that were left open on v0.1.2 ("PDF absent, placeholders,
release-surface issues"). No source-code or numerical-claim changes
relative to v0.1.2; this is a paper / README / packaging release.

### Added (0.1.3)

- `paper/main.pdf` — compiled paper bundled in the tag commit and
  attached as a GitHub release asset. First release in which the PDF
  is part of the tagged source tree.
- `paper/main.tex`: `\DeclareUrlCommand{\tname}{...}` helper (built on
  the `url` package, transitively loaded by hyperref). Renders long
  test / function / path names in monospace with break opportunities
  at `_`, `/`, `.`, `:`, `-`, `(`, `)`. Replaces overflowing
  `\texttt{long\_underscored\_identifier}` calls throughout sections
  2–5 (Phase 1, Phase 2, Phase 3, eq (2.2) reproduction).
- `paper/main.tex`: `\clearpage` around `\tableofcontents`, so the ToC
  and the first section ("Background and scope") each begin on a fresh
  page.
- `docs/DEVIATION_LOG.md` cross-link from the README documentation
  index (the file already existed; it is now discoverable from the
  README).

### Changed (0.1.3)

- `README.md`: full rewrite for GitHub-reader flow. New section order
  is What This Is, Quick Start, Verification path, Evidence,
  Phase-by-phase description, Known limits, Documentation, Citation.
  The hero paragraph under the badges now states what the artifact is
  in one sentence and links to the OpenAI announcement. Attribution
  corrected from "OpenAI / Sawin disproof" to the nine named authors
  of the remarks PDF (Alon, Bloom, Gowers, Litt, Sawin, Shankar,
  Tsimerman, Wang, Wood). The secondary-coverage clarification (the
  figures `0.014` and `0.0318` do not appear verbatim in the formal
  PDFs) is now its own section instead of a buried bullet in Known
  limits. The automated-checker report is framed as recorded engineering
  output, not third-party endorsement. The "Zenodo deposit contents"
  section was dropped (not a common pattern on GitHub READMEs).
- `paper/main.tex`: bump `\date{}` to `Version 0.1.3 --- 2026-05-25`.
- `paper/sections/07_reproducibility.tex`: bump `Version (paper)` to
  `v0.1.3`.
- `CITATION.cff`: bump `version` to `0.1.3`.

### Audit log (0.1.3)

The external audit's round-2 verdict was ACCEPT for the code artifact
and HOLD UNTIL RELEASE ARTIFACT FINALIZATION for the publication
package, with three specific release-surface reasons: (i) PDF absent
from the tracked repository, (ii) `<COMMIT_HASH>` and `<ZENODO_DOI>`
placeholders, (iii) layout defects in the compiled PDF (margin
overflow on long identifiers, ToC and section-1 sharing a page with
the abstract). This release closes (i) and (iii). The two placeholders
remain in `paper/sections/07_reproducibility.tex` because the Zenodo
DOI for this release is only issued at GitHub-Release-publish time;
they will be filled in a v0.1.4 follow-up once the DOI is known. The
v0.1.2 tag (commit `b074344`) is preserved as the pre-closure
snapshot; the audit reviewed `2fee65f`/`db14fbe`/`90eac09`, all of
which remain unchanged.

## [0.1.2] - 2026-05-25 (round 2 polish)

### Added (round 2)

- `--write-evidence` flag on `erdos-ant-verify` / `python -m erdos_ant.verify` / `scripts/verify.py`. Default is now **frozen-report mode**: the verification runs, prints the verdict + summary, and does NOT touch tracked evidence files. Maintainers pass `--write-evidence` to refresh `reports/verification_result.json` and `reports/verification_report.md`.
- `--quiet` flag on the same command for verdict-only output.
- CI workflow `verify` job now uses `python -m erdos_ant.verify` (exit code as verdict) plus a `--write-evidence` re-run that fails if the tracked evidence differs from the freshly generated version by anything other than the timestamp line.

### Changed (round 2)

- `README.md` author/citation section: the `paper/main.pdf` direct link was replaced by `LaTeX source in paper/main.tex. The compiled PDF is produced as a CI/release artifact once the paper text is finalized; it is not committed to the repository.` This closes the audit finding that the README was promising a file not present in the tracked repository.
- `README.md` Zenodo deposit contents section reordered: README + CITATION + LaTeX source come first, with the compiled PDF described as a release-asset attachment rather than a tracked file.
- `paper/main.tex` abstract and `paper/sections/07_reproducibility.tex`: reproduction commands updated to reflect frozen-report-mode default (`python -m erdos_ant.verify` for the verdict, `--write-evidence` to also refresh the tracked JSON certificate).

### Audit log (round 2)

External audit re-checked v0.1.2 first commit (`2fee65f`) and accepted the code artifact; the remaining HOLD reasons were release-surface issues (PDF absent, placeholders, regenerated-report timestamps dirtying the tree). The round-2 commit (`db14fbe` + this commit) addresses all three release-surface points; the compiled PDF and DOI fill-in remain pending until the actual v0.1.2 release tag is published on GitHub.

## [0.1.2] - 2026-05-25 (round 1)

### Added

- `src/erdos_ant/verify.py` — verification logic moved here from `scripts/verify.py`. Reachable as `python -m erdos_ant.verify` and the console script `erdos-ant-verify` (fixed entry point in `pyproject.toml`).
- SHA-256 manifest of source files in `reports/verification_result.json` and `reports/verification_report.md`. Binds the numerical claim in the paper to the exact source-file state at verify time.
- `reports/verification_result.json`, `reports/verification_report.md`,
  historical source-level checker outputs, and the historical checker
  summary are now tracked in git as frozen evidence (previously
  gitignored despite being referenced in README/CHANGELOG).
- Phase 2 regression test: two-non-principal-primes case `(3, 7)` confirms the `h = 2` partition is trivial (all candidates in the same class).

### Changed

- `src/erdos_ant/genus_class_field.py` — Phase 2 ideal-class pigeonhole math corrected. In `Cl(K)` of order 2, `[P_j] = [cP_j]`, so the choice of `eps_j` does NOT change the ideal class of `A_eps`. All `2^s` candidates therefore land in the same class, determined by the parity of non-principal primes in `split_primes`. (Audit finding: the previous code split `(29, 3)` into 2+2 across classes; this was mathematically incorrect.)
- `src/erdos_ant/sawin_multiquadratic.py` — removed `+ 1.0` slack in `admissible = r_bound <= gs_threshold + 1.0`. For the documented Sawin parameters the strict inequality `6 <= 6.25` holds, so the slack was unnecessary and could mask a wrong admissible verdict for other parameter choices.
- `pyproject.toml` — `[tool.pytest.ini_options]` now sets `pythonpath = ["src"]`, so `pytest -q` works from a clean checkout without `pip install -e .` or manual `PYTHONPATH`.
- `pyproject.toml` — console script fixed: `erdos-ant-verify = "erdos_ant.verify:main"` (was pointing to a non-existent `erdos_ant.cli:main`).
- `scripts/verify.py` — thin shim delegating to `erdos_ant.verify.main()`.
- `paper/sections/04_phase3.tex` — wording "The tower is infinite" softened to "By the cited Golod--Shafarevich theorem, this admissibility implies the tower is infinite. The artifact verifies the admissibility inequality only; it does not itself prove or compute the infinitude." (Audit finding: original wording risked being read as a computational verification of the infinite tower.)
- `paper/main.tex`, `paper/sections/07_reproducibility.tex` — explicit DOI citation for the predecessor release v0.1.1 (`10.5281/zenodo.20366884`); `<COMMIT_HASH>` and `<ZENODO_DOI>` placeholders annotated as "filled at v0.1.2 release-tag time".
- `.gitignore` — explicit allow-list for the tracked frozen-evidence files under `reports/`.
- `tests/test_genus_class_field.py` — `(29, 3)` mixed-genus test updated to expect 4-in-one-class (matching the corrected Phase 2 math).

### Fixed

- `python -m erdos_ant.verify` and `erdos-ant-verify` now both work after `pip install -e .`. (Previously promised in README/paper but broken.)
- `pytest -q` works from a clean checkout. (Previously `ModuleNotFoundError: No module named 'erdos_ant'`.)
- `ruff check src tests scripts` is clean. (Previously: import order + `datetime.UTC` (UP017).)

### Not Claimed

- Same as v0.1.0 / v0.1.1. The paper's §6 "Limits and explicit non-claims" lists the full set.
- The Phase 2 partition correction does NOT change the Lemma 2.2 lower bound `(k+1)^s / h(K) = 2`; the bound is still met, just by a single populated fiber rather than a split partition.

## [0.1.1] - 2026-05-24

### Added

- `CITATION.cff` — Citation File Format v1.2.0 metadata recognized by Zenodo and GitHub. Carries the artifact framing as `type: software` (executable verification artifact, not original research) with five primary mathematical references.
- `paper/` — LaTeX source of the accompanying verification paper:
  - `main.tex` using a custom `Verification` environment instead of `Theorem` (the paper does NOT claim a new mathematical result).
  - 8 section files: Background, Phase 1/2/3, central eq (2.2) reproduction, Limits, Reproducibility, Acknowledgements.
  - `references.bib` with 8 entries (OpenAI proof, Sawin remarks, Erdős 1946, Golod-Shafarevich, Cox, Hajir-Maire, mpmath, Kalai blog as secondary).
  - `paper/README.md` documenting compile paths (local, Overleaf, CI).
- `.github/workflows/paper.yml` — honesty-grep scan ("we prove", banned buzzwords) + latexmk PDF compile + workflow artifact upload.
- `reports/` — frozen outputs from a local source-level check stack run against this artifact:
  - historical project-specific source-level checker JSON.
  - additional historical local source-level checker outputs.
  - historical checker summary.

### Changed

- None. v0.1.0 source code is unchanged; v0.1.1 is purely additive (citation metadata + paper + inspection reports).

### Not Claimed

- Same as v0.1.0. The paper restates the non-claims explicitly in its own §6 "Limits and non-claims".

## [0.1.0] - 2026-05-24

### Added

- Initial public release as a standalone reproducibility artifact, extracted from the `Flamehaven-TOE` TOE-TEST cell for the OpenAI/Erdős unit-distance integration.
- `erdos_ant.algebraic_geometry` — Phase 0: core dataclasses, 3-field `SourceClaim` provenance, `ProofDeltaFormula`, `HighDensityVacuumConfiguration` research probe, `GolodShafarevichConstraint`.
- `erdos_ant.imaginary_quadratic_lattice` — Phase 1: `h(K)=1` lattices (`Z[i]`, `Z[ω]`, `Z[√-2]`) with exact unit-distance counting.
- `erdos_ant.genus_class_field` — Phase 2: `K = Q(√-5)`, `h = 2`, explicit Lemma 2.2 pigeonhole, genus-theoretic Hilbert class field.
- `erdos_ant.sawin_multiquadratic` — Phase 3: finite checkable parts of the Sawin multi-quadratic construction. mpmath-200-bit evaluation of remarks PDF eq (2.2), reproducing `~ 6.24 × 10⁻³⁸` to 0.01% relative error.
- `scripts/verify.py` — end-to-end verification, writes `reports/verification_result.json` and `reports/verification_report.md`.
- `scripts/fetch_pdfs.py` — downloads and extracts text from the two OpenAI PDFs for local audit.
- GitHub Actions CI on Ubuntu + Windows × Python 3.11/3.12, with separate `verify` job that confirms `verdict == "PASS"`.
- Documentation: `README.md`, `docs/PROOF_ORIGIN.md`, `docs/ARCHITECTURE.md`, `docs/REMARKS_PDF_REPRODUCTION.md`, `CONTRIBUTING.md`, `SECURITY.md`.

### Not Claimed

- No new proof of Theorem 1.1.
- No explicit construction of the infinite Golod-Shafarevich tower (Phase 4 is intentionally out of scope).
- No peer review.
- No improvement on the published bound; the reported values `0.014` and `0.0318` are not verbatim in either formal PDF.
