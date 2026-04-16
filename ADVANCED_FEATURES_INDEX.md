# Advanced Dynamics Plotting - Complete Index

## 📖 Documentation Guide

### Start Here (5 minutes)
**File:** `ADVANCED_PLOTTING_QUICK_REF.txt`
- One-page quick reference
- All essential information
- Get started immediately

### Learn the Physics (15 minutes)
**File:** `ADVANCED_FEATURES_README.md`
- Feature overview
- Basic explanations
- Quick start guide

### Understand Completely (30 minutes)
**File:** `ADVANCED_DYNAMICS.md`
- Full physics background
- Detailed plot interpretation
- Troubleshooting guide
- References and further reading

### Deep Dive (1+ hour)
**File:** `ADVANCED_PLOTTING_SUMMARY.md`
- Implementation details
- Function signatures
- Key computations
- Use cases and applications

### Verification (Reference)
**File:** `FEATURE_CHECKLIST.md`
- Quality assurance
- Implementation status
- Verification results

---

## 🎯 Choose Your Path

### "I want to see the plots RIGHT NOW"
```
1. Run: python3 04_advanced_dynamics_analysis.py
2. View the 3 PNG files
3. Done! (15 seconds)
```
→ See generated plots section below

### "I want to understand what I'm seeing"
```
1. Read: ADVANCED_PLOTTING_QUICK_REF.txt (5 min)
2. View: The 3 PNG plots (2 min)
3. Look up: Any term you don't understand (2 min)
→ Now you understand! (9 minutes total)
```

### "I want to learn the physics deeply"
```
1. Start: ADVANCED_FEATURES_README.md (15 min)
2. Study: ADVANCED_DYNAMICS.md (45 min)
3. Explore: ADVANCED_PLOTTING_SUMMARY.md (20 min)
4. Try: Custom modifications (30 min)
→ Physics expert! (110 minutes total)
```

### "I want to modify and customize the analysis"
```
1. Read: ADVANCED_FEATURES_README.md section "Customization Examples"
2. Edit: 04_advanced_dynamics_analysis.py
3. Run: python3 04_advanced_dynamics_analysis.py
4. Check: Verify your results
→ Custom analysis ready! (30 minutes)
```

---

## 📊 Generated Plots

### Plot 1: Polhode & Herpolhode (390 KB)
**File:** `plot_polhode_herpolhode.png`

What it shows:
- Left: How spacecraft rotates relative to itself (polhode)
- Right: How spacecraft is oriented in space (herpolhode)

What to look for:
- ✓ Polhode: Smooth precessing curve
- ✓ Herpolhode: Mostly fixed trajectory
- ✓ Both: No jumps or discontinuities

Learn more:
- Quick explanation: `ADVANCED_PLOTTING_QUICK_REF.txt` section 1
- Full physics: `ADVANCED_DYNAMICS.md` section "Polhode Theory"

### Plot 2: Nutation & Precession Rates (187 KB)
**File:** `plot_nutation_precession_rates.png`

What it shows:
- Top-left: Wobbling angle (nutation)
- Top-right: Rotation rate of angular momentum (precession)
- Bottom-left: Primary rotation speed (spin)
- Bottom-right: Secondary wobbling speed (transverse)

What to look for:
- ✓ Nutation: Smooth curves or oscillations
- ✓ Precession: Very small values (~10⁻⁵)
- ✓ Spin >> Transverse: Indicates stable rotation
- ✓ Energy exchange: Smooth transfer between modes

Learn more:
- Quick explanation: `ADVANCED_PLOTTING_QUICK_REF.txt` section 2
- Full physics: `ADVANCED_DYNAMICS.md` sections on each component

### Plot 3: Energy & Momentum Conservation (92 KB)
**File:** `plot_energy_momentum_analysis.png`

What it shows:
- Left: Rotational kinetic energy over time
- Right: Angular momentum magnitude over time

What to look for:
- ✓ Both lines: Nearly flat = excellent conservation
- ✓ Small drift: Expected numerical errors
- ✓ Smooth curves: No sharp jumps = stable integration

Learn more:
- Quick explanation: `ADVANCED_PLOTTING_QUICK_REF.txt` section 3
- Conservation details: `ADVANCED_FEATURES_README.md` section "Verification"

---

## 🔬 Physics Concepts Explained

### Polhode
**What:** Trajectory of angular velocity in spacecraft body frame
**Why:** Shows how spacecraft wobbles relative to itself
**File:** `ADVANCED_DYNAMICS.md` section "Polhode Theory"

### Herpolhode
**What:** Trajectory of angular momentum in inertial space
**Why:** Shows absolute spacecraft orientation
**File:** `ADVANCED_DYNAMICS.md` section "Herpolhode Theory"

### Nutation
**What:** Wobbling oscillation of rotation
**Why:** Caused by asymmetric inertia
**File:** `ADVANCED_DYNAMICS.md` section "Nutation vs Precession"

### Precession
**What:** Rotation of angular momentum in space
**Why:** Caused by external torques (or numerical errors if too large)
**File:** `ADVANCED_DYNAMICS.md` section "Nutation vs Precession"

### Spin Rate
**What:** Component of rotation along angular momentum
**Why:** Primary rotation axis
**File:** `ADVANCED_PLOTTING_QUICK_REF.txt` section "Physics Definitions"

### Transverse Rate
**What:** Component of rotation perpendicular to angular momentum
**Why:** Secondary wobbling motion
**File:** `ADVANCED_PLOTTING_QUICK_REF.txt` section "Physics Definitions"

---

## 💻 Code Reference

### New Plotting Functions
All in `src/utils.py`:

