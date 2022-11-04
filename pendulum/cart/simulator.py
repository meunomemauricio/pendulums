"""PyMunk simulation of a Pendulum attached to a moving Cart."""
import pymunk
from pyglet import clock, window
from pyglet.window import key
from pymunk import Vec2d
from pymunk.pyglet_util import DrawOptions

from pendulum import settings as sett
from pendulum.munk.entities import Cart, Circle
from pendulum.munk.utils import FPSDisplay
from pendulum.recorder import Recorder


class CartPendulumModel:
    """Cart Pendulum PyMunk Model."""

    #: Distance between the rail endings and the screen width
    RAIL_OFFSET = 50  # mm

    #: Cart Force
    FORCE = 10  # mN

    def __init__(self, space: pymunk.Space, window: window.Window):
        self.space = space
        self.window = window

        self._create_entities()
        self._create_constraints()

    def _create_entities(self) -> None:
        """Create the entities that form the Pendulum."""
        self.cart = Cart(
            space=self.space,
            mass=0.200,
            size=(50, 25),
            initial_pos=(640, 360),
        )
        self.circle = Circle(
            space=self.space, mass=0.100, radius=10.0, initial_pos=(640, 650)
        )

    def _create_constraints(self) -> None:
        """Create the constraints between the Entities."""
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

        self.space.add(rod_joint, rail_joint)

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
    def vector(self) -> Vec2d:
        """Pendulum Vector, from Fixed point to the center of the Cart."""
        return self.circle.body.position - self.cart.body.position

    def accelerate_left(self) -> None:
        """Apply lateral acceleration to the left."""
        impulse = Vec2d(-self.FORCE, 0)
        self.cart.body.apply_impulse_at_local_point(impulse=impulse)

    def accelerate_right(self) -> None:
        """Apply lateral acceleration to the right."""
        impulse = Vec2d(self.FORCE, 0)
        self.cart.body.apply_impulse_at_local_point(impulse=impulse)


class CartPendulumSim(window.Window):
    """Application simulating a Cart Pendulum."""

    CAPTION = "PyMunk Pendulum on a Cart Simulation"

    #: Recorder fields
    REC_FIELDS = (
        "angle",
        "cart_x",
        "input_left",
        "input_right",
    )

    def __init__(
        self,
        width: int = sett.WIDTH,
        height: int = sett.HEIGHT,
        caption: str = CAPTION,
    ):
        super().__init__(width=width, height=height, caption=caption)

        self.space = pymunk.Space()
        self.space.gravity = sett.GRAVITY

        self.draw_options = DrawOptions()
        self.fps_display = FPSDisplay(window=self)
        self.keyboard = key.KeyStateHandler()
        self.model = CartPendulumModel(space=self.space, window=self)
        self.recorder = Recorder(fields=self.REC_FIELDS, prefix="cart")

        self.push_handlers(self.keyboard)

        clock.schedule_interval(self.update, interval=sett.INTERVAL)

    def on_draw(self) -> None:
        """Screen Draw Event."""
        self.clear()
        self.space.debug_draw(options=self.draw_options)
        self.fps_display.draw()

    def update(self, dt: float) -> None:
        """Update PyMunk's Space state.

        :param float dt: Time between calls of `update`.
        """
        self.handle_input()
        self.space.step(sett.INTERVAL)
        self.recorder.insert(
            angle=self.model.angle,
            cart_x=self.model.cart_x,
            input_left=self.keyboard[key.LEFT],
            input_right=self.keyboard[key.RIGHT],
        )

    def _handle_input(self) -> None:
        """Handle User Input."""
        if self.keyboard[key.LEFT]:
            self.model.accelerate_left()
        elif self.keyboard[key.RIGHT]:
            self.model.accelerate_right()
