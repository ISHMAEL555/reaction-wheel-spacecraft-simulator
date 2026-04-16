# Run Guide (Standalone Python Scripts)

This repository is designed to run directly from the command line (no notebook dependency required).

## 1) Environment setup

```bash
# from repository root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Core scripts

```bash
python3 01_single_rw_derivation.py
python3 02_single_rw_simulation.py
python3 03_pd_control.py
```

### `01_single_rw_derivation.py`
Educational walkthrough of:
- rigid-body rotational dynamics,
- attitude representations (Euler/DCM/quaternion),
- reaction-wheel torque coupling.

Expected: console output only.

### `02_single_rw_simulation.py`
Full 50-second closed-loop simulation with PD control.

Expected artifacts:
- `simulation_results.csv`
- `plot_attitude.png`
- `plot_angular_velocity.png`
- `plot_wheel_velocity.png`
- `plot_angular_momentum.png`
- `plot_phase_portrait.png`

### `03_pd_control.py`
Runs a gain sweep across four PD configurations and compares performance under disturbance.

Expected artifacts:
- `plot_pd_comparison_pitch.png`
- `plot_pd_comparison_wheel.png`

## 3) Create your own experiment

```bash
cp 00_template_custom.py my_experiment.py
python3 my_experiment.py
```

## 4) Troubleshooting

- If `ModuleNotFoundError` occurs, make sure you run scripts from repository root.
- If plots do not render in a headless environment, files are still saved via `matplotlib`.
- If results differ run-to-run after parameter edits, compare your modified gains, disturbance profile, and initial conditions.
