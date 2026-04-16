"""Rigid body model for spacecraft attitude dynamics.

This module implements rigid body kinematics and dynamics based on Euler's
equations for a rotating rigid body without external forces.
"""

import numpy as np
from typing import Tuple, Optional


def dcm_from_euler_angles(
    roll: float, pitch: float, yaw: float, convention: str = '321'
) -> np.ndarray:
    """Compute Direction Cosine Matrix (DCM) from Euler angles.
    
    Parameters
    ----------
    roll : float
        Roll angle (rad)
    pitch : float
        Pitch angle (rad)
    yaw : float
        Yaw angle (rad)
    convention : str
        Euler angle convention ('321' for yaw-pitch-roll). Default: '321'
    
    Returns
    -------
    np.ndarray
        Direction Cosine Matrix (3x3) - transforms from body to inertial frame
    """
    if convention != '321':
        raise NotImplementedError("Only '321' convention currently supported")
    
    cy, sy = np.cos(yaw), np.sin(yaw)
    cp, sp = np.cos(pitch), np.sin(pitch)
    cr, sr = np.cos(roll), np.sin(roll)
    
    dcm = np.array([
        [cy*cp, cy*sp*sr - sy*cr, cy*sp*cr + sy*sr],
        [sy*cp, sy*sp*sr + cy*cr, sy*sp*cr - cy*sr],
        [-sp, cp*sr, cp*cr]
    ])
    return dcm


def euler_angles_from_dcm(dcm: np.ndarray, convention: str = '321') -> Tuple[float, float, float]:
    """Extract Euler angles from Direction Cosine Matrix.
    
    Parameters
    ----------
    dcm : np.ndarray
        Direction Cosine Matrix (3x3)
    convention : str
        Euler angle convention ('321' for yaw-pitch-roll). Default: '321'
    
    Returns
    -------
    roll, pitch, yaw : float
        Euler angles (rad)
    """
    if convention != '321':
        raise NotImplementedError("Only '321' convention currently supported")
    
    pitch = np.arcsin(-dcm[2, 0])
    roll = np.arctan2(dcm[2, 1], dcm[2, 2])
    yaw = np.arctan2(dcm[1, 0], dcm[0, 0])
    
    return roll, pitch, yaw


def quaternion_from_dcm(dcm: np.ndarray) -> np.ndarray:
    """Compute quaternion from Direction Cosine Matrix.
    
    Returns quaternion in format [q1, q2, q3, q4] where q4 is the scalar part.
    
    Parameters
    ----------
    dcm : np.ndarray
        Direction Cosine Matrix (3x3)
    
    Returns
    -------
    np.ndarray
        Quaternion [q1, q2, q3, q4] (4,)
    """
    trace = dcm[0, 0] + dcm[1, 1] + dcm[2, 2]
    
    if trace > 0:
        s = 0.5 / np.sqrt(trace + 1.0)
        q4 = 0.25 / s
        q1 = (dcm[2, 1] - dcm[1, 2]) * s
        q2 = (dcm[0, 2] - dcm[2, 0]) * s
        q3 = (dcm[1, 0] - dcm[0, 1]) * s
    elif dcm[0, 0] > dcm[1, 1] and dcm[0, 0] > dcm[2, 2]:
        s = 2.0 * np.sqrt(1.0 + dcm[0, 0] - dcm[1, 1] - dcm[2, 2])
        q4 = (dcm[2, 1] - dcm[1, 2]) / s
        q1 = 0.25 * s
        q2 = (dcm[0, 1] + dcm[1, 0]) / s
        q3 = (dcm[0, 2] + dcm[2, 0]) / s
    elif dcm[1, 1] > dcm[2, 2]:
        s = 2.0 * np.sqrt(1.0 + dcm[1, 1] - dcm[0, 0] - dcm[2, 2])
        q4 = (dcm[0, 2] - dcm[2, 0]) / s
        q1 = (dcm[0, 1] + dcm[1, 0]) / s
        q2 = 0.25 * s
        q3 = (dcm[1, 2] + dcm[2, 1]) / s
    else:
        s = 2.0 * np.sqrt(1.0 + dcm[2, 2] - dcm[0, 0] - dcm[1, 1])
        q4 = (dcm[1, 0] - dcm[0, 1]) / s
        q1 = (dcm[0, 2] + dcm[2, 0]) / s
        q2 = (dcm[1, 2] + dcm[2, 1]) / s
        q3 = 0.25 * s
    
    return np.array([q1, q2, q3, q4])


