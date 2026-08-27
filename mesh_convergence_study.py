#!/usr/bin/env python3
"""
mesh_convergence_study.py
-------------------------
Stage-2 mesh-convergence driver for the electrostatic BEM on the
0.45 asymmetric Sierpinski surface.

Protocol
--------
1. Generate meshes at successive aft depths n_aft = 1,2,3[,4].
2. Solve the collocation BEM (uniform external E).
3. Record |F_net|, direction, face count, sigma_rms.
4. Apply Richardson extrapolation (richardson_extrapolation.py).
5. Write a machine-readable JSON/Markdown summary.

This script does **not**:
  - claim physical thrust,
  - fit kappa to a target,
  - assert experimental validation.

It only quantifies numerical residual behaviour under refinement.

Claim flags remain:
  experimental_validation = false
  thrust_validated        = false
"""

from __future__ import annotations
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
import numpy as np

# Path bootstrap (sibling repo or local copy)
for c in [
    Path("/tmp/sg"),
    Path.cwd().parent / "sierpinski-geometry-045",
    Path(__file__).resolve().parent.parent / "sierpinski-geometry-045",
]:
    if (c / "sierpinski_generator.py").exists():
        sys.path.insert(0, str(c))
        break

from sierpinski_generator import generate_asymmetric_sierpinski  # noqa: E402
from bem_sierpinski import mesh_elements, bem_solve_conductor, maxwell_stress_force  # noqa: E402
from richardson_extrapolation import extrapolate_sequence, vector_extrapolate  # noqa: E402

EPS0 = 8.854187817e-12


def run_depth(n_aft: int, n_fore: int = 1, E0: float = 1.0) -> dict:
    V, F = generate_asymmetric_sierpinski(alpha=0.45, n_aft=n_aft, n_fore=n_fore)
    cents, norms, areas = mesh_elements(V, F)
    E_inf = np.array([0.0, 0.0, E0])
    sigma = bem_solve_conductor(cents, norms, areas, E_inf)
    F_net = maxwell_stress_force(norms, areas, sigma)
    return {
        "n_aft": n_aft,
        "n_fore": n_fore,
        "n_faces": int(len(areas)),
        "n_verts": int(len(V)),
        "Q_total": float(np.sum(sigma * areas)),
        "F_net": F_net.tolist(),
        "|F|": float(np.linalg.norm(F_net)),
        "direction": (F_net / (np.linalg.norm(F_net) + 1e-30)).tolist(),
        "sigma_rms": float(np.sqrt(np.mean(sigma ** 2))),
    }


def study(depths=(1, 2, 3), n_fore: int = 1, assumed_order: float | None = 1.0) -> dict:
    results = []
    for n in depths:
        print(f"Running n_aft={n} …")
        r = run_depth(n_aft=n, n_fore=n_fore)
        results.append(r)
        print(f"  faces={r['n_faces']}  |F|={r['|F|']:.6e}")

    mags = [r["|F|"] for r in results]
    forces = [np.array(r["F_net"]) for r in results]

    mag_extrap = extrapolate_sequence(mags, refinement_ratio=2.0, assumed_order=assumed_order)
    vec_extrap = vector_extrapolate(forces, refinement_ratio=2.0, assumed_order=assumed_order)

    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "protocol": "electrostatic collocation BEM, uniform E_z, alpha=0.45",
        "depths": list(depths),
        "n_fore": n_fore,
        "per_depth": results,
        "magnitude_richardson": mag_extrap,
        "vector_richardson": {
            "Q_star_vector": vec_extrap["Q_star_vector"].tolist(),
            "|Q_star|": vec_extrap["|Q_star|"],
            "direction_dots": vec_extrap["direction_dots"],
        },
        "claim_flags": {
            "experimental_validation": False,
            "thrust_validated": False,
            "energy_extraction_validated": False,
            "mesh_convergence_established": False,  # set True only after human review
        },
        "notes": [
            "Assumed order p=1 is the theoretical rate for piecewise-constant collocation.",
            "Observed order may differ because refinement is anisotropic (aft-only).",
            "|F| on a closed conductor in uniform E is a pure discretisation residual;",
            "  continuum limit should approach 0; non-zero Q* indicates remaining bias.",
            "Do not interpret residual as physical thrust.",
        ],
    }
    return report


def write_report(report: dict, prefix: str = "mesh_convergence") -> None:
    json_path = Path(f"{prefix}_report.json")
    md_path = Path(f"{prefix}_report.md")

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(f"Wrote {json_path}")

    lines = [
        "# Mesh Convergence Report (electrostatic BEM)",
        "",
        f"Generated: {report['timestamp_utc']}",
        "",
        "## Per-depth results",
        "",
        "| n_aft | faces | |F| | direction (x,y,z) |",
        "|------:|------:|----:|:------------------|",
    ]
    for r in report["per_depth"]:
        d = r["direction"]
        lines.append(
            f"| {r['n_aft']} | {r['n_faces']} | {r['|F|']:.6e} | "
            f"({d[0]:.4f}, {d[1]:.4f}, {d[2]:.4f}) |"
        )

    mr = report["magnitude_richardson"]
    lines += [
        "",
        "## Richardson (magnitude)",
        "",
        f"- relative changes : {[f'{x:.4e}' for x in mr['relative_changes']]}",
        f"- observed orders  : {mr['observed_orders']}",
        f"- p_used           : {mr['p_used']}",
        f"- Q_star (|F|)     : {mr['Q_star']}",
        "",
        "## Vector extrapolation",
        "",
        f"- Q_star vector    : {report['vector_richardson']['Q_star_vector']}",
        f"- |Q_star|         : {report['vector_richardson']['|Q_star|']}",
        f"- direction dots   : {report['vector_richardson']['direction_dots']}",
        "",
        "## Claim flags",
        "",
        "```",
        str(report["claim_flags"]),
        "```",
        "",
        "## Notes",
        "",
    ]
    for n in report["notes"]:
        lines.append(f"- {n}")

    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"Wrote {md_path}")


def main():
    print("=" * 60)
    print("Stage-2 Mesh Convergence Study (electrostatic BEM)")
    print("=" * 60)
    report = study(depths=(1, 2, 3), assumed_order=1.0)
    write_report(report)
    print("\nDone. Review Q_star and direction stability before any claim update.")
    print("=" * 60)


if __name__ == "__main__":
    main()
