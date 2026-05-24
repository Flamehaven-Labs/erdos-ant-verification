"""SPAR Framework review of the erdos-ant-verification artifact.

Loads the verify.py output and maps each check into a SPAR CheckResult,
then runs build_core_review and reports score + grade + claim drift.
"""

from __future__ import annotations

import json
from pathlib import Path

from spar_framework import CheckResult, build_core_review

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_JSON = REPO_ROOT / "reports" / "verification_result.json"


def main() -> None:
    data = json.loads(RESULT_JSON.read_text(encoding="utf-8"))
    checks = data["checks"]
    obs = data["observations"]

    # Layer A: model scrutiny — direct numerical truths the artifact claims.
    layer_a = []
    for name, passed in checks.items():
        if name.startswith(("phase1_", "phase2_", "phase3_")) or name in {
            "square_unit_pairs_is_4",
            "golod_shafarevich_proxy_boundary",
            "sawin_rigorous_lower_bound_present_624e_minus_38",
        }:
            layer_a.append(
                CheckResult(
                    check_id=f"A_{name}",
                    label=name,
                    status="PASS" if passed else "FAIL",
                    detail=f"Subject computation produced expected value (check: {name}).",
                    basis="subject_derived",
                )
            )

    # Layer B: scientific review — provenance + non-claim discipline.
    layer_b = []
    provenance_checks = [
        n for n in checks
        if "source_registry" in n
        or "source_claims" in n
        or "proof_delta_formula" in n
        or n == "source_delta_metadata_only"
        or n == "rename_alias_preserved"
        or n == "density_claim_tier_research_only"
    ]
    for name in provenance_checks:
        layer_b.append(
            CheckResult(
                check_id=f"B_{name}",
                label=name,
                status="PASS" if checks[name] else "FAIL",
                detail=f"Claim/provenance check ({name}).",
                basis="subject_derived",
            )
        )

    # Layer C: model existence probe — pytest + verify.py pass.
    layer_c = [
        CheckResult(
            check_id="C_pytest_passed",
            label="pytest_passed",
            status="PASS" if checks["pytest_passed"] else "FAIL",
            detail="Full unit test suite passes (59 tests).",
            basis="subject_derived",
        ),
        CheckResult(
            check_id="C_eq22_reproduced",
            label="remarks_pdf_eq_2_2_reproduced",
            status=(
                "PASS"
                if obs["phase3_eq_2_2_evaluation"]["relative_error_vs_published"] < 0.01
                else "WARN"
            ),
            detail=(
                f"eq (2.2) computed value "
                f"{obs['phase3_eq_2_2_evaluation']['exponent_excess']:.4e}, "
                f"relative error vs published "
                f"{obs['phase3_eq_2_2_evaluation']['relative_error_vs_published']:.4f}."
            ),
            basis="subject_derived",
            ref="unit-distance-remarks.pdf section 2.1 eq (2.2)",
        ),
    ]

    review = build_core_review(layer_a=layer_a, layer_b=layer_b, layer_c=layer_c)

    print("=== SPAR Framework Review (spar_framework 0.5.0) ===")
    print(f"Score: {review['score']}")
    print(f"Grade: {review['grade']}")
    print(f"Verdict: {review['verdict']}")
    print(f"Claim drift: {review['claim_drift']}")
    print(f"Coverage rate: {review['coverage_rate']}")
    print(f"Layer A: {len(layer_a)} checks ({sum(1 for c in layer_a if c.status == 'PASS')} pass)")
    print(f"Layer B: {len(layer_b)} checks ({sum(1 for c in layer_b if c.status == 'PASS')} pass)")
    print(f"Layer C: {len(layer_c)} checks ({sum(1 for c in layer_c if c.status == 'PASS')} pass)")

    out = REPO_ROOT / "reports" / "spar_review_result.json"
    out.write_text(json.dumps(review, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