def dcm_from_quaternion(q: np.ndarray) -> np.ndarray:
    """Compute Direction Cosine Matrix from quaternion.
    
    Parameters
    ----------
    q : np.ndarray
        Quaternion [q1, q2, q3, q4] where q4 is scalar part (4,)
    
    Returns
    -------
    np.ndarray
        Direction Cosine Matrix (3x3)
    """
    q1, q2, q3, q4 = q
    
    dcm = np.array([
        [q4**2 + q1**2 - q2**2 - q3**2, 2*(q1*q2 + q3*q4), 2*(q1*q3 - q2*q4)],
        [2*(q1*q2 - q3*q4), q4**2 - q1**2 + q2**2 - q3**2, 2*(q2*q3 + q1*q4)],
        [2*(q1*q3 + q2*q4), 2*(q2*q3 - q1*q4), q4**2 - q1**2 - q2**2 + q3**2]
    ])
    return dcm


def kinematics_euler(
    euler_angles: np.ndarray, w_body: np.ndarray
) -> np.ndarray:
    """Compute Euler angle rates from body angular velocity.
    
    Parameters
    ----------
    euler_angles : np.ndarray
        [roll, pitch, yaw] (rad)
    w_body : np.ndarray
        Angular velocity in body frame [wx, wy, wz] (rad/s)
    
    Returns
    -------
    np.ndarray
        Euler angle rates [d_roll, d_pitch, d_yaw] (rad/s)
    """
    roll, pitch, yaw = euler_angles
    wx, wy, wz = w_body
    
    sin_roll = np.sin(roll)
    cos_roll = np.cos(roll)
    tan_pitch = np.tan(pitch)
    cos_pitch = np.cos(pitch)
    
    d_roll = wx + wy * sin_roll * tan_pitch + wz * cos_roll * tan_pitch
    d_pitch = wy * cos_roll - wz * sin_roll
    d_yaw = wy * sin_roll / cos_pitch + wz * cos_roll / cos_pitch
    
    return np.array([d_roll, d_pitch, d_yaw])


def euler_dynamics(
    I: np.ndarray,
    w: np.ndarray,
    tau: np.ndarray
) -> np.ndarray:
    """Compute rigid body angular acceleration from Euler's equations.
    
    Euler's rotational equation of motion:
    I * alpha + w × (I * w) = tau
    
    Parameters
    ----------
    I : np.ndarray
        Principal moment of inertia matrix (3x3, kg*m^2)
    w : np.ndarray
        Angular velocity in body frame [wx, wy, wz] (rad/s)
    tau : np.ndarray
        Applied torque in body frame [tx, ty, tz] (N*m)
    
    Returns
    -------
    np.ndarray
        Angular acceleration [ax, ay, az] (rad/s^2)
    """
    # Gyroscopic torque: w × (I * w)
    Iw = I @ w
    gyro_torque = np.cross(w, Iw)
    
    # Solve for angular acceleration: I * alpha = tau - gyro_torque
    try:
        alpha = np.linalg.solve(I, tau - gyro_torque)
    except np.linalg.LinAlgError:
        alpha = np.zeros(3)
    
    return alpha


def angular_momentum(I: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Compute angular momentum vector.
    
    Parameters
    ----------
    I : np.ndarray
        Inertia matrix (3x3, kg*m^2)
    w : np.ndarray
        Angular velocity [wx, wy, wz] (rad/s)
    
    Returns
    -------
    np.ndarray
        Angular momentum [hx, hy, hz] (kg*m^2/s)
    """
    return I @ w


def rotational_kinetic_energy(I: np.ndarray, w: np.ndarray) -> float:
    """Compute rotational kinetic energy.
    
    Parameters
    ----------
    I : np.ndarray
        Inertia matrix (3x3, kg*m^2)
    w : np.ndarray
        Angular velocity [wx, wy, wz] (rad/s)
    
    Returns
    -------
    float
        Rotational kinetic energy (J)
    """
    return 0.5 * (w @ I @ w)
