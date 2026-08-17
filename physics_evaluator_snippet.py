#!/usr/bin/env python3
"""
DEPRECATED — DO NOT USE
=======================
This file is retained only so old links do not 404.

Problems with the historical snippet:
  - Maxwell stress was a zero placeholder
  - Default model "M2" conflicted with Option A (M2 is geometric only)
  - Numerical output was never physical validation

Use instead:
  physics_evaluator.py          — Maxwell + Ware surface evaluator
  bem_sierpinski.py             — electrostatic BEM
  rf_bem_sierpinski.py          — magnetostatic / quasi-static RF
  fullwave_bem.py               — frequency-domain EFIE
  couple_sierpinski_evaluator.py

Baseline: W_star = 1/(4π) ≈ 0.08 (phenomenology ledger); Option A.
"""

raise ImportError(
    "physics_evaluator_snippet.py is deprecated. "
    "Import physics_evaluator.py instead."
)
