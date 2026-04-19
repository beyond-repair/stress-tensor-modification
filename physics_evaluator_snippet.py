# Excerpt from physics_evaluator.py — Ware injection only
scaled_ldos = self.ware.apply_ware_coupling(ldos_field, n)
grad_psi_info = self.compute_stress_gradient(
    T * scaled_ldos[:, None, :, :, :], mesh_dx
)
