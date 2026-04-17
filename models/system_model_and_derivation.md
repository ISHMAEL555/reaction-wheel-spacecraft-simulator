# System Model and Derivation

## 1) Problem statement

Design and validate a **single-reaction-wheel attitude dynamics and control simulation** for a rigid spacecraft hub. The objective is to:

1. model nonlinear rotational dynamics using Euler’s equation,
2. propagate attitude using quaternion kinematics,
3. demonstrate conservation behavior in torque-free motion,
4. close the loop with a physically interpretable PD law,
5. quantify stability/performance and practical failure modes.

## 2) Assumptions

- Rigid spacecraft hub with principal-axis inertia matrix \(I_h = \mathrm{diag}(I_x, I_y, I_z)\).
- One reaction wheel aligned with body axis \(\hat{e}_a\) (default: body-z).
- Wheel inertia about its spin axis: \(I_w\).
- Body rates represented in body frame: \(\omega = [\omega_x,\omega_y,\omega_z]^T\).
- Quaternion attitude \(q=[q_1,q_2,q_3,q_4]^T\), scalar-last convention.
- No environmental torques for validation; bounded disturbance torque available for robustness checks.

## 3) Dynamics (Euler + momentum exchange)

Hub rotational dynamics:

\[
I_h\dot\omega + \omega \times (I_h\omega) = \tau_{ext} + \tau_{rw}
\]

Reaction wheel acceleration command \(\alpha_w\) gives wheel torque \(u=I_w\alpha_w\). By Newton's third law, hub torque from wheel is:

\[
\tau_{rw} = -u\,\hat{e}_a
\]

Wheel speed dynamics:

\[
\dot\omega_w = \alpha_w = \frac{u}{I_w}
\]

Hub angular momentum:

\[
H_h = I_h\omega
\]

Under \(\tau_{ext}=0\), \(\|H_h\|\) is conserved for the rigid hub dynamics implemented here and is used as a validation metric.

## 4) Quaternion kinematics

Define
\[
\Omega(\omega)=
\begin{bmatrix}
0 & \omega_z & -\omega_y & \omega_x\\
-\omega_z & 0 & \omega_x & \omega_y\\
\omega_y & -\omega_x & 0 & \omega_z\\
-\omega_x & -\omega_y & -\omega_z & 0
\end{bmatrix}
\]

Then quaternion propagation is

\[
\dot q = \frac{1}{2}\Omega(\omega)q
\]

Numerically, after each integration step enforce normalization:

\[
q \leftarrow \frac{q}{\|q\|}
\]

This avoids attitude drift and makes conservation/control results interpretable.

## 5) Control law and gain reasoning

For single-axis pitch regulation (wheel aligned with the controlled axis in repository demos):

\[
u = s_\tau (K_p\,\theta + K_d\,\dot\theta)
\]

where \(s_\tau\in\{-1,+1\}\) maps actuator sign convention (wheel torque to body reaction torque), with actuator saturation \(|u|\le u_{max}\).

Small-angle linearization around \(\theta=0\), \(\omega\approx 0\):

\[
I_{eq}\ddot\theta + K_d\dot\theta + K_p\theta = 0
\]

So the standard second-order mapping gives:

- \(\omega_n = \sqrt{K_p/I_{eq}}\)
- \(\zeta = K_d/(2\sqrt{I_{eq}K_p})\)

Gain selection practice:

1. pick target settling time / damping,
2. choose \(K_p\) from bandwidth limits,
3. choose \(K_d\) to hit \(\zeta\in[0.7,1.1]\),
4. verify actuator/speed margins against expected disturbances.

## 6) Stability discussion

Candidate Lyapunov form for the linearized axis:

\[
V = \frac12 I_{eq}\dot\theta^2 + \frac12 K_p\theta^2
\]

With ideal unsaturated PD control:

\[
\dot V = -K_d\dot\theta^2 \le 0
\]

Hence asymptotic damping in rate and bounded attitude response. Practical implementations deviate from this ideal due to saturation and unmodeled torques.

## 7) Failure modes to evaluate

1. **Wheel saturation** (torque or speed): loss of authority, larger settling times.
2. **Integrator step too large**: artificial energy growth / conservation drift.
3. **Euler-angle singularities** near pitch \(\pm 90^\circ\): use quaternion propagation for mission-like maneuvers.
4. **Inertia mismatch**: degraded damping and overshoot.
5. **Persistent disturbances** without momentum dumping: wheel momentum accumulation.

## 8) Validation checks

- Torque-free run: drift in \(\|H_h\|\) and total kinetic energy should remain small.
- Closed-loop run: attitude/rate converge and control effort remains within limits.
- Disturbance run: bounded transient and recovery after disturbance removal.
