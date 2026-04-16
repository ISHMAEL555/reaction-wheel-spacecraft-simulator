"""Coupled spacecraft + reaction wheel dynamics model.

Combines rigid body dynamics with reaction wheel actuator for spacecraft
attitude control simulations.
"""

import numpy as np
from typing import Tuple, Optional
from dataclasses import dataclass

import rigid_body
from reaction_wheel import ReactionWheel


@dataclass
class SpacecraftState:
    """State vector for spacecraft + reaction wheel system."""
    euler_angles: np.ndarray  # [roll, pitch, yaw] (rad)
    w_body: np.ndarray        # Angular velocity [wx, wy, wz] (rad/s)
    w_wheel: float            # Reaction wheel angular velocity (rad/s)
    time: float = 0.0         # Current simulation time (s)


class CoupledSpacecraft:
    """Coupled spacecraft hub + single reaction wheel system.
    
    Implements integrated dynamics for a rigid spacecraft hub with
    a reaction wheel actuator for attitude control.
    """
    
    def __init__(
        self,
        I_hub: np.ndarray,
        I_wheel: float,
        wheel_axis: int = 2,
        mass: float = 1.0,
        name: str = "Spacecraft"
    ):
        """Initialize coupled spacecraft-wheel system.
        
        Parameters
        ----------
        I_hub : np.ndarray
            Hub moment of inertia matrix (3x3, kg*m^2)
        I_wheel : float
            Reaction wheel moment of inertia (kg*m^2)
        wheel_axis : int
            Reaction wheel spin axis (0=x, 1=y, 2=z). Default: 2 (z-axis)
        mass : float
            Spacecraft total mass (kg). Default: 1.0
        name : str
            System name. Default: "Spacecraft"
        """
        self.I_hub = I_hub
        self.I_wheel = I_wheel
        self.wheel_axis = wheel_axis
        self.mass = mass
        self.name = name
        
        # Initialize reaction wheel
        self.wheel = ReactionWheel(I_wheel, axis=wheel_axis)
        
        # Initialize state
        self.state = SpacecraftState(
            euler_angles=np.zeros(3),
            w_body=np.zeros(3),
            w_wheel=0.0,
            time=0.0
        )
        
        # Accumulated torques for logging
        self.external_torque = np.zeros(3)
        self.control_torque = np.zeros(3)
    
    def set_external_torque(self, tau: np.ndarray) -> None:
        """Set external torque on spacecraft.
        
        Parameters
        ----------
        tau : np.ndarray
            External torque [tx, ty, tz] (N*m)
        """
        self.external_torque = np.array(tau)
    
    def set_reaction_wheel_torque(self, u: float) -> None:
        """Set control torque command to reaction wheel.
        
        Parameters
        ----------
        u : float
            Control torque about reaction wheel spin axis (N*m)
        """
        self.wheel.set_angular_acceleration(u / self.I_wheel)
    
    def get_state_vector(self) -> np.ndarray:
        """Return current state as vector for ODE integration.
        
        Returns
        -------
        np.ndarray
            State vector [roll, pitch, yaw, wx, wy, wz, w_wheel] (7,)
        """
        return np.concatenate([
            self.state.euler_angles,
            self.state.w_body,
            [self.state.w_wheel]
        ])
    
    def set_state_vector(self, state_vec: np.ndarray) -> None:
        """Set state from vector (inverse of get_state_vector).
        
        Parameters
        ----------
        state_vec : np.ndarray
            State vector [roll, pitch, yaw, wx, wy, wz, w_wheel] (7,)
        """
        self.state.euler_angles = state_vec[0:3]
        self.state.w_body = state_vec[3:6]
        self.state.w_wheel = state_vec[6]
    
    def dynamics(self, t: float, state_vec: np.ndarray) -> np.ndarray:
        """Compute state derivatives for ODE integration.
        
        Parameters
        ----------
        t : float
            Current time (s)
        state_vec : np.ndarray
            Current state [roll, pitch, yaw, wx, wy, wz, w_wheel] (7,)
        
        Returns
        -------
        np.ndarray
            State derivatives [d_roll, d_pitch, d_yaw, ax, ay, az, a_wheel] (7,)
        """
        # Extract state
        euler = state_vec[0:3]
        w_body = state_vec[3:6]
        w_wheel = state_vec[6]
        
        # Update wheel state
        self.wheel.w = w_wheel
        
        # Reaction torque from wheel
        tau_wheel = np.zeros(3)
        tau_wheel[self.wheel_axis] = -self.I_wheel * self.wheel.alpha
        
        # Total torque on hub
        tau_hub = self.external_torque + tau_wheel
        
        # Hub dynamics: Euler's equations
        alpha_hub = rigid_body.euler_dynamics(self.I_hub, w_body, tau_hub)
        
        # Wheel dynamics
        alpha_wheel = self.wheel.alpha
        
        # Kinematics: Euler angle rates
        euler_rates = rigid_body.kinematics_euler(euler, w_body)
        
        # Assemble derivative vector
        derivatives = np.concatenate([
            euler_rates,      # [d_roll, d_pitch, d_yaw]
            alpha_hub,        # [ax, ay, az]
            [alpha_wheel]     # [a_wheel]
        ])
        
        return derivatives
    
    def step(self, dt: float, u_wheel: float = 0.0, tau_ext: Optional[np.ndarray] = None) -> None:
        """Integrate forward one time step using simple Euler integration.
        
        Parameters
        ----------
        dt : float
            Time step (s)
        u_wheel : float
            Reaction wheel control torque (N*m)
        tau_ext : np.ndarray, optional
            External torque on spacecraft [tx, ty, tz] (N*m)
        """
        if tau_ext is not None:
            self.external_torque = np.array(tau_ext)
        
        self.wheel.alpha = u_wheel / self.I_wheel
        
        # Compute derivatives at current state
        state_vec = self.get_state_vector()
        derivatives = self.dynamics(self.state.time, state_vec)
        
        # Update state
        new_state = state_vec + derivatives * dt
        self.set_state_vector(new_state)
        
        # Update wheel
        self.state.w_wheel = new_state[6]
        self.wheel.w = self.state.w_wheel
        
        # Update time
        self.state.time += dt
    
    def get_angular_momentum(self) -> np.ndarray:
        """Get total angular momentum of system (hub + wheel).
        
        Returns
        -------
        np.ndarray
            Angular momentum [hx, hy, hz] (kg*m^2/s)
        """
        h_hub = rigid_body.angular_momentum(self.I_hub, self.state.w_body)
        h_wheel = self.wheel.get_angular_momentum()
        return h_hub + h_wheel
    
    def get_rotational_kinetic_energy(self) -> float:
        """Get total rotational kinetic energy.
        
        Returns
        -------
        float
            Kinetic energy (J)
        """
        ke_hub = rigid_body.rotational_kinetic_energy(self.I_hub, self.state.w_body)
        ke_wheel = rigid_body.rotational_kinetic_energy(
            np.diag([self.I_wheel, self.I_wheel, self.I_wheel]),
            np.array([self.state.w_wheel if self.wheel_axis == 0 else 0,
                      self.state.w_wheel if self.wheel_axis == 1 else 0,
                      self.state.w_wheel if self.wheel_axis == 2 else 0])
        )
        return ke_hub + ke_wheel
