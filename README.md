# reaction-wheel-spacecraft-simulator

Python simulation of rigid spacecraft attitude dynamics with reaction wheel actuator (based on Schaub & Junkins *Analytical Mechanics of Space Systems*).

## Project structure

```text
reaction-wheel-spacecraft-simulator/
├── README.md
├── requirements.txt
├── src/
│   ├── rigid_body.py
│   ├── reaction_wheel.py
│   ├── spacecraft.py
│   └── utils.py
├── notebooks/
│   ├── 01_single_rw_derivation.ipynb
│   ├── 02_single_rw_simulation.ipynb
│   └── 03_pd_control.ipynb
├── plots/
├── animations/
└── tests/
```

## Next steps

1. Derive single reaction wheel equations in `notebooks/01_single_rw_derivation.ipynb`.
2. Implement coupled hub + wheel dynamics in `src/`.
3. Build simulation/visualization and PD controller notebooks.
