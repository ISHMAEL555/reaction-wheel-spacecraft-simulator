# Reaction Wheel Spacecraft Simulator (Flagship GNC Repo)

A nonlinear attitude-dynamics and control repository for a rigid spacecraft with a single reaction wheel.

## Problem statement

This repository demonstrates that a single-wheel spacecraft model can be used for **engineering-grade GNC reasoning** (not just animation):

- nonlinear rotational dynamics from Euler equations,
- attitude propagation with explicit quaternion kinematics,
- conservation-law validation in torque-free conditions,
- closed-loop PD control with disturbance rejection,
- plots and metrics that verify behavior.

## Repository structure

```text
.
├── models/
│   └── system_model_and_derivation.md   # Assumptions, equations, stability, failure modes
├── simulation/
│   └── closed_loop_pd_demo.py           # Closed-loop response + disturbance case
├── validation/
│   └── torque_free_validation.py        # Conservation-law verification
├── plots/                               # Generated figures proving model behavior
├── src/
│   ├── rigid_body.py                    # Dynamics + kinematics utilities
│   ├── reaction_wheel.py                # Wheel model
│   ├── spacecraft.py                    # Coupled spacecraft + wheel system
│   └── utils.py                         # Logging/plot helpers
└── requirements.txt
```

## System model

Core equations are in `models/system_model_and_derivation.md` and implemented in `src/`.

- Hub rotational dynamics:
  \(I_h\dot\omega + \omega\times(I_h\omega) = \tau_{ext}+\tau_{rw}\)
- Wheel momentum exchange:
  \(\tau_{rw}=-u\hat e_a\), \(\dot\omega_w = u/I_w\)
- Quaternion kinematics (scalar-last):
  \(\dot q=\frac12\Omega(\omega)q\), with normalization.
- Conservation check quantity used in validation:
  \(H_h = I_h\omega\) (hub angular momentum norm under torque-free motion).

## Assumptions

- Rigid body hub, principal inertia frame.
- Single wheel aligned with a principal axis.
- Optional bounded disturbance torque for robustness demos.
- Small-angle interpretation only for linearized gain discussion; simulation remains nonlinear.

## Control law implementation

Closed-loop pitch-axis PD control in `simulation/closed_loop_pd_demo.py`:

- \(u = K_p\theta + K_d\dot\theta\) in the current sign convention
- actuator saturation \(|u|\le u_{max}\)
- disturbance injection window to test recovery.
- reaction wheel aligned with the pitch axis in this demo (single-axis authority).

Gain rationale follows second-order mapping:

- \(\omega_n=\sqrt{K_p/I_{eq}}\)
- \(\zeta=K_d/(2\sqrt{I_{eq}K_p})\)

## Validation cases

### 1) Torque-free motion and conservation laws

Run:

```bash
python3 validation/torque_free_validation.py
```

Output:

- `plots/torque_free_conservation.png`
- printed max drift in \(|H_h|\) and kinetic energy.

### 2) Closed-loop response with disturbance

Run:

```bash
python3 simulation/closed_loop_pd_demo.py
```

Output:

- `plots/closed_loop_pd_response.png`
- peak pitch, settling estimate, peak control effort, peak wheel speed.

> Note: generated figures in `plots/` are intentionally not versioned (binary-free repo policy).

## Engineering seriousness checklist

This repo explicitly includes:

- ✅ system model and assumptions,
- ✅ derivation notes (Euler + quaternion kinematics),
- ✅ conservation validation,
- ✅ closed-loop control + disturbance response,
- ✅ stability and gain-selection discussion,
- ✅ failure modes (saturation, inertia mismatch, singularity risk, momentum buildup).

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 validation/torque_free_validation.py
python3 simulation/closed_loop_pd_demo.py
```

Legacy scripts (`01_*.py`, `02_*.py`, `03_*.py`) are retained for comparison and educational walkthroughs.
