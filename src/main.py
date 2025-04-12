import numpy as np
import matplotlib.pyplot as plt


def ik(L1, L2, x, y):

    d = np.sqrt(x**2 + y**2)

    if d > (L1 + L2) or d < abs(L1 - L2):
        return None, None

    theta2 = np.arccos((L1**2 + L2**2 - d**2) / (2 * L1 * L2))

    theta1_alpha = np.arctan2(y, x)
    theta1_beta = np.arccos((L1**2 + d**2 - L2**2) / (2 * L1 * d))

    theta1 = theta1_alpha + theta1_beta

    return theta1, theta2


class RobotArm:
    def __init__(self, L1, L2, theta1, theta2, shoulder_joint, elbow_joint, effector):
        self.L1 = L1
        self.L2 = L2
        self.theta1 = theta1
        self.theta2 = theta2
        self.shoulder_joint = shoulder_joint
        self.elbow_joint = elbow_joint
        self.effector = effector

    def update_position(self, target_x, target_y):
        self.theta1, self.theta2 = ik(self.L1, self.L2, target_x, target_y)
        if self.theta1 is not None and self.theta2 is not None:
            self.elbow_joint = (
                self.shoulder_joint[0] + self.L1 * np.cos(self.theta1),
                self.shoulder_joint[1] + self.L1 * np.sin(self.theta1),
            )
            self.effector = (
                self.elbow_joint[0] - self.L2 * np.cos(self.theta1 + self.theta2),
                self.elbow_joint[1] - self.L2 * np.sin(self.theta1 + self.theta2),
            )


def plot_robot_arm(robot):

    plt.cla()
    plt.plot(
        [robot.shoulder_joint[0], robot.elbow_joint[0]],
        [robot.shoulder_joint[1], robot.elbow_joint[1]],
        "ro-",
    )
    plt.plot(
        [robot.elbow_joint[0], robot.effector[0]],
        [robot.elbow_joint[1], robot.effector[1]],
        "bo-",
    )
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    plt.grid()
    plt.draw()


def on_click(event):
    target_x, target_y = event.xdata, event.ydata
    robot.update_position(target_x, target_y)
    plot_robot_arm(robot)
    plt.plot(event.xdata, event.ydata, "go")


robot = RobotArm(1.0, 0.5, 45, 45, (0, 0), (1.0, 1.0), (1.5, 1.5))
plot_robot_arm(robot)

plt.gca().set_aspect("equal")
plt.connect("button_press_event", on_click)
plt.connect(
    "motion_notify_event",
    lambda event: (
        on_click(event) if event.button is not None and event.button == 1 else None
    ),
)

plt.show()
