# Advanced Dynamics Analysis Guide

## Overview

The spacecraft simulator now includes advanced dynamics visualization and analysis capabilities, specifically designed for studying:

- **Polhode**: Trajectory of angular velocity in the body-fixed frame
- **Herpolhode**: Trajectory of angular momentum in the inertial frame
- **Nutation**: Wobbling motion of the spacecraft
- **Precession**: Rotation of the angular momentum vector
- **Spin Rate**: Primary rotation component
- **Transverse Rate**: Secondary rotation components
- **Energy & Momentum**: Conservation analysis

## Quick Start

Run the advanced analysis script:

```bash
cd /workspaces/SPACE_SYSTEMS
python3 04_advanced_dynamics_analysis.py
```

**Duration**: ~15 seconds  
**Output**: 3 high-quality PNG plots + comprehensive statistics

## Generated Plots

### 1. Polhode & Herpolhode (`plot_polhode_herpolhode.png`)

This plot shows two complementary views of spacecraft rotation:

**Left panel - Polhode (Body-Fixed Frame)**
- 3D trajectory of the angular velocity vector **ω** in spacecraft body coordinates
- The curve traces the tip of the angular velocity vector as it rotates within the body
- **Closed loops** indicate periodic motion (precession)
- Shape determined by the spacecraft's inertia tensor asymmetry
- Color progression: Start (green) → End (red)

**Right panel - Herpolhode (Inertial Frame)**
- 3D trajectory of the angular momentum vector **h** in space-fixed coordinates
- Shows how the angular momentum direction changes in absolute space
- Nearly constant magnitude (if no external torques) indicates excellent energy conservation
- Reveals precession around fixed inertial axis
- Start (green) → End (black)

**Physical Interpretation:**
- The polhode is *relative* to the spacecraft body axes
- The herpolhode is *absolute* in inertial space
- For a torque-free spacecraft with axial symmetry, the herpolhode remains fixed in space
- Asymmetric inertia causes visible herpolhode deviations

### 2. Nutation & Precession Rates (`plot_nutation_precession_rates.png`)

Four-panel plot showing the fundamental dynamics modes:

**Top-Left: Nutation Angle**
- Angle (in degrees) between angular velocity **ω** and angular momentum **h**
- Periodic oscillation reveals precession behavior
- Zero nutation = simple spin rotation
- Non-zero nutation = coupled motion with tumbling

**Top-Right: Precession Rate**
- Rate of change of angular momentum direction in the inertial frame
- Computed from: dh/dt = τ (torque)
- Zero for torque-free motion (unless coupled dynamics present)
- Units: degrees/second

**Bottom-Left: Spin Rate**
- Component of angular velocity along the angular momentum vector
- ω_spin = **ω** · (h / |h|)
- Represents the primary rotation axis
- Approximately constant for momentum-conserving systems

**Bottom-Right: Transverse Rate**
- Component of angular velocity perpendicular to angular momentum
- ω_trans = |**ω** - ω_spin · (h / |h|)|
- Causes nutation and wobbling motion
- Small for stable spinning spacecraft

**Physical Interpretation:**
- The four rates describe the complete rotational motion
- Large nutation amplitude indicates strong coupling between modes
- Stable precession appears as quasi-periodic oscillations
- Tumbling motion shows high transverse rates

### 3. Energy & Momentum Analysis (`plot_energy_momentum_analysis.png`)

Conservation laws verification:

**Left: Rotational Kinetic Energy**
- KE = 0.5 * **ω**^T · I · **ω**
- Should remain constant for torque-free systems
- Deviations indicate numerical integration errors
- Typical error: < 1% for Euler integration method

**Right: Angular Momentum Magnitude**
- |**h**| = |I · **ω**|
- Conserved quantity in absence of external torques
- Excellent conservation (~constant) proves accurate dynamics
- Small variations reveal numerical precision limits

**Expected Results:**
- Flat horizontal lines = good energy/momentum conservation
- Smooth oscillations = acceptable numerical error
- Rapid changes = integration instability or torque application

## Physics Background

### Polhode Theory

The polhode (from Greek "path of the pole") is the trajectory traced by the angular velocity vector in body-fixed coordinates. Key properties:

1. **Closed curves** (or open curves) in body frame due to conservation of:
   - Rotational kinetic energy: E = 0.5 * ω^T · I · ω
   - Angular momentum magnitude (if torque-free): |h| = constant

2. **Shape determined by**:
   - Spacecraft inertia tensor I
   - Angular momentum magnitude |h|

3. **Precession of body frame** causes polhode to appear "rotating" in body frame while herpolhode remains fixed in inertial frame

### Herpolhode Theory

The herpolhode (from Greek "path of the sacred pole") is the trajectory of angular momentum in the inertial frame:

1. **Fixed in space** for isolated (torque-free) spacecraft
2. **Deviates** when external torques applied (reaction wheel coupling, gravity gradient, etc.)
3. **Fundamental axis** for understanding absolute motion in space

### Nutation vs Precession

