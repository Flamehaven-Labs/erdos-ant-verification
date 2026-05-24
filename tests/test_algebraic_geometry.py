"""Tests for the core algebraic_geometry module of erdos_ant.

TOE-bound tests (CompactGeometry, LandscapeScanner, SPAR model registry)
have been removed from this standalone repository; the standalone package
does not include the TOE physics/governance modules those tests depended on.
"""

from __future__ import annotations

import numpy as np
import pytest

from erdos_ant.algebraic_geometry import (
    SOURCE_REFINED_DELTA,
    AlgebraicNumberField,
    ClassFieldTowerGenerator,
    GolodShafarevichConstraint,
    HighDensityVacuumConfiguration,
    SourceClaim,
    count_near_unit_pairs,
    estimate_unit_distance_delta,
    get_source_claim,
    local_density_exponent_probe,
)


def test_algebraic_number_field_degree_uses_polynomial_degree() -> None:
    field = AlgebraicNumberField(
        polynomial_coefficients=(1.0, 0.0, 1.0),
        discriminant=-4.0,
    )
    assert field.degree == 2


def test_count_near_unit_pairs_square_grid() -> None:
    coords = [
        [0.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0],
    ]
    assert count_near_unit_pairs(coords) == 4


def test_delta_estimate_does_not_force_source_delta() -> None:
    exponent, delta = estimate_unit_distance_delta(num_points=16, pair_count=16)
    assert exponent == pytest.approx(1.0)
    assert delta == pytest.approx(0.0)
    assert delta != SOURCE_REFINED_DELTA


def test_density_metrics_are_research_only_and_do_not_import_proof_delta() -> None:
    tower = ClassFieldTowerGenerator(prime_degree=2, base_discriminant=-4.0)
    config = HighDensityVacuumConfiguration(num_points=12, tower=tower, depth=2)
    metrics = config.calculate_density_metrics()

    assert metrics["claim_tier"] == "research_only_proxy"
    assert metrics["source_claim_delta"] == SOURCE_REFINED_DELTA
    assert metrics["observed_delta"] >= 0.0
    assert "Does not reproduce the OpenAI proof." in metrics["not_claimed"]


def test_golod_shafarevich_constraint_boundary() -> None:
    assert GolodShafarevichConstraint(generator_count=4, relation_count=3).is_admissible()
    assert not GolodShafarevichConstraint(
        generator_count=4,
        relation_count=4,
    ).is_admissible()


def test_golod_shafarevich_score_in_unit_interval() -> None:
    score = GolodShafarevichConstraint(
        generator_count=5,
        relation_count=2,
    ).calculate_stability_score()
    assert 0.0 <= score <= 1.0


def test_source_claims_record_three_provenance_categories() -> None:
    openai_index = get_source_claim("openai_index_reported")
    sawin_rigorous = get_source_claim("sawin_rigorous_lower_bound")
    sawin_reported = get_source_claim("sawin_refinement_reported")
    for c in (openai_index, sawin_rigorous, sawin_reported):
        assert isinstance(c, SourceClaim)

    # Reported values (OpenAI index page, blog) are NOT in formal PDF.
    assert openai_index.delta == pytest.approx(0.014)
    assert openai_index.verified_numerical_in_formal_pdf is False
    assert sawin_reported.delta == pytest.approx(0.0318)
    assert sawin_reported.verified_numerical_in_formal_pdf is False

    # Sawin's rigorous lower bound 6.24e-38 IS verbatim in remarks PDF eq 2.2.
    assert sawin_rigorous.delta == pytest.approx(6.24e-38)
    assert sawin_rigorous.verified_numerical_in_formal_pdf is True
    # Note: rigorous lower bound is enormously smaller than reported figures.
    assert sawin_rigorous.delta < openai_index.delta
    assert sawin_rigorous.delta < sawin_reported.delta

    # Backward-compatible legacy alias still maps to 0.014.
    assert pytest.approx(0.014) == SOURCE_REFINED_DELTA


def test_source_claims_three_field_provenance_present() -> None:
    for claim in (
        get_source_claim("openai_index_reported"),
        get_source_claim("sawin_rigorous_lower_bound"),
        get_source_claim("sawin_refinement_reported"),
    ):
        assert claim is not None
        assert claim.primary_source_url.startswith("https://")
        assert claim.formal_proof_pdf_url.endswith(".pdf")
        assert isinstance(claim.verified_numerical_in_formal_pdf, bool)


