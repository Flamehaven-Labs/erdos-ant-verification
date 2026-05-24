# Architecture

## Module layout

```
src/erdos_ant/
  algebraic_geometry.py          Core dataclasses + Phase 0 anchors:
                                   AlgebraicNumberField,
                                   ClassFieldTowerGenerator (toy coordinate gen),
                                   HighDensityVacuumConfiguration (research probe),
                                   GolodShafarevichConstraint (simple r < d^2/4 proxy),
                                   SourceClaim (3-field provenance),
                                   ProofDeltaFormula (eq from proof PDF Thm 2.3).
  imaginary_quadratic_lattice.py Phase 1: h(K) = 1 case.
                                   Standard complex embedding of O_K for
                                   K in {Q(i), Q(sqrt(-2)), Q(sqrt(-3))}.
                                   Exact unit-distance pair counting.
  genus_class_field.py           Phase 2: K = Q(sqrt(-5)), h = 2.
                                   QSqrtMinus5Element arithmetic.
                                   Lemma 2.2 ideal-class pigeonhole.
                                   Hilbert class field via genus theory.
  sawin_multiquadratic.py        Phase 3: finite checkable parts of
                                   the Sawin remarks PDF construction.
                                   T = {3,5,7,11,13,17}, S = {101,inf}.
                                   L_T = Q(sqrt 5, sqrt 13, sqrt 17,
                                          sqrt 21, sqrt 33).
                                   Eq (2.2) numerical reproduction via mpmath.
```

## What each layer claims and what it does not

| Layer | Faithful claim | Explicit non-claim |
|---|---|---|
| Phase 0 | Source provenance is 3-field tagged (primary URL, formal PDF URL, verified-in-PDF flag). | Not a verifier of the underlying mathematics. |
| Phase 1 | Z[i], Z[omega], Z[sqrt(-2)] embed standardly in R^2; unit-distance pairs counted exactly. | Does not improve the asymptotic Erdos exponent (`[K:Q] = 2` only). |
| Phase 2 | Q(sqrt(-5)) has h = 2; its HCF is Q(i, sqrt 5) by genus theory; Lemma 2.2 pigeonhole works in h > 1 case. | Does not construct an infinite tower; `K` fixed. |
| Phase 3 | The finite, explicitly checkable parts of the Sawin construction (splitting of 101 in `L_T`, Galois-rank counts, GS admissibility, eq (2.2) numerical value). | Does not construct the infinite pro-2 tower; existence is Hajir-Maire. |

## Charter-style result_tags

Every `analyze()` method emits a `result_tags` dict with the following
keys (modeled after the `Flamehaven-TOE` Generative Discovery Charter,
adapted to a standalone setting):

- `tier`: `validated_numeric_proxy` (we verify finite, checkable parts).
- `evidence_level`: e.g. `exact_finite_enumeration`,
  `exact_finite_pigeonhole`,
  `exact_arithmetic_verification_of_published_construction`.
- `model_kind`: e.g. `ring_of_integers_O_K`,
  `imaginary_quadratic_h_eq_2`,
  `multi_quadratic_pro_2_tower_finite_part`.
- `exactness`: `exact` for all current modules (small-integer arithmetic
  + mpmath at 200-bit for the eq (2.2) evaluation).
- `registry_state`: `research_only` -- this artifact does not certify
  anything beyond reproducing the published numerics.

## Eq (2.2) numerical reproduction notes

The remarks PDF expression

```
delta - 1 = log(u * pi / (36 * v)) / log(36 / delta_min^2)
         where
           r = 2 * 3 * 5 * 7 * 11 * 13 * 17 = 510510
           K = ceil(18 * r^3 / pi)
           u = K / r^2
           v = r / 2
           delta_min = 101^(-2 * K)
```

simplifies to

```
delta - 1 = log(K * pi / (18 * r^3)) / (log(36) + 4 * K * log(101))
```

where the numerator is `log(1 + tiny)` with `tiny in (0, pi / (18 r^3)] ~ 1.3e-18`.

Float64 evaluation of `log(K * pi / (18 r^3))` suffers catastrophic
cancellation: the relative perturbation of `K * pi / (18 r^3)` from 1
is below machine epsilon. We therefore evaluate the ratio in mpmath at
200-bit precision, giving the result `6.2391e-38`, which matches the
published value `~ 6.24e-38` to 0.01% relative error.

## Phase boundaries (what is intentionally out of scope)

- **Phase 4** (infinite tower explicit construction): the
  Golod-Shafarevich theorem proves existence, not constructivity. No finite
  computation can exhibit the entire infinite tower. Phase 4 is therefore
  out of scope for any artifact of this kind.
- **Formal proof checking**: this is not a Lean or Coq formalization.
  Each module's correctness rests on the test suite and code-readability,
  not on a trusted proof kernel.
- **Peer review**: this artifact has not been reviewed by external
  mathematicians; correctness claims are limited to "the test suite
  passes" and "the eq (2.2) reproduction matches to 0.01%".
