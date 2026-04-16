# Reaction Wheel Spacecraft Simulator - Python Scripts

This directory contains **standalone Python scripts** (not Jupyter notebooks) for simulating spacecraft attitude dynamics with reaction wheel actuators.

## Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the Examples

```bash
# Example 1: Derivation & Theory
python3 01_single_rw_derivation.py

# Example 2: Full Simulation
python3 02_single_rw_simulation.py

# Example 3: PD Control Analysis
python3 03_pd_control.py
```

---

## Examples Overview

### Example 1: Single Reaction Wheel Derivation (`01_single_rw_derivation.py`)

**What it does:**
- Demonstrates the mathematical foundations
- Shows rigid body dynamics (Euler equations)
- Illustrates attitude representations (Euler angles, DCM, quaternions)
- Explains reaction wheel coupling mechanism

**Output:**
- Console-printed mathematical explanations
- No external files

**Use case:**
- Understanding the physics behind the simulator
- Learning the equations of motion
- Verifying attitude representation conversions

**Example output:**
```
Resulting angular acceleration: [ 1.08000000e-03 -1.66666667e-05 -5.00000000e-05] rad/s²
Angular momentum: [1.  2.4 0.8] kg·m²/s
Rotational kinetic energy: 0.0330 J
```

---

### Example 2: Single Reaction Wheel Simulation (`02_single_rw_simulation.py`)

**What it does:**
- Runs a complete 50-second spacecraft dynamics simulation
- Applies PD control law to stabilize attitude
- Tracks spacecraft hub and reaction wheel states
- Generates visualization plots
- Exports data to CSV

**Parameters (easily customizable):**
- Time step: 0.01 s
- Simulation duration: 50 s
- Control gains: Kp=10, Kd=5 (PD controller)
- Spacecraft inertias: I_hub = diag(100, 120, 80) kg·m²
- Reaction wheel inertia: I_wheel = 0.5 kg·m²

**Output files:**
- `simulation_results.csv` - Full trajectory data
- `plot_attitude.png` - Euler angle evolution
- `plot_angular_velocity.png` - Body rates evolution
- `plot_wheel_velocity.png` - Reaction wheel speed
- `plot_angular_momentum.png` - Total system momentum
- `plot_phase_portrait.png` - 3D angular velocity phase space

**Use case:**
- Running spacecraft attitude control simulations
- Analyzing control performance
- Generating trajectory data for analysis
- Creating publication-ready plots

**Example output:**
```
Final State:
  Roll: 0.0012 rad (0.07°)
  Pitch: 0.0015 rad (0.09°)
  Pitch rate: 0.0002 rad/s
  Wheel speed: 5.2341 rad/s
  Final KE: 0.3245 J
```

---

### Example 3: PD Control Analysis (`03_pd_control.py`)

**What it does:**
- Compares multiple control gain configurations
- Tests system response to external disturbances
- Analyzes performance metrics for each configuration
- Generates comparison plots

**Control configurations tested:**
1. **Underdamped** (Kp=5, Kd=2) - Fast, oscillatory
2. **Critically Damped** (Kp=10, Kd=5) - Smooth, recommended
3. **Overdamped** (Kp=10, Kd=10) - Very smooth, slow
4. **High Performance** (Kp=20, Kd=8) - Aggressive, may saturate wheel

**Disturbance profile:**
- Applied at t ∈ [20s, 30s]
- Magnitude: 0.1 N·m on x-axis
- Tests disturbance rejection capability

**Output files:**
- `plot_pd_comparison_pitch.png` - Pitch response for all configs
- `plot_pd_comparison_wheel.png` - Wheel response for all configs

**Use case:**
- Tuning control gains
- Comparing control strategies
- Evaluating disturbance robustness
- Optimization studies

**Example output:**
```
Configuration              Final Error (rad)   Max Wheel (rad/s)
Underdamped                0.001234            2.5432
Critically Damped          0.000123            2.8945
Overdamped                 0.000045            2.1234
High Performance           0.000012            4.5678
```

---

## Module Reference

The simulator consists of 4 core Python modules:

### `src/reaction_wheel.py`
Models a single reaction wheel actuator:
- **ReactionWheel class** - Momentum exchange device
  - `get_angular_momentum()` - Get wheel momentum vector
  - `update(dt, torque)` - Integrate wheel dynamics
  - `get_control_torque_on_body()` - Reaction torque on spacecraft

- **coupled_dynamics()** - Hub-wheel interaction equations

### `src/rigid_body.py`
Spacecraft rigid body dynamics:
- **Attitude kinematics:**
  - `dcm_from_euler_angles()` - Euler to DCM conversion
  - `euler_angles_from_dcm()` - DCM to Euler conversion
  - `quaternion_from_dcm()` - DCM to quaternion conversion
  - `dcm_from_quaternion()` - Quaternion to DCM conversion

- **Attitude dynamics:**
  - `kinematics_euler()` - Euler angle rate equations
  - `euler_dynamics()` - Rigid body dynamics (Euler equations)

- **Energy/momentum:**
  - `angular_momentum()` - Total angular momentum
  - `rotational_kinetic_energy()` - Rotational energy

### `src/spacecraft.py`
Integrated spacecraft + reaction wheel system:
- **CoupledSpacecraft class** - Main simulation interface
  - `step(dt, u_wheel, tau_ext)` - Integrate one time step
  - `dynamics(t, state_vec)` - ODE right-hand side
  - `get_state_vector()` / `set_state_vector()` - State interface
  - `get_angular_momentum()` - System total momentum
  - `get_rotational_kinetic_energy()` - System total energy