def test_proof_delta_formula_evaluates() -> None:
    from erdos_ant.algebraic_geometry import PROOF_DELTA_FORMULA

    # Sanity: gamma > 0 requires t * log(2) > log(H_ell).
    delta = PROOF_DELTA_FORMULA.evaluate(
        t=100, log_H_ell=10.0, R=2.0, D=1000.0
    )
    # Closed form: gamma = 100*log(2) - 10, B = 2*log(8000),
    # delta = (100*log2 - 10) / (8*log(8000)).
    import math

    expected = (100 * math.log(2.0) - 10.0) / (8.0 * math.log(8000.0))
    assert delta == pytest.approx(expected)
    assert delta > 0

    with pytest.raises(ValueError):
        PROOF_DELTA_FORMULA.evaluate(t=0, log_H_ell=1.0, R=1.0, D=1.0)


def test_rename_alias_preserves_estimate_unit_distance_delta() -> None:
    assert estimate_unit_distance_delta is local_density_exponent_probe


def test_local_density_exponent_probe_basic_algebra() -> None:
    exp_eq, delta_eq = local_density_exponent_probe(num_points=16, pair_count=16)
    assert exp_eq == pytest.approx(1.0)
    assert delta_eq == pytest.approx(0.0)

    exp_super, delta_super = local_density_exponent_probe(num_points=4, pair_count=8)
    # log(8)/log(4) = 1.5
    assert exp_super == pytest.approx(1.5)
    assert delta_super == pytest.approx(0.5)

    assert local_density_exponent_probe(1, 10) == (0.0, 0.0)
    assert local_density_exponent_probe(10, 0) == (0.0, 0.0)


def test_polynomial_must_be_monic_constant_first() -> None:
    # x^2 + 1 -> (1.0, 0.0, 1.0) is accepted
    AlgebraicNumberField(polynomial_coefficients=(1.0, 0.0, 1.0), discriminant=-4.0)

    with pytest.raises(ValueError, match="monic"):
        AlgebraicNumberField(polynomial_coefficients=(1.0, 0.0, 2.0), discriminant=-4.0)

    with pytest.raises(ValueError, match="discriminant"):
        AlgebraicNumberField(polynomial_coefficients=(1.0, 0.0, 1.0), discriminant=0.0)

    with pytest.raises(ValueError, match="degree"):
        AlgebraicNumberField(polynomial_coefficients=(1.0,), discriminant=-4.0)


def test_density_metrics_expose_dated_source_registry() -> None:
    tower = ClassFieldTowerGenerator(prime_degree=2, base_discriminant=-4.0)
    config = HighDensityVacuumConfiguration(num_points=12, tower=tower, depth=2)
    metrics = config.calculate_density_metrics()

    claims = metrics["source_claims"]
    labels = {c["label"] for c in claims}
    assert {
        "openai_index_reported",
        "sawin_rigorous_lower_bound",
        "sawin_refinement_reported",
    }.issubset(labels)
    sawin_entry = next(
        c for c in claims if c["label"] == "sawin_refinement_reported"
    )
    assert sawin_entry["delta"] == pytest.approx(0.0318)


def test_density_probe_sensitivity_sweep_never_forces_source_delta() -> None:
    tower = ClassFieldTowerGenerator(prime_degree=2, base_discriminant=-4.0)
    for n in (4, 8, 16, 32):
        for depth in (0, 1, 2, 3):
            config = HighDensityVacuumConfiguration(
                num_points=n, tower=tower, depth=depth
            )
            analysis = config.analyze_unit_distance_density()
            # Observed pair count and delta are computed locally only.
            assert analysis.near_unit_pairs >= 0
            assert analysis.observed_delta >= 0.0
            # If zero pairs were found, delta must also be zero (no silent
            # fallback to the source delta).
            if analysis.near_unit_pairs == 0:
                assert analysis.observed_delta == 0.0
            # Source delta of 0.014 must never appear as the observed value.
            assert analysis.observed_delta != pytest.approx(SOURCE_REFINED_DELTA)


def test_phase_coefficients_are_configurable_and_validated() -> None:
    tower = ClassFieldTowerGenerator(prime_degree=2, base_discriminant=-4.0)
    base = HighDensityVacuumConfiguration(num_points=8, tower=tower, depth=1)
    perturbed = HighDensityVacuumConfiguration(
        num_points=8, tower=tower, depth=1, phase_x=0.19, phase_y=0.23
    )
    base_coords = base.generate_coordinates()
    perturbed_coords = perturbed.generate_coordinates()
    # Different phases produce different coordinate sets.
    assert not np.allclose(base_coords, perturbed_coords)

    with pytest.raises(ValueError, match="phase_x"):
        HighDensityVacuumConfiguration(
            num_points=4, tower=tower, depth=1, phase_x=0.0, phase_y=0.1
        ).generate_coordinates()
