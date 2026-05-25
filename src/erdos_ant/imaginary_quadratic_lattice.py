"""
Phase 1 faithful imaginary quadratic lattice module.

This module implements the *trivial-class-number degenerate case* of
Proposition 2.2 of OpenAI's "Planar Point Sets with Many Unit Distances"
(unit-distance-proof.pdf). It is faithful in the following sense:

- The points are actual elements of the ring of integers O_K for an
  imaginary quadratic field K = Q(sqrt(-d)) with class number h(K) = 1
  (so the class-group pigeonhole step in Proposition 2.2 is trivial and
  no Chebotarev choice is required).
- The standard complex embedding K -> C is used (not a decorative
  generator).
- Unit-distance pairs are counted exactly.

What this module is NOT:

- It does not reproduce the polynomial improvement nu(n) >= n^(1 + delta)
  from Theorem 1.1, which strictly requires [K : Q] -> infinity via an
  infinite Golod-Shafarevich pro-3 tower (Section 3 of the paper). With
  [K : Q] = 2 the construction degenerates to the classical sqrt(n) x
  sqrt(n) Erdos grid (for Z[i]) or the triangular lattice (for Z[omega]),
  both of which satisfy nu(n) = n^(1 + O(1 / log log n)) and therefore
  obey the Erdos conjecture.
- It does not adjoin i to get a CM field; for d = 1 we already have
  K = Q(i), so the construction is direct.

Reference: Theorem 1.1, Section 2, and Proposition 2.2 of
https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Literal

import numpy as np

# Imaginary quadratic fields Q(sqrt(-d)) with class number 1.
# Full list of d for which h(Q(sqrt(-d))) = 1: 1, 2, 3, 7, 11, 19, 43, 67, 163.
# We implement only the three smallest because their O_K embeds as a
# computationally simple lattice in R^2.
CLASS_NUMBER_ONE_DISCRIMINANTS: tuple[int, ...] = (1, 2, 3, 7, 11, 19, 43, 67, 163)

FieldTag = Literal["Q(i)", "Q(sqrt(-2))", "Q(sqrt(-3))"]


@dataclass(frozen=True)
class ImaginaryQuadraticLattice:
    """Lattice O_K embedded in R^2 for an imaginary quadratic field of h = 1.

    For K = Q(sqrt(-d)) the ring of integers O_K is

      - Z[i]                       if d == 1 (Gaussian integers),
      - Z[sqrt(-2)]                if d == 2,
      - Z[omega], omega = (-1 + sqrt(-3)) / 2  if d == 3 (Eisenstein integers).

    The standard complex embedding sends a + b*theta (where theta is the
    generator above) to its complex value, which we then identify with R^2.

    The lattice has rank 2 over Z, so elements are enumerated by integer
    coefficients (a, b) with |a|, |b| <= bound.
    """

    discriminant_d: int
    coefficient_bound: int

    def __post_init__(self) -> None:
        if self.discriminant_d not in (1, 2, 3):
            raise ValueError(
                "Phase 1 supports only d in {1, 2, 3}; "
                f"got d={self.discriminant_d}. Other class-number-1 d are "
                "valid number-theoretically but not implemented here."
            )
        if self.coefficient_bound < 0:
            raise ValueError("coefficient_bound must be non-negative")

    @property
    def field_tag(self) -> FieldTag:
        if self.discriminant_d == 1:
            return "Q(i)"
        if self.discriminant_d == 2:
            return "Q(sqrt(-2))"
        return "Q(sqrt(-3))"

    def basis_vectors(self) -> tuple[tuple[float, float], tuple[float, float]]:
        """Return the standard R^2 embedding of (1, theta) for O_K."""

        if self.discriminant_d == 1:
            # 1 -> (1, 0), i -> (0, 1)
            return (1.0, 0.0), (0.0, 1.0)
        if self.discriminant_d == 2:
            # 1 -> (1, 0), sqrt(-2) -> (0, sqrt(2))
            return (1.0, 0.0), (0.0, sqrt(2.0))
        # d == 3: 1 -> (1, 0), omega = (-1 + i*sqrt(3))/2 -> (-1/2, sqrt(3)/2)
        return (1.0, 0.0), (-0.5, sqrt(3.0) / 2.0)

    def enumerate_points(self) -> np.ndarray:
        """Return all O_K lattice points a + b*theta with |a|, |b| <= bound."""

        v1, v2 = self.basis_vectors()
        bound = self.coefficient_bound
        side = 2 * bound + 1
        coeffs_a = np.arange(-bound, bound + 1)
        coeffs_b = np.arange(-bound, bound + 1)
        aa, bb = np.meshgrid(coeffs_a, coeffs_b, indexing="ij")
        xs = aa * v1[0] + bb * v2[0]
        ys = aa * v1[1] + bb * v2[1]
        coords = np.stack([xs.ravel(), ys.ravel()], axis=-1).astype(float)
        assert coords.shape == (side * side, 2)
        return coords

    def count_unit_distance_pairs(
        self,
        *,
        target_distance: float = 1.0,
        tolerance: float = 1e-9,
    ) -> int:
        """Count exact unit-distance pairs in the enumerated lattice region."""

        if target_distance <= 0:
            raise ValueError("target_distance must be positive")
        if tolerance < 0:
            raise ValueError("tolerance must be non-negative")

        coords = self.enumerate_points()
        n = len(coords)
        if n < 2:
            return 0
        diffs = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
        dists = np.sqrt(np.sum(diffs**2, axis=-1))
        upper = dists[np.triu_indices(n, k=1)]
        return int(np.count_nonzero(np.abs(upper - target_distance) <= tolerance))

    def analyze(self) -> dict[str, object]:
        """Return a dict with point count, exact pair count, observed exponent."""

        coords = self.enumerate_points()
        n = len(coords)
        pairs = self.count_unit_distance_pairs()
        if n >= 2 and pairs > 0:
            from math import log

            exponent = log(float(pairs)) / log(float(n))
        else:
            exponent = 0.0
        return {
            "field": self.field_tag,
            "discriminant_d": self.discriminant_d,
            "class_number_h": 1,
            "coefficient_bound": self.coefficient_bound,
            "num_points": n,
            "unit_distance_pairs": pairs,
            "observed_exponent": exponent,
            "observed_delta": max(0.0, exponent - 1.0),
            "claim_tier": "faithful_h1_degenerate_case",
            "not_claimed": [
                "Does not reproduce Theorem 1.1 polynomial improvement.",
                "Does not construct an infinite Golod-Shafarevich tower.",
                "[K : Q] = 2 only; the asymptotic result requires [K : Q] -> infinity.",
            ],
            "paper_reference": "Proposition 2.2 with h(K) = 1 (degenerate case)",
            # Per-phase result tags: a small machine-readable
            # provenance block (tier, evidence level, claim type) for
            # downstream consumers and the verifier.
            "result_tags": {
                "tier": "validated_numeric_proxy",
                "evidence_level": "exact_finite_enumeration",
                "model_kind": "ring_of_integers_O_K",
                "exactness": "exact",
                "registry_state": "research_only",
                "charter_phase": "Phase 1: Discovery Engine",
            },
        }


def gaussian_integer_grid(bound: int) -> ImaginaryQuadraticLattice:
    """Factory: Z[i] lattice with coefficients in [-bound, bound]."""

    return ImaginaryQuadraticLattice(discriminant_d=1, coefficient_bound=bound)


def eisenstein_integer_lattice(bound: int) -> ImaginaryQuadraticLattice:
    """Factory: Z[omega] (Eisenstein integers, triangular lattice)."""

    return ImaginaryQuadraticLattice(discriminant_d=3, coefficient_bound=bound)


def quadratic_minus_two_lattice(bound: int) -> ImaginaryQuadraticLattice:
    """Factory: Z[sqrt(-2)] rectangular lattice."""

    return ImaginaryQuadraticLattice(discriminant_d=2, coefficient_bound=bound)
