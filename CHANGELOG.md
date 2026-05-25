# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2026-05-25

### Added

- `src/erdos_ant/verify.py` — verification logic moved here from `scripts/verify.py`. Reachable as `python -m erdos_ant.verify` and the console script `erdos-ant-verify` (fixed entry point in `pyproject.toml`).
- SHA-256 manifest of source files in `reports/verification_result.json` and `reports/verification_report.md`. Binds the numerical claim in the paper to the exact source-file state at verify time.
- `reports/verification_result.json`, `reports/verification_report.md`, `reports/slop_scan.json`, `reports/spar_review_result.json`, `reports/TRIPLE_INSPECTION_REPORT.md` are now tracked in git as frozen evidence (previously gitignored despite being referenced in README/CHANGELOG).
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
- `reports/` — frozen outputs from a three-tool inspection stack run against this artifact:
  - `reports/slop_scan.json` — AI-SLOP-Detector v3.7.5 (clean, 6/6 files, weighted deficit 2.83).
  - `reports/spar_review.py` + `spar_review_result.json` — SPAR Framework v0.5.0 (ACCEPT, score 100/100).
  - `reports/sidrce_certification.yaml` — SIDRCE SaaS v1.1.15 (CERTIFIED, omega 0.9289, signed trace chain).
  - `reports/TRIPLE_INSPECTION_REPORT.md` — summary of all three.

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
