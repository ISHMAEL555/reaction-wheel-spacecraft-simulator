# Reaction Wheel Spacecraft Simulator

A Python simulator for rigid spacecraft attitude dynamics with a single reaction wheel actuator.

The project focuses on:
- nonlinear rotational dynamics (Euler equations),
- reaction-wheel momentum exchange,
- simple attitude-control experiments,
- plotting and CSV export for analysis.

## Repository layout

```text
.
├── src/
│   ├── rigid_body.py           # Attitude math + rigid-body dynamics
│   ├── reaction_wheel.py       # Reaction wheel model
│   ├── spacecraft.py           # Coupled spacecraft + wheel simulator
│   └── utils.py                # Logging and plotting helpers
├── 00_template_custom.py       # Recommended starting point for custom experiments
├── 01_single_rw_derivation.py  # Educational derivation/demo script
├── 02_single_rw_simulation.py  # Full closed-loop simulation example
├── 03_pd_control.py            # PD gain-comparison study
├── RUN_THESE_SCRIPTS.md        # Quick-start usage guide
├── TESTING_GUIDE.md            # Validation/test workflow
└── requirements.txt
```

## Quick start

```bash
# from repository root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 01_single_rw_derivation.py
python3 02_single_rw_simulation.py
python3 03_pd_control.py
```

## Typical outputs

- `simulation_results.csv`
- `plot_attitude.png`
- `plot_angular_velocity.png`
- `plot_wheel_velocity.png`
- `plot_angular_momentum.png`
- `plot_phase_portrait.png`
- `plot_pd_comparison_pitch.png`
- `plot_pd_comparison_wheel.png`

## Notes

- Scripts are intentionally simple and transparent for education and rapid experimentation.
- For custom work, copy `00_template_custom.py` and adapt parameters/controllers.
