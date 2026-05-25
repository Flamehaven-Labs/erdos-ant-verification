# erdos-ant-verification report

**Verdict:** `PASS`
**Generated:** `2026-05-25T04:22:25.282552+00:00`
**Repo:** `D:\Sanctum\Flamehaven-Labs\erdos-ant-verification`

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
| `src/erdos_ant/sawin_multiquadratic.py` | `7733059f5d1c2bbc3ec484255ae2b007b0884f4a71870b60d39458bed5468f94` |
| `src/erdos_ant/algebraic_geometry.py` | `bb4114da77bf727c99dbcf2237724abfb8faf74c87eec85b400ad2350a46a55e` |
| `src/erdos_ant/imaginary_quadratic_lattice.py` | `fe93dc8a8ef8dcece0769546b3517bca5d601144d98b9437ff091783f41062fe` |
| `src/erdos_ant/genus_class_field.py` | `246e768575601d48bc074128b4e2a6f025534c925e0f25389af3d5611db7e89a` |
| `src/erdos_ant/verify.py` | `3fdb19ee6314a6658b98639d90a1c5b4a052fbc0c75f0ded2d56105a8ea0e007` |

## Pytest

```text
D:\Sanctum\venv\Scripts\python.exe -m pytest -q tests
returncode=0
............................................................             [100%]
```
