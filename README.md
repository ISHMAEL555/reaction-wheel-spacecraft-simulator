# Reaction Wheel Spacecraft Attitude Control Simulator

**Python simulation of rigid spacecraft + reaction wheel dynamics** based on **Schaub & Junkins - Analytical Mechanics of Space Systems (Chapter 4)**.

This project implements the coupled equations of motion for a rigid body spacecraft with a single fixed reaction wheel actuator.

## Features
- Derivation and implementation of spacecraft + reaction wheel EOMs
- Numerical integration using `scipy.integrate.solve_ivp`
- Torque-free motion simulation
- Controlled motion (constant torque or simple PD controller - coming soon)
- Visualization of angular velocity ω(t) and wheel speed Ω(t)

## Technologies
- Python 3
- NumPy, SciPy, Matplotlib
- Jupyter Notebooks

## Reference
- Problems 4.20 – 4.23 from Schaub & Junkins textbook

## Project Structure
