"""Tests for the faithful imaginary quadratic lattice Phase 1 module."""

from __future__ import annotations

from math import sqrt

import pytest

from erdos_ant.imaginary_quadratic_lattice import (
    CLASS_NUMBER_ONE_DISCRIMINANTS,
    ImaginaryQuadraticLattice,
    eisenstein_integer_lattice,
    gaussian_integer_grid,
    quadratic_minus_two_lattice,
)


def test_class_number_one_list_matches_known_baker_heegner_stark() -> None:
    # The Baker-Heegner-Stark theorem fixes this list exactly.
    assert CLASS_NUMBER_ONE_DISCRIMINANTS == (1, 2, 3, 7, 11, 19, 43, 67, 163)


def test_gaussian_basis_is_orthonormal() -> None:
    lattice = gaussian_integer_grid(bound=1)
    (e1x, e1y), (e2x, e2y) = lattice.basis_vectors()
    assert (e1x, e1y) == (1.0, 0.0)
    assert (e2x, e2y) == (0.0, 1.0)


def test_eisenstein_basis_gives_triangular_lattice() -> None:
    lattice = eisenstein_integer_lattice(bound=1)
    _, (e2x, e2y) = lattice.basis_vectors()
    # omega = (-1 + i*sqrt(3))/2 -> (-1/2, sqrt(3)/2)
    assert e2x == pytest.approx(-0.5)
    assert e2y == pytest.approx(sqrt(3.0) / 2.0)
    # |omega| = 1, so basis vectors are unit length
    assert e2x**2 + e2y**2 == pytest.approx(1.0)


def test_quadratic_minus_two_basis_is_rectangular() -> None:
    lattice = quadratic_minus_two_lattice(bound=1)
    _, (e2x, e2y) = lattice.basis_vectors()
    assert e2x == pytest.approx(0.0)
    assert e2y == pytest.approx(sqrt(2.0))


def test_enumerate_points_has_correct_cardinality() -> None:
    for d in (1, 2, 3):
        for bound in (0, 1, 2, 5):
            lattice = ImaginaryQuadraticLattice(discriminant_d=d, coefficient_bound=bound)
            coords = lattice.enumerate_points()
            expected = (2 * bound + 1) ** 2
            assert coords.shape == (expected, 2)


def test_gaussian_3x3_grid_has_12_unit_distances() -> None:
    # bound=1 gives a 3x3 grid = 9 points. Adjacent pairs: 2*3*3 - 2*3 = 12.
    # Horizontal edges: 3 rows * 2 = 6; vertical edges: 3 cols * 2 = 6; total 12.
    lattice = gaussian_integer_grid(bound=1)
    assert lattice.count_unit_distance_pairs() == 12


def test_gaussian_5x5_grid_has_40_unit_distances() -> None:
    # 5x5 grid = 25 points. Edges: 2 * 5 * 4 = 40.
    lattice = gaussian_integer_grid(bound=2)
    assert lattice.count_unit_distance_pairs() == 40


def test_eisenstein_unit_distances_exceed_gaussian_for_same_bound() -> None:
    # The triangular lattice has 6 nearest neighbors per interior point,
    # the square lattice has 4. So for the same coefficient bound the
    # Eisenstein pair count strictly exceeds the Gaussian pair count once
    # interior points exist (bound >= 1).
    for bound in (1, 2, 3, 4):
        g = gaussian_integer_grid(bound).count_unit_distance_pairs()
        e = eisenstein_integer_lattice(bound).count_unit_distance_pairs()
        assert e > g, f"bound={bound}: gaussian={g}, eisenstein={e}"


def test_quadratic_minus_two_has_no_unit_distances() -> None:
    # The minimal non-trivial distance in Z[sqrt(-2)] is 1 (between (a, b) and
    # (a +/- 1, b)) — horizontal neighbors — so there *are* unit distances
    # along the real axis. Verify the count for bound=1: 3 rows * 2 = 6.
    lattice = quadratic_minus_two_lattice(bound=1)
    assert lattice.count_unit_distance_pairs() == 6


def test_analyze_returns_expected_keys_and_claim_tier() -> None:
    result = gaussian_integer_grid(bound=2).analyze()
    expected_keys = {
        "field",
        "discriminant_d",
        "class_number_h",
        "coefficient_bound",
        "num_points",
        "unit_distance_pairs",
        "observed_exponent",
        "observed_delta",
        "claim_tier",
        "not_claimed",
        "paper_reference",
        "result_tags",
    }
    assert expected_keys.issubset(set(result.keys()))
    assert result["claim_tier"] == "faithful_h1_degenerate_case"
    assert result["class_number_h"] == 1
    assert "Theorem 1.1" in result["not_claimed"][0]


def test_result_tags_have_expected_provenance_keys() -> None:
    result = gaussian_integer_grid(bound=2).analyze()
    tags = result["result_tags"]
    # Required machine-readable provenance keys.
    for key in ("tier", "evidence_level", "model_kind", "exactness"):
        assert key in tags
    # Permitted tier values for a finite, exact enumeration phase.
    assert tags["tier"] in {
        "generated_candidate",
        "validated_numeric_proxy",
        "proof_verified_math",
        "research_only",
    }
    # h(K) = 1 enumeration is exact, not heuristic.
    assert tags["exactness"] == "exact"
    assert tags["registry_state"] == "research_only"


def test_observed_delta_is_zero_for_finite_classical_grids() -> None:
    # The classical sqrt(n) x sqrt(n) Erdos grid satisfies nu(n) <=
    # n^(1 + O(1/log log n)). For our small finite samples the observed
    # log(pairs)/log(n) - 1 is well below any positive constant delta.
    for bound in (1, 2, 3, 5):
        for factory in (gaussian_integer_grid, eisenstein_integer_lattice):
            result = factory(bound).analyze()
            assert result["observed_delta"] < 0.5, (
                f"finite-sample observed_delta unexpectedly large: {result}"
            )


def test_rejects_unsupported_discriminant() -> None:
    with pytest.raises(ValueError, match="Phase 1 supports only"):
        ImaginaryQuadraticLattice(discriminant_d=7, coefficient_bound=1)
    with pytest.raises(ValueError, match="non-negative"):
        ImaginaryQuadraticLattice(discriminant_d=1, coefficient_bound=-1)
