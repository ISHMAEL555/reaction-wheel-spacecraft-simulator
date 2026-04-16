# 🚀 Reaction Wheel Spacecraft Simulator - Complete Index

## ✅ What You Have

You have a **complete, production-ready Python simulation** of spacecraft attitude dynamics with reaction wheels. **NOT Jupyter notebooks** — these are standalone Python scripts you can run from the terminal.

---

## 📂 Files at a Glance

### 🎯 START HERE
- **`RUN_THESE_SCRIPTS.md`** ← Read this first! Quick start guide with examples
- **`00_template_custom.py`** ← Copy this to create your own simulations

### 🐍 Python Scripts (Ready to Run)
```
01_single_rw_derivation.py    Physics & math explanations       ~1 second
02_single_rw_simulation.py    Full 50-second dynamics sim       ~15 seconds  
03_pd_control.py              Control gain comparison           ~40 seconds
00_template_custom.py         Template for your experiments     N/A
```

### 📚 Documentation
```
RUN_THESE_SCRIPTS.md          ← Quick reference (RECOMMENDED)
PYTHON_SCRIPTS_README.md      ← Detailed module documentation
INDEX.md                      ← This file
README.md                     ← Original project README
```

### 🔧 Source Code Modules (in `src/`)
```
reaction_wheel.py   →  ReactionWheel class & coupled_dynamics()
rigid_body.py       →  Rigid body kinematics/dynamics 
spacecraft.py       →  Integrated CoupledSpacecraft simulator
utils.py            →  Logging, plotting, math utilities
```

---

## ⚡ Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run an Example
```bash
python3 01_single_rw_derivation.py    # Learn the theory (1 sec)
python3 02_single_rw_simulation.py    # See full simulation (15 sec)
python3 03_pd_control.py              # Compare controllers (40 sec)
```

### Step 3: Create Your Own
```bash
cp 00_template_custom.py my_experiment.py
# Edit my_experiment.py with your parameters
python3 my_experiment.py
```

---

## 📖 Reading Guide by Interest

### 🎓 **I want to understand the physics**
1. Read: `RUN_THESE_SCRIPTS.md` (overview)
2. Run: `python3 01_single_rw_derivation.py`
3. Read: `PYTHON_SCRIPTS_README.md` (module details)
4. Explore: `src/rigid_body.py` (look at the functions)

### 🧪 **I want to run simulations**
1. Run: `python3 02_single_rw_simulation.py`
2. Check outputs: `simulation_results.csv`, `plot_*.png`
3. Modify: Edit spacecraft parameters, control gains, disturbances
4. Copy: Use `00_template_custom.py` as starting point

### 🎛️ **I want to tune control parameters**
1. Run: `python3 03_pd_control.py`
2. Review: `plot_pd_comparison_*.png` 
3. Edit: Change `Kp`, `Kd` values in `02_single_rw_simulation.py`
4. Compare: Run multiple times with different gains

### 🚀 **I want to create custom experiments**
1. Copy: `cp 00_template_custom.py my_sim.py`
2. Modify: Edit the `control_law()` function
3. Run: `python3 my_sim.py`
4. Analyze: Check CSV and PNG outputs

---

## 🎯 What Each Script Does (5 Seconds Each)

### **01_single_rw_derivation.py**
Prints math explanations to console.
```
✓ Rigid body dynamics (Euler equations)
✓ Attitude representations (Euler angles, DCM, quaternions)
✓ Reaction wheel model
✓ Hub-wheel coupling
```
**Output:** Console text only
**Time:** ~1 second

---

### **02_single_rw_simulation.py**
Runs a complete 50-second spacecraft control simulation.
```
✓ Simulates spacecraft + reaction wheel dynamics
✓ Applies PD attitude control
✓ Tracks momentum and energy
✓ Generates 5 visualization plots
✓ Exports data to CSV
```
**Output:** 
- `simulation_results.csv` (data)
- `plot_attitude.png` 
- `plot_angular_velocity.png`
- `plot_wheel_velocity.png`
- `plot_angular_momentum.png`
- `plot_phase_portrait.png`

**Time:** ~15 seconds

---

### **03_pd_control.py**
Compares 4 different control gain configurations.
```
✓ Underdamped (Kp=5, Kd=2)
✓ Critically Damped (Kp=10, Kd=5) ← Recommended
✓ Overdamped (Kp=10, Kd=10)
✓ High Performance (Kp=20, Kd=8)
```
Applies disturbance (0.1 N·m, t∈[20s, 30s]) to test robustness.

**Output:**
- `plot_pd_comparison_pitch.png`
- `plot_pd_comparison_wheel.png`

**Time:** ~40 seconds

---

### **00_template_custom.py** 
Template for your own custom simulations.
```
✓ Easy-to-modify spacecraft parameters
✓ Custom control_law() function
✓ Built-in data logging
✓ Automatic plot generation
✓ Step-by-step comments
```
**How to use:**
```bash
cp 00_template_custom.py my_experiment.py
# Edit my_experiment.py
python3 my_experiment.py
```

---

## 🔍 Common Questions

### Q: Are these Jupyter notebooks?
**A:** No! These are standalone Python scripts. Run them with `python3 script_name.py`