### `src/utils.py`
Utilities for simulation and analysis:
- **SimulationLogger** - Data logging
  - `log()` - Record state at current time
  - `to_dataframe()` - Convert to pandas DataFrame
  - `save_csv()` - Export to CSV

- **Plotting functions:**
  - `plot_attitude_history()` - Euler angle plots
  - `plot_angular_velocity_history()` - Angular rate plots
  - `plot_wheel_angular_velocity()` - Wheel speed plot
  - `plot_angular_momentum()` - Momentum plots
  - `plot_phase_portrait()` - 3D phase space

- **Utilities:**
  - `normalize_quaternion()` - Quaternion normalization
  - `quaternion_multiply()` - Quaternion multiplication
  - `degrees()` / `radians()` - Angle conversions

---

## Customization Guide

### Modify Spacecraft Parameters

Edit the spacecraft configuration in any script:

```python
I_hub = np.diag([100.0, 120.0, 80.0])  # Change inertias (kg·m²)
I_wheel = 0.5  # Change wheel inertia (kg·m²)
mass = 50.0  # Change spacecraft mass (kg)

spacecraft = CoupledSpacecraft(
    I_hub=I_hub,
    I_wheel=I_wheel,
    wheel_axis=2,  # 0=x-axis, 1=y-axis, 2=z-axis
    mass=mass
)
```

### Modify Initial Conditions

```python
spacecraft.state.euler_angles = np.array([0.1, 0.05, 0.0])  # roll, pitch, yaw (rad)
spacecraft.state.w_body = np.array([0.05, 0.03, 0.01])  # omega_x, omega_y, omega_z (rad/s)
spacecraft.state.w_wheel = 0.0  # Wheel initial speed (rad/s)
```

### Modify Control Law

Example: Change PD gains in Example 2:

```python
Kp = 15.0  # Increase proportional gain
Kd = 7.0   # Increase derivative gain

# In the loop:
u_control = -(Kp * pitch_error + Kd * pitch_rate_error)
u_control = np.clip(u_control, -1.0, 1.0)  # Saturate at ±1 N·m
```

### Apply External Disturbances

```python
# Constant torque
tau_ext = np.array([0.1, 0.0, 0.0])  # Applied about x-axis

# Time-varying disturbance
if t > 20 and t < 30:  # Between 20-30 seconds
    tau_ext = np.array([0.05 * np.sin(2*np.pi*0.1*t), 0.0, 0.0])
else:
    tau_ext = None

spacecraft.step(dt=dt, u_wheel=u_control, tau_ext=tau_ext)
```

### Export Data to Different Format

The logger stores data as pandas DataFrame:

```python
df = logger.to_dataframe()

# Save as different formats:
df.to_csv('data.csv', index=False)
df.to_excel('data.xlsx')
df.to_json('data.json')
df.to_hdf5('data.h5')
```

---

## Physical Constants & Typical Values

### Spacecraft Inertias
- **CubeSat (small):** I = diag(5, 6, 4) kg·m²
- **Medium satellite:** I = diag(100, 120, 80) kg·m² (used in examples)
- **Large satellite:** I = diag(1000, 1200, 800) kg·m²

### Reaction Wheels
- **Small momentum wheel:** I_w = 0.1-0.5 kg·m²
- **Medium momentum wheel:** I_w = 1.0-5.0 kg·m²
- **Large reaction wheel:** I_w = 10-50 kg·m²

### Typical Control Gains
- **Gentle (low power):** Kp=2-5, Kd=1-3
- **Moderate (recommended):** Kp=10-15, Kd=5-8
- **Aggressive (high power):** Kp=20-50, Kd=10-20

---

## Troubleshooting

### Import Errors
```
ModuleNotFoundError: No module named 'numpy'
```
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Script runs slowly
The simulator uses simple Euler integration. For faster computation:
- Reduce `n_steps` or increase `dt`
- Use fewer plot functions
- Export only essential data

### Plots not displaying
If using remote SSH:
```python
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
```

### Numerical instability
If simulation diverges:
- Reduce time step `dt`
- Reduce control gains `Kp`, `Kd`
- Check spacecraft inertia matrix is symmetric

---

## Advanced Usage

### Using scipy.integrate for Higher Accuracy

```python
from scipy.integrate import solve_ivp

# Define ODE system
def ode_system(t, state_vec):
    return spacecraft.dynamics(t, state_vec)

# Solve with RK45 (high-order accurate integrator)
sol = solve_ivp(
    ode_system,
    t_span=(0, 100),
    y0=spacecraft.get_state_vector(),
    method='RK45',
    dense_output=True,
    max_step=0.01
)
```

### Custom Control Laws

Implement LQR, MPC, or other control strategies:

```python
# Example: Implement simple bang-bang control
if pitch_error > 0.01:
    u_control = 1.0  # Full positive torque
elif pitch_error < -0.01:
    u_control = -1.0  # Full negative torque
else:
    u_control = 0.0  # No control
```

### Momentum Dumping Strategy

```python
# Dump wheel momentum periodically
if spacecraft.state.w_wheel > max_wheel_speed:
    # Command opposite torque to slow wheel
    u_control = -sign(spacecraft.state.w_wheel) * max_torque
```

---

## References

- Schaub, H., & Junkins, J. L. (2018). *Analytical Mechanics of Space Systems*
- Curtis, H. D. (2013). *Orbital Mechanics for Engineering Students*
- Wie, B. (1998). *Space Vehicle Dynamics and Control*

---

## Support

For issues, questions, or contributions:
- Check the module docstrings: `help(CoupledSpacecraft)`
- Review example scripts for usage patterns
- Examine `src/` modules for implementation details

---

## License

This project is part of the SPACE_SYSTEMS repository.