**Nutation:**
- Wobbling of the spin axis
- Periodic variation of angle between ω and h
- High frequency (tens of seconds typical for spacecraft)
- Caused by inertia asymmetry or external disturbances

**Precession:**
- Rotation of the angular momentum vector
- Steady or slowly varying
- Low frequency
- Caused by external torques (control, gravity gradient, etc.)

### Euler Equations

The fundamental differential equations for rigid body rotation:

```
I · dω/dt + ω × (I · ω) = τ
```

Where:
- I = inertia tensor (3×3 symmetric matrix)
- ω = angular velocity [ωx, ωy, ωz]
- τ = external torque
- ω × (I · ω) = gyroscopic coupling term

The gyroscopic term couples all three rotation axes for asymmetric inertia.

## Using the Plotting Functions

The new functions are available in `src/utils.py`:

### 1. plot_polhode_herpolhode()

```python
from src.utils import plot_polhode_herpolhode
import matplotlib.pyplot as plt

fig, axes = plot_polhode_herpolhode(
    t=time_history,
    w_body=angular_velocity_history,
    h_inertial=angular_momentum_history,
    figsize=(14, 6)
)
plt.savefig('polhode_plot.png')
```

### 2. plot_nutation_precession_rates()

```python
from src.utils import plot_nutation_precession_rates

fig, axes = plot_nutation_precession_rates(
    t=time_history,
    w_body=angular_velocity_history,
    h_inertial=angular_momentum_history,
    I_hub=inertia_matrix,
    figsize=(14, 10)
)
plt.savefig('rates_plot.png')
```

### 3. plot_energy_momentum_analysis()

```python
from src.utils import plot_energy_momentum_analysis

fig, axes = plot_energy_momentum_analysis(
    t=time_history,
    w_body=angular_velocity_history,
    h_inertial=angular_momentum_history,
    I_hub=inertia_matrix,
    figsize=(14, 6)
)
plt.savefig('conservation_plot.png')
```

## Advanced Examples

### Example 1: Asymmetric Inertia Study

Modify `04_advanced_dynamics_analysis.py`:

```python
# Highly asymmetric inertia
I_hub = np.array([
    [50.0,   0.0,   0.0],  # Low inertia about x-axis
    [ 0.0, 150.0,   0.0],  # High inertia about y-axis
    [ 0.0,   0.0, 100.0]   # Medium inertia about z-axis
])

# This creates pronounced polhode precession
```

### Example 2: Nutation Study

```python
# Small initial angular velocities to see pure nutation
wx_0 = 0.001   # Small x-rate
wy_0 = 0.001   # Small y-rate
wz_0 = 0.05    # Dominant spin rate

# This creates clear nutation oscillations
```

### Example 3: Energy Dissipation

For studies with energy loss (damping, friction):

```python
# Apply damping torque proportional to angular velocity
tau_damping = -0.1 * spacecraft.state.w_body
spacecraft.step(dt, u_wheel=0.0, tau_ext=tau_damping)

# The energy plot will show linear decay
```

## Troubleshooting

### Q: Polhode curves look distorted or chaotic

**Possible causes:**
1. Integration timestep too large → reduce `dt`
2. Inertia tensor singular → check matrix properties
3. Initial conditions too large → start with small angular velocities

**Solution:**
```python
dt = 0.001  # Smaller timestep
```

### Q: Herpolhode is not fixed (drifts in time)

**Possible causes:**
1. Angular momentum not properly computed
2. Coordinate transformation errors
3. Numerical drift accumulation

**Solution:**
```python
# Check conservation
h_mag = np.linalg.norm(h_inertial, axis=1)
print(f"Conservation: {(h_mag[-1] - h_mag[0])/h_mag[0] * 100}%")
# Should be < 0.1%
```

### Q: Nutation angle is zero or very small

**Possible causes:**
1. Angular velocity parallel to angular momentum
2. Initial conditions chosen to align with principal axis
3. Axial symmetry in inertia tensor

**Solution:**
```python
# Create asymmetric initial conditions
I_hub = np.array([
    [100, 0, 0],
    [0, 120, 0],
    [0, 0, 80]
])
# With unequal diagonal terms, you'll see nutation
```

## Performance Notes

- **Timestep sensitivity**: Smaller dt → more accurate, slower execution
- **Integration method**: Simple Euler used (adequate for visualization)
- **For production**: Use scipy.integrate.solve_ivp() with RK45
- **Typical run time**: 15 seconds for 30-second simulation with 0.01 s timestep

## Further Reading

- Goldstein, Poole & Safko: Classical Mechanics, Ch. 5 (rigid body dynamics)
- Vallado & Crawford: Fundamentals of Astrodynamics (spacecraft attitude)
- NASA Technical Report: Spacecraft Attitude Dynamics Determination (technical review)

## Files Reference

- **`04_advanced_dynamics_analysis.py`** - Main analysis script
- **`src/utils.py`** - Three new plotting functions
- **`src/rigid_body.py`** - Euler equations implementation
- **`src/spacecraft.py`** - CoupledSpacecraft dynamics integrator

---

**Last Updated**: 2026-04-16  
**Version**: 1.0
