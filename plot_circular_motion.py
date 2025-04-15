import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class DynamicalSystem:
    def __init__(self, initial_state, dt=0.01):
        self.state = np.array(initial_state, dtype=float)
        self.dt = dt
        self.t = 0

    def step(self):
        dx = self.derivatives(self.state, self.t)
        self.state += self.dt * dx
        self.t += self.dt
        return self.state

    def derivatives(self, state, t):
        raise NotImplementedError("Override this in subclasses")

class SimpleOscillator(DynamicalSystem):
    def __init__(self, omega=1.0, **kwargs):
        self.omega = omega
        super().__init__(**kwargs)

    def derivatives(self, state, t):
        x, y = state
        dx = -self.omega * y
        dy = self.omega * x
        return np.array([dx, dy])

def run_simulation(system, steps=1000):
    states = []
    for _ in range(steps):
        states.append(system.step().copy())
    return np.array(states)

def animate(states, dt):
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    xdata, ydata = [], []
    time = np.linspace(0, dt * len(states), len(states))

    def init():
        for ax in axs:
            ax.clear()
        axs[0].set_title("x(t)")
        axs[1].set_title("y(t)")
        axs[2].set_title("Phase space (x vs y)")
        return axs

    def update(frame):
        x, y = states[frame]
        xdata.append(x)
        ydata.append(y)

        axs[0].cla()
        axs[0].plot(time[:frame], [s[0] for s in states[:frame]])
        axs[0].set_title("x(t)")

        axs[1].cla()
        axs[1].plot(time[:frame], [s[1] for s in states[:frame]])
        axs[1].set_title("y(t)")

        axs[2].cla()
        axs[2].plot(xdata, ydata)
        axs[2].set_title("x vs y")

        return axs

    ani = FuncAnimation(fig, update, frames=len(states), init_func=init, blit=False, interval=10)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    osc = SimpleOscillator(omega=2.0, initial_state=[1.0, 0.0])
    states = run_simulation(osc, steps=1000)
    animate(states, dt=osc.dt)
