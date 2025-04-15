import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider


class TwoLinkArm:
    def __init__(self, link_lengths=[1, 0.8]):
        self.l1 = link_lengths[0]  # Length of link 1
        self.l2 = link_lengths[1]  # Length of link 2

        # Initial joint angles
        self.theta1 = 0
        self.theta2 = 0

    def forward_kinematics(self, theta1, theta2):
        """Calculate end effector position given joint angles"""
        x1 = self.l1 * np.cos(theta1)
        y1 = self.l1 * np.sin(theta1)

        x2 = x1 + self.l2 * np.cos(theta1 + theta2)
        y2 = y1 + self.l2 * np.sin(theta1 + theta2)

        return [0, x1, x2], [0, y1, y2]

    def inverse_kinematics(self, x, y):
        """Calculate joint angles given end effector position"""
        # Distance from origin to end effector
        r = np.sqrt(x*2 + y*2)

        # Check if the point is reachable
        if r > (self.l1 + self.l2) or r < abs(self.l1 - self.l2):
            # Point is outside reachable workspace
            return None, None

        # Calculate theta2 using law of cosines
        cos_theta2 = (r*2 - self.l1 - self.l2*2) / (2 * self.l1 * self.l2)
        # Clamp to handle floating point errors
        cos_theta2 = max(-1, min(1, cos_theta2))

        # Two possible solutions: elbow up or elbow down
        theta2 = np.arccos(cos_theta2)  # Elbow up solution

        # Calculate theta1
        theta1 = np.arctan2(y, x) - np.arctan2(
            self.l2 * np.sin(theta2), self.l1 + self.l2 * np.cos(theta2)
        )

        return theta1, theta2


# Set up the figure for visualization
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect("equal")
ax.grid(True)
ax.set_title("2D Arm Inverse Kinematics")

# Create the arm
arm = TwoLinkArm()
(line,) = ax.plot([], [], "o-", lw=2)

# Initialize target point that can be dragged
(target,) = ax.plot([], [], "ro")
target_x, target_y = 1.0, 0.5


# Function to update the arm position
def update(frame):
    theta1, theta2 = arm.inverse_kinematics(target_x, target_y)

    if theta1 is not None and theta2 is not None:
        arm.theta1 = theta1
        arm.theta2 = theta2
        x, y = arm.forward_kinematics(theta1, theta2)
        line.set_data(x, y)

    target.set_data([target_x], [target_y])
    return line, target


# Function to handle mouse clicks
def on_click(event):
    global target_x, target_y
    if event.inaxes == ax:
        target_x, target_y = event.xdata, event.ydata
        update(0)
        fig.canvas.draw_idle()


# Connect the click event
fig.canvas.mpl_connect("button_press_event", on_click)
fig.canvas.mpl_connect(
    "motion_notify_event",
    lambda event: (
        on_click(event) if event.button is not None and event.button == 1 else None
    ),
)

# Initial position
update(0)

plt.show()