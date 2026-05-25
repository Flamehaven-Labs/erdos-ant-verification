"""End-to-end verification entry point for the erdos-ant-verification artifact.

Runs the Phase 1/2/3 analyses, evaluates the remarks PDF eq (2.2) exponent
excess, prints the verdict, and optionally writes machine-readable +
human-readable reports under the project's ``reports/`` directory.

Exposed as the console script ``erdos-ant-verify`` (see
``pyproject.toml``) and also runnable as ``python -m erdos_ant.verify``.
Exits 0 if the verdict is PASS, 1 otherwise.

Frozen-report mode (default)
----------------------------
By default this command does **not** write to the tracked
``reports/verification_result.json`` or ``reports/verification_report.md``
files. It prints the verdict and (optionally) a summary table to stdout.
This keeps the working tree clean for ordinary developer runs.

To refresh the tracked evidence files (intended for release maintainers
freezing a new release), pass ``--write-evidence``. Continuous integration
uses this flag during release-tag builds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from erdos_ant.algebraic_geometry import (
    PROOF_DELTA_FORMULA,
    SOURCE_CLAIMS,
    SOURCE_REFINED_DELTA,
    AlgebraicNumberField,
    ClassFieldTowerGenerator,
    GolodShafarevichConstraint,
    HighDensityVacuumConfiguration,
    count_near_unit_pairs,
    estimate_unit_distance_delta,
    get_source_claim,
    local_density_exponent_probe,
)
from erdos_ant.genus_class_field import GenusClassFieldProbe
from erdos_ant.imaginary_quadratic_lattice import (
    eisenstein_integer_lattice,
    gaussian_integer_grid,
)
from erdos_ant.sawin_multiquadratic import (
    analyze as sawin_analyze,
)
from erdos_ant.sawin_multiquadratic import (
    evaluate_sawin_exponent_bound,
)


def _resolve_repo_root() -> Path:
    """Return the repository root (the directory containing reports/).

    Honour the ``ERDOS_ANT_REPO_ROOT`` env var if set; otherwise walk up
    from this file to find the first ancestor containing ``reports/`` or
    fall back to the current working directory.
    """

    env = os.environ.get("ERDOS_ANT_REPO_ROOT")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "reports").is_dir() and (parent / "src").is_dir():
            return parent
    return Path.cwd()


def _sha256_of(path: Path) -> str:
    """Return hex SHA-256 of file content, or 'missing' if file absent."""

    if not path.is_file():
        return "missing"
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _run_pytest(repo_root: Path) -> dict[str, object]:
    cmd = [sys.executable, "-m", "pytest", "-q", "tests"]
    proc = subprocess.run(
        cmd,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": " ".join(cmd),
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "passed": proc.returncode == 0,
    }


def execute_verification(repo_root: Path | None = None) -> dict[str, object]:
    """Run the full verification pipeline and return the result dict."""

    if repo_root is None:
        repo_root = _resolve_repo_root()

    openai_initial_claim = get_source_claim("openai_index_reported")
    sawin_refinement_claim = get_source_claim("sawin_refinement_reported")
    sawin_rigorous_claim = get_source_claim("sawin_rigorous_lower_bound")

    proof_delta_sample = PROOF_DELTA_FORMULA.evaluate(
        t=100, log_H_ell=10.0, R=2.0, D=1000.0
    )

    square_pairs = count_near_unit_pairs(
        np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    )
    square_exponent, square_delta = local_density_exponent_probe(16, 16)

    field = AlgebraicNumberField((1.0, 0.0, 1.0), discriminant=-4.0)
    tower = ClassFieldTowerGenerator(prime_degree=2, base_discriminant=-4.0)
    hdvc = HighDensityVacuumConfiguration(num_points=12, tower=tower, depth=2)
    density_metrics = hdvc.calculate_density_metrics()
    gs = GolodShafarevichConstraint(generator_count=4, relation_count=3)

    gaussian_analysis = gaussian_integer_grid(bound=3).analyze()
    eisenstein_analysis = eisenstein_integer_lattice(bound=3).analyze()
    phase2_analysis = GenusClassFieldProbe(split_primes=(29, 41)).analyze()
    phase3_analysis = sawin_analyze()
    sawin_eval = evaluate_sawin_exponent_bound()

    checks = {
        "square_unit_pairs_is_4": square_pairs == 4,
        "source_delta_metadata_only": square_delta != SOURCE_REFINED_DELTA,
        "density_claim_tier_research_only": (
            density_metrics["claim_tier"] == "research_only_proxy"
        ),
        "golod_shafarevich_proxy_boundary": gs.is_admissible(),
        "rename_alias_preserved": (
            estimate_unit_distance_delta is local_density_exponent_probe
        ),
        "source_registry_openai_initial_0014": (
            openai_initial_claim is not None
            and abs(openai_initial_claim.delta - 0.014) < 1e-12
            and "OpenAI" in openai_initial_claim.attribution
        ),
        "source_registry_sawin_refinement_00318": (
            sawin_refinement_claim is not None
            and abs(sawin_refinement_claim.delta - 0.0318) < 1e-12
            and "Sawin" in sawin_refinement_claim.attribution
        ),
        "source_registry_sawin_delta_not_equal_legacy_label": (
            sawin_refinement_claim is not None
            and abs(sawin_refinement_claim.delta - SOURCE_REFINED_DELTA) > 1e-6
        ),
        "source_claims_three_field_provenance_marked_correctly": (
            openai_initial_claim is not None
            and sawin_refinement_claim is not None
            and sawin_rigorous_claim is not None
            and openai_initial_claim.verified_numerical_in_formal_pdf is False
            and sawin_refinement_claim.verified_numerical_in_formal_pdf is False
            and sawin_rigorous_claim.verified_numerical_in_formal_pdf is True
        ),
        "sawin_rigorous_lower_bound_present_624e_minus_38": (
            sawin_rigorous_claim is not None
            and abs(sawin_rigorous_claim.delta - 6.24e-38) / 6.24e-38 < 0.01
        ),
        "proof_delta_formula_positive_for_reasonable_params": proof_delta_sample > 0,
        "phase1_gaussian_7x7_grid_has_expected_84_pairs": (
            gaussian_analysis["unit_distance_pairs"] == 84
        ),
        "phase1_eisenstein_exceeds_gaussian_at_same_bound": (
            eisenstein_analysis["unit_distance_pairs"]
            > gaussian_analysis["unit_distance_pairs"]
        ),
        "phase1_claims_h1_degenerate_tier": (
            gaussian_analysis["claim_tier"] == "faithful_h1_degenerate_case"
        ),
        "phase2_h2_genus_theory_hcf_is_Q_i_sqrt5": (
            phase2_analysis["hilbert_class_field"]["hilbert_class_field"]
            == "Q(i, sqrt(5))"
        ),
        "phase2_lemma22_pigeonhole_lower_bound_is_2": (
            phase2_analysis["lemma_22_predicted_lower_bound"] == 2
        ),
        "phase3_101_splits_in_L_T_compositum": (
            phase3_analysis["101_splits_in_L_T"] is True
        ),
        "phase3_golod_shafarevich_admissible": (
            phase3_analysis["galois_rank"]["admissible"] is True
        ),
        "phase3_matches_remarks_pdf_eq_2_2_624e_minus_38": (
            phase3_analysis["sawin_exponent_bound"]["matches_remarks_eq_2_2"]
            is True
        ),
        "phase3_external_verification_pdf_registered": (
            phase3_analysis["external_verification_pdf_url"].endswith(
                "unit-distance-remarks.pdf"
            )
        ),
    }

    pytest_result = _run_pytest(repo_root)
    checks["pytest_passed"] = pytest_result["passed"]

    # SHA-256 manifest binding the numerical claim to source files.
    sha_manifest = {
        path: _sha256_of(repo_root / path)
        for path in (
            "src/erdos_ant/sawin_multiquadratic.py",
            "src/erdos_ant/algebraic_geometry.py",
            "src/erdos_ant/imaginary_quadratic_lattice.py",
            "src/erdos_ant/genus_class_field.py",
            "src/erdos_ant/verify.py",
        )
    }

    result = {
        "schema_id": "erdos_ant_verification.v1",
        "schema_version": "1.0.0",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "repo_root": str(repo_root),
        "verdict": "PASS" if all(checks.values()) else "REVIEW_REQUIRED",
        "checks": checks,
        "source_sha256_manifest": sha_manifest,
        "observations": {
            "field_degree": field.degree,
            "square_near_unit_pairs": square_pairs,
            "square_exponent": square_exponent,
            "square_delta": square_delta,
            "source_refined_delta": SOURCE_REFINED_DELTA,
            "density_metrics": density_metrics,
            "phase1_lattice": {
                "gaussian": gaussian_analysis,
                "eisenstein": eisenstein_analysis,
                "proof_delta_formula_sample": proof_delta_sample,
            },
            "phase2_genus_class_field": phase2_analysis,
            "phase3_sawin_multiquadratic": phase3_analysis,
            "phase3_eq_2_2_evaluation": {
                "r": sawin_eval.r,
                "k": sawin_eval.k,
                "exponent_excess": sawin_eval.exponent_excess,
                "published_value": 6.24e-38,
                "relative_error_vs_published": (
                    abs(sawin_eval.exponent_excess - 6.24e-38) / 6.24e-38
                ),
            },
            "source_claims_registry": [
                {
                    "label": c.label,
                    "delta": c.delta,
                    "announced_date": c.announced_date,
                    "attribution": c.attribution,
                    "verified_numerical_in_formal_pdf": (
                        c.verified_numerical_in_formal_pdf
                    ),
                }
                for c in SOURCE_CLAIMS
            ],
        },
        "pytest": pytest_result,
    }
    return result


def write_report(result: dict[str, object], repo_root: Path) -> tuple[Path, Path]:
    reports_dir = repo_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / "verification_result.json"
    md_path = reports_dir / "verification_report.md"

    json_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    checks = result["checks"]
    check_lines = "\n".join(
        f"- {'PASS' if passed else 'FAIL'} `{name}`"
        for name, passed in checks.items()
    )
    pytest_result = result["pytest"]
    obs = result["observations"]
    eq22 = obs["phase3_eq_2_2_evaluation"]

    report = f"""# erdos-ant-verification report

