# Testing Guide

This guide validates that the simulator executes correctly and produces expected artifacts.

## Prerequisites

```bash
# from repository root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Smoke tests

### Test 1 — Theory/derivation script

```bash
python3 01_single_rw_derivation.py
```

Pass criteria:
- process exits successfully,
- sections 1..5 print,
- summary banner appears.

### Test 2 — Full simulation script

```bash
python3 02_single_rw_simulation.py
```

Pass criteria:
- process exits successfully,
- simulation reaches completion banner,
- output files are created:
  - `simulation_results.csv`
  - `plot_attitude.png`
  - `plot_angular_velocity.png`
  - `plot_wheel_velocity.png`
  - `plot_angular_momentum.png`
  - `plot_phase_portrait.png`

### Test 3 — PD comparison script

```bash
python3 03_pd_control.py
```

Pass criteria:
- process exits successfully,
- all four controller configurations are evaluated,
- output files are created:
  - `plot_pd_comparison_pitch.png`
  - `plot_pd_comparison_wheel.png`

## Programmatic artifact checks

```bash
test -f simulation_results.csv
test -f plot_attitude.png
test -f plot_angular_velocity.png
test -f plot_wheel_velocity.png
test -f plot_angular_momentum.png
test -f plot_phase_portrait.png
test -f plot_pd_comparison_pitch.png
test -f plot_pd_comparison_wheel.png
```

## Optional: one-command validation

```bash
python3 01_single_rw_derivation.py >/tmp/rw_test1.log
python3 02_single_rw_simulation.py >/tmp/rw_test2.log
python3 03_pd_control.py >/tmp/rw_test3.log
```

Then inspect logs if needed:

```bash
tail -n 40 /tmp/rw_test1.log
tail -n 40 /tmp/rw_test2.log
tail -n 40 /tmp/rw_test3.log
```
