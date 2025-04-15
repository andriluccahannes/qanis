import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc

# Lengths
l1 = 11.8
l2 = 8.6

# Inverse kinematics function
def ik(x, y):
    d_squared = x ** 2 + y ** 2
    cos_theta2 = (d_squared - l1 ** 2 - l2 ** 2) / -(2 * l1 * l2)
    cos_theta1 = (l1 ** 2 + d_squared - l2 ** 2) / (2 * l1 * np.sqrt(d_squared))
    print(cos_theta1, cos_theta2)
    theta2 = np.arccos(cos_theta2)
    theta1 = np.arctan2(y, x) + np.arccos(cos_theta1)
    return np.degrees(theta1), np.degrees(theta2)

# Test point
x, y = (- 5, 10)
theta1_deg, theta2_deg = ik(x, y)
theta1_rad = np.radians(theta1_deg)
theta2_rad = np.radians(theta2_deg)

# Joint positions
x1 = l1 * np.cos(theta1_rad)
y1 = l1 * np.sin(theta1_rad)
x2 = x1 + l2 * np.cos(theta1_rad + theta2_rad + np.pi)
y2 = y1 + l2 * np.sin(theta1_rad + theta2_rad + np.pi)

# Plot
fig, ax = plt.subplots(figsize=(8, 8))

# Plot arm links
ax.plot([0, x1], [0, y1], 'b-', lw=2, label="Link 1")
ax.plot([x1, x2], [y1, y2], 'g-', lw=2, label="Link 2")

# Target and End-Effector
ax.plot(x, y, 'ro', label="Target (x, y)")
ax.plot(x2, y2, 'go', label="End Effector")

# ---- Draw angle arcs ----

# θ1 arc at base
arc1 = Arc((0, 0), 2, 2, angle=0,
           theta1=0, theta2=theta1_deg, color='purple', label="Theta1")
ax.add_patch(arc1)

# θ2 arc at joint 1
# Vector A = link1, Vector B = link2 (reversed to show internal angle)
v1 = np.array([x1, y1])
v2 = np.array([x2 - x1, y2 - y1])
angle_between_links = np.arccos(
    np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
)
angle_between_links_deg = np.degrees(angle_between_links)

# Draw arc at the joint for theta2
arc2 = Arc((x1, y1), 2, 2, angle=np.degrees(theta1_rad),
           theta1=0, theta2=theta2_deg, color='orange', label="Theta2")
ax.add_patch(arc2)

# ---- Print calculated angles for verification ----
print(f"IK theta1 = {theta1_deg:.2f}°")
print(f"IK theta2 = {theta2_deg:.2f}°")
print(f"Angle between links (geometric) = {angle_between_links_deg:.2f}°")

# Plot setup
ax.set_xlim(-16, 16)
ax.set_ylim(0, 24)
ax.set_aspect('equal')
ax.grid(True)
ax.legend()
ax.set_title("2-Link Arm with Angle Arcs")

plt.show()
