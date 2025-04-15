import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
x_off = 0.0
x_fore = 0.1  # 10 cm forward span during stance phase
x_hind = 0.08  # 8 cm backward span during swing phase
z_off = 0.0
z_ztop = 0.05  # 5 cm peak height
z_zbtm = 0.01  # 1 cm ground clearance

# Phase from 0 to 2π
phi = np.linspace(0, 2 * np.pi, 100)

# x-coordinate
x = np.where(
    (phi > np.pi / 2) & (phi <= 3 * np.pi / 2),
    x_off - x_fore * np.cos(phi),
    x_off - x_hind * np.cos(phi)
)

# z-coordinate
z = np.where(
    (phi > 0) & (phi <= np.pi),
    z_off + z_ztop * np.sin(phi),
    z_off + z_zbtm * np.sin(phi)
)

print(x)
# Set up the plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, z, label="Fußtrajektorie", color='royalblue')
point, = ax.plot([], [], 'ro', label='aktueller Punkt')
ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
ax.axvline(0, color='gray', linestyle='--', linewidth=0.5)
ax.set_title("Fußtrajektorie in der X-Z-Ebene (Animation)")
ax.set_xlabel("X (Vor-Zurück)")
ax.set_ylabel("Z (Höhe)")
ax.grid(True)
ax.legend()
ax.axis('equal')
#ax.set_xlim(np.min(x) - 0.01, np.max(x) + 0.01)
#ax.set_ylim(np.min(z) - 0.01, np.max(z) + 0.01)
plt.tight_layout()

# Update function for animation
def update(frame):
    point.set_data([x[frame]], [z[frame]])
    return point,

# Create animation
ani = FuncAnimation(fig, update, frames=len(phi), interval=20, blit=True)

plt.show()
