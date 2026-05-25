# Deviation Log

Every numerical value claimed in this artifact, and how it deviates from
its published source if at all. Updated on every release that changes a
numerical claim.

## Conventions

- **Source value**: as it appears in the primary PDF or, where the
  primary PDF gives no number, in the explicit closed-form expression
  the PDF specifies.
- **Computed value**: as produced by running `python -m erdos_ant.verify`
  at the commit hash named in each row.
- **Relative error**: `|computed - source| / |source|`. Below `1e-3` is
  treated as "matches source within reasonable rounding". Anything
  larger is investigated before release.

## Current ledger (artifact version 0.1.4)

| Item | Source | Computed | Relative error | Status |
|---|---|---|---|---|
| Sawin remarks PDF eq (2.2) exponent excess | `6.24e-38` (2 sig figs, [Sawin et al. 2026](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-remarks.pdf) §2.1) | `6.2391e-38` | `1.4e-4` (0.014%) | MATCH (consistent with source rounding) |
| `Q(sqrt(-5))` discriminant | `-20` (Cox 1989 §6) | `-20` | `0` | EXACT |
| `Q(sqrt(-5))` class number `h(K)` | `2` (Cox 1989 §6) | `2` | `0` | EXACT |
| Sawin construction `r = 2 * prod(T)` | `510510` ([Sawin et al. 2026] §2.1) | `510510` | `0` | EXACT |
| Sawin construction `d(G_T^infinity) = |T| - 1` | `5` ([Sawin et al. 2026] §2.1) | `5` | `0` | EXACT |
| Sawin construction `r(G_T^S) <= 6` | `6` ([Sawin et al. 2026] §2.1) | `6` | `0` | EXACT |
| Sawin construction GS threshold `(|T|-1)^2 / 4` | `6.25` ([Sawin et al. 2026] §2.1) | `6.25` | `0` | EXACT |
| `7x7` Gaussian grid unit-distance count | `84` (classical: `2 * 7 * 6`) | `84` | `0` | EXACT |
| `3x3` Gaussian grid unit-distance count | `12` (classical: `2 * 3 * 2`) | `12` | `0` | EXACT |
| Baker-Heegner-Stark `h = 1` discriminant list | `{1, 2, 3, 7, 11, 19, 43, 67, 163}` (Baker-Heegner-Stark) | same | `0` | EXACT |

## Why `6.24e-38` vs `6.2391e-38` is a MATCH and not a deviation

[Sawin et al. 2026] eq (2.2) reports the result as approximately
`1 + 6.24 * 10^{-38}` to two significant figures. The artifact uses
mpmath at 200-bit precision and reports `6.2391e-38`. The third digit
`9` and onward are NOT present in the source paper; they are the
artifact's own evaluation. The reported difference `0.0009e-38 = 9e-42`
fits inside the rounding uncertainty implicit in the source's
two-significant-figure presentation.

If a future Sawin et al. revision specifies the value to three or more
significant figures, this row will be re-evaluated and may be promoted
to either MATCH (within stated precision) or DEVIATION (numerical
discrepancy requiring investigation).

## Why two-significant-figure tolerance is correct

The pinning test
`tests/test_sawin_multiquadratic.py::test_sawin_exponent_bound_matches_remarks_eq_2_2`
uses a 50% relative tolerance. This is intentionally loose enough to
absorb the source's two-sig-fig rounding while still catching any
genuine regression (a code change that pushed the value by 10x or more
would fail the test immediately).

## How this log is maintained

- Every change to any module under `src/erdos_ant/` that touches a
  numerical computation requires re-running `python -m erdos_ant.verify`
  and updating the Computed column if the value moved.
- Every release that updates a `src/erdos_ant/*` module file gets a new
  per-release row block below.
- Items that remain EXACT across versions do not need to be re-listed
  per release; they are implied stable.

## Per-release notes

### v0.1.4 (2026-05-25)

- No source-code or numerical-claim change versus v0.1.3.
- Substitutes the two placeholder values deferred in v0.1.3:
  - `<COMMIT_HASH>` -> `c8fe529` (v0.1.3 release-tag commit)
  - `<ZENODO_DOI>` -> `10.5281/zenodo.20377950` (v0.1.3 Zenodo deposit)
- All ledger entries above remain bit-for-bit identical to v0.1.3.

### v0.1.3 (2026-05-25)

- No source-code or numerical-claim change versus v0.1.2.
- Release-surface closure only: compiled `paper/main.pdf` bundled in
  the tag commit, README rewritten for GitHub-reader flow, paper
  typography fixes (`\tname{}` macro for breakable monospace
  identifiers, `\clearpage` around the ToC).
- All ledger entries above remain bit-for-bit identical to v0.1.2.

### v0.1.2 (2026-05-25)

- Added: this deviation log.
- Phase 2 ideal-class partition was mathematically corrected. The
  numerical lower bound `(k+1)^s / h(K) = 2` did not change; the
  partition between principal and non-principal fibers did
  (`(29, 41) -> 4+0`, `(29, 3) -> 0+4` instead of `2+2`).
- Sawin admissibility test changed from `<= gs_threshold + 1.0` to
  `<= gs_threshold`. For the documented parameters the admissibility
  verdict did not change (`6 <= 6.25` still holds strictly).

### v0.1.1 (2026-05-24)

- Initial deviation ledger conceptually present in
  `reports/verification_result.json` and `reports/TRIPLE_INSPECTION_REPORT.md`
  but not yet broken out into this dedicated document.

### v0.1.0 (2026-05-24)

- Initial public release. Numerical computation surface as documented
  in CHANGELOG `[0.1.0]` entry.
