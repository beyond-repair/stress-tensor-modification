# physics_evaluator.py — Ware Injection & Stress Tensor Evaluator (v1.1)
import numpy as np

class MaxwellStressTensorEvaluator:
    def __init__(self, W_base=0.08, model='M2', chi_vac=1.0):
        self.W_base = W_base
        self.model = model
        self.chi_vac = chi_vac  # vacuum susceptibility (tuned from baseline sim)

    def W(self, n):
        """M2 renormalization"""
        return self.W_base * np.exp(0.23 * (n - 1))

    def apply_ware_coupling(self, ldos_field, n):
        """Apply Ware scaling to LDOS gradient (fractal transducer)"""
        scaled = self.W(n) * self.chi_vac * ldos_field
        # Optional: |A|^4 saturation proxy at high LDOS
        # scaled = scaled / (1 + lambda_A * np.abs(scaled)**2)
        return scaled

    def compute_stress_gradient(self, tensor_field, mesh_dx):
        """Compute (∇ Ψ_info) contribution for surface integral"""
        # Finite difference gradient (vectorized)
        grad = np.gradient(tensor_field, mesh_dx, axis=(2,3,4))  # adjust axes per mesh
        return grad

    def evaluate_force_density(self, E, H, ldos_field, n=3, mesh_dx=1.0, mesh_L=1.0):
        """Full evaluation: EM + Ware contribution"""
        # EM part (cancels on closed surface)
        T_em = self.compute_maxwell_stress(E, H)  # placeholder impl

        scaled_ldos = self.apply_ware_coupling(ldos_field, n)
        grad_psi_info = self.compute_stress_gradient(
            T_em * scaled_ldos[:, None, :, :, :], mesh_dx  # corrected tensor multiply
        )

        # Surface integral proxy (net Ware flux)
        F_surface = np.sum(grad_psi_info * mesh_L**3, axis=(2,3,4))  # volume → flux approx
        delta_F = F_surface  # Ware residual (EM \~0)

        # Validation
        if n == 3:
            assert abs(self.W(n) - 0.1267) < 0.001, "W(3) mismatch"
        # Add W=0 test: delta_F ≈0

        return {"F_total": F_surface, "delta_F_Ware": delta_F, "scaled_ldos": scaled_ldos}

    def compute_maxwell_stress(self, E, H):
        """Standard EM tensor (placeholder)"""
        # Implement full Maxwell stress tensor here
        return np.zeros_like(E)  # stub for integration

# Usage
# evaluator = MaxwellStressTensorEvaluator()
# results = evaluator.evaluate_force_density(E, H, ldos_field, n=4)