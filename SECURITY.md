# Security Policy

## Scope

This repository is a **pure mathematical reproducibility artifact**. It performs no network operations at runtime (except `scripts/fetch_pdfs.py`, which downloads two PDFs over HTTPS), accesses no credentials, and writes only to a local `reports/` directory.

The primary security-relevant question is **trust in the published numerical claims** rather than traditional attack surface.

## Trust Boundary

- **Local boundary**: all numerical evaluation, tests, and report generation. No network access during `pytest` or `scripts/verify.py`.
- **External-provider boundary**: `scripts/fetch_pdfs.py` downloads two PDFs from `cdn.openai.com` over HTTPS. The PDFs are not redistributed; they are written to `docs/pdf_extracts/` (gitignored) for local audit.
- **Secret-handling boundary**: none. The repository requires no API keys, tokens, or credentials.

## Safe Use Guidance

- **Deployment**: this is a library, not a service. There is no production deployment context.
- **Credential guidance**: not applicable.
- **Unsupported or weak modes**: do not interpret `claim_tier="research_only_proxy"` outputs as proofs. Do not interpret the Phase 0 `HighDensityVacuumConfiguration.calculate_density_metrics()` result as a verification of any mathematical claim — it is a research probe with explicit `not_claimed` fields.

## Numerical Trust

- The eq (2.2) reproduction depends on `mpmath` at 200-bit precision. If `mpmath` is downgraded or the precision setting is changed, the result will collapse to 0 via float64 catastrophic cancellation.
- All test assertions use `pytest.approx` with documented tolerances. The Sawin eq (2.2) check uses 50% relative tolerance because the published value is given to two significant figures; this is intentionally loose enough to absorb the rounding while catching genuine regressions.

## Reporting

For correctness issues (incorrect numerical results, broken citations, missing caveats), open a public GitHub issue.

For any security-sensitive concern that should not be public, contact the repository maintainers privately via GitHub (`@Flamehaven-Labs`).
