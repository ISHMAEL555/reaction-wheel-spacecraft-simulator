#!/usr/bin/env python3
"""Closed-loop PD demonstration with disturbance and control metrics."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import matplotlib.pyplot as plt
from spacecraft import CoupledSpacecraft


def main() -> None:
    I_hub = np.diag([100.0, 120.0, 80.0])
    I_wheel = 0.5

    # Use wheel aligned with pitch axis for direct single-axis control authority.
    sc = CoupledSpacecraft(I_hub=I_hub, I_wheel=I_wheel, wheel_axis=1, mass=50.0)
    # Single-axis case: initialize mainly pitch to evaluate pitch-loop behavior.
    sc.state.euler_angles = np.array([0.0, 0.10, 0.0])
    sc.state.w_body = np.array([0.0, -0.03, 0.0])
    sc.state.w_wheel = 0.0

    dt = 0.01
    t_final = 60.0
    n_steps = int(t_final / dt)

    # gains selected for near-critical damping in pitch channel
    Kp = 12.0
    Kd = 6.0
    u_max = 1.2

    t = np.zeros(n_steps)
    pitch = np.zeros(n_steps)
    pitch_rate = np.zeros(n_steps)
    wheel_speed = np.zeros(n_steps)
    u_hist = np.zeros(n_steps)

    disturbance = np.array([0.0, 0.0, 0.0])

    for k in range(n_steps):
        t[k] = sc.state.time
        theta = sc.state.euler_angles[1]
        theta_dot = sc.state.w_body[1]

        # Positive wheel torque produces negative body reaction torque in this model,
        # so the stabilizing sign is +Kp*theta + Kd*theta_dot.
        u = Kp * theta + Kd * theta_dot
        u = np.clip(u, -u_max, u_max)

        if 18.0 <= sc.state.time <= 24.0:
            disturbance = np.array([0.0, 0.03, 0.0])
        else:
            disturbance = np.zeros(3)

        sc.step(dt=dt, u_wheel=u, tau_ext=disturbance)

        pitch[k] = sc.state.euler_angles[1]
        pitch_rate[k] = sc.state.w_body[1]
        wheel_speed[k] = sc.state.w_wheel
        u_hist[k] = u

    out_dir = Path(__file__).resolve().parents[1] / "plots"
    out_dir.mkdir(exist_ok=True)

    fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    ax[0].plot(t, np.degrees(pitch), lw=1.8)
    ax[0].axhline(0.0, color="k", lw=0.8)
    ax[0].set_ylabel("Pitch [deg]")
    ax[0].grid(alpha=0.3)

    ax[1].plot(t, pitch_rate, lw=1.8, color="tab:orange")
    ax[1].set_ylabel("Pitch rate [rad/s]")
    ax[1].grid(alpha=0.3)

    ax[2].plot(t, u_hist, lw=1.5, color="tab:green", label="u")
    ax[2].plot(t, wheel_speed, lw=1.2, color="tab:red", label="wheel speed")
    ax[2].set_ylabel("Control / wheel")
    ax[2].set_xlabel("Time [s]")
    ax[2].grid(alpha=0.3)
    ax[2].legend(loc="best")

    fig.suptitle("Closed-loop PD response with disturbance window")
    fig.tight_layout()
    fig.savefig(out_dir / "closed_loop_pd_response.png", dpi=170)

    settle_idx = np.where(np.abs(np.degrees(pitch)) < 0.5)[0]
    settle_time = t[settle_idx[0]] if len(settle_idx) > 0 else np.nan

    print("Closed-loop PD demo complete")
    print(f"Peak |pitch| [deg]: {np.max(np.abs(np.degrees(pitch))):.3f}")
    print(f"Approx settling time to ±0.5 deg [s]: {settle_time:.2f}")
    print(f"Peak |u| [N m]: {np.max(np.abs(u_hist)):.3f}")
    print(f"Peak |wheel speed| [rad/s]: {np.max(np.abs(wheel_speed)):.3f}")
    print(f"Saved: {out_dir / 'closed_loop_pd_response.png'}")


if __name__ == "__main__":
    main()