### Q: Can I modify the parameters?
**A:** Yes! Edit the scripts or use `00_template_custom.py` as your starting point.

### Q: Can I add my own control law?
**A:** Yes! Modify the control logic in any script. Template shows how.

### Q: How long do they take?
**A:** 01: 1 sec | 02: 15 sec | 03: 40 sec | Template: depends on parameters

### Q: Can I export data to Excel/JSON?
**A:** Yes! The scripts use pandas, so you can export to any format.

### Q: How do I understand the physics?
**A:** Read `PYTHON_SCRIPTS_README.md` for detailed explanations of all functions.

---

## 🛠️ Typical Workflow

```
1. Run 01_single_rw_derivation.py
   ↓ (understand the physics)
   
2. Run 02_single_rw_simulation.py
   ↓ (see full simulation, examine plots & CSV)
   
3. Run 03_pd_control.py
   ↓ (understand control gain effects)
   
4. Copy 00_template_custom.py → my_experiment.py
   ↓ (modify for your own needs)
   
5. Run my_experiment.py
   ↓ (test your custom simulation)
   
6. Analyze results (view plots, examine CSV data)
   ↓ (adjust parameters and repeat)
```

---

## 📊 What Gets Generated

### CSV Files
Contains columns: time, roll, pitch, yaw, wx, wy, wz, w_wheel, ...
Load in Excel or Python:
```python
import pandas as pd
df = pd.read_csv('simulation_results.csv')
```

### PNG Plots
Publication-ready visualization plots:
- Attitude evolution (Euler angles)
- Angular rate evolution
- Reaction wheel speed
- System momentum
- Phase portrait (3D)

### Console Output
Summary statistics and progress reports.

---

## �� Learning Resources

**To understand the physics:**
- Read the docstrings in `src/` modules
- Run `python3 01_single_rw_derivation.py`
- Check `PYTHON_SCRIPTS_README.md` section "Module Reference"

**To learn scripting patterns:**
- Copy `00_template_custom.py`
- Study the comments
- Modify one parameter at a time
- Run and observe changes

**To understand the math:**
- Consult Schaub & Junkins references in docs
- Print intermediate values in the simulation
- Use Python debugger if needed

---

## 🚀 Example Commands

### Run everything in sequence
```bash
python3 01_single_rw_derivation.py
python3 02_single_rw_simulation.py
python3 03_pd_control.py
```

### Create and run custom simulation
```bash
cp 00_template_custom.py my_test.py
nano my_test.py  # Edit parameters
python3 my_test.py
```

### Quick one-liner test
```bash
cd /workspaces/SPACE_SYSTEMS/reaction-wheel-spacecraft-simulator && python3 01_single_rw_derivation.py
```

---

## 📋 File Structure

```
reaction-wheel-spacecraft-simulator/
│
├── 🎯 PYTHON SCRIPTS (Main Entry Points)
│   ├── 01_single_rw_derivation.py    ← Physics theory demo
│   ├── 02_single_rw_simulation.py    ← Full simulation
│   ├── 03_pd_control.py              ← Control analysis
│   └── 00_template_custom.py         ← Your starting template
│
├── 📚 DOCUMENTATION
│   ├── RUN_THESE_SCRIPTS.md          ← ⭐ START HERE
│   ├── PYTHON_SCRIPTS_README.md      ← Module reference
│   ├── INDEX.md                      ← This file
│   └── README.md                     ← Project overview
│
├── 🔧 SOURCE CODE (Don't need to edit)
│   └── src/
│       ├── reaction_wheel.py         ← Reaction wheel model
│       ├── rigid_body.py             ← Rigid body dynamics
│       ├── spacecraft.py             ← Simulator integration
│       └── utils.py                  ← Utilities & plotting
│
├── 📦 DEPENDENCIES
│   └── requirements.txt
│
└── 📂 OUTPUT (Generated when running scripts)
    ├── simulation_results.csv        ← Data export
    ├── plot_attitude.png             ← Visualization
    ├── plot_angular_velocity.png     ← Visualization
    └── ... (more plots)
```

---

## ✅ Verification

Verify everything works:
```bash
cd /workspaces/SPACE_SYSTEMS/reaction-wheel-spacecraft-simulator
pip install -r requirements.txt
python3 01_single_rw_derivation.py
```

If you see the output without errors, you're all set! ✓

---

## 🎉 Summary

You have:
- ✅ **4 Python scripts** (not Jupyter) ready to run
- ✅ **Complete source code** in `src/` modules  
- ✅ **Comprehensive documentation** explaining everything
- ✅ **Template** for creating custom simulations
- ✅ **Example outputs** (plots, data, analysis)

**Next step:** Read `RUN_THESE_SCRIPTS.md` and pick a script to try!

---

## 📞 Need Help?

1. **Error running scripts?** → Check `requirements.txt` is installed
2. **Want to understand the code?** → Read `PYTHON_SCRIPTS_README.md`
3. **Need physics explanations?** → Run `01_single_rw_derivation.py`
4. **Want to create own sim?** → Use `00_template_custom.py`
5. **Have questions about modules?** → Check docstrings: `python3 -c "from src.spacecraft import CoupledSpacecraft; help(CoupledSpacecraft)"`

---

**You're all set! Happy simulating! 🚀**
