"""Reaction wheel model for spacecraft attitude control.

This module implements a single reaction wheel model that can be integrated
with spacecraft rigid body dynamics for attitude control simulation.
"""

import numpy as np
from typing import Tuple, Optional


class ReactionWheel:
    """Single reaction wheel model.
    
    Models a momentum exchange reaction wheel (MERW) with:
    - Moment of inertia (Iw)
    - Spin axis along a principal body axis
    - Current angular velocity and acceleration
    """
    
    def __init__(self, Iw: float, axis: int = 2):
        """Initialize reaction wheel.
        
        Parameters
        ----------
        Iw : float
            Moment of inertia of reaction wheel (kg*m^2)
        axis : int
            Spin axis (0=x, 1=y, 2=z). Default: z-axis (2)
        """
        if Iw <= 0:
            raise ValueError("Moment of inertia Iw must be positive")
        if axis not in [0, 1, 2]:
            raise ValueError("Axis must be 0 (x), 1 (y), or 2 (z)")
        
        self.Iw = Iw
        self.axis = axis
        self.w = 0.0  # Current angular velocity (rad/s)
        self.alpha = 0.0  # Current angular acceleration (rad/s^2)
        
    def get_angular_momentum(self) -> np.ndarray:
        """Get angular momentum vector of reaction wheel.
        
        Returns
        -------
        np.ndarray
            Angular momentum vector [hx, hy, hz] in body frame (kg*m^2/s)
        """
        h = np.zeros(3)
        h[self.axis] = self.Iw * self.w
        return h
    
    def get_torque_from_acceleration(self, alpha: float) -> float:
        """Calculate required torque for given angular acceleration.
        
        Parameters
        ----------
        alpha : float
            Desired angular acceleration (rad/s^2)
        
        Returns
        -------
        float
            Required torque about spin axis (N*m)
        """
        return self.Iw * alpha
    
    def set_angular_velocity(self, w: float) -> None:
        """Set reaction wheel angular velocity.
        
        Parameters
        ----------
        w : float
            Angular velocity (rad/s)
        """
        self.w = w
    
    def set_angular_acceleration(self, alpha: float) -> None:
        """Set reaction wheel angular acceleration.
        
        Parameters
        ----------
        alpha : float
            Angular acceleration (rad/s^2)
        """
        self.alpha = alpha
    
    def update(self, dt: float, torque: float) -> None:
        """Update reaction wheel state given applied torque.
        
        Parameters
        ----------
        dt : float
            Time step (seconds)
        torque : float
            Applied torque about spin axis (N*m)
        """
        # Calculate angular acceleration
        self.alpha = torque / self.Iw
        
        # Update angular velocity
        self.w += self.alpha * dt
    
    def get_control_torque_on_body(self) -> np.ndarray:
        """Get reaction torque applied to spacecraft body.
        
        By Newton's third law, the torque exerted by the wheel on the body
        is equal and opposite to the torque applied to the wheel.
        
        Returns
        -------
        np.ndarray
            Reaction torque on body [tx, ty, tz] (N*m)
        """
        torque = np.zeros(3)
        torque[self.axis] = -self.Iw * self.alpha
        return torque


def coupled_dynamics(
    Ih: np.ndarray,
    w_body: np.ndarray,
    Iw: float,
    w_wheel: float,
    u_wheel: float,
    external_torque: Optional[np.ndarray] = None,
    axis: int = 2
) -> Tuple[np.ndarray, float]:
    """Compute coupled hub-wheel angular accelerations.
    
    For a rigid spacecraft hub (moment of inertia Ih) coupled with a reaction
    wheel (moment of inertia Iw) spinning about a principal body axis.
    
    Parameters
    ----------
    Ih : np.ndarray
        Inertia matrix of hub (3x3, kg*m^2)
    w_body : np.ndarray
        Current angular velocity of hub (rad/s)
    Iw : float
        Moment of inertia of wheel about spin axis (kg*m^2)
    w_wheel : float
        Current angular velocity of wheel about spin axis (rad/s)
    u_wheel : float
        Control torque applied to wheel about spin axis (N*m)
    external_torque : np.ndarray, optional
        External torques on system (3,) (N*m). Default: zero
    axis : int
        Spin axis of reaction wheel (0=x, 1=y, 2=z). Default: 2
    
    Returns
    -------
    alpha_hub : np.ndarray
        Angular acceleration of hub (rad/s^2)
    alpha_wheel : float
        Angular acceleration of wheel (rad/s^2)
    """
    if external_torque is None:
        external_torque = np.zeros(3)
    
    # Reaction torque on body from wheel
    tau_reaction = np.zeros(3)
    tau_reaction[axis] = -Iw * (u_wheel / Iw)  # Wheel acceleration from control
    
    # Total torque on body
    tau_total = external_torque + tau_reaction
    
    # Hub angular acceleration: Ih * alpha_h = tau_total - (gyro terms)
    # For small angles or momentum exchange, simplified:
    try:
        alpha_hub = np.linalg.solve(Ih, tau_total)
    except np.linalg.LinAlgError:
        alpha_hub = np.zeros(3)
    
    # Wheel angular acceleration
    alpha_wheel = u_wheel / Iw
    
    return alpha_hub, alpha_wheel


def skew_symmetric(v: np.ndarray) -> np.ndarray:
    """Create skew-symmetric matrix from 3D vector.
    
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
