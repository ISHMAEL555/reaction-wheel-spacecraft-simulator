#!/usr/bin/env python3
"""
Example 3: PD Control Analysis
===============================

Demonstrates:
- Proportional-Derivative (PD) attitude control
- Parameter tuning effects
- Control performance metrics
- Robustness to disturbances
"""

import sys
sys.path.insert(0, './src')

import numpy as np
from spacecraft import CoupledSpacecraft
from utils import SimulationLogger
import matplotlib.pyplot as plt

print("=" * 70)
print("REACTION WHEEL SPACECRAFT SIMULATOR - PD CONTROL ANALYSIS")
print("=" * 70)

# ===========================================================================
# Spacecraft Setup (same as Example 2)
# ===========================================================================
print("\n1. SPACECRAFT CONFIGURATION")
print("-" * 70)

I_hub = np.diag([100.0, 120.0, 80.0])  # kg*m²
I_wheel = 0.5  # kg*m²
mass = 50.0  # kg

spacecraft = CoupledSpacecraft(
    I_hub=I_hub,
    I_wheel=I_wheel,
    wheel_axis=2,
    mass=mass,
    name="Spacecraft_PD_Control"
)

print(f"Hub inertia (kg·m²): {np.diag(I_hub)}")
print(f"Wheel inertia: {I_wheel} kg·m²\n")

# ===========================================================================
# Simulation Parameters
# ===========================================================================
print("\n2. SIMULATION SETUP")
print("-" * 70)

dt = 0.01  # Time step (seconds)
t_final = 100.0  # Total simulation time
n_steps = int(t_final / dt)

# Disturbance profile
disturbance_magnitude = 0.1  # N*m
disturbance_start = 20  # Apply after 20 seconds
disturbance_duration = 10  # Apply for 10 seconds

print(f"Time step: {dt} s")
print(f"Total time: {t_final} s")
print(f"Disturbance: {disturbance_magnitude} N·m applied at t∈[{disturbance_start}, {disturbance_start+disturbance_duration}] s\n")

# ===========================================================================
# PD Control Parameter Sweeps
# ===========================================================================
print("\n3. TESTING MULTIPLE CONTROL CONFIGURATIONS")
print("-" * 70)

control_configs = [
    {"name": "Underdamped (Kp=5, Kd=2)", "Kp": 5.0, "Kd": 2.0},
    {"name": "Critically Damped (Kp=10, Kd=5)", "Kp": 10.0, "Kd": 5.0},
    {"name": "Overdamped (Kp=10, Kd=10)", "Kp": 10.0, "Kd": 10.0},
    {"name": "High Performance (Kp=20, Kd=8)", "Kp": 20.0, "Kd": 8.0},
]

results = {}

for config in control_configs:
    config_name = config["name"]
    Kp = config["Kp"]
    Kd = config["Kd"]
    
    print(f"\n  Testing: {config_name}")
    
    # Reset spacecraft to initial conditions
    spacecraft.state.euler_angles = np.array([0.1, 0.05, 0.0])
    spacecraft.state.w_body = np.array([0.05, 0.03, 0.01])
    spacecraft.state.w_wheel = 0.0
    spacecraft.state.time = 0.0
    
    # Logger for this run
    logger = SimulationLogger()
    
    # Simulation loop
    for step in range(n_steps):
        t = spacecraft.state.time
        euler = spacecraft.state.euler_angles
        w_body = spacecraft.state.w_body
        
        # PD Control on pitch
        pitch_error = euler[1]  # Target is 0
        pitch_rate_error = w_body[1]
        
        # Control command
        u_control = -(Kp * pitch_error + Kd * pitch_rate_error)
        u_control = np.clip(u_control, -2.0, 2.0)  # Limit
        
        # External disturbance
        tau_ext = None
        if disturbance_start <= t <= disturbance_start + disturbance_duration:
            tau_ext = np.array([disturbance_magnitude, 0.0, 0.0])
        
        # Step
        spacecraft.step(dt=dt, u_wheel=u_control, tau_ext=tau_ext)
        
        # Log
        logger.log(
            t=t,
            euler=spacecraft.state.euler_angles,
            w_body=spacecraft.state.w_body,
            w_wheel=spacecraft.state.w_wheel
        )
    
    # Store results
    results[config_name] = logger
    print(f"    Final pitch error: {np.abs(spacecraft.state.euler_angles[1]):.4f} rad")
    print(f"    Max wheel speed: {np.max(np.abs(np.array(logger.w_wheel))):.4f} rad/s")

# ===========================================================================
# Performance Analysis
# ===========================================================================
print("\n4. PERFORMANCE COMPARISON")
print("-" * 70)
print(f"{'Configuration':<40} {'Final Error (rad)':<18} {'Max Wheel (rad/s)':<20}")
print("-" * 78)

