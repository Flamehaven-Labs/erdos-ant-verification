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

## Current ledger (artifact version 0.2.5)

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

## Why the eq (2.2) tolerance is strict enough

The pinning test
`tests/test_sawin_multiquadratic.py::test_sawin_exponent_bound_matches_remarks_eq_2_2`
uses a `1e-3` relative tolerance. This matches the ledger policy above:
below `1e-3` is treated as consistent with the two-significant-figure
source value, while anything larger requires investigation before
release. The observed error is `1.4e-4`.

## How this log is maintained

- Every change to any module under `src/erdos_ant/` that touches a
  numerical computation requires re-running `python -m erdos_ant.verify`
  and updating the Computed column if the value moved.
- Every release that updates a `src/erdos_ant/*` module file gets a new
  per-release row block below.
- Items that remain EXACT across versions do not need to be re-listed
  per release; they are implied stable.

## Per-release notes

### v0.2.5 (2026-05-25)

- Drop inline per-release DOI / commit-hash references from
  `paper/main.tex` (abstract footnote) and
  `paper/sections/07_reproducibility.tex` (pinned-environment table).
  DOI metadata now lives exclusively in `CITATION.cff` and on the
  GitHub Releases page.
- No source code, test count, or numerical claim changed versus v0.2.4.
- Eliminates the recurring DOI-fill-in patch cycle (v0.1.3 -> v0.1.4
  and v0.2.3 -> v0.2.4 were both motivated by this drift).

### v0.2.4 (2026-05-25)

- Paper-bearing patch over v0.2.3. Adds the compiled `paper/main.pdf`
  built from the v0.2.3 paper sources, and fills in the v0.2.3 Zenodo
  DOI (`10.5281/zenodo.20382963`) into `CITATION.cff`, `README.md`,
  and the README citation block.
- No source code, test count, or numerical claim changed versus v0.2.3.

### v0.2.3 (2026-05-25)

- Paper readability + jargon cleanup release. The abstract reproduction
  instructions were shortened, the pinned-environment table was made
  line-wrappable, and the public paper now frames supplementary checks
  as local author-operated engineering evidence only.
- Added a precision-budget explanation for the 200-bit mpmath setting,
  clarified the `1e-3` tolerance versus observed `1.4e-4` relative error,
  and softened the finite Golod-Shafarevich admissibility wording.
- Removed residual `charter_phase` key from the three phase modules'
  `result_tags`. The remaining provenance keys (`tier`,
  `evidence_level`, `model_kind`, `exactness`, `registry_state`) are
  externally meaningful and unchanged.
- Removed the "anonymous external reviewer" sentence from §8 of the
  paper; the v0.1.x audit pass was scanner-driven and is not claimed
  as mathematician peer review.
- No numerical claim, test count, or source-PDF mapping changed versus
  v0.2.2. The `result_tags` dict structure changed only by dropping
  one project-internal key.

### v0.2.2 (2026-05-25)

- Public naming alignment only. Repository/package metadata now uses
  `openai-erdos-eq22-reproduction`; README and paper title now foreground
  the OpenAI Erdős unit-distance eq. (2.2) reproduction scope.
- No numerical claim, code path, test count, or source-PDF mapping
  changed versus v0.2.1.

### v0.2.1 (2026-05-25)

- Verification CLI hardened against user-environment pytest plugin
  leakage: the internal pytest subprocess now defaults
  `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and records a bounded timeout as a
  failed check rather than waiting indefinitely.
- Eq (2.2) pass/fail tolerance tightened from `0.5` relative error to
  `1e-3`, matching the deviation-ledger policy and preventing a very
  loose source-match check from passing as "reproduction".
- No numerical claim changed. The tracked evidence files were refreshed
  so the source SHA-256 manifest binds to the updated verifier module.
- Paper/docs consistency pass: Phase 2 text now follows the corrected
  v0.1.2 class-fiber partition `(29, 3) -> 0+4`, not the earlier `2+2`
  description.
- Paper CI/CD pass: `.github/workflows/paper.yml` now runs on `v*` tag
  pushes and validates that `paper/main.pdf` is non-empty before upload.

### v0.2.0 (2026-05-25)

- No source-code or numerical-claim change versus v0.1.4.
- Documentation-only positioning pass: paper title, abstract, §1.3
  scope, §6.3 peer-review note, §7.3 release-check framing, §8
  acknowledgements, and the README all reworded to bind the artifact
  scope to eq (2.2) of \cite{Sawin2026Remarks} specifically, and to
  state explicitly that the artifact does not reproduce Sawin's
  separately published explicit lower bound or any informal figure in
  secondary coverage.
- Test count corrected from "59" / "60+" to the actual `60`
  everywhere.
- "Three independent inspection tools" reworded to recorded local
  release checks.
- All ledger entries above remain bit-for-bit identical to v0.1.4.

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
  verdict did not change (`6 <= 6.25`, margin `0.25`).

### v0.1.1 (2026-05-24)

- Initial deviation ledger conceptually present in
  `reports/verification_result.json` and `reports/TRIPLE_INSPECTION_REPORT.md`
  but not yet broken out into this dedicated document.

### v0.1.0 (2026-05-24)

- Initial public release. Numerical computation surface as documented
  in CHANGELOG `[0.1.0]` entry.
