"""Utility helpers for simulation, plotting, and math operations."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Tuple, Dict, Optional
import pandas as pd


# ============================================================================
# Math Utilities
# ============================================================================

def skew_symmetric(v: np.ndarray) -> np.ndarray:
    """Create skew-symmetric matrix from 3D vector.
    
    For vector v = [v1, v2, v3], returns matrix such that
    skew(v) @ u = v × u (cross product).
    
    Parameters
    ----------
    v : np.ndarray
        Input vector (3,)
    
    Returns
    -------
    np.ndarray
        Skew-symmetric matrix (3x3)
    """
    return np.array([
        [0, -v[2], v[1]],
        [v[2], 0, -v[0]],
        [-v[1], v[0], 0]
    ])


def normalize_quaternion(q: np.ndarray) -> np.ndarray:
    """Normalize quaternion to unit length.
    
    Parameters
    ----------
    q : np.ndarray
        Quaternion [q1, q2, q3, q4] (4,)
    
    Returns
    -------
    np.ndarray
        Normalized quaternion (4,)
    """
    return q / np.linalg.norm(q)


def quaternion_multiply(q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
    """Multiply two quaternions.
    
    Quaternions in format [q1, q2, q3, q4] where q4 is scalar part.
    
    Parameters
    ----------
    q1, q2 : np.ndarray
        Quaternions (4,) each
    
    Returns
    -------
    np.ndarray
        Product quaternion (4,)
    """
    q1_vec = q1[:3]
    q1_scal = q1[3]
    q2_vec = q2[:3]
    q2_scal = q2[3]
    
    q_vec = q1_scal * q2_vec + q2_scal * q1_vec + np.cross(q1_vec, q2_vec)
    q_scal = q1_scal * q2_scal - np.dot(q1_vec, q2_vec)
    
    return np.array([q_vec[0], q_vec[1], q_vec[2], q_scal])


def degrees(radians: float) -> float:
    """Convert radians to degrees."""
    return radians * 180.0 / np.pi


def radians(degrees: float) -> float:
    """Convert degrees to radians."""
    return degrees * np.pi / 180.0


# ============================================================================
# Data Logging and Analysis
# ============================================================================

class SimulationLogger:
    """Log simulation state history for analysis and visualization."""
    
    def __init__(self):
        """Initialize empty logs."""
        self.time = []
        self.euler_angles = []
        self.w_body = []
        self.w_wheel = []
        self.tau_ext = []
        self.tau_wheel = []
        self.h_total = []
        self.ke_total = []
    
    def log(
        self,
        t: float,
        euler: np.ndarray,
        w_body: np.ndarray,
        w_wheel: float,
        tau_ext: np.ndarray = None,
        tau_wheel: np.ndarray = None,
        h: np.ndarray = None,
        ke: float = None
    ) -> None:
        """Log state at current time.
        
        Parameters
        ----------
        t : float
            Current time (s)
        euler : np.ndarray
            Euler angles [roll, pitch, yaw] (rad)
        w_body : np.ndarray
            Body angular velocity (rad/s)
        w_wheel : float
            Wheel angular velocity (rad/s)
        tau_ext : np.ndarray, optional
            External torque
        tau_wheel : np.ndarray, optional
            Wheel reaction torque
        h : np.ndarray, optional
            Total angular momentum
        ke : float, optional
            Total kinetic energy
        """
        self.time.append(t)
        self.euler_angles.append(np.array(euler))
        self.w_body.append(np.array(w_body))
        self.w_wheel.append(w_wheel)
        
        if tau_ext is not None:
            self.tau_ext.append(np.array(tau_ext))
        if tau_wheel is not None:
            self.tau_wheel.append(np.array(tau_wheel))
        if h is not None:
            self.h_total.append(np.array(h))
        if ke is not None:
            self.ke_total.append(ke)
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert logs to pandas DataFrame.
        
        Returns
        -------
        pd.DataFrame
            Simulation data with columns for each state variable
        """
        data = {
            'time': self.time,
            'roll': [e[0] for e in self.euler_angles],
            'pitch': [e[1] for e in self.euler_angles],
            'yaw': [e[2] for e in self.euler_angles],
            'wx': [w[0] for w in self.w_body],
            'wy': [w[1] for w in self.w_body],
            'wz': [w[2] for w in self.w_body],
            'w_wheel': self.w_wheel,
        }
        
        if self.tau_ext:
            data['tau_x'] = [t[0] for t in self.tau_ext]
            data['tau_y'] = [t[1] for t in self.tau_ext]
            data['tau_z'] = [t[2] for t in self.tau_ext]
        
        if self.ke_total:
            data['ke'] = self.ke_total
        
        return pd.DataFrame(data)
    
    def save_csv(self, filename: str) -> None:
        """Save logs to CSV file.
        
        Parameters
        ----------
        filename : str
            Output CSV filename
        """
        df = self.to_dataframe()
        df.to_csv(filename, index=False)


# ============================================================================
# Plotting Utilities
# ============================================================================

def plot_attitude_history(
    t: List[float],
    euler_angles: List[np.ndarray],
    figsize: Tuple[int, int] = (12, 8)
) -> Tuple[plt.Figure, np.ndarray]:
    """Plot Euler angle evolution over time.
    
    Parameters
    ----------
    t : List[float]
        Time history (s)
    euler_angles : List[np.ndarray]
        Euler angle history [[roll, pitch, yaw], ...]
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    fig : plt.Figure
    axes : np.ndarray
        Subplot axes
    """
    euler = np.array(euler_angles)
    
    fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=True)
    labels = ['Roll', 'Pitch', 'Yaw']
    
    for i, ax in enumerate(axes):
        ax.plot(t, degrees(euler[:, i]), 'b-', linewidth=1.5)
        ax.set_ylabel(f'{labels[i]} (deg)')
        ax.grid(True, alpha=0.3)
    
    axes[-1].set_xlabel('Time (s)')
    fig.suptitle('Spacecraft Attitude History', fontsize=14)
    plt.tight_layout()
    
    return fig, axes


def plot_angular_velocity_history(
    t: List[float],
    w_body: List[np.ndarray],
    figsize: Tuple[int, int] = (12, 8)
) -> Tuple[plt.Figure, np.ndarray]:
    """Plot body angular velocity evolution over time.
    
    Parameters
    ----------
    t : List[float]
        Time history (s)
    w_body : List[np.ndarray]
        Angular velocity history [[wx, wy, wz], ...]
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    fig : plt.Figure
    axes : np.ndarray
        Subplot axes
    """
    w = np.array(w_body)
    
    fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=True)
    labels = [r'$\omega_x$', r'$\omega_y$', r'$\omega_z$']
    
    for i, ax in enumerate(axes):
        ax.plot(t, w[:, i], 'r-', linewidth=1.5)
        ax.set_ylabel(f'{labels[i]} (rad/s)')
        ax.grid(True, alpha=0.3)
    
    axes[-1].set_xlabel('Time (s)')
    fig.suptitle('Angular Velocity History', fontsize=14)
    plt.tight_layout()
    
    return fig, axes


