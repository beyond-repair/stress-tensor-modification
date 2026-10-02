#!/usr/bin/env python3
"""One-page stress-tensor diagnostic. Not a thrust claim."""
from __future__ import annotations

import warnings

import numpy as np

from bem_sierpinski import run as bem_run
from closure import uniform_E_two_surface
from couple_sierpinski_evaluator import run_case
from fullwave_bem import C, solve_fullwave
from physics_evaluator import (
    W_M2_PIN,
    W_STAR,
    MaxwellStressTensorEvaluator,
    make_unit_sphere_surface,
)
from rf_bem_sierpinski import run_all as rf_run

TARGET_FP = 3.0e-8  # published engineering figure, N/W; not fitted here


def collect() -> dict:
    ev = MaxwellStressTensorEvaluator(model="star")
    cents, norms, areas = make_unit_sphere_surface(8, 16)
    null = ev.evaluate(np.zeros_like(cents), np.zeros_like(cents), norms, areas)
    E = np.zeros_like(cents)
    E[:, 0] = 1.0
    uniform = ev.evaluate(E, np.zeros_like(cents), norms, areas)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        m2 = MaxwellStressTensorEvaluator(model="M2")
        w_m2 = {n: float(m2.W(n)) for n in (2, 3, 4, 5)}
    dual = uniform_E_two_surface()
    bem = [bem_run(n_aft=n) for n in (1, 2, 3)]
    rf = [rf_run(n_aft=n) for n in (1, 2, 3)]
    waves = []
    for n_aft in (1, 2, 3):
        for freq in (1e8, 1e9):
            waves.append(solve_fullwave(n_aft=n_aft, freq=freq))
    couple = [run_case(n_aft=n, n_fore=1) for n in (1, 2, 3)]
    photon = 1.0 / C
    pattern = []
    for row in waves:
        a = float(row["pattern_asymmetry"]["|A|"])
        pattern.append(
            {
                "n_aft": None,
                "freq_Hz": row["freq_Hz"],
                "n_faces": row["n_faces"],
                "|A|": a,
                "|A|/c": a / C,
                "|F|_surface_diagnostic": row["|F|_surface_diagnostic"],
                "P_rad_proxy": row["P_rad_proxy"],
                "thrust_validated": row["claim_flags"]["thrust_validated"],
            }
        )
    # n_aft is not a return key; recover from the loop order.
    i = 0
    for n_aft in (1, 2, 3):
        for _freq in (1e8, 1e9):
            pattern[i]["n_aft"] = n_aft
            i += 1
    return {
        "W_star": float(ev.W()),
        "W_m2_pin": float(W_M2_PIN),
        "W_m2": w_m2,
        "null_|F|": float(np.linalg.norm(null["F_total"])),
        "uniform_|F_em|": float(np.linalg.norm(uniform["F_em"])),
        "dual_closed": bool(dual.closed),
        "dual_|Fi|": float(np.linalg.norm(dual.F_inner)),
        "dual_|Fo|": float(np.linalg.norm(dual.F_outer)),
        "dual_epsilon_surface": float(dual.epsilon_surface),
        "bem": bem,
        "rf": rf,
        "pattern": pattern,
        "couple": couple,
        "one_over_c": photon,
        "target_F_per_P": TARGET_FP,
        "target_over_one_over_c": TARGET_FP / photon,
    }


def _fmt(v: np.ndarray) -> str:
    return np.array2string(np.asarray(v, dtype=float), precision=6, separator=" ")


def main() -> int:
    data = collect()
    w5 = data["W_m2"][5]
    print("=" * 68)
    print("Stress-tensor modification — diagnostic report")
    print("NOT thrust. NOT propulsion. NOT a completed physical law.")
    print("Class-B dual-surface epsilon_F is not computed.")
    print("=" * 68)
    print(f"W_star (model=star) = {data['W_star']:.17g} = 1/(4π)")
    print(f"equals W_STAR constant {W_STAR:.17g}: {abs(data['W_star'] - W_STAR) < 1e-15}")
    print(f"M2 pin W(3) = {data['W_m2'][3]:.17g} (declared {data['W_m2_pin']})")
    print(f"M2 W(4) = {data['W_m2'][4]:.17g}")
    print(
        f"M2 W(5) = {w5:.17g}  "
        + ("ABOVE 0.125 model-internal bound (miss; not refit)" if w5 > 0.125 else "within 0.125")
    )
    print(f"sphere null |F| = {data['null_|F|']:.6e}")
    print(f"uniform-E closed surface |F_em| = {data['uniform_|F_em|']:.6e}")
    print(
        f"dual uniform-E closed={data['dual_closed']} "
        f"|Fi|={data['dual_|Fi|']:.6e} |Fo|={data['dual_|Fo|']:.6e}"
    )
    print(
        "dual epsilon_surface uses a 1e-18 denominator floor when both forces "
        f"are ~0; printed ratio {data['dual_epsilon_surface']:.6e} is not epsilon_F."
    )
    print("-" * 68)
    print("Electrostatic BEM on the open 0.45 gasket (E_inf=1 V/m, unit edge)")
    for row in data["bem"]:
        print(
            f"  n_aft={row['n_aft']} faces={row['n_faces']} "
            f"|F|={row['|F|']:.6e} dir={_fmt(row['direction'])}"
        )
    bem_mags = [row["|F|"] for row in data["bem"]]
    print(
        f"  |F| {bem_mags[0]:.6e} → {bem_mags[-1]:.6e}: "
        + (
            "grew with refinement; not a closed-conductor null."
            if bem_mags[-1] > bem_mags[0]
            else "did not grow."
        )
    )
    print("-" * 68)
    print("Quasi-static RF / magnetostatic (B_inf=1 T is not a device force)")
    for row in data["rf"]:
        print(
            f"  faces={row['n_faces']} |Fe|={row['|Fe|']:.4e} "
            f"|Fm|={row['|Fm|']:.4e} |Frf|={row['|Frf|']:.4e}"
        )
    print("-" * 68)
    print("Full-wave scalarized EFIE pattern estimate")
    max_fp = 0.0
    for row in data["pattern"]:
        max_fp = max(max_fp, row["|A|/c"])
        print(
            f"  n_aft={row['n_aft']} f={row['freq_Hz']:.0e} faces={row['n_faces']} "
            f"|F|_diag={row['|F|_surface_diagnostic']:.4e} "
            f"|A|={row['|A|']:.4e} |A|/c={row['|A|/c']:.4e}"
        )
    print(f"photon ceiling 1/c = {data['one_over_c']:.6e} N/W")
    print(
        f"engineering target {data['target_F_per_P']:.6e} N/W "
        f"= {data['target_over_one_over_c']:.6f} / c"
    )
    print(
        f"max simulated |A|/c = {max_fp:.6e} N/W "
        "misses 3e-8; 1/c itself misses 3e-8. Not refit."
    )
    print("thrust_validated=false  epsilon_F_reported=false")
    print("-" * 68)
    print("Synthetic informational proxy (not a solved BVP; F_info is not newtons)")
    for row in data["couple"]:
        print(
            f"  n_aft={row['n_aft']} faces={row['n_faces']} "
            f"W_used={row['W_used']:.17g} |F_total|={np.linalg.norm(row['F_total']):.6e}"
        )
    print("=" * 68)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
