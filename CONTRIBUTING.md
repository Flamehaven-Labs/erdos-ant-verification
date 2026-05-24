# Contributing

## Scope

This repository is a **reproducibility artifact**, not an evolving research codebase. Contributions are welcome in the following narrow categories:

- Bug fixes (incorrect numerical results, broken tests, packaging issues).
- Documentation improvements (clarity, typos, additional cross-references to the source PDFs).
- Additional regression tests pinning published mathematical facts.
- CI hardening (additional Python versions, additional platforms).

Out of scope:

- New mathematical claims that go beyond the published PDFs.
- Speculative extensions (Phase 4, infinite tower construction, etc.) — these are intentionally excluded.
- Renaming the module structure (modules are pinned for citability).

## Before Opening A Change

- Read the [README](README.md).
- Read [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for module boundaries and the claim/non-claim contract per layer.
- Run the verification path:

```bash
pytest -q
ruff check src tests
python scripts/verify.py
```

## Change Discipline

- **Docs must match behavior.** If you change a function's return shape, update its docstring and any doc that quotes it.
- **Claims must not exceed evidence.** Every numerical claim in code or docs must trace to (a) a primary PDF, or (b) an arithmetic computation runnable in this repository, or (c) be explicitly tagged as `not_claimed`.
- **Caveats stay visible.** The `not_claimed` lists and `claim_tier` fields are part of the public contract; do not remove or weaken them.
- **No silent fallbacks.** If a computation cannot produce a value, return `0.0` / `None` and log; never substitute a published external value as a fallback.

## Verification

```bash
pytest -q                       # 50+ unit tests
ruff check src tests            # lint
python scripts/verify.py        # end-to-end, writes reports/verification_result.json
```

CI must be green before merge.

## Pull Request Notes

Summarize:

- **Behavior change**: what calculation, signature, or output changed.
- **Trust-surface impact**: any change to claim tiers, `not_claimed` lists, or `verified_numerical_in_formal_pdf` flags.
- **Docs impact**: which docs were updated to match.

If the change touches the numerical reproduction in `sawin_multiquadratic.py`, include the new `exponent_excess` value in the PR description and its relative error vs the published `~ 6.24e-38`.
