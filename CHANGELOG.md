# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