def plot_wheel_angular_velocity(
    t: List[float],
    w_wheel: List[float],
    figsize: Tuple[int, int] = (10, 5)
) -> Tuple[plt.Figure, plt.Axes]:
    """Plot reaction wheel angular velocity.
    
    Parameters
    ----------
    t : List[float]
        Time history (s)
    w_wheel : List[float]
        Wheel angular velocity history (rad/s)
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    fig : plt.Figure
    ax : plt.Axes
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(t, w_wheel, 'g-', linewidth=2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Angular Velocity (rad/s)')
    ax.set_title('Reaction Wheel Angular Velocity')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig, ax


def plot_angular_momentum(
    t: List[float],
    h_total: List[np.ndarray],
    figsize: Tuple[int, int] = (12, 8)
) -> Tuple[plt.Figure, np.ndarray]:
    """Plot total angular momentum history.
    
    Parameters
    ----------
    t : List[float]
        Time history (s)
    h_total : List[np.ndarray]
        Angular momentum history [[hx, hy, hz], ...]
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    fig : plt.Figure
    axes : np.ndarray
    """
    h = np.array(h_total)
    h_magnitude = np.linalg.norm(h, axis=1)
    
    fig, axes = plt.subplots(2, 1, figsize=figsize, sharex=True)
    
    # Components
    ax = axes[0]
    ax.plot(t, h[:, 0], label='$h_x$')
    ax.plot(t, h[:, 1], label='$h_y$')
    ax.plot(t, h[:, 2], label='$h_z$')
    ax.set_ylabel('Components (kg·m²/s)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Magnitude
    ax = axes[1]
    ax.plot(t, h_magnitude, 'k-', linewidth=2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Magnitude (kg·m²/s)')
    ax.grid(True, alpha=0.3)
    
    fig.suptitle('Total Angular Momentum', fontsize=14)
    plt.tight_layout()
    
    return fig, axes


def plot_phase_portrait(
    w_body: List[np.ndarray],
    figsize: Tuple[int, int] = (10, 8)
) -> Tuple[plt.Figure, plt.Axes]:
    """Plot 3D phase portrait of angular velocity.
    
    Parameters
    ----------
    w_body : List[np.ndarray]
        Angular velocity history [[wx, wy, wz], ...]
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    fig : plt.Figure
    ax : plt.Axes
    """
    from mpl_toolkits.mplot3d import Axes3D
    
    w = np.array(w_body)
    
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(w[:, 0], w[:, 1], w[:, 2], 'b-', linewidth=1)
    ax.scatter(w[0, 0], w[0, 1], w[0, 2], c='g', s=100, label='Start')
    ax.scatter(w[-1, 0], w[-1, 1], w[-1, 2], c='r', s=100, label='End')
    
    ax.set_xlabel(r'$\omega_x$ (rad/s)')
    ax.set_ylabel(r'$\omega_y$ (rad/s)')
    ax.set_zlabel(r'$\omega_z$ (rad/s)')
    ax.set_title('Angular Velocity Phase Portrait (Polhode)')
    ax.legend()
    
    plt.tight_layout()
    return fig, ax


def plot_polhode_herpolhode(
    t: List[float],
    w_body: List[np.ndarray],
    h_inertial: List[np.ndarray],
    figsize: Tuple[int, int] = (14, 6)
) -> Tuple[plt.Figure, np.ndarray]:
    """Plot polhode (body frame) and herpolhode (inertial frame).
    
    Polhode: Trace of angular velocity vector in body-fixed frame
    Herpolhode: Trace of angular velocity vector in inertial frame
    
    Parameters
    ----------
    t : List[float]
        Time history (s)
    w_body : List[np.ndarray]
        Angular velocity in body frame [[wx, wy, wz], ...]
    h_inertial : List[np.ndarray]
        Angular momentum in inertial frame [[hx, hy, hz], ...]
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    fig : plt.Figure
    axes : np.ndarray
    """
    from mpl_toolkits.mplot3d import Axes3D
    
    w = np.array(w_body)
    h = np.array(h_inertial)
    
    fig = plt.figure(figsize=figsize)
    
    # Polhode (body frame)
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(w[:, 0], w[:, 1], w[:, 2], 'b-', linewidth=1.5, label='Polhode')
    ax1.scatter(w[0, 0], w[0, 1], w[0, 2], c='g', s=100, marker='o', label='Start')
    ax1.scatter(w[-1, 0], w[-1, 1], w[-1, 2], c='r', s=100, marker='s', label='End')
    ax1.set_xlabel(r'$\omega_x$ (rad/s)')
    ax1.set_ylabel(r'$\omega_y$ (rad/s)')
    ax1.set_zlabel(r'$\omega_z$ (rad/s)')
    ax1.set_title('Polhode (Body-Fixed Frame)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Herpolhode (inertial frame)
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot(h[:, 0], h[:, 1], h[:, 2], 'r-', linewidth=1.5, label='Herpolhode')
    ax2.scatter(h[0, 0], h[0, 1], h[0, 2], c='g', s=100, marker='o', label='Start')
    ax2.scatter(h[-1, 0], h[-1, 1], h[-1, 2], c='k', s=100, marker='s', label='End')
    ax2.set_xlabel(r'$h_x$ (kg·m²/s)')
    ax2.set_ylabel(r'$h_y$ (kg·m²/s)')
    ax2.set_zlabel(r'$h_z$ (kg·m²/s)')
    ax2.set_title('Herpolhode (Inertial Frame)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    fig.suptitle('Polhode and Herpolhode Trajectories', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig, np.array([ax1, ax2])


def plot_nutation_precession_rates(
    t: List[float],
    w_body: List[np.ndarray],
    h_inertial: List[np.ndarray],
    I_hub: np.ndarray,
    figsize: Tuple[int, int] = (14, 10)
) -> Tuple[plt.Figure, np.ndarray]:
    """Plot nutation, precession, transverse, and spin rates.
    
    Nutation: Rate of change of angle between spin axis and angular momentum
    Precession: Rate of rotation of angular momentum vector around inertial axis
    Transverse: Components of angular velocity perpendicular to spin axis
    Spin: Component along spin axis
    
    Parameters
    ----------
    t : List[float]
        Time history (s)
    w_body : List[np.ndarray]
        Angular velocity in body frame [[wx, wy, wz], ...]
    h_inertial : List[np.ndarray]
        Angular momentum in inertial frame [[hx, hy, hz], ...]
    I_hub : np.ndarray
        Spacecraft inertia matrix (3x3)
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    fig : plt.Figure
    axes : np.ndarray
    """
    w = np.array(w_body)
    h = np.array(h_inertial)
    
    # Calculate magnitudes
    h_mag = np.linalg.norm(h, axis=1)
    w_mag = np.linalg.norm(w, axis=1)
    
    # Angular momentum direction (space-fixed)
    h_unit = np.array([h[i] / h_mag[i] if h_mag[i] > 1e-6 else np.array([0, 0, 1]) 
                       for i in range(len(h))])
    
    # Spin rate (component along angular momentum direction)
    spin_rate = np.array([np.dot(w[i], h_unit[i]) for i in range(len(w))])
    
    # Transverse angular velocity
    w_trans = np.array([w[i] - spin_rate[i] * h_unit[i] for i in range(len(w))])
    w_trans_mag = np.linalg.norm(w_trans, axis=1)
    
    # Nutation angle (angle between angular velocity and angular momentum)
    cos_nutation = np.array([np.dot(w[i], h_unit[i]) / (w_mag[i] + 1e-8) 
                            for i in range(len(w))])
    cos_nutation = np.clip(cos_nutation, -1, 1)
    nutation_angle = np.arccos(cos_nutation)
    
    # Precession rate (rate of change of angular momentum direction)
    # dp = |dh/dt × h_unit| / |h|
    h_dot = np.gradient(h, t, axis=0)
    precession_rate = np.zeros(len(t))
    for i in range(len(t)):
        h_unit_dot = np.gradient(h_unit, axis=0)[i]
        torque_mag = np.linalg.norm(np.cross(h_unit_dot, h_unit[i])) if h_mag[i] > 1e-6 else 0
        precession_rate[i] = torque_mag * h_mag[i]
    
    fig, axes = plt.subplots(2, 2, figsize=figsize, sharex=True)
    
    # Nutation angle
    ax = axes[0, 0]
    ax.plot(t, degrees(nutation_angle), 'b-', linewidth=2)
    ax.set_ylabel('Nutation Angle (deg)', fontsize=11)
    ax.set_title('Nutation Angle (angle between ω and h)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Precession rate
    ax = axes[0, 1]
    ax.plot(t, degrees(precession_rate), 'r-', linewidth=2)
    ax.set_ylabel('Precession Rate (deg/s)', fontsize=11)
    ax.set_title('Precession Rate (rotation of h in inertial frame)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Spin rate
    ax = axes[1, 0]
    ax.plot(t, spin_rate, 'g-', linewidth=2)
    ax.set_ylabel('Spin Rate (rad/s)', fontsize=11)
    ax.set_xlabel('Time (s)', fontsize=11)
    ax.set_title('Spin Rate (component along h)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Transverse rate
    ax = axes[1, 1]
    ax.plot(t, w_trans_mag, 'm-', linewidth=2)
    ax.set_ylabel('Transverse Rate (rad/s)', fontsize=11)
    ax.set_xlabel('Time (s)', fontsize=11)
    ax.set_title('Transverse Rate (component ⊥ to h)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    fig.suptitle('Nutation, Precession, and Spin Dynamics', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig, axes


def plot_energy_momentum_analysis(
    t: List[float],
    w_body: List[np.ndarray],
    h_inertial: List[np.ndarray],
    I_hub: np.ndarray,
    figsize: Tuple[int, int] = (14, 6)
) -> Tuple[plt.Figure, np.ndarray]:
    """Plot rotational energy and angular momentum magnitude.
    
    Parameters
    ----------
    t : List[float]
        Time history (s)
    w_body : List[np.ndarray]
        Angular velocity [[wx, wy, wz], ...]
    h_inertial : List[np.ndarray]
        Angular momentum [[hx, hy, hz], ...]
    I_hub : np.ndarray
        Inertia matrix (3x3)
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    fig : plt.Figure
    axes : np.ndarray
    """
    w = np.array(w_body)
    h = np.array(h_inertial)
    h_mag = np.linalg.norm(h, axis=1)
    
    # Rotational kinetic energy: E = 0.5 * w^T * I * w
    kinetic_energy = np.zeros(len(t))
    for i in range(len(t)):
        kinetic_energy[i] = 0.5 * np.dot(w[i], np.dot(I_hub, w[i]))
    
    fig, axes = plt.subplots(1, 2, figsize=figsize, sharex=True)
    
    # Rotational energy
    ax = axes[0]
    ax.plot(t, kinetic_energy, 'b-', linewidth=2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Rotational Energy (J)')
    ax.set_title('Rotational Kinetic Energy')
    ax.grid(True, alpha=0.3)
    
    # Angular momentum magnitude
    ax = axes[1]
    ax.plot(t, h_mag, 'r-', linewidth=2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Angular Momentum (kg·m²/s)')
    ax.set_title('Total Angular Momentum Magnitude')
    ax.grid(True, alpha=0.3)
    
    fig.suptitle('Energy and Momentum Conservation', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig, axes
