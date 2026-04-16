#!/usr/bin/env python3
"""
Example 2: Single Reaction Wheel Simulation
============================================

Runs a complete spacecraft dynamics simulation:
- Starts with initial attitude and angular velocity
- Applies continuous reaction wheel torque
- Logs trajectory and computes statistics
- Demonstrates momentum exchange and control effectiveness
"""

import sys
sys.path.insert(0, './src')

import numpy as np
from spacecraft import CoupledSpacecraft
from utils import SimulationLogger, plot_attitude_history, plot_angular_velocity_history
from utils import plot_wheel_angular_velocity, plot_angular_momentum, plot_phase_portrait
import matplotlib.pyplot as plt

print("=" * 70)
print("REACTION WHEEL SPACECRAFT SIMULATOR - FULL SIMULATION")
print("=" * 70)

# ===========================================================================
# Setup: Spacecraft Configuration
# ===========================================================================
print("\n1. SPACECRAFT CONFIGURATION")
print("-" * 70)

# Hub inertia (cubesat-like spacecraft)
I_hub = np.diag([100.0, 120.0, 80.0])  # kg*m²
I_wheel = 0.5  # kg*m²
mass = 50.0  # kg

spacecraft = CoupledSpacecraft(
    I_hub=I_hub,
    I_wheel=I_wheel,
    wheel_axis=2,  # Reaction wheel spins about z-axis
    mass=mass,
    name="Spacecraft_RW"
)

print(f"Hub inertia (diagonal): {np.diag(I_hub)} kg·m²")
print(f"Wheel inertia: {I_wheel} kg·m²")
print(f"Total mass: {mass} kg")
print(f"Wheel spin axis: z-axis\n")

# Initial conditions
euler_init = np.array([0.1, 0.05, 0.0])  # rad (small initial attitudes)
w_body_init = np.array([0.05, 0.03, 0.01])  # rad/s (small initial rates)
w_wheel_init = 0.0  # rad/s

spacecraft.state.euler_angles = euler_init
spacecraft.state.w_body = w_body_init
spacecraft.state.w_wheel = w_wheel_init

print(f"Initial Euler angles (rad): {euler_init}")
print(f"Initial body rates (rad/s): {w_body_init}")
print(f"Initial wheel rate (rad/s): {w_wheel_init}\n")

# ===========================================================================
# Simulation Parameters
# ===========================================================================
print("\n2. SIMULATION PARAMETERS")
print("-" * 70)

dt = 0.01  # Time step (seconds)
t_final = 50.0  # Total simulation time
n_steps = int(t_final / dt)

print(f"Time step: {dt} s")
print(f"Final time: {t_final} s")
print(f"Number of steps: {n_steps}\n")

# ===========================================================================
# Control Law: Simple PD Controller
# ===========================================================================
print("\n3. CONTROL LAW")
print("-" * 70)

# PD gains for attitude control
Kp = 10.0  # Proportional gain
Kd = 5.0   # Derivative gain

# Setpoint (desired attitudes)
roll_target = 0.0
pitch_target = 0.0
yaw_target = 0.0

print(f"Control objective: Drive to zero attitude error")
print(f"PD gains: Kp={Kp}, Kd={Kd}")
print(f"Target attitude (rad): ({roll_target}, {pitch_target}, {yaw_target})")
print(f"Control law: u = -Kp·e - Kd·de/dt\n")

# ===========================================================================
# Logger for Results
# ===========================================================================
logger = SimulationLogger()

# ===========================================================================
# Main Simulation Loop
# ===========================================================================
print("\n4. RUNNING SIMULATION")
print("-" * 70)

print(f"Step {0:5d}/{n_steps:5d} - t={0.0:6.2f} s", end="\r")

for step in range(n_steps):
    t = spacecraft.state.time
    
    # Current state
    euler = spacecraft.state.euler_angles
    w_body = spacecraft.state.w_body
    
    # PD Control: Compute command to spin up/down reaction wheel
    # Error in attitude (roll and pitch control via reaction wheel)
    roll_error = euler[0] - roll_target
    pitch_error = euler[1] - pitch_target
    
    # Error rates
    roll_rate_error = w_body[0]
    pitch_rate_error = w_body[1]
    
    # Control torque (simplified single-axis): control via z-axis wheel
    # This would normally use a more sophisticated control allocation matrix
    u_control = -(Kp * pitch_error + Kd * pitch_rate_error)
    
    # Clamp to prevent saturation
    u_control = np.clip(u_control, -1.0, 1.0)  # N*m
    
    # Take one simulation step
    spacecraft.step(dt=dt, u_wheel=u_control, tau_ext=None)
    
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
    
    # Print progress every 500 steps
    if step % 500 == 0:
        print(f"Step {step:5d}/{n_steps:5d} - t={t:6.2f} s", end="\r")

