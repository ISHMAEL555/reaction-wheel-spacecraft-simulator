#!/usr/bin/env python3
"""
Template: Creating Your Own Custom Simulation Script
=====================================================

This is a template you can copy and modify to create custom simulations.
Use this as a starting point for your own experiments.
"""

import sys
sys.path.insert(0, './src')

import numpy as np
from spacecraft import CoupledSpacecraft
from utils import SimulationLogger
import matplotlib.pyplot as plt

print("=" * 70)
print("CUSTOM SIMULATION TEMPLATE")
print("=" * 70)

# ===========================================================================
# STEP 1: Configure Your Spacecraft
# ===========================================================================
print("\nSTEP 1: Configuring spacecraft...")

# Define spacecraft properties
I_hub = np.diag([100.0, 120.0, 80.0])  # Principal inertias (kg·m²)
I_wheel = 0.5  # Reaction wheel inertia (kg·m²)
mass = 50.0  # Total mass (kg)

# Create spacecraft object
spacecraft = CoupledSpacecraft(
    I_hub=I_hub,
    I_wheel=I_wheel,
    wheel_axis=2,  # Z-axis for reaction wheel
    mass=mass,
    name="MySpacecraft"
)

print(f"✓ Spacecraft created")
print(f"  Hub inertia: {np.diag(I_hub)}")
print(f"  Wheel inertia: {I_wheel} kg·m²")

# ===========================================================================
# STEP 2: Set Initial Conditions
# ===========================================================================
print("\nSTEP 2: Setting initial conditions...")

# Initial attitude (Euler angles in radians)
initial_roll = 0.1  # rad (~5.7 degrees)
initial_pitch = 0.05  # rad (~2.9 degrees)
initial_yaw = 0.0  # rad

# Initial angular velocities (rad/s)
initial_wx = 0.05  # rad/s
initial_wy = 0.03  # rad/s
initial_wz = 0.01  # rad/s

# Initial reaction wheel speed (rad/s)
initial_w_wheel = 0.0  # Start from rest

# Apply initial conditions
spacecraft.state.euler_angles = np.array([initial_roll, initial_pitch, initial_yaw])
spacecraft.state.w_body = np.array([initial_wx, initial_wy, initial_wz])
spacecraft.state.w_wheel = initial_w_wheel

print(f"✓ Initial conditions set")
print(f"  Euler angles (rad): {spacecraft.state.euler_angles}")
print(f"  Body rates (rad/s): {spacecraft.state.w_body}")
print(f"  Wheel speed (rad/s): {spacecraft.state.w_wheel}")

# ===========================================================================
# STEP 3: Define Simulation Parameters
# ===========================================================================
print("\nSTEP 3: Setting up simulation...")

dt = 0.01  # Time step (seconds)
t_final = 50.0  # Total simulation time (seconds)
n_steps = int(t_final / dt)

print(f"✓ Simulation parameters")
print(f"  Time step: {dt} s")
print(f"  Duration: {t_final} s")
print(f"  Total steps: {n_steps}")

# ===========================================================================
# STEP 4: Initialize Logger
# ===========================================================================
print("\nSTEP 4: Initializing data logger...")

logger = SimulationLogger()
print(f"✓ Logger ready")

# ===========================================================================
# STEP 5: Define Your Control Law
# ===========================================================================
print("\nSTEP 5: Defining control law...")

# Example: Simple PD controller on pitch angle
Kp = 10.0  # Proportional gain
Kd = 5.0   # Derivative gain

def control_law(spacecraft, t):
    """
    Compute control command at time t.
    
    Inputs:
        spacecraft: CoupledSpacecraft object (read current state)
        t: Current simulation time (seconds)
    
    Outputs:
        u_wheel: Control torque command (N·m)
        tau_ext: External disturbance (3,) or None
    """
    # Extract current state
    euler = spacecraft.state.euler_angles
    w_body = spacecraft.state.w_body
    
    # Compute pitch error
    pitch_target = 0.0  # Desired pitch angle
    pitch = euler[1]
    pitch_rate = w_body[1]
    
    pitch_error = pitch - pitch_target
    pitch_rate_error = pitch_rate
    
    # PD control law
    u_control = -(Kp * pitch_error + Kd * pitch_rate_error)
    
    # Limit control authority
    u_max = 1.0  # Maximum control torque (N·m)
    u_control = np.clip(u_control, -u_max, u_max)
    
    # Define external disturbances
    tau_ext = None  # No external disturbance by default
    
    # Example: Apply a pulse disturbance at t=25s
    if 25.0 <= t <= 26.0:
        tau_ext = np.array([0.1, 0.0, 0.0])  # 0.1 N·m pulse about x-axis
    
    return u_control, tau_ext

print(f"✓ Control law defined")
print(f"  Controller: PD (Kp={Kp}, Kd={Kd})")
print(f"  Target: Pitch angle = 0 rad")
print(f"  Disturbance: 0.1 N·m pulse at t∈[25, 26] s")

# ===========================================================================
# STEP 6: Run Simulation Loop
# ===========================================================================
print("\nSTEP 6: Running simulation...")
print(f"  Progress: [", end="", flush=True)