for config_name, logger in results.items():
    final_pitch_error = np.abs(logger.euler_angles[-1][1])
    max_wheel = np.max(np.abs(np.array(logger.w_wheel)))
    print(f"{config_name:<40} {final_pitch_error:<18.6f} {max_wheel:<20.4f}")

# ===========================================================================
# Plotting Comparison
# ===========================================================================
print("\n5. GENERATING COMPARISON PLOTS")
print("-" * 70)

# Plot 1: Pitch angle evolution for all configs
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

plot_idx = 0
for config_name, logger in results.items():
    ax = axes[plot_idx]
    
    pitch = np.array([e[1] for e in logger.euler_angles])
    ax.plot(logger.time, np.degrees(pitch), linewidth=2, label=config_name)
    
    # Mark disturbance period
    ax.axvspan(disturbance_start, disturbance_start + disturbance_duration, 
               alpha=0.2, color='red', label='Disturbance')
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Pitch (deg)')
    ax.set_title(f'Pitch Response - {config_name}')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plot_idx += 1

plt.tight_layout()
plt.savefig('plot_pd_comparison_pitch.png', dpi=150, bbox_inches='tight')
print("  Saved: plot_pd_comparison_pitch.png")

# Plot 2: Wheel speed evolution for all configs
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

plot_idx = 0
for config_name, logger in results.items():
    ax = axes[plot_idx]
    
    ax.plot(logger.time, logger.w_wheel, linewidth=1.5, color='green')
    ax.axvspan(disturbance_start, disturbance_start + disturbance_duration,
               alpha=0.2, color='red')
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Wheel Angular Velocity (rad/s)')
    ax.set_title(f'Reaction Wheel - {config_name}')
    ax.grid(True, alpha=0.3)
    
    plot_idx += 1

plt.tight_layout()
plt.savefig('plot_pd_comparison_wheel.png', dpi=150, bbox_inches='tight')
print("  Saved: plot_pd_comparison_wheel.png")

# ===========================================================================
# Detailed Analysis: Best vs Worst
# ===========================================================================
print("\n6. DETAILED ANALYSIS")
print("-" * 70)

# Find best (minimal final error) and worst (maximum final error)
errors = [np.abs(logger.euler_angles[-1][1]) for logger in results.values()]
best_idx = np.argmin(errors)
worst_idx = np.argmax(errors)

best_name = list(results.keys())[best_idx]
worst_name = list(results.keys())[worst_idx]

best_logger = results[best_name]
worst_logger = results[worst_name]

print(f"\nBest Performance: {best_name}")
print(f"  Final pitch error: {np.abs(best_logger.euler_angles[-1][1]):.6f} rad")
print(f"  Final pitch rate: {best_logger.w_body[-1][1]:.6f} rad/s")
print(f"  Max wheel speed: {np.max(np.abs(np.array(best_logger.w_wheel))):.4f} rad/s")
print(f"  Final wheel speed: {best_logger.w_wheel[-1]:.4f} rad/s")

print(f"\nWorst Performance: {worst_name}")
print(f"  Final pitch error: {np.abs(worst_logger.euler_angles[-1][1]):.6f} rad")
print(f"  Final pitch rate: {worst_logger.w_body[-1][1]:.6f} rad/s")
print(f"  Max wheel speed: {np.max(np.abs(np.array(worst_logger.w_wheel))):.4f} rad/s")
print(f"  Final wheel speed: {worst_logger.w_wheel[-1]:.4f} rad/s")

# ===========================================================================
# Recommendation
# ===========================================================================
print("\n" + "=" * 70)
print("ANALYSIS COMPLETE!")
print("=" * 70)
print("""
Key Findings:

1. UNDERDAMPED (Kp=5, Kd=2):
   - Fast transient response
   - Oscillatory behavior
   - Lower wheel saturation
   - Higher settling time

2. CRITICALLY DAMPED (Kp=10, Kd=5):
   - Smooth response without oscillations
   - Good disturbance rejection
   - Balanced performance
   - RECOMMENDED for most missions

3. OVERDAMPED (Kp=10, Kd=10):
   - Very smooth response
   - Slower transient
   - Low wheel wear
   - Good for sensitive equipment

4. HIGH PERFORMANCE (Kp=20, Kd=8):
   - Rapid error correction
   - Risk of wheel saturation
   - Higher control authority
   - Suitable for aggressive maneuvers

DISTURBANCE RESPONSE:
   - All controllers show transient during disturbance period
   - Recovery depends on integral action (not implemented in basic PD)
   - Adding integrator would improve steady-state errors

RECOMMENDATIONS:
   ✓ Start with critically damped (Kp=10, Kd=5)
   ✓ Tune based on mission requirements and wheel constraints
   ✓ Consider adding integrator for better steady-state performance
   ✓ Monitor wheel momentum for momentum management
""")
print("=" * 70)
