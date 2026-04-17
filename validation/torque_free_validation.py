#!/usr/bin/env python3
"""Torque-free validation for conservation laws.

Runs the existing coupled spacecraft model with zero external torque and zero wheel command,
then quantifies drift in angular momentum norm and kinetic energy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import matplotlib.pyplot as plt
import rigid_body
from spacecraft import CoupledSpacecraft


def main() -> None:
    I_hub = np.diag([100.0, 120.0, 80.0])
    I_wheel = 0.5

    sc = CoupledSpacecraft(I_hub=I_hub, I_wheel=I_wheel, wheel_axis=2, mass=50.0)
    sc.state.euler_angles = np.array([0.2, -0.15, 0.1])
    sc.state.w_body = np.array([0.08, -0.05, 0.06])
    sc.state.w_wheel = 2.0

    dt = 0.01
    t_final = 80.0
    n_steps = int(t_final / dt)

    t = np.zeros(n_steps)
    h_hub_norm = np.zeros(n_steps)
    ke = np.zeros(n_steps)

    for k in range(n_steps):
        t[k] = sc.state.time
        h_hub_norm[k] = np.linalg.norm(rigid_body.angular_momentum(sc.I_hub, sc.state.w_body))
        ke[k] = sc.get_rotational_kinetic_energy()
        sc.step(dt=dt, u_wheel=0.0, tau_ext=np.zeros(3))

    h0 = h_hub_norm[0]
    ke0 = ke[0]
    h_drift_pct = 100.0 * np.max(np.abs((h_hub_norm - h0) / h0))
    ke_drift_pct = 100.0 * np.max(np.abs((ke - ke0) / ke0))

    out_dir = Path(__file__).resolve().parents[1] / "plots"
    out_dir.mkdir(exist_ok=True)

    fig, ax = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    ax[0].plot(t, h_hub_norm, lw=1.7)
    ax[0].set_ylabel("||H_hub|| [kg m$^2$/s]")
    ax[0].set_title("Torque-free conservation check (hub)")
    ax[0].grid(alpha=0.3)

    ax[1].plot(t, ke, lw=1.7, color="darkorange")
    ax[1].set_ylabel("Kinetic energy [J]")
    ax[1].set_xlabel("Time [s]")
    ax[1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_dir / "torque_free_conservation.png", dpi=170)

    print("Torque-free validation complete")
    print(f"Max |H_hub| relative drift: {h_drift_pct:.5f}%")
    print(f"Max KE relative drift:   {ke_drift_pct:.5f}%")
    print(f"Saved: {out_dir / 'torque_free_conservation.png'}")


if __name__ == "__main__":
    main()
