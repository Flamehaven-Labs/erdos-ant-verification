"""Tests for Phase 2 genus class field module: K = Q(sqrt(-5))."""

from __future__ import annotations

import pytest

from erdos_ant.genus_class_field import (
    CLASS_NUMBER,
    K_DISCRIMINANT,
    GenusClassFieldProbe,
    QSqrtMinus5Element,
    first_split_primes_for_K,
    splits_completely_in_K,
    two_squares_with_5,
)


def test_constants_match_classical_theory() -> None:
    # Q(sqrt(-5)) has discriminant -20 (since -5 = 3 mod 4 gives -4 * 5).
    assert K_DISCRIMINANT == -20
    # h(Q(sqrt(-5))) = 2, classical.
    assert CLASS_NUMBER == 2


def test_norm_and_conjugate_in_OK() -> None:
    alpha = QSqrtMinus5Element(a=3, b=2)
    # N(3 + 2 sqrt(-5)) = 9 + 5 * 4 = 29
    assert alpha.norm() == 29
    # Conjugate
    bar = alpha.conjugate()
    assert bar == QSqrtMinus5Element(a=3, b=-2)
    # alpha * conjugate = N(alpha)
    product = alpha * bar
    assert product.a == 29
    assert product.b == 0


def test_multiplication_associativity_sample() -> None:
    a = QSqrtMinus5Element(1, 1)
    b = QSqrtMinus5Element(2, -1)
    c = QSqrtMinus5Element(0, 3)
    assert ((a * b) * c) == (a * (b * c))


def test_splits_completely_known_cases() -> None:
    # 29 = 3^2 + 5 * 2^2 (principal genus), splits completely
    assert splits_completely_in_K(29) is True
    # 41 = 6^2 + 5 * 1^2 (principal genus), splits completely (41 mod 20 = 1)
    assert splits_completely_in_K(41) is True
    # 3 mod 20 = 3, splits but is non-principal genus
    assert splits_completely_in_K(3) is True
    # 7 mod 20 = 7, splits but non-principal genus
    assert splits_completely_in_K(7) is True
    # 11 mod 20 = 11, does NOT split (Legendre (-5/11) = -1)
    assert splits_completely_in_K(11) is False
    # 13 mod 20 = 13, does NOT split
    assert splits_completely_in_K(13) is False
    # 2 ramifies in Q(sqrt(-5)), not "splits completely"
    assert splits_completely_in_K(2) is False
    # 5 ramifies
    assert splits_completely_in_K(5) is False


def test_two_squares_with_5_principal_genus() -> None:
    # 29 = 3^2 + 5 * 2^2
    rep = two_squares_with_5(29)
    assert rep is not None
    a, b = rep
    assert a * a + 5 * b * b == 29

    # 41 = 6^2 + 5 * 1^2
    rep = two_squares_with_5(41)
    assert rep is not None
    a, b = rep
    assert a * a + 5 * b * b == 41

    # 61 = 4^2 + 5 * 3^2 = 16 + 45
    rep = two_squares_with_5(61)
    assert rep is not None


def test_two_squares_with_5_non_principal_genus_fails() -> None:
    # 3 mod 20 = 3 is split but non-principal: NOT representable as a^2 + 5 b^2
    assert two_squares_with_5(3) is None
    # 7 mod 20 = 7 is split but non-principal
    assert two_squares_with_5(7) is None


def test_hilbert_class_field_is_genus_field() -> None:
    hcf = GenusClassFieldProbe.hilbert_class_field_description()
    assert hcf["base_field"] == "Q(sqrt(-5))"
    assert hcf["class_number"] == "2"
    assert hcf["hilbert_class_field"] == "Q(i, sqrt(5))"
    assert "Cox" in hcf["reference"]


def test_first_split_primes_returns_in_increasing_order() -> None:
    primes = first_split_primes_for_K(5)
    assert primes == sorted(primes)
    assert len(primes) == 5
    for p in primes:
        assert splits_completely_in_K(p)


def test_lemma_22_pigeonhole_with_two_principal_primes() -> None:
    # 29 and 41 both in the principal genus (representable as a^2 + 5 b^2).
    probe = GenusClassFieldProbe(split_primes=(29, 41))
    out = probe.lemma_22_pigeonhole()
    assert out.s == 2
    assert out.k == 1
    assert out.candidate_count == 4  # (k+1)^s = 4
    # In Cl(K) of order 2, [P_j] = [cP_j], so eps choice does not change
    # the class. With both primes principal, all 4 candidates are
    # principal. The Lemma 2.2 lower bound (k+1)^s / h(K) = 2 is met.
    assert out.principal_class_fiber_size == 4
    assert out.non_principal_class_fiber_size == 0
    assert out.predicted_lower_bound == 2


def test_lemma_22_pigeonhole_with_mixed_genus() -> None:
    # 29 is principal (a^2 + 5 b^2), 3 is non-principal (2 p form).
    probe = GenusClassFieldProbe(split_primes=(29, 3))
    out = probe.lemma_22_pigeonhole()
    assert out.candidate_count == 4
    # In Cl(K) of order 2 the eps choice does not change the class, so all
    # 4 candidates land in the SAME class, determined by the parity of
    # non-principal primes. (29 principal, 3 non-principal) -> total class
    # = 1 -> all 4 candidates are non-principal.
    assert out.non_principal_class_fiber_size == 4
    assert out.principal_class_fiber_size == 0
    # The Lemma 2.2 lower bound (k+1)^s / h(K) = 2 is still met by the
    # populated (non-principal) fiber.
    assert out.predicted_lower_bound == 2


def test_lemma_22_pigeonhole_with_two_non_principal_primes() -> None:
    # 3 and 7 are both non-principal genus (mod 20 in {3, 7}).
    probe = GenusClassFieldProbe(split_primes=(3, 7))
    out = probe.lemma_22_pigeonhole()
    # Total class = 1 + 1 = 0 mod 2, so all 4 candidates are principal.
    assert out.principal_class_fiber_size == 4
    assert out.non_principal_class_fiber_size == 0
    assert out.predicted_lower_bound == 2


def test_analyze_carries_provenance_result_tags() -> None:
    result = GenusClassFieldProbe(split_primes=(29, 41)).analyze()
    tags = result["result_tags"]
    assert tags["tier"] == "validated_numeric_proxy"
    assert tags["model_kind"] == "imaginary_quadratic_h_eq_2"
    assert tags["exactness"] == "exact"
    assert tags["registry_state"] == "research_only"
    assert result["class_number_h"] == 2
    assert "infinite class field tower" in result["not_claimed"][0]


def test_rejects_non_splitting_prime() -> None:
    with pytest.raises(ValueError, match="does not split"):
        GenusClassFieldProbe(split_primes=(11,))