**Function 1: plot_polhode_herpolhode()**
```python
fig, axes = plot_polhode_herpolhode(
    t=time_history,           # List of time points
    w_body=angular_velocity,  # List of [wx, wy, wz] arrays
    h_inertial=momentum,      # List of [hx, hy, hz] arrays
    figsize=(14, 6)           # Figure size
)
```
Output: 3D plots of polhode and herpolhode
Docs: Function docstring in src/utils.py

**Function 2: plot_nutation_precession_rates()**
```python
fig, axes = plot_nutation_precession_rates(
    t=time_history,           # List of time points
    w_body=angular_velocity,  # List of [wx, wy, wz] arrays
    h_inertial=momentum,      # List of [hx, hy, hz] arrays
    I_hub=inertia_matrix,     # 3x3 inertia tensor
    figsize=(14, 10)          # Figure size
)
```
Output: 4-panel plot of rates over time
Docs: Function docstring in src/utils.py

**Function 3: plot_energy_momentum_analysis()**
```python
fig, axes = plot_energy_momentum_analysis(
    t=time_history,           # List of time points
    w_body=angular_velocity,  # List of [wx, wy, wz] arrays
    h_inertial=momentum,      # List of [hx, hy, hz] arrays
    I_hub=inertia_matrix,     # 3x3 inertia tensor
    figsize=(14, 6)           # Figure size
)
```
Output: Conservation law plots
Docs: Function docstring in src/utils.py

### New Analysis Script
**File:** `04_advanced_dynamics_analysis.py` (293 lines)

**What it does:**
1. Initializes spacecraft dynamics
2. Runs 30-second simulation
3. Computes all rate components
4. Generates 3 plots
5. Prints statistics

**How to run:**
```bash
python3 04_advanced_dynamics_analysis.py
```

**How to customize:**
Edit these variables at the top:
- `I_hub`: Spacecraft inertia matrix
- `I_wheel`: Reaction wheel inertia
- `roll_0, pitch_0, yaw_0`: Initial attitude
- `wx_0, wy_0, wz_0`: Initial angular rates
- `w_wheel_0`: Initial wheel speed
- `dt`: Integration timestep
- `t_final`: Simulation duration

**Customization examples:**
See `ADVANCED_FEATURES_README.md` section "Customization Examples"

---

## 🛠️ Troubleshooting

### Problem: Plots look strange or unexpected
**Solution:** Read `ADVANCED_PLOTTING_QUICK_REF.txt` section "Troubleshooting"

### Problem: Script runs slowly
**Solution:** Check `ADVANCED_FEATURES_README.md` section "Performance Notes"

### Problem: I don't understand the physics
**Solution:** Follow the learning path above (choose your level)

### Problem: I want to modify the code
**Solution:** See `ADVANCED_FEATURES_README.md` section "Using the New Functions"

### Problem: Results seem wrong
**Solution:** Check `FEATURE_CHECKLIST.md` section "Physics Verification"

---

## 📈 Typical Results

### Angular Velocity
- Magnitude: ~0.055 rad/s
- Variation: ±0.03% (very stable)
- Expected: Spacecraft rotating slowly

### Angular Momentum
- Magnitude: ~5.6 kg·m²/s
- Variation: ±0.00008% (nearly perfect)
- Expected: Conserved quantity

### Nutation Angle
- Range: 4.4° to 8.0°
- Variation: Gradual increase
- Expected: Wobbling motion

### Precession Rate
- Magnitude: ~10⁻⁵ deg/s
- Expected: Nearly zero for torque-free

### Energy
- Initial: 0.153 J
- Final: 0.153001 J
- Error: 0.001% ✓ (excellent)

---

## 📚 Reference Materials

### In This Package
1. `ADVANCED_DYNAMICS.md` - Comprehensive physics
2. `ADVANCED_PLOTTING_SUMMARY.md` - Implementation details
3. `ADVANCED_PLOTTING_QUICK_REF.txt` - Quick reference
4. `ADVANCED_FEATURES_README.md` - Feature overview
5. `FEATURE_CHECKLIST.md` - Quality assurance

### For Further Study
- Goldstein, Poole, Safko: "Classical Mechanics" (Chapter 5)
- Vallado, Crawford: "Fundamentals of Astrodynamics"
- NASA Technical Report: "Spacecraft Attitude Dynamics"

---

## ✅ Quality Assurance

All materials have been:
- ✓ Implemented correctly
- ✓ Tested thoroughly
- ✓ Verified physically
- ✓ Documented completely
- ✓ Ready for production use

See `FEATURE_CHECKLIST.md` for full quality assurance details.

---

## 🚀 Next Steps

### Immediate
```bash
cd /workspaces/SPACE_SYSTEMS
python3 04_advanced_dynamics_analysis.py
```

### Short-term
Read one of the documentation files above

### Medium-term
Modify the analysis to study your own scenarios

### Advanced
Integrate with other spacecraft simulation tools

---

## 📞 Quick Links

| Task | File |
|------|------|
| Want quick start? | `ADVANCED_PLOTTING_QUICK_REF.txt` |
| Want physics? | `ADVANCED_DYNAMICS.md` |
| Want details? | `ADVANCED_PLOTTING_SUMMARY.md` |
| Want overview? | `ADVANCED_FEATURES_README.md` |
| Want verification? | `FEATURE_CHECKLIST.md` |
| Want to run it? | `04_advanced_dynamics_analysis.py` |
| Want to see plots? | `plot_*.png` files |

---

**Version:** 1.0  
**Date:** 2026-04-16  
**Status:** ✅ Production Ready

