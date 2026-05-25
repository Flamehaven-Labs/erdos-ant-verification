# Source-Code Alignment Audit

Status: source-aligned finite reproduction

This audit records whether the repository's executable surface matches
the two OpenAI-hosted source PDFs and whether the implementation relies
on hidden hard-coded results.

## Source Boundary

Primary source PDFs:

- `unit-distance-proof.pdf`: proves Theorem 1.1 using an unramified
  pro-3 tower and a geometric unit-distance construction.
- `unit-distance-remarks.pdf`: gives the simplified Sawin
  multi-quadratic pro-2 construction and the explicit eq. (2.2)
  exponent excess used by this repository.

The code follows the remarks PDF for the finite executable portion. It
does not attempt to replay the original proof PDF's pro-3 tower.

## Source-to-Code Map

| Source item | Code anchor | Audit result |
|---|---|---|
| `T = {3, 5, 7, 11, 13, 17}` | `src/erdos_ant/sawin_multiquadratic.py::T_SET` | Traceable constant copied from remarks PDF. |
| `S = {101, infinity}` | `S_SET_SPLIT = (101,)` plus documented infinite place | Traceable; finite split prime is executable, infinity is metadata. |
| `L_T = Q(sqrt(5), sqrt(13), sqrt(17), sqrt(21), sqrt(33))` | `L_T_GENERATOR_RADICANDS` | Traceable and test-pinned. |
| `101` splits completely in `L_T` | `splits_completely_in_L_T()` | Computed from Jacobi-symbol checks over every radicand. |
| `d = |T| - 1 = 5` | `galois_rank_report()` | Computed from `T_SET` and the `3 mod 4` condition. |
| `r <= 6 <= 25/4` | `galois_rank_report()` | Computed and recorded as finite Golod-Shafarevich admissibility only. |
| Eq. (2.2) exponent excess `~ 6.24e-38` | `evaluate_sawin_exponent_bound()` | Computed from `K = ceil(18 r^3 / pi)`, `r`, `101`, and high-precision logarithms. |

## Hardcoding Audit

The implementation contains source constants, not hidden result
substitution. The expected source value `6.24e-38` appears only as:

- source metadata in `algebraic_geometry.py`;
- the published comparison target in `sawin_multiquadratic.py` and
  `verify.py`;
- regression-test expected value in `tests/`;
- documentation and evidence reports.

The computed value is not returned from a literal. It is produced by:

1. computing `r = 2 * 3 * 5 * 7 * 11 * 13 * 17`;
2. computing `K = ceil(18 * r^3 / pi)` using `mpmath` at 200-bit
   precision;
3. evaluating `log(K*pi/(18*r^3))`;
4. evaluating the denominator `log(36) + 4*K*log(101)`;
5. dividing the two values.

This is an acceptable source-target pattern for a reproduction artifact:
the published number is used to judge drift, not to generate the
computed output.

## Slop / Spaghetti Audit

The code is not spaghetti in the current finite reproduction surface:

- Phase-specific modules have narrow ownership:
  `imaginary_quadratic_lattice.py`, `genus_class_field.py`,
  `sawin_multiquadratic.py`, and `algebraic_geometry.py`.
- `verify.py` orchestrates checks and evidence writing; it does not add
  a mathematical claim layer.
- The infinite tower boundary is explicit: the code checks finite
  admissibility and cites Golod-Shafarevich/Hajir-Maire for infinitude.
- The eq. (2.2) tolerance is now `1e-3` relative error, matching the
  deviation-ledger policy and avoiding an overly loose pass condition.

Remaining risk is not hidden hardcoding. The residual risk is scope
interpretation: readers may overread a finite executable reproduction as
proof verification. The README, paper, architecture document, and
deviation log now state that boundary explicitly.
