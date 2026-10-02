"""Checks that the diagnostics run and report misses. Not a thrust suite."""
from __future__ import annotations

import importlib
import warnings
from pathlib import Path

import numpy as np
import pytest

from bem_sierpinski import run as bem_run
from cli import collect
from couple_sierpinski_evaluator import run_case
from fullwave_bem import C, solve_fullwave
from local_geometry import generate_asymmetric_sierpinski
from physics_evaluator import W_STAR, MaxwellStressTensorEvaluator, make_unit_sphere_surface
from rf_bem_sierpinski import run_all as rf_run

ROOT = Path(__file__).resolve().parents[1]
TARGET = 3.0e-8


def test_scripts_do_not_import_sibling_repo():
    for name in (
        "bem_sierpinski.py",
        "rf_bem_sierpinski.py",
        "fullwave_bem.py",
        "couple_sierpinski_evaluator.py",
        "local_geometry.py",
    ):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "sierpinski_generator" not in text
        assert "sys.path" not in text


def test_open_gasket_face_counts():
    expected = {1: 12, 2: 18, 3: 36}
    for n_aft, n_faces in expected.items():
        _v, faces = generate_asymmetric_sierpinski(alpha=0.45, n_aft=n_aft, n_fore=1)
        assert len(faces) == n_faces


def test_constant_info_cancels_on_sphere_varying_does_not():
    ev = MaxwellStressTensorEvaluator(model="star")
    cents, norms, areas = make_unit_sphere_surface(12, 24)
    zeros = np.zeros_like(cents)
    constant = ev.evaluate(zeros, zeros, norms, areas, info_field=np.ones(len(cents)))
    varying = ev.evaluate(zeros, zeros, norms, areas, info_field=cents[:, 2])
    assert np.linalg.norm(constant["F_info"]) < 1e-8
    assert np.linalg.norm(varying["F_info"]) > 1e-4
    assert constant["W_used"] == pytest.approx(W_STAR)


def test_electrostatic_residual_grows_and_is_not_thrust():
    rows = [bem_run(n_aft=n) for n in (1, 2, 3)]
    mags = [row["|F|"] for row in rows]
    assert mags[0] == pytest.approx(2.991747e-11, rel=1e-4)
    assert mags[2] > mags[1] > mags[0]
    assert all(np.isfinite(row["direction"]).all() for row in rows)


def test_magnetostatic_bookkeeping_is_huge_at_one_tesla():
    row = rf_run(n_aft=1)
    assert row["|Fe|"] < 1e-9
    assert row["|Fm|"] > 1.0e5


def test_fullwave_pattern_misses_engineering_target():
    max_fp = 0.0
    for n_aft in (1, 2, 3):
        for freq in (1e8, 1e9):
            row = solve_fullwave(n_aft=n_aft, freq=freq)
            assert row["claim_flags"]["thrust_validated"] is False
            assert row["claim_flags"]["epsilon_F_reported"] is False
            assert row["claim_flags"]["reactionless_closed_thrust"] is False
            a = row["pattern_asymmetry"]["|A|"]
            assert 0.0 < a <= 1.0
            fp = a / C
            assert fp < TARGET
            assert fp < (1.0 / C) + 1e-15
            max_fp = max(max_fp, fp)
    assert max_fp < TARGET
    assert (1.0 / C) < TARGET


def test_synthetic_couple_uses_star_anchor_not_m2_pin():
    row = run_case(n_aft=1, n_fore=1)
    assert row["W_used"] == pytest.approx(1.0 / (4.0 * np.pi))
    assert row["W_used"] != pytest.approx(0.08)
    assert np.linalg.norm(row["F_em"]) < 1e-8
    assert np.linalg.norm(row["F_info"]) > 1e-3


def test_m2_depth_five_exceeds_internal_bound():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        ev = MaxwellStressTensorEvaluator(model="M2")
    assert ev.W(3) == pytest.approx(0.08)
    assert ev.W(5) == pytest.approx(0.08 * np.exp(0.46))
    assert ev.W(5) > 0.125


def test_snippet_stays_quarantined():
    with pytest.raises(ImportError, match="deprecated"):
        importlib.import_module("physics_evaluator_snippet")


def test_collect_report_flags():
    data = collect()
    assert data["W_star"] == pytest.approx(W_STAR)
    assert data["dual_closed"] is True
    assert data["dual_|Fi|"] < 1e-8
    assert data["W_m2"][5] > 0.125
    assert data["bem"][-1]["|F|"] > data["bem"][0]["|F|"]
    assert max(row["|A|/c"] for row in data["pattern"]) < TARGET
    assert data["target_over_one_over_c"] == pytest.approx(3e-8 * C, rel=1e-9)
    assert all(row["W_used"] == pytest.approx(W_STAR) for row in data["couple"])
