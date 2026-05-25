# erdos-ant-verification report

**Verdict:** `PASS`
**Generated:** `2026-05-25T15:50:22.295815+00:00`

## Checks

- PASS `square_unit_pairs_is_4`
- PASS `source_delta_metadata_only`
- PASS `density_claim_tier_research_only`
- PASS `golod_shafarevich_proxy_boundary`
- PASS `rename_alias_preserved`
- PASS `source_registry_openai_initial_0014`
- PASS `source_registry_sawin_refinement_00318`
- PASS `source_registry_sawin_delta_not_equal_legacy_label`
- PASS `source_claims_three_field_provenance_marked_correctly`
- PASS `sawin_rigorous_lower_bound_present_624e_minus_38`
- PASS `proof_delta_formula_positive_for_reasonable_params`
- PASS `phase1_gaussian_7x7_grid_has_expected_84_pairs`
- PASS `phase1_eisenstein_exceeds_gaussian_at_same_bound`
- PASS `phase1_claims_h1_degenerate_tier`
- PASS `phase2_h2_genus_theory_hcf_is_Q_i_sqrt5`
- PASS `phase2_lemma22_pigeonhole_lower_bound_is_2`
- PASS `phase3_101_splits_in_L_T_compositum`
- PASS `phase3_golod_shafarevich_admissible`
- PASS `phase3_matches_remarks_pdf_eq_2_2_624e_minus_38`
- PASS `phase3_external_verification_pdf_registered`
- PASS `pytest_passed`

## Phase 3 highlight: remarks PDF eq (2.2) reproduction

| | |
|---|---|
| r = 2 * prod(T) | `510510` |
| k | `762316628416213961` |
| Computed exponent excess | `6.2391e-38` |
| Published value | `6.2400e-38` |
| Relative error vs published | `0.0001` |

## Source SHA-256 manifest

| File | SHA-256 |
|---|---|
| `src/erdos_ant/sawin_multiquadratic.py` | `635007a604081ffdc422a861e254486bf9b85c1f76bccb41162c4dc2524f7188` |
| `src/erdos_ant/algebraic_geometry.py` | `847769efc93a601de6931aae794910bd83e986f4217c0efc867350f2228f23c9` |
| `src/erdos_ant/imaginary_quadratic_lattice.py` | `8f975ebdf2355be76430a3d2585588e6588144bfb1e1c0beb2ca141fd1d683b0` |
| `src/erdos_ant/genus_class_field.py` | `bd614cb7362c3bd7bcafa4505b8069b43458e7d23d3e9bd722db4006576af91a` |
| `src/erdos_ant/verify.py` | `401de26d28b9d54b6449d9ecda505f8d0f2500d8a34ebf933a92fcab34841551` |

## Pytest

```text
python -m pytest -q tests
returncode=0
............................................................             [100%]
```
