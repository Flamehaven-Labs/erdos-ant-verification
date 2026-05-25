# erdos-ant-verification

Independent Python reproduction of the **2026 OpenAI/Sawin disproof of the Erdős planar unit-distance conjecture**, including a verbatim numerical match (0.01% rel. error) to equation (2.2) of the remarks PDF.

[![CI](https://github.com/Flamehaven-Labs/erdos-ant-verification/actions/workflows/ci.yml/badge.svg)](https://github.com/Flamehaven-Labs/erdos-ant-verification/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/)
[![Tests: 50+](https://img.shields.io/badge/tests-50%2B-brightgreen.svg)](tests/)
[![Reproduction: 0.01%](https://img.shields.io/badge/eq(2.2)%20rel.%20err.-0.01%25-brightgreen.svg)](docs/REMARKS_PDF_REPRODUCTION.md)

## Author and citation

- **Project lead:** Yun Kwansub (Flamehaven Initiative)
- **Maintained by:** [Flamehaven Initiative](https://github.com/Flamehaven-Labs)
- **License:** MIT — see [LICENSE](LICENSE)
- **Citation file:** [`CITATION.cff`](CITATION.cff) — recognised by Zenodo and the GitHub "Cite this repository" sidebar
- **Accompanying paper (draft):** LaTeX source in [`paper/main.tex`](paper/main.tex). The compiled PDF is produced as a CI/release artifact once the paper text is finalized; it is **not** committed to the repository.
- **DOI:** issued by Zenodo on each tagged release — see [Releases](https://github.com/Flamehaven-Labs/erdos-ant-verification/releases). Latest source-only DOI: [10.5281/zenodo.20366884](https://doi.org/10.5281/zenodo.20366884) (v0.1.1).

## Zenodo deposit contents

When a tagged release is archived to Zenodo, the deposit contains the
full source tarball at that tag. The most relevant files for a reader
opening the Zenodo page are:

1. **`README.md`** — this file (Zenodo renders it as the deposit description)
2. **`CITATION.cff`** — formal citation metadata
3. **`paper/main.tex`** + `paper/sections/*.tex` — LaTeX source of the accompanying paper (compiled PDF is attached as a release asset once the paper text is finalized; see GitHub Releases)
4. **`reports/TRIPLE_INSPECTION_REPORT.md`** — frozen output of three independent inspection tools (AI-SLOP-Detector, SPAR Framework, SIDRCE SaaS)
5. **`reports/verification_result.json`** + `verification_report.md` — frozen evidence of `python -m erdos_ant.verify` at the tagged commit, including per-source-file SHA-256 manifest
6. Full source tree (`src/`, `tests/`, `scripts/`, `docs/`, `paper/`)

## Why This Exists

- **Who it is for**: anyone who wants a citable, runnable reference implementation of the finite, explicitly checkable parts of the OpenAI/Sawin construction.
- **What pain it removes**: the published PDFs contain rigorous proofs but no associated code. Re-deriving the numerical lower bound `~ 6.24 × 10⁻³⁸` from eq (2.2) by hand is non-trivial (float64 catastrophic cancellation collapses the naive evaluation to 0).
- **What makes it different**: independent, standalone, MIT-licensed, no dependence on SageMath/PARI, pure NumPy + mpmath, fully deterministic, CI-verified on Linux + Windows.

## Quick Start

```bash
git clone https://github.com/Flamehaven-Labs/erdos-ant-verification
cd erdos-ant-verification
pip install -e ".[dev]"

# Run the verification (writes reports/verification_result.json + .md)
python scripts/verify.py
```

Expected:

```
Verdict: PASS
```

## Verification Path

```bash
# tests (50+ tests, ~1s)
pytest -q

# lint
ruff check src tests

# end-to-end verification
python scripts/verify.py
```

## Platform Notes

- **Linux**: primary CI target (Ubuntu, Python 3.11/3.12).
- **macOS**: not tested in CI, but no platform-specific code — expected to work.
- **Windows**: secondary CI target (Python 3.11/3.12). PowerShell entry: `scripts/verify.ps1`.
- **WSL**: same as Linux.

## Trust Boundary

- **Stays local**: all numerical evaluation, tests, and reports.
- **Crosses external boundary** only via `scripts/fetch_pdfs.py`, which downloads the two OpenAI PDFs over HTTPS from `cdn.openai.com`. The PDFs are NOT redistributed in this repository.
- **No secrets, no credentials, no API keys** required.

## What It Does

- **Phase 1** — `h(K) = 1` imaginary quadratic lattices (`Z[i]`, `Z[ω]`, `Z[√-2]`) with exact unit-distance pair counting via the standard complex embedding.
- **Phase 2** — `K = Q(√-5)` (`h = 2`) with the Lemma 2.2 ideal-class pigeonhole made explicit; Hilbert class field `Q(i, √5)` supplied by genus theory.
- **Phase 3** — finite checkable parts of the Sawin multi-quadratic construction (`T = {3,5,7,11,13,17}`, `S = {101,∞}`, `L_T = Q(√5,√13,√17,√21,√33)`) with mpmath-200-bit reproduction of remarks PDF eq (2.2).

## Evidence

| | |
|---|---|
| Test count | 50+ tests, all green on CI |
| Numerical reproduction | `6.2391e-38` computed vs `~ 6.24e-38` published — **0.01% relative error** |
| Precision needed | mpmath, 200-bit (float64 collapses the result to 0 via catastrophic cancellation) |
| Python | 3.11, 3.12 |
| Runtime deps | numpy ≥ 1.26, mpmath ≥ 1.3 |
| CI | GitHub Actions, Ubuntu + Windows × Python 3.11/3.12 |

Concrete reproduction:

```python
from erdos_ant.sawin_multiquadratic import evaluate_sawin_exponent_bound
e = evaluate_sawin_exponent_bound()
print(f"{e.exponent_excess:.4e}")
# 6.2391e-38
```

## Documentation

- [`docs/PROOF_ORIGIN.md`](docs/PROOF_ORIGIN.md) — what was proved (by them), what was not, primary sources.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — module boundaries, claim/non-claim per layer, charter-style result tags.
- [`docs/REMARKS_PDF_REPRODUCTION.md`](docs/REMARKS_PDF_REPRODUCTION.md) — the eq (2.2) reproduction in detail, why mpmath is required.
- [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md), [`CHANGELOG.md`](CHANGELOG.md).

## Known Limits

- **Not a new proof.** Theorem 1.1 (existence of `δ > 0`) is proved by OpenAI / Sawin et al. in the source PDFs; this repository does not re-prove it.
- **Not the infinite Golod-Shafarevich tower.** Its existence is non-constructive (Hajir–Maire technique, Proposition 2.3 of the remarks PDF); no finite computation can exhibit it. Phase 4 is therefore out of scope for any artifact of this kind.
- **Not peer-reviewed.** Correctness rests on the test suite passing, the 0.01% numerical reproduction, and source-readable code — not on external mathematician review.
- **No improvement on the published bound.** The figures `0.014` and `0.0318` appearing in secondary coverage do not appear verbatim in either formal PDF; the only verbatim numerical lower bound is `~ 6.24 × 10⁻³⁸`.

## Primary Sources

- OpenAI (2026), *Planar Point Sets with Many Unit Distances* — [PDF](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf)
- Alon, Bloom, Gowers, Litt, Sawin, Shankar, Tsimerman, Wang, Wood (2026), *Remarks on the Disproof of the Unit Distance Conjecture* — [PDF](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-remarks.pdf)
- [OpenAI index page](https://openai.com/index/model-disproves-discrete-geometry-conjecture/)

## Development

```bash
pip install -e ".[dev]"
pytest -q
ruff check src tests
python scripts/verify.py
```

## License

MIT — see [LICENSE](LICENSE).
