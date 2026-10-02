#!/usr/bin/env python3
"""Frozen face-subdivision mesh for the stress evaluators.

This is a snapshot of ``generate_asymmetric_sierpinski`` so a clone of
this repository can build the 0.45 gasket without checking out
``sierpinski-geometry-045``. It is geometry input only: no fields,
no force, no thrust. The canonical geometry repository is not imported.
"""
from __future__ import annotations

from typing import List, Tuple

import numpy as np

# Regular tetrahedron vertices (centered, unit edge).
_BASE_VERTICES = np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, -1.0, -1.0],
        [-1.0, 1.0, -1.0],
        [-1.0, -1.0, 1.0],
    ],
    dtype=float,
)
_BASE_VERTICES -= _BASE_VERTICES.mean(axis=0)
_BASE_VERTICES /= np.linalg.norm(_BASE_VERTICES[0] - _BASE_VERTICES[1])


def _midpoint(a: np.ndarray, b: np.ndarray, alpha: float = 0.45) -> np.ndarray:
    """Point dividing segment a→b at fraction alpha from a."""
    return (1.0 - alpha) * a + alpha * b


def _subdivide_face(
    v0: np.ndarray,
    v1: np.ndarray,
    v2: np.ndarray,
    depth: int,
    alpha: float,
    vertices: List[np.ndarray],
    faces: List[Tuple[int, int, int]],
    vertex_index: dict,
) -> None:
    """Recursive face subdivision. Center triangle is omitted."""

    def idx(v: np.ndarray) -> int:
        key = tuple(np.round(v, decimals=10))
        if key not in vertex_index:
            vertex_index[key] = len(vertices)
            vertices.append(v.copy())
        return vertex_index[key]

    i0, i1, i2 = idx(v0), idx(v1), idx(v2)
    if depth <= 0:
        faces.append((i0, i1, i2))
        return

    m01 = _midpoint(v0, v1, alpha)
    m12 = _midpoint(v1, v2, alpha)
    m20 = _midpoint(v2, v0, alpha)
    _subdivide_face(v0, m01, m20, depth - 1, alpha, vertices, faces, vertex_index)
    _subdivide_face(v1, m12, m01, depth - 1, alpha, vertices, faces, vertex_index)
    _subdivide_face(v2, m20, m12, depth - 1, alpha, vertices, faces, vertex_index)


def generate_asymmetric_sierpinski(
    alpha: float = 0.45,
    n_aft: int = 3,
    n_fore: int = 1,
    aft_vertex: int = 3,
) -> Tuple[np.ndarray, np.ndarray]:
    """Build the asymmetric tetrahedron surface used by the BEM scripts.

    The center child of every subdivided face is omitted, so the mesh is
    an open gasket, not a watertight conductor.
    """
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must lie in (0, 1)")
    if n_aft < 0 or n_fore < 0:
        raise ValueError("depths must be non-negative")

    base = _BASE_VERTICES.copy()
    vertices: List[np.ndarray] = []
    faces: List[Tuple[int, int, int]] = []
    vertex_index: dict = {}

    # Face i is opposite vertex i. Face 3 is the default aft face.
    face_indices = [
        (1, 2, 3),
        (0, 2, 3),
        (0, 1, 3),
        (0, 1, 2),
    ]
    for opp, (a, b, c) in enumerate(face_indices):
        depth = n_aft if opp == aft_vertex else n_fore
        _subdivide_face(
            base[a], base[b], base[c], depth, alpha, vertices, faces, vertex_index
        )

    return np.array(vertices, dtype=float), np.array(faces, dtype=int)
