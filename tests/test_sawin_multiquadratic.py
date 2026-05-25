"""Tests for Phase 3 Sawin multi-quadratic construction.

External ground truth: unit-distance-remarks.pdf section 2.1.
"""

from __future__ import annotations

import pytest

from erdos_ant.sawin_multiquadratic import (
    EQ22_RELATIVE_ERROR_TOLERANCE,
    L_T_GENERATOR_RADICANDS,
    PUBLISHED_EQ22_EXPONENT_EXCESS,
    S_SET_SPLIT,
    SAWIN_R_PRODUCT,
    T_SET,
    analyze,
    evaluate_sawin_exponent_bound,
    galois_rank_report,
    jacobi_symbol,
    splits_completely_in_L_T,
    splits_completely_in_Q_sqrt_d,
)

# -- Constants match remarks PDF section 2.1 verbatim ----------------------


def test_T_set_matches_remarks_pdf() -> None:
    # Remarks PDF: "T = {3, 5, 7, 11, 13, 17}"
    assert T_SET == (3, 5, 7, 11, 13, 17)


def test_S_set_split_matches_remarks_pdf() -> None:
    # Remarks PDF: "S = {101, infinity}"; we store the finite part.
    assert S_SET_SPLIT == (101,)


def test_L_T_generators_match_remarks_pdf() -> None:
    # Remarks PDF: "L_T = Q(sqrt(5), sqrt(13), sqrt(17), sqrt(21), sqrt(33))"
    assert L_T_GENERATOR_RADICANDS == (5, 13, 17, 21, 33)


def test_r_product_matches_remarks_pdf() -> None:
    # r = 2 * 3 * 5 * 7 * 11 * 13 * 17 = 510510
    assert SAWIN_R_PRODUCT == 510510


# -- Jacobi symbol primitives ----------------------------------------------


def test_jacobi_symbol_known_values() -> None:
    # (5 / 7) = (-2/7) = (-1/7)(2/7) = (-1)(1) = -1
    assert jacobi_symbol(5, 7) == -1
    # (1 / 7) = 1
    assert jacobi_symbol(1, 7) == 1
    # (3 / 11) = 1 since 5^2 = 25 = 3 mod 11
    assert jacobi_symbol(3, 11) == 1
    # (-1 / 5) = 1 since 5 = 1 mod 4
    assert jacobi_symbol(-1, 5) == 1
    # (-1 / 7) = -1 since 7 = 3 mod 4
    assert jacobi_symbol(-1, 7) == -1


def test_jacobi_symbol_rejects_even_or_nonpositive() -> None:
    with pytest.raises(ValueError):
        jacobi_symbol(3, 4)
    with pytest.raises(ValueError):
        jacobi_symbol(3, 0)


# -- 101 splits completely in L_T ------------------------------------------


@pytest.mark.parametrize("d", L_T_GENERATOR_RADICANDS)
def test_101_splits_completely_in_each_Q_sqrt_d(d: int) -> None:
    assert splits_completely_in_Q_sqrt_d(101, d), f"101 must split in Q(sqrt({d}))"


def test_101_splits_in_L_T_compositum() -> None:
    # Splitting in a compositum of linearly disjoint quadratic fields is
    # equivalent to splitting in each factor.
    assert splits_completely_in_L_T() is True


# -- Galois rank counts per remarks PDF section 2.1 ------------------------


def test_d_G_infty_equals_T_minus_1_because_T_contains_3_mod_4() -> None:
    rank = galois_rank_report()
    # T = {3, 5, 7, 11, 13, 17} contains 3, 7, 11 (all 3 mod 4),
    # so d(G_T^infty) = |T| - 1 = 5.
    assert rank.d_G_infty == len(T_SET) - 1 == 5


def test_r_bound_is_six_per_remarks_pdf() -> None:
    rank = galois_rank_report()
    # Remarks PDF: r(G_T^S) <= 6.
    assert rank.r_G_S == 6


def test_golod_shafarevich_inequality_holds() -> None:
    rank = galois_rank_report()
    # Remarks PDF: 6 <= (5)^2 / 4 = 6.25.
    assert rank.golod_shafarevich_threshold == pytest.approx(6.25)
    assert rank.r_G_S <= rank.golod_shafarevich_threshold + 1e-12
    assert rank.admissible is True


# -- Numerical evaluation of remarks PDF eq (2.2) --------------------------


def test_sawin_exponent_bound_matches_remarks_eq_2_2() -> None:
    # Remarks PDF eq (2.2): "the exponent ... approximately 1 + 6.24e-38".
    out = evaluate_sawin_exponent_bound()
    relative_error = (
        abs(out.exponent_excess - PUBLISHED_EQ22_EXPONENT_EXCESS)
        / PUBLISHED_EQ22_EXPONENT_EXCESS
    )
    assert relative_error < EQ22_RELATIVE_ERROR_TOLERANCE, (
        f"Sawin exponent bound {out.exponent_excess:.3e} differs from "
        f"remarks PDF 6.24e-38 by relative error {relative_error:.3f}"
    )


def test_k_is_positive_and_huge_per_remarks_construction() -> None:
    out = evaluate_sawin_exponent_bound()
    # k = ceil(18 * 510510^3 / pi) - 1 is astronomically large.
    assert out.k > 10 ** 17
    assert out.r == 510510


# -- Charter alignment -----------------------------------------------------


def test_analyze_carries_charter_result_tags() -> None:
    result = analyze()
    tags = result["result_tags"]
    assert tags["tier"] == "validated_numeric_proxy"
    assert tags["model_kind"] == "multi_quadratic_pro_2_tower_finite_part"
    assert tags["exactness"] == "exact"
    assert tags["registry_state"] == "research_only"
    assert tags["ground_truth_document"] == "unit-distance-remarks.pdf section 2.1"
    assert result["external_verification_pdf_url"].endswith("unit-distance-remarks.pdf")
    assert result["101_splits_in_L_T"] is True


def test_analyze_states_what_is_not_claimed() -> None:
    result = analyze()
    not_claimed = result["not_claimed"]
    assert any("infinite pro-2 tower" in s for s in not_claimed)
    assert any("Hajir-Maire" in s for s in not_claimed)
