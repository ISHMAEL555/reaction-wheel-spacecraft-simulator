#!/usr/bin/env python3
"""
Example 1: Single Reaction Wheel Derivation
============================================

Demonstrates the mathematical derivation and basic setup of:
- Spacecraft rigid body dynamics (Euler equations)
- Reaction wheel model
- Coupled hub-wheel equations
"""

import sys
sys.path.insert(0, './src')

import numpy as np
from reaction_wheel import ReactionWheel
import rigid_body

print("=" * 70)
print("REACTION WHEEL SPACECRAFT SIMULATOR - DERIVATION EXAMPLE")
print("=" * 70)

# ===========================================================================
# Part 1: Rigid Body Dynamics
# ===========================================================================
print("\n1. RIGID BODY DYNAMICS (Euler Equations)")
print("-" * 70)

# Define a spacecraft with principal inertias
I_hub = np.diag([100.0, 120.0, 80.0])  # kg*m^2 (typical cubesat-like)
print(f"Spacecraft hub inertia matrix (kg·m²):\n{I_hub}\n")

# Small perturbation in angular velocity
w_body = np.array([0.01, 0.02, 0.01])  # rad/s
print(f"Initial body angular velocity: {w_body} rad/s")

# Small external torque
tau_ext = np.array([0.1, 0.0, 0.0])  # N*m
print(f"Applied external torque: {tau_ext} N·m")

# Compute angular acceleration using Euler equations
alpha = rigid_body.euler_dynamics(I_hub, w_body, tau_ext)
print(f"Resulting angular acceleration: {alpha} rad/s²\n")

# Compute angular momentum and kinetic energy
h = rigid_body.angular_momentum(I_hub, w_body)
ke = rigid_body.rotational_kinetic_energy(I_hub, w_body)
print(f"Angular momentum: {h} kg·m²/s")
print(f"Rotational kinetic energy: {ke:.4f} J\n")

# ===========================================================================
# Part 2: Attitude Representations
# ===========================================================================
print("\n2. ATTITUDE REPRESENTATIONS")
print("-" * 70)

# Euler angles (321 convention: yaw-pitch-roll)
roll = 0.1  # rad
pitch = 0.05  # rad
yaw = 0.2  # rad
print(f"Euler angles (rad): roll={roll}, pitch={pitch}, yaw={yaw}")

# Convert to DCM
dcm = rigid_body.dcm_from_euler_angles(roll, pitch, yaw)
print(f"\nDirection Cosine Matrix (DCM):\n{dcm}")

# Convert back to Euler angles
roll2, pitch2, yaw2 = rigid_body.euler_angles_from_dcm(dcm)
print(f"\nRecovered Euler angles (rad): roll={roll2}, pitch={pitch2}, yaw={yaw2}")

# Convert to quaternion
q = rigid_body.quaternion_from_dcm(dcm)
print(f"\nQuaternion representation: {q}")

# Convert quaternion back to DCM
dcm2 = rigid_body.dcm_from_quaternion(q)
print(f"\nRecovered DCM from quaternion:\n{dcm2}")
print(f"DCM recovery error: {np.linalg.norm(dcm - dcm2):.2e}\n")

# ===========================================================================
# Part 3: Kinematics (Euler Angle Rates)
# ===========================================================================
print("\n3. KINEMATICS (Euler Angle Rates)")
print("-" * 70)

euler_angles = np.array([roll, pitch, yaw])
w_body_small = np.array([0.01, 0.02, 0.015])  # rad/s

euler_rates = rigid_body.kinematics_euler(euler_angles, w_body_small)
print(f"Body rates: {w_body_small} rad/s")
print(f"Euler angle rates: {euler_rates} rad/s")
print(f"  d(roll)/dt   = {euler_rates[0]:.6f} rad/s")
print(f"  d(pitch)/dt  = {euler_rates[1]:.6f} rad/s")
print(f"  d(yaw)/dt    = {euler_rates[2]:.6f} rad/s\n")

# ===========================================================================
# Part 4: Reaction Wheel Model
# ===========================================================================
print("\n4. REACTION WHEEL MODEL")
print("-" * 70)

Iw = 0.5  # kg*m^2 (typical reaction wheel)
wheel = ReactionWheel(Iw, axis=2)  # Spinning about z-axis
print(f"Reaction wheel moment of inertia: {Iw} kg·m²")
print(f"Spin axis: z-axis (index=2)")

# Spin up the wheel with control torque
u_control = 0.5  # N*m control torque
wheel.update(dt=1.0, torque=u_control)
print(f"\nAfter 1 second with control torque {u_control} N·m:")
print(f"  Wheel angular velocity: {wheel.w:.4f} rad/s")
print(f"  Wheel angular acceleration: {wheel.alpha:.4f} rad/s²")

# Get angular momentum and torque
h_wheel = wheel.get_angular_momentum()
tau_on_body = wheel.get_control_torque_on_body()
print(f"\nWheel angular momentum: {h_wheel} kg·m²/s")
print(f"Reaction torque on body (Newton's 3rd law): {tau_on_body} N·m\n")

# ===========================================================================
# Part 5: Coupled Hub-Wheel Dynamics
# ===========================================================================
print("\n5. COUPLED HUB-WHEEL SYSTEM")
print("-" * 70)

from reaction_wheel import coupled_dynamics

# System parameters
w_hub_curr = np.array([0.01, 0.02, 0.01])  # rad/s
w_wheel_curr = 10.0  # rad/s
u_control = 0.1  # N*m control command
external_torque = np.array([0.05, 0.0, 0.0])  # Small external disturbance

# Compute coupled accelerations
alpha_hub, alpha_wheel = coupled_dynamics(
    Ih=I_hub,
    w_body=w_hub_curr,
    Iw=Iw,
    w_wheel=w_wheel_curr,
    u_wheel=u_control,
    external_torque=external_torque,
    axis=2
)

print(f"Hub angular velocity: {w_hub_curr} rad/s")
print(f"Wheel angular velocity: {w_wheel_curr} rad/s")
print(f"External torque: {external_torque} N·m")
print(f"Control torque to wheel: {u_control} N·m")
print(f"\nResulting accelerations:")
print(f"  Hub angular acceleration: {alpha_hub} rad/s²")
print(f"  Wheel angular acceleration: {alpha_wheel:.6f} rad/s²\n")

# ===========================================================================
# Summary
# ===========================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
The reaction wheel spacecraft simulator consists of:

1. RIGID BODY DYNAMICS:
   - Models spacecraft hub with 3 principal inertias
   - Implements Euler equations: I·α + ω×(I·ω) = τ
   - Supports multiple attitude representations (Euler angles, DCM, quaternions)

2. REACTION WHEEL ACTUATOR:
   - Momentum exchange device spinning about a principal axis
   - Generates control torque on spacecraft via Newton's 3rd law
   - Can store or release angular momentum

3. INTEGRATED DYNAMICS:
   - Hub and wheel coupled through momentum conservation
   - External torques applied to hub only
   - Control torques applied to wheel directly

This framework is suitable for:
- Attitude control simulations
- Reaction wheel saturation analysis
- Momentum dumping strategies
- Non-linear dynamics visualization
""")

print("=" * 70)
print("For full simulation example, run: 02_single_rw_simulation.py")
print("=" * 70)
