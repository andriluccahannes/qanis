import numpy as np

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

class HopfOscillator(DynamicalSystem):
    def __init__(self, alpha=1.0, mu=1.0, omega=2.0, **kwargs):
        self.alpha = alpha
        self.mu = mu
        self.omega = omega
        super().__init__(**kwargs)

    def derivatives(self, state, t):
        x, y = state
        r_squared = x**2 + y**2
        dx = self.alpha * (self.mu - r_squared) * x - self.omega * y
        dy = self.alpha * (self.mu - r_squared) * y + self.omega * x
        return np.array([dx, dy])
