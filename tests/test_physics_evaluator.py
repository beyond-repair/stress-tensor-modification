import warnings
import numpy as np
from physics_evaluator import MaxwellStressTensorEvaluator, make_unit_sphere_surface
from closure import mesh_epsilon, uniform_E_two_surface


def test_null_and_uniform_E():
    ev = MaxwellStressTensorEvaluator(model="star")
    cents, norms, areas = make_unit_sphere_surface(8, 16)
    out = ev.evaluate(np.zeros_like(cents), np.zeros_like(cents), norms, areas)
    assert np.allclose(out["F_total"], 0.0)
    E = np.zeros_like(cents); E[:, 0] = 1.0
    out = ev.evaluate(E, np.zeros_like(cents), norms, areas)
    assert np.allclose(out["F_em"], 0.0, atol=1e-10)


def test_m2_uses_n_minus_3_not_n_minus_1():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ev = MaxwellStressTensorEvaluator(model="M2")
    assert abs(ev.W(3) - 0.08) < 1e-15
    assert ev.W(4) < 0.125
    assert ev.W(2) < ev.W(3) < ev.W(4)
    assert ev.W(3) < 0.10


def test_dual_surface_uniform_E_closes():
    r = uniform_E_two_surface()
    assert r.closed
    assert np.linalg.norm(r.F_inner) < 1e-8
    assert np.linalg.norm(r.F_outer) < 1e-8


def test_mesh_epsilon_definition():
    assert mesh_epsilon(np.array([1.0, 0, 0]), np.array([1.01, 0, 0])) < 0.02