print(f"Step {n_steps:5d}/{n_steps:5d} - t={t_final:6.2f} s - COMPLETE!")

# ===========================================================================
# Results Summary
# ===========================================================================
print("\n5. RESULTS SUMMARY")
print("-" * 70)

df = logger.to_dataframe()

print("\nFinal State:")
print(f"  Time: {df['time'].iloc[-1]:.2f} s")
print(f"  Roll: {df['roll'].iloc[-1]:.4f} rad ({np.degrees(df['roll'].iloc[-1]):.2f}°)")
print(f"  Pitch: {df['pitch'].iloc[-1]:.4f} rad ({np.degrees(df['pitch'].iloc[-1]):.2f}°)")
print(f"  Yaw: {df['yaw'].iloc[-1]:.4f} rad ({np.degrees(df['yaw'].iloc[-1]):.2f}°)")
print(f"  ωx: {df['wx'].iloc[-1]:.4f} rad/s")
print(f"  ωy: {df['wy'].iloc[-1]:.4f} rad/s")
print(f"  ωz: {df['wz'].iloc[-1]:.4f} rad/s")
print(f"  Wheel speed: {df['w_wheel'].iloc[-1]:.4f} rad/s")

print("\nAttitude Error Statistics:")
roll_error = df['roll'].values
pitch_error = df['pitch'].values
print(f"  Roll - Mean: {np.mean(roll_error):.4f}, Max: {np.max(np.abs(roll_error)):.4f} rad")
print(f"  Pitch - Mean: {np.mean(pitch_error):.4f}, Max: {np.max(np.abs(pitch_error)):.4f} rad")

print("\nEnergy Statistics:")
ke = df['ke'].values
print(f"  Initial KE: {ke[0]:.4f} J")
print(f"  Final KE: {ke[-1]:.4f} J")
print(f"  KE change: {ke[-1] - ke[0]:.4f} J ({100*(ke[-1]-ke[0])/ke[0]:.2f}%)")

print("\nWheel Momentum:")
print(f"  Max wheel speed: {np.max(np.abs(df['w_wheel'].values)):.4f} rad/s")
print(f"  Max stored momentum: {I_wheel * np.max(np.abs(df['w_wheel'].values)):.4f} kg·m²/s\n")

# ===========================================================================
# Save Results
# ===========================================================================
logger.save_csv('simulation_results.csv')
print("Simulation data saved to: simulation_results.csv\n")

# ===========================================================================
# Plotting
# ===========================================================================
print("\n6. GENERATING PLOTS")
print("-" * 70)

fig1, ax1 = plot_attitude_history(logger.time, logger.euler_angles)
plt.savefig('plot_attitude.png', dpi=150, bbox_inches='tight')
print("  Saved: plot_attitude.png")

fig2, ax2 = plot_angular_velocity_history(logger.time, logger.w_body)
plt.savefig('plot_angular_velocity.png', dpi=150, bbox_inches='tight')
print("  Saved: plot_angular_velocity.png")

fig3, ax3 = plot_wheel_angular_velocity(logger.time, logger.w_wheel)
plt.savefig('plot_wheel_velocity.png', dpi=150, bbox_inches='tight')
print("  Saved: plot_wheel_velocity.png")

fig4, ax4 = plot_angular_momentum(logger.time, logger.h_total)
plt.savefig('plot_angular_momentum.png', dpi=150, bbox_inches='tight')
print("  Saved: plot_angular_momentum.png")

fig5, ax5 = plot_phase_portrait(logger.w_body)
plt.savefig('plot_phase_portrait.png', dpi=150, bbox_inches='tight')
print("  Saved: plot_phase_portrait.png")

print("\n" + "=" * 70)
print("SIMULATION COMPLETE!")
print("=" * 70)
print("""
Output files generated:
  - simulation_results.csv (full trajectory data)
  - plot_attitude.png
  - plot_angular_velocity.png
  - plot_wheel_velocity.png
  - plot_angular_momentum.png
  - plot_phase_portrait.png

Next steps:
  - Examine the CSV for detailed numerical analysis
  - View plots for visualization
  - Modify control gains (Kp, Kd) and re-run
  - Try different initial conditions
""")
print("=" * 70)
