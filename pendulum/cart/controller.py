import numpy as np
from pymunk import Vec2d

import pendulum.settings as sett


class LQRController:

    K_MATRIX = np.loadtxt("pendulum/cart/lqr_params.csv")

    MAX_FORCE = 500  # nN

    SET_POINT = np.array([0.0, 0.0, 180, 0.0])

    def step(self, x, v, theta, omega) -> Vec2d:
        """Return the impulse to apply to the cart.

        Force should be in mN.
        """
        state = np.array([x, v, theta, omega])
        x_impulse = -self.K_MATRIX @ (state - self.SET_POINT)
        x_impulse = x_impulse * sett.SIMULATION_STEP
        x_impulse = np.clip(x_impulse, -self.MAX_FORCE, self.MAX_FORCE)
        print(state, state - self.SET_POINT, x_impulse)
        return Vec2d(x_impulse, 0.0)