prev_percent = -1
for step in range(n_steps):
    t = spacecraft.state.time
    
    # Compute control command
    u_control, tau_ext = control_law(spacecraft, t)
    
    # Take one simulation step
    spacecraft.step(dt=dt, u_wheel=u_control, tau_ext=tau_ext)
    
    # Log data
    logger.log(
        t=t,
        euler=spacecraft.state.euler_angles,
        w_body=spacecraft.state.w_body,
        w_wheel=spacecraft.state.w_wheel,
        tau_wheel=spacecraft.wheel.get_control_torque_on_body(),
        h=spacecraft.get_angular_momentum(),
        ke=spacecraft.get_rotational_kinetic_energy()
    )
    
    # Progress bar
    percent = (step + 1) * 100 // n_steps
    if percent != prev_percent and percent % 10 == 0:
        print("=", end="", flush=True)
        prev_percent = percent

print("] DONE!")

# ===========================================================================
# STEP 7: Analyze Results
# ===========================================================================
print("\nSTEP 7: Analyzing results...")

df = logger.to_dataframe()

# Key metrics
final_pitch = df['pitch'].iloc[-1]
final_pitch_rate = df['wy'].iloc[-1]
final_wheel_speed = df['w_wheel'].iloc[-1]
max_wheel_speed = np.max(np.abs(df['w_wheel'].values))
final_ke = df['ke'].iloc[-1]

print(f"✓ Final state:")
print(f"  Pitch angle: {final_pitch:.6f} rad ({np.degrees(final_pitch):.3f}°)")
print(f"  Pitch rate: {final_pitch_rate:.6f} rad/s")
print(f"  Wheel speed: {final_wheel_speed:.4f} rad/s")
print(f"  Max wheel speed: {max_wheel_speed:.4f} rad/s")
print(f"  Total kinetic energy: {final_ke:.4f} J")

# Compute statistics
pitch_error_rms = np.sqrt(np.mean(df['pitch'].values ** 2))
print(f"\n✓ Performance metrics:")
print(f"  Pitch RMS error: {pitch_error_rms:.6f} rad")
print(f"  Pitch max error: {np.max(np.abs(df['pitch'].values)):.6f} rad")
print(f"  Wheel momentum: {I_wheel * final_wheel_speed:.4f} kg·m²/s")

# ===========================================================================
# STEP 8: Export Data
# ===========================================================================
print("\nSTEP 8: Exporting data...")

# Save to CSV
logger.save_csv('my_simulation_results.csv')
print(f"✓ Data exported to: my_simulation_results.csv")

# ===========================================================================
# STEP 9: Create Plots
# ===========================================================================
print("\nSTEP 9: Creating plots...")

# Plot 1: Pitch angle over time
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(logger.time, np.degrees(np.array(logger.euler_angles)[:, 1]), 'b-', linewidth=2)
ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
ax.axvspan(25, 26, alpha=0.2, color='red', label='Disturbance')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Pitch (degrees)')
ax.set_title('Pitch Angle vs Time')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig('my_custom_pitch.png', dpi=150)
print(f"  Saved: my_custom_pitch.png")

# Plot 2: Wheel speed over time
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(logger.time, logger.w_wheel, 'g-', linewidth=2)
ax.axvspan(25, 26, alpha=0.2, color='red', label='Disturbance')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Wheel Angular Velocity (rad/s)')
ax.set_title('Reaction Wheel Speed vs Time')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig('my_custom_wheel.png', dpi=150)
print(f"  Saved: my_custom_wheel.png")

# Plot 3: Control input (reconstruct from pitch error)
control_history = []
for i in range(len(logger.euler_angles)):
    pitch = logger.euler_angles[i][1]
    pitch_rate = logger.w_body[i][1]
    u = -(Kp * pitch + Kd * pitch_rate)
    u = np.clip(u, -1.0, 1.0)
    control_history.append(u)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(logger.time, control_history, 'r-', linewidth=1.5)
ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.3, label='Saturation limits')
ax.axhline(y=-1.0, color='k', linestyle='--', alpha=0.3)
ax.axvspan(25, 26, alpha=0.2, color='red', label='Disturbance')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Control Torque (N·m)')
ax.set_title('Control Input vs Time')
ax.set_ylim([-1.5, 1.5])
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig('my_custom_control.png', dpi=150)
print(f"  Saved: my_custom_control.png")

# ===========================================================================
# Summary
# ===========================================================================
print("\n" + "=" * 70)
print("SIMULATION COMPLETE!")
print("=" * 70)
print(f"""
✓ Generated files:
  - my_simulation_results.csv (data export)
  - my_custom_pitch.png (pitch response)
  - my_custom_wheel.png (wheel response)
  - my_custom_control.png (control input)

✓ Next steps:
  1. Modify the control_law() function to test different strategies
  2. Change spacecraft parameters (inertias, wheel size)
  3. Add different disturbance profiles
  4. Experiment with different initial conditions
  5. Create custom plots for your analysis

✓ Tips for customization:
  - Control law is defined in control_law() function at the top
  - Easily add new disturbances or modify existing ones
  - Change Kp and Kd gains to tune control performance
  - Add more logged variables in the logger.log() call
  - Create new plots by accessing logger.time, logger.euler_angles, etc.
""")
print("=" * 70)
