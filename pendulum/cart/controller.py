import numpy as np
from pymunk import Vec2d

import pendulum.settings as sett


class LQRController:

    K_MATRIX = np.loadtxt("pendulum/cart/lqr_params.csv")

    SET_POINT = np.array([0.0, 0.0, 180, 0.0])

    def __init__(self, is_active: bool) -> None:
        self.is_active = is_active

    def step(self, x, v, theta, omega) -> Vec2d:
        """Return the impulse to apply to the cart.

        Force should be in mN.
        """
        if not self.is_active:
            return Vec2d(0.0, 0.0)

        state = np.array([x, v, theta, omega])
        x_impulse = -self.K_MATRIX @ (state - self.SET_POINT)
        x_impulse = x_impulse * sett.SIMULATION_STEP
        return Vec2d(x_impulse, 0.0)
