"""PyMunk simulation of a Pendulum attached to a moving Cart."""
import pymunk
from pyglet import window
from pyglet.window import key
from pymunk import Vec2d

from pendulum import settings as sett
from pendulum.cart.parameters import Parameters
from pendulum.munk.entities import Cart, Circle
from pendulum.simulation import BaseSimulation


class CartPendulumModel:
    """Cart Pendulum PyMunk Model."""

    #: Distance between the rail endings and the screen width
    RAIL_OFFSET = 50  # mm

    #: Cart Impulse
    IMPULSE = sett.SIMULATION_STEP * 3000  # mN

    def __init__(
        self,
        space: pymunk.Space,
        window: window.Window,
        params: Parameters,
    ):
        self.space = space
        self.window = window
        self.params = params

        self._create_entities()
        self._create_constraints()

        self._last_angle = self.params.angle

    def _create_entities(self) -> None:
        cart_pos_x = (self.window.width / 2) + self.params.cart_x
        cart_pos = Vec2d(cart_pos_x, 360)
        self.cart = Cart(
            space=self.space,
            mass=self.params.cart_mass,
            size=self.params.cart_size,
            initial_pos=cart_pos,
        )
        self.cart.body.velocity = Vec2d(self.params.cart_v, 0)

        self.circle = Circle(
            space=self.space,
            mass=self.params.circle_mass,
            radius=self.params.circle_radius,
            initial_pos=self._get_circle_initial_pos(cart_pos=cart_pos),
        )

    def _get_circle_initial_pos(self, cart_pos: Vec2d) -> Vec2d:
        resting_pendulum = Vec2d(0, -self.params.circle_length)
        return cart_pos + resting_pendulum.rotated_degrees(self.params.angle)

    def _create_constraints(self) -> None:
        rod_joint = pymunk.constraints.PinJoint(
            a=self.cart.body,
            b=self.circle.body,
        )

        rail_x_1 = self.RAIL_OFFSET
        rail_x_2 = self.window.width - self.RAIL_OFFSET
        rail_joint = pymunk.constraints.GrooveJoint(
            a=self.space.static_body,
            b=self.cart.body,
            groove_a=(rail_x_1, self.cart.initial_pos[1]),
            groove_b=(rail_x_2, self.cart.initial_pos[1]),
            anchor_b=(0, 0),
        )

        # Lock rotation of the cart
        gear = pymunk.GearJoint(
            self.space.static_body, self.cart.body, 0.0, 1.0
        )
        self.space.add(rod_joint, rail_joint, gear)

        # Simulate linear friciton by creating a PivotJoint, disabling
        # correction and setting a maximum force. (Based on tank.py example)
        if self.params.cart_friction:
            self.friction_joint = pymunk.PivotJoint(
                self.space.static_body, self.cart.body, (0, 0), (0, 0)
            )
            self.friction_joint.max_bias = 0
            self.friction_joint.max_force = (
                self.params.cart_friction * sett.SIMULATION_STEP
            )

            self.space.add(self.friction_joint)

    @property
    def cart_friction(self) -> float:
        """Friction Force applied by the joint on the cart."""
        if not self.params.cart_friction:
            return 0.0

        return self.friction_joint.impulse / sett.SIMULATION_STEP

    @property
    def angle(self) -> float:
        """Angle (deg) between the Pendulum and the resting location."""
        return -self.vector.get_angle_degrees_between(Vec2d(0, -1))

    @property
    def angular_velocity(self) -> float:
        """Pendulum Angular Velocity (dev/s)."""
        ang_vel = self.angle - self._last_angle
        self._last_angle = self.angle
        return ang_vel

    @property
    def cart_x(self) -> float:
        """Cart position related to the center of the rails.

        Assume the rails are centered in the middle of the screen.
        """
        return self.cart.body.position.x - (self.window.width / 2)

    @property
    def cart_velocity(self) -> float:
        """Linear Velocity of the Center of Mass of the Cart in the X axis."""
        return self.cart.body.velocity.dot(Vec2d(1, 0))

    @property
    def vector(self) -> Vec2d:
        """Pendulum Vector, from Fixed point to the center of the Cart."""
        return self.circle.body.position - self.cart.body.position

    def accelerate_left(self) -> None:
        impulse = Vec2d(-self.IMPULSE, 0)
        self.cart.body.apply_impulse_at_local_point(impulse=impulse)

    def accelerate_right(self) -> None:
        impulse = Vec2d(self.IMPULSE, 0)
        self.cart.body.apply_impulse_at_local_point(impulse=impulse)


class CartPendulumSim(BaseSimulation):
    """Application simulating a Cart Pendulum."""

    CAPTION = "PyMunk Pendulum on a Cart Simulation"

    REC_PREFIX = "cart"
    REC_FIELDS = (
        "angle",
        "angular_velocity",
        "cart_friction",
        "cart_x",
        "cart_velocity",
        "input_left",
        "input_right",
    )

    def __init__(self, record: bool, params: Parameters):
        super().__init__(record=record)

        self.model = CartPendulumModel(
            space=self.space, window=self, params=params
        )

    def update(self, dt: float) -> None:
        """Update PyMunk's Space state.

        :param float dt: Time between calls of `update`.
        """
        self._handle_input()
        self.space.step(sett.SIMULATION_STEP)
        if self.recorder:
            self.recorder.insert(
                angle=self.model.angle,
                angular_velocity=self.model.angular_velocity,
                cart_friction=self.model.cart_friction,
                cart_velocity=self.model.cart_velocity,
                cart_x=self.model.cart_x,
                input_left=self.keyboard[key.LEFT],
                input_right=self.keyboard[key.RIGHT],
            )

    def _handle_input(self) -> None:
        if self.keyboard[key.LEFT]:
            self.model.accelerate_left()
        elif self.keyboard[key.RIGHT]:
            self.model.accelerate_right()
