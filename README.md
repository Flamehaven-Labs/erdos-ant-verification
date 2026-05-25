# OpenAI Erdős Unit-Distance Disproof: Eq. (2.2) Executable Reproduction

[![CI](https://github.com/Flamehaven-Labs/openai-erdos-eq22-reproduction/actions/workflows/ci.yml/badge.svg)](https://github.com/Flamehaven-Labs/openai-erdos-eq22-reproduction/actions/workflows/ci.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20377950.svg)](https://doi.org/10.5281/zenodo.20377950)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/)
[![Tests: 60](https://img.shields.io/badge/tests-60-brightgreen.svg)](tests/)
[![Reproduction: 0.014%](https://img.shields.io/badge/eq(2.2)%20rel.%20err.-0.014%25-brightgreen.svg)](docs/REMARKS_PDF_REPRODUCTION.md)

Independent Python reproduction for the 2026 OpenAI/Sawin disproof of the Erdős unit-distance conjecture: `mpmath`-200-bit check of remarks PDF equation (2.2), matching the published value at 0.014% relative error. MIT, NumPy + `mpmath` only. **Not** a new proof, **not** a verification of any sharpened bound (e.g., Sawin's separately published `δ ≈ 0.014`), **not** peer-reviewed.

## What this is

In May 2026, a reasoning model from OpenAI produced a construction that refutes the planar unit-distance conjecture of Erdős. The result was announced on the [OpenAI index page](https://openai.com/index/model-disproves-discrete-geometry-conjecture/) and written up in two PDFs (linked under [Primary sources](#primary-sources)). The substantive mathematics is the work of the nine human authors named above.

The remarks paper contains a single rigorous numerical lower bound — equation (2.2) — that, for the explicit choice `T = {3, 5, 7, 11, 13, 17}`, `S = {101, ∞}`, `L_T = Q(√5, √13, √17, √21, √33)`, gives an exponent excess `δ_excess ≈ 6.24 × 10⁻³⁸` over the classical Erdős exponent. The number is small enough that a naive `float64` evaluation of eq (2.2) collapses to zero by catastrophic cancellation. The published proof is correct but ships no executable evaluation of that number.

This repository:

- re-derives eq (2.2) in `mpmath` at 200-bit precision and matches the published two-significant-figure value to `1.4 × 10⁻⁴` relative error;
- implements every step of the finite, explicitly computable portion of the construction (Phase 1: imaginary quadratic lattices with `h(K) = 1`; Phase 2: `Q(√-5)` Lemma 2.2 pigeonhole via genus theory; Phase 3: Sawin multi-quadratic setup, finite parts);
- stops at the boundary of the cited Golod–Shafarevich infinitude — the artifact checks the admissibility inequality only; the tower's existence is taken as given from \cite{GolodShafarevich1964};
- ships 60 unit tests, 21 verifier checks, a CI matrix across Linux × Windows × Python 3.11/3.12, and frozen per-source-file SHA-256 evidence.

The intended reader is anyone who, having read §2 of the remarks paper, wants a citable, runnable Python implementation of eq (2.2) on which they can run their own sensitivity checks. It is not a substitute for the published proof, and it is not a peer review of it.

## Quick Start

```bash
git clone https://github.com/Flamehaven-Labs/openai-erdos-eq22-reproduction
cd openai-erdos-eq22-reproduction
pip install -e ".[dev]"

# Default: print verdict only (does not touch tracked evidence)
python -m erdos_ant.verify
```

Expected:

```
Verdict: PASS
Checks: 21/21 passed
eq (2.2) exponent excess: 6.2391e-38 (published ~6.24e-38, rel.err 0.0001)
```

To regenerate the tracked evidence files (`reports/verification_result.json` and `verification_report.md`), pass `--write-evidence`. For the full check suite (tests + lint + verifier) see [Verification path](#verification-path) below.

## Verification path

```bash
# 60 unit tests
pytest -q

# lint
ruff check src tests scripts reports

# end-to-end verifier (verdict via exit code)
python -m erdos_ant.verify
```

The verifier runs its internal pytest subprocess with external pytest
plugin autoloading disabled, so ordinary user-environment plugins do not
change the verification result. CI runs the same checks on Ubuntu ×
Windows × Python 3.11/3.12.

## Evidence

The reproduced quantity is the exponent excess `δ` in equation (2.2) of the remarks PDF — the amount by which the construction beats the classical Erdős exponent `1 + 1/(3 log₂ log₂ n)` for unit-distance pair density.

| | |
|---|---|
| Test count | 60 unit tests + 21 verifier checks, all green on CI |
| Numerical reproduction | `6.2391e-38` computed vs `≈ 6.24e-38` published — **0.014% relative error** |
| Precision needed | `mpmath` at 200-bit (float64 collapses the result to 0 via catastrophic cancellation) |
| Source manifest | per-file SHA-256 in [`reports/verification_result.json`](reports/verification_result.json) under `source_sha256_manifest` |
| Python | 3.11, 3.12 |
| Runtime deps | `numpy ≥ 1.26`, `mpmath ≥ 1.3` |
| CI | GitHub Actions, Ubuntu × Windows × Python 3.11 / 3.12 |

Concrete one-liner:

```python
from erdos_ant.sawin_multiquadratic import evaluate_sawin_exponent_bound
e = evaluate_sawin_exponent_bound()
print(f"{e.exponent_excess:.4e}")
# 6.2391e-38
```

## What this artifact verifies, and what it only cites

There are several distinct numerical and mathematical claims associated with the 2026 disproof. They are not interchangeable, and this repository covers only one of them:

| Claim | Source | This artifact … |
|---|---|---|
| Erdős unit-distance conjecture is false (∃ `δ > 0`, Theorem 1.1) | OpenAI 2026 proof PDF and remarks PDF | **cites only** — does not formalise or re-derive the proof |
| `δ_excess ≈ 6.24 × 10⁻³⁸` for the explicit `(T, S, L_T)` of remarks §2 (eq 2.2) | Remarks PDF §2.1 | **reproduces** numerically to `1.4 × 10⁻⁴` relative error |
| Sawin's later explicit lower bound `δ ≈ 0.014` | Sawin, "An explicit lower bound for the unit distance problem" ([arXiv:2605.20579](https://arxiv.org/abs/2605.20579)) | **does not verify** — different source, different construction, out of scope here |
| Various sharper `δ` from community optimisation (forums, blogs, secondary coverage) | informal | **does not verify** — values not present verbatim in either formal PDF |

If a reader has seen the larger numbers `0.014` or `0.0318` attributed to "the OpenAI/Sawin result", they were not stated verbatim in the formal proof or remarks PDF. The `6.24 × 10⁻³⁸` figure is the only rigorous numerical lower bound in those two documents, and it is the only claim this artifact pins.

## What it does (by phase)

- **Phase 1** — `h(K) = 1` imaginary quadratic lattices (`Z[i]`, `Z[ω]`, `Z[√-2]`) with exact unit-distance pair counting via the standard complex embedding.
- **Phase 2** — `K = Q(√-5)` (`h = 2`) with the Lemma 2.2 ideal-class pigeonhole made explicit; Hilbert class field `Q(i, √5)` supplied by genus theory.
- **Phase 3** — finite checkable parts of the Sawin multi-quadratic construction (`T = {3,5,7,11,13,17}`, `S = {101, ∞}`, `L_T = Q(√5, √13, √17, √21, √33)`) with `mpmath`-200-bit reproduction of remarks PDF eq (2.2).

## Known limits

- **Not a new proof.** Theorem 1.1 (existence of `δ > 0`) is proved by the authors in the source PDFs; this repository does not re-prove it.
- **Not the infinite Golod–Shafarevich tower.** Its existence is non-constructive (Hajir–Maire technique, Proposition 2.3 of the remarks PDF); no finite computation can exhibit it. The artifact verifies admissibility (`d² − 4r ≥ 0`) only — the infinitude follows from the cited theorem, not from any computation here.
- **Not peer-reviewed.** Correctness rests on the test suite passing, the 0.014% numerical reproduction, and source-readable code — not on external mathematician review.

## Trust boundary

- **Stays local**: all numerical evaluation, tests, and reports.
- **Crosses external boundary** only via `scripts/fetch_pdfs.py`, which downloads the two source PDFs over HTTPS from `cdn.openai.com`. The PDFs are **not** redistributed in this repository.
- **No secrets, no credentials, no API keys** required.

## Platform notes

- **Linux** — primary CI target (Ubuntu, Python 3.11 / 3.12).
- **macOS** — not in CI, but no platform-specific code — expected to work.
- **Windows** — secondary CI target (Python 3.11 / 3.12). PowerShell entry: `scripts/verify.ps1`.
- **WSL** — same as Linux.

## Documentation

- [`docs/PROOF_ORIGIN.md`](docs/PROOF_ORIGIN.md) — what was proved (by the authors), what was not, primary sources.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — module boundaries, claim / non-claim per layer.
- [`docs/SOURCE_CODE_ALIGNMENT_AUDIT.md`](docs/SOURCE_CODE_ALIGNMENT_AUDIT.md) — source-PDF to code mapping, hardcoding audit, slop / spaghetti boundary.
- [`docs/PAPER_SCIENTIFIC_READINESS_AUDIT.md`](docs/PAPER_SCIENTIFIC_READINESS_AUDIT.md) — paper content suitability, bibliography scope, and CI/CD PDF production boundary.
- [`docs/REMARKS_PDF_REPRODUCTION.md`](docs/REMARKS_PDF_REPRODUCTION.md) — the eq (2.2) reproduction in detail, why `mpmath` is required.
- [`docs/DEVIATION_LOG.md`](docs/DEVIATION_LOG.md) — every place a number, command, or claim in the paper differs from a published source, and why.
- [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md), [`CHANGELOG.md`](CHANGELOG.md).
- [`reports/TRIPLE_INSPECTION_REPORT.md`](reports/TRIPLE_INSPECTION_REPORT.md) — output of three automated source-level scanners (one in-house: AI-SLOP-Detector; two external: SPAR Framework, SIDRCE). Included for transparency, not as third-party endorsement; none of the three performs mathematical peer review.

## Primary sources

- OpenAI (2026), *Planar Point Sets with Many Unit Distances* — [PDF](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf)
- Alon, Bloom, Gowers, Litt, Sawin, Shankar, Tsimerman, Wang, Wood (2026), *Remarks on the Disproof of the Unit Distance Conjecture* — [PDF](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-remarks.pdf)
- OpenAI index page — [model-disproves-discrete-geometry-conjecture](https://openai.com/index/model-disproves-discrete-geometry-conjecture/)

## Citation

Preferred citation metadata lives in [`CITATION.cff`](CITATION.cff) (recognised by Zenodo and by the GitHub "Cite this repository" sidebar).

DOI is issued by Zenodo on each tagged release; see [Releases](https://github.com/Flamehaven-Labs/openai-erdos-eq22-reproduction/releases). Latest paper-bearing DOI: [10.5281/zenodo.20377950](https://doi.org/10.5281/zenodo.20377950) (v0.1.3). Predecessor source-only DOI: [10.5281/zenodo.20366884](https://doi.org/10.5281/zenodo.20366884) (v0.1.1).

```bibtex
@software{erdos_ant_verification,
  author  = {Yun, Kwansub},
  title   = {openai-erdos-eq22-reproduction: Executable Reproduction
             of Equation (2.2) in the OpenAI Erd\H{o}s Unit-Distance
             Disproof Remarks},
  version = {0.2.2},
  year    = {2026},
  doi     = {10.5281/zenodo.20377950},
  url     = {https://github.com/Flamehaven-Labs/openai-erdos-eq22-reproduction}
}
```

The companion paper (LaTeX source in [`paper/main.tex`](paper/main.tex), compiled PDF bundled in the tag commit and attached as a release asset) cites the same key. **Citing this software is not a substitute for citing the primary mathematical sources above** — please cite both.

## License

MIT — see [LICENSE](LICENSE). Project lead: Yun Kwansub ([Flamehaven Initiative](https://github.com/Flamehaven-Labs)).