**Verdict:** `{result["verdict"]}`
**Generated:** `{result["generated_at_utc"]}`
**Repo:** `{result["repo_root"]}`

## Checks

{check_lines}

## Phase 3 highlight: remarks PDF eq (2.2) reproduction

| | |
|---|---|
| r = 2 * prod(T) | `{eq22["r"]}` |
| k | `{eq22["k"]}` |
| Computed exponent excess | `{eq22["exponent_excess"]:.4e}` |
| Published value | `{eq22["published_value"]:.4e}` |
| Relative error vs published | `{eq22["relative_error_vs_published"]:.4f}` |

## Source SHA-256 manifest

| File | SHA-256 |
|---|---|
"""
    for src_path, digest in result["source_sha256_manifest"].items():
        report += f"| `{src_path}` | `{digest}` |\n"

    report += f"""
## Pytest

```text
{pytest_result["command"]}
returncode={pytest_result["returncode"]}
{pytest_result["stdout"]}
```
"""
    md_path.write_text(report, encoding="utf-8")
    return json_path, md_path


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="erdos-ant-verify",
        description=(
            "Run the erdos-ant-verification end-to-end checks and print "
            "the verdict. By default does not write to tracked evidence "
            "files; use --write-evidence to refresh them."
        ),
    )
    parser.add_argument(
        "--write-evidence",
        action="store_true",
        help=(
            "Write reports/verification_result.json and "
            "reports/verification_report.md (the tracked release-evidence "
            "files). Without this flag the verification runs but only "
            "prints the verdict, keeping the working tree clean."
        ),
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print only the verdict line (no per-check summary).",
    )
    return parser.parse_args(argv)


def _print_summary(analysis: dict[str, object], quiet: bool) -> None:
    print(f"Verdict: {analysis['verdict']}")
    if quiet:
        return
    checks = analysis["checks"]
    passed = sum(1 for v in checks.values() if v)
    print(f"Checks: {passed}/{len(checks)} passed")
    eq22 = analysis["observations"]["phase3_eq_2_2_evaluation"]
    print(
        f"eq (2.2) exponent excess: {eq22['exponent_excess']:.4e} "
        f"(published ~{eq22['published_value']:.2e}, "
        f"rel.err {eq22['relative_error_vs_published']:.4f})"
    )
    failed = [name for name, v in checks.items() if not v]
    if failed:
        print("Failed checks:")
        for name in failed:
            print(f"  - {name}")


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    repo_root = _resolve_repo_root()
    analysis = execute_verification(repo_root)
    _print_summary(analysis, args.quiet)

    if args.write_evidence:
        json_path, md_path = write_report(analysis, repo_root)
        print(f"Wrote: {json_path}")
        print(f"Wrote: {md_path}")
    else:
        print("(frozen-report mode: tracked evidence not written; "
              "pass --write-evidence to refresh)")

    return 0 if analysis["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
