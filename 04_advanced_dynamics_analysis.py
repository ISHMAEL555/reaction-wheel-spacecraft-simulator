#!/usr/bin/env python3
"""
Advanced Dynamics Analysis Script
==================================

Comprehensive analysis of spacecraft attitude dynamics with advanced plots:
- Polhode (body-fixed frame trajectory)
- Herpolhode (inertial frame trajectory)
- Nutation, precession, transverse, and spin rates
- Energy and momentum conservation analysis

This script runs a full spacecraft dynamics simulation and generates
advanced visualization plots for attitude analysis.

Run: python3 04_advanced_dynamics_analysis.py
Expected time: ~15 seconds
Generated files: 3 PNG plots
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from spacecraft import CoupledSpacecraft
from utils import (
    SimulationLogger,
    plot_polhode_herpolhode,
    plot_nutation_precession_rates,
    plot_energy_momentum_analysis,
    degrees
)

# ============================================================================
# Configuration
# ============================================================================

# Spacecraft inertia tensor (kg·m²) - asymmetric body
I_hub = np.array([
    [100.0,   0.0,   0.0],
    [  0.0, 120.0,   0.0],
    [  0.0,   0.0,  80.0]
])

# Reaction wheel inertia (kg·m²)
I_wheel = 0.5

# Initial conditions
roll_0 = 0.0          # rad
pitch_0 = 0.0         # rad
yaw_0 = 0.0           # rad
wx_0 = 0.05           # rad/s
wy_0 = 0.02           # rad/s
wz_0 = 0.01           # rad/s
w_wheel_0 = 100.0     # rad/s (reaction wheel spin rate)

# Simulation parameters
dt = 0.01             # Time step (s)
t_final = 30.0        # Simulation duration (s)

# ============================================================================
# Helper Functions
# ============================================================================

def compute_inertial_angular_momentum(spacecraft, euler_angles, w_body):
    """
    Transform angular momentum from body frame to inertial frame.
    
    Parameters
    ----------
    spacecraft : CoupledSpacecraft
        Spacecraft dynamics object
    euler_angles : np.ndarray
        [roll, pitch, yaw] in radians
    w_body : np.ndarray
        Angular velocity in body frame [wx, wy, wz]
    
    Returns
    -------
    np.ndarray
        Angular momentum in inertial frame [hx, hy, hz]
    """
    # Compute DCM (body to inertial)
    phi, theta, psi = euler_angles
    
    # 321 Euler angle convention (Yaw-Pitch-Roll)
    c_phi = np.cos(phi)
    s_phi = np.sin(phi)
    c_theta = np.cos(theta)
    s_theta = np.sin(theta)
    c_psi = np.cos(psi)
    s_psi = np.sin(psi)
    
    # DCM matrix (body to inertial)
    DCM = np.array([
        [c_theta*c_psi, c_theta*s_psi, -s_theta],
        [s_phi*s_theta*c_psi - c_phi*s_psi, 
         s_phi*s_theta*s_psi + c_phi*c_psi, 
         s_phi*c_theta],
        [c_phi*s_theta*c_psi + s_phi*s_psi, 
         c_phi*s_theta*s_psi - s_phi*c_psi, 
         c_phi*c_theta]
    ])
    
    # Angular momentum in body frame
    h_body = np.dot(I_hub, w_body)
    
    # Transform to inertial frame
    h_inertial = np.dot(DCM.T, h_body)
    
    return h_inertial


def run_simulation():
    """Run the spacecraft dynamics simulation."""
    
    print("=" * 76)
    print("ADVANCED DYNAMICS ANALYSIS - SPACECRAFT ATTITUDE SIMULATION")
    print("=" * 76)
    print()
    
    # Create spacecraft
    print("Initializing spacecraft dynamics...")
    spacecraft = CoupledSpacecraft(I_hub, I_wheel, wheel_axis=2)
    
    # Set initial conditions
    state_init = np.array([
        roll_0, pitch_0, yaw_0,
        wx_0, wy_0, wz_0,
        w_wheel_0
    ])
    spacecraft.set_state_vector(state_init)
    
    print(f"  Hub inertia: {np.diag(I_hub)} kg·m²")
    print(f"  Wheel inertia: {I_wheel} kg·m²")
    print(f"  Initial rates: ωx={wx_0}, ωy={wy_0}, ωz={wz_0} rad/s")
    print(f"  Wheel speed: {w_wheel_0} rad/s")
    print()
    
    # Logger
    logger = SimulationLogger()
    
    # Run simulation
    print("Running simulation...")
    num_steps = int(t_final / dt)
    
    for step in range(num_steps):
        t = step * dt
        
        # Get current state
        state = spacecraft.get_state_vector()
        euler = state[:3]
        w = state[3:6]
        w_wheel = state[6]
        
        # Compute inertial angular momentum
        h_inertial = compute_inertial_angular_momentum(spacecraft, euler, w)
        
        # Log
        logger.log(
            t=t,
            euler=euler,
            w_body=w,
            w_wheel=w_wheel,
            h=h_inertial
        )
        
        # Integrate one step
        spacecraft.step(dt, u_wheel=0.0, tau_ext=np.array([0.0, 0.0, 0.0]))
        
        if (step + 1) % int(num_steps / 10) == 0:
            progress = 100 * (step + 1) / num_steps
            print(f"  {progress:5.1f}% complete...")
    
    print(f"✓ Simulation complete ({num_steps} steps, {t_final} seconds)")
    print()
    
    return logger, spacecraft


def generate_plots(logger, spacecraft):
    """Generate advanced dynamics plots."""
    
    print("Generating advanced dynamics plots...")
    print()
    
    t = logger.time
    w_body = logger.w_body
    h_inertial = logger.h_total
    
    # 1. Polhode and Herpolhode
    print("  1. Polhode & Herpolhode (trajectory plots)...")
    fig, axes = plot_polhode_herpolhode(t, w_body, h_inertial, figsize=(14, 6))
    fig.savefig('plot_polhode_herpolhode.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("     ✓ Saved: plot_polhode_herpolhode.png")
    
    # 2. Nutation, Precession, Transverse, Spin Rates
    print("  2. Nutation & Precession Rates (time series)...")
    fig, axes = plot_nutation_precession_rates(t, w_body, h_inertial, spacecraft.I_hub, figsize=(14, 10))
    fig.savefig('plot_nutation_precession_rates.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("     ✓ Saved: plot_nutation_precession_rates.png")
    
    # 3. Energy and Momentum Analysis
    print("  3. Energy & Momentum Conservation...")
    fig, axes = plot_energy_momentum_analysis(t, w_body, h_inertial, spacecraft.I_hub, figsize=(14, 6))
    fig.savefig('plot_energy_momentum_analysis.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("     ✓ Saved: plot_energy_momentum_analysis.png")
    
    print()
    print("=" * 76)
    print("ANALYSIS RESULTS")
    print("=" * 76)
    
    # Compute and display statistics
    w_mag = np.linalg.norm(np.array(w_body), axis=1)
    h_mag = np.linalg.norm(np.array(h_inertial), axis=1)
    
    print(f"\nAngular Velocity Statistics:")
    print(f"  Mean magnitude: {np.mean(w_mag):.6f} rad/s")
    print(f"  Min magnitude:  {np.min(w_mag):.6f} rad/s")
    print(f"  Max magnitude:  {np.max(w_mag):.6f} rad/s")
    print(f"  Std deviation:  {np.std(w_mag):.6f} rad/s")
    
    print(f"\nAngular Momentum Statistics:")
    print(f"  Mean magnitude: {np.mean(h_mag):.6f} kg·m²/s")
    print(f"  Min magnitude:  {np.min(h_mag):.6f} kg·m²/s")
    print(f"  Max magnitude:  {np.max(h_mag):.6f} kg·m²/s")
    print(f"  Std deviation:  {np.std(h_mag):.6f} kg·m²/s")
    print(f"  Change (%):     {100*(h_mag[-1]-h_mag[0])/h_mag[0]:.3f}%")
    
    # Energy conservation
    KE = np.zeros(len(t))
    for i in range(len(t)):
        w = np.array(w_body[i])
        KE[i] = 0.5 * np.dot(w, np.dot(spacecraft.I_hub, w))
    
    print(f"\nRotational Kinetic Energy:")
    print(f"  Initial: {KE[0]:.6f} J")
    print(f"  Final:   {KE[-1]:.6f} J")
    print(f"  Change:  {KE[-1] - KE[0]:.6f} J ({100*(KE[-1]-KE[0])/KE[0]:.3f}%)")
    
    print()
    print("=" * 76)
    print("INTERPRETATION GUIDE")
    print("=" * 76)
    print("""
