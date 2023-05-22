"""PyMunk simulation of a Pendulum attached to a moving Cart."""
import pymunk
from pyglet import window
from pyglet.window import key
from pymunk import Vec2d

from pendulum import settings as sett
from pendulum.cart.initial_conditions import InitialConditions
from pendulum.munk.entities import Cart, Circle
from pendulum.simulation import BaseSimulation


class CartPendulumModel:
    """Cart Pendulum PyMunk Model."""

    #: Distance between the rail endings and the screen width
    RAIL_OFFSET = 50  # mm

    #: Cart Impulse
    IMPULSE = sett.INTERVAL * 3000  # mN

    #: Cart Friction Impulse
    CART_FRICTION = sett.INTERVAL * 60000  # mN

    def __init__(
        self,
        space: pymunk.Space,
        window: window.Window,
        initial: InitialConditions,
    ):
        self.space = space
        self.window = window
        self.initial = initial

        self._create_entities()
        self._create_constraints()

    def _create_entities(self) -> None:
        self.cart = Cart(
            space=self.space,
            mass=0.200,
            size=(50, 25),
            initial_pos=(640, 360),
        )
        self.circle = Circle(
            space=self.space, mass=0.005, radius=10.0, initial_pos=(640, 50)
        )

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

        # Simulate linear friciton by creating a PivotJoint, disabling
        # correction and setting a maximum force. (Based on tank.py example)
        self.friction_joint = pymunk.PivotJoint(
            self.space.static_body, self.cart.body, (0, 0), (0, 0)
        )
        self.friction_joint.max_bias = 0
        self.friction_joint.max_force = self.CART_FRICTION

        # Lock rotation of the cart
        gear = pymunk.GearJoint(
            self.space.static_body, self.cart.body, 0.0, 1.0
        )

        self.space.add(rod_joint, rail_joint, self.friction_joint, gear)

    @property
    def cart_friction(self) -> float:
        """Friction Force applied by the joint on the cart."""
        return self.friction_joint.impulse / sett.INTERVAL

    @property
    def angle(self) -> float:
        """Angle (deg) between the Pendulum and the resting location."""
        return self.vector.get_angle_degrees_between(Vec2d(0, -1))

    @property
    def cart_x(self) -> float:
        """Cart position related to the center of the rails.

        Assume the rails are centered in the middle of the screen.
        """
        return self.cart.body.position.x - (self.window.width / 2)

    @property
    def cart_velocity(self) -> float:
        """Linear Velocity of the Center of Mass of the Cart."""
        return self.cart.body.velocity.length

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
        "cart_friction",
        "cart_x",
        "cart_velocity",
        "input_left",
        "input_right",
    )

    def __init__(self, record: bool, initial: InitialConditions):
        super().__init__(record=record)

        self.model = CartPendulumModel(
            space=self.space, window=self, initial=initial
        )

    def update(self, dt: float) -> None:
        """Update PyMunk's Space state.

        :param float dt: Time between calls of `update`.
        """
        self._handle_input()
        self.space.step(sett.INTERVAL)
        if self.recorder:
            self.recorder.insert(
                angle=self.model.angle,
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
