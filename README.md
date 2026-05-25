# erdos-ant-verification

[![CI](https://github.com/Flamehaven-Labs/erdos-ant-verification/actions/workflows/ci.yml/badge.svg)](https://github.com/Flamehaven-Labs/erdos-ant-verification/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/)
[![Tests: 60+](https://img.shields.io/badge/tests-60%2B-brightgreen.svg)](tests/)
[![Reproduction: 0.014%](https://img.shields.io/badge/eq(2.2)%20rel.%20err.-0.014%25-brightgreen.svg)](docs/REMARKS_PDF_REPRODUCTION.md)

Independent Python reproduction of the finite, numerically checkable parts of the 2026 disproof of the Erdős planar unit-distance conjecture by Alon, Bloom, Gowers, Litt, Sawin, Shankar, Tsimerman, Wang, and Wood. Verified to 0.014% relative error against equation (2.2) of the remarks PDF.

## What This Is

In 2026, an OpenAI assistant identified a construction that disproves the planar unit-distance conjecture of Erdős. The result was announced on the [OpenAI index page](https://openai.com/index/model-disproves-discrete-geometry-conjecture/) and written up in two PDFs (linked under [Primary sources](#primary-sources)). The underlying mathematics is the work of nine named authors.

The proof contains a numerical lower bound — equation (2.2) of the remarks PDF — that asserts an explicit, finite-precision excess `δ ≈ 6.24 × 10⁻³⁸` above the classical Erdős exponent for a specific multi-quadratic construction. The number is small enough that a naive `float64` evaluation collapses to zero by catastrophic cancellation. The published proof is correct but ships no code.

This repository:

- re-derives eq (2.2) in `mpmath` at 200-bit precision and matches the published number to within `1.4 × 10⁻⁴` (0.014%) relative error;
- checks every step of the construction that is amenable to finite computation (Phase 1: small `h(K)=1` lattices; Phase 2: `Q(√-5)` genus theory; Phase 3: Sawin multi-quadratic, finite parts);
- stops at the boundary of the cited Golod–Shafarevich infinitude — the artifact verifies admissibility, not the infinite tower itself;
- ships 60+ unit tests, a CI matrix across Linux and Windows, and frozen per-source-file SHA-256 evidence.

It is intended as a citable, runnable reference for the numerical content of the disproof — not as an independent mathematical contribution.

## Quick Start

```bash
git clone https://github.com/Flamehaven-Labs/erdos-ant-verification
cd erdos-ant-verification
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
# 60+ unit tests
pytest -q

# lint
ruff check src tests

# end-to-end verifier (verdict via exit code)
python -m erdos_ant.verify
```

CI runs this exact sequence on Ubuntu × Windows × Python 3.11/3.12.

## Evidence

The reproduced quantity is the exponent excess `δ` in equation (2.2) of the remarks PDF — the amount by which the construction beats the classical Erdős exponent `1 + 1/(3 log₂ log₂ n)` for unit-distance pair density.

| | |
|---|---|
| Test count | 60+ unit tests + 21 verifier checks, all green on CI |
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

## A note on secondary coverage

The figures `0.014` and `0.0318` that have circulated in secondary coverage of the result do **not** appear verbatim in either formal PDF. The only verbatim numerical lower bound in the remarks PDF is `≈ 6.24 × 10⁻³⁸`, which is what this artifact reproduces. If a reader has seen the larger numbers attributed to this result, they were not stated in the formal source.

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
- [`docs/REMARKS_PDF_REPRODUCTION.md`](docs/REMARKS_PDF_REPRODUCTION.md) — the eq (2.2) reproduction in detail, why `mpmath` is required.
- [`docs/DEVIATION_LOG.md`](docs/DEVIATION_LOG.md) — every place a number, command, or claim in the paper differs from a published source, and why.
- [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md), [`CHANGELOG.md`](CHANGELOG.md).
- [`reports/TRIPLE_INSPECTION_REPORT.md`](reports/TRIPLE_INSPECTION_REPORT.md) — output of three scanners that were run against this repository. **Note on independence:** one of them (AI-SLOP-Detector) is maintained by the same author as this repository; the other two (SPAR Framework, SIDRCE SaaS) are external. The report is included as recorded scanner output, not as a third-party endorsement.

## Primary sources

- OpenAI (2026), *Planar Point Sets with Many Unit Distances* — [PDF](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf)
- Alon, Bloom, Gowers, Litt, Sawin, Shankar, Tsimerman, Wang, Wood (2026), *Remarks on the Disproof of the Unit Distance Conjecture* — [PDF](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-remarks.pdf)
- OpenAI index page — [model-disproves-discrete-geometry-conjecture](https://openai.com/index/model-disproves-discrete-geometry-conjecture/)

## Citation

Preferred citation metadata lives in [`CITATION.cff`](CITATION.cff) (recognised by Zenodo and by the GitHub "Cite this repository" sidebar).

DOI is issued by Zenodo on each tagged release; see [Releases](https://github.com/Flamehaven-Labs/erdos-ant-verification/releases). The predecessor source-only DOI is [10.5281/zenodo.20366884](https://doi.org/10.5281/zenodo.20366884) (v0.1.1).

```bibtex
@software{erdos_ant_verification,
  author  = {Yun, Kwansub},
  title   = {erdos-ant-verification: An Executable Verification Artifact
             for the 2026 Disproof of the Erd\H{o}s Unit-Distance Conjecture},
  version = {0.1.3},
  year    = {2026},
  doi     = {10.5281/zenodo.20366884},
  url     = {https://github.com/Flamehaven-Labs/erdos-ant-verification}
}
```

The companion paper (LaTeX source in [`paper/main.tex`](paper/main.tex), compiled PDF bundled in the tag commit and attached as a release asset starting with `v0.1.3`) cites the same key. **Citing this software is not a substitute for citing the primary mathematical sources above** — please cite both.

## License

MIT — see [LICENSE](LICENSE). Project lead: Yun Kwansub ([Flamehaven Initiative](https://github.com/Flamehaven-Labs)).