POLHODE: Body-fixed frame trajectory of angular velocity vector
  - Shows natural precession of ω around body principal axes
  - Closed curve indicates periodic motion
  - Shape depends on inertia tensor asymmetry

HERPOLHODE: Inertial frame trajectory of angular momentum vector
  - Shows absolute motion in space-fixed frame
  - Angular momentum is approximately conserved (if no external torques)
  - Precession around fixed inertial axis

NUTATION: Wobbling motion of angular velocity
  - Angle between ω and angular momentum vector h
  - Periodic oscillation indicates coupled hub-wheel dynamics
  - Amplitude and frequency depend on system parameters

PRECESSION: Rotation of angular momentum in inertial frame
  - Rate of change of h direction
  - Can be computed from torque: dh/dt = τ
  - Zero precession for torque-free motion

SPIN RATE: Component of ω along angular momentum direction
  - Approximately constant for torque-free body
  - Reflects primary rotation axis

TRANSVERSE RATE: Component of ω perpendicular to h
  - Causes nutation and tumbling motion
  - Small for stable spinning spacecraft

ENERGY & MOMENTUM:
  - Rotational KE = 0.5 * ω^T * I * ω
  - Angular momentum h = I * ω (in body frame)
  - Conservation violations indicate numerical integration errors
""")
    
    print("=" * 76)


def main():
    """Main execution."""
    try:
        logger, spacecraft = run_simulation()
        generate_plots(logger, spacecraft)
        
        print("\n✓ Analysis complete!")
        print("\nGenerated files:")
        print("  - plot_polhode_herpolhode.png")
        print("  - plot_nutation_precession_rates.png")
        print("  - plot_energy_momentum_analysis.png")
        print()
        
        return 0
    
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
