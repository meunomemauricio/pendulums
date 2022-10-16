"""Simple Example Pymunk + Pyglet Application."""
import pymunk
from pyglet import clock, window
from pyglet.window import key
from pymunk.pyglet_util import DrawOptions

from pendulum import settings
from pendulum.utils import FPSDisplay


class Circle:
    """Circle that sits on the end of the pendulum rod."""

    def __init__(
        self,
        space: pymunk.Space,
        mass: float,
        radius: float,
        initial_pos: tuple[float, float] = (0, 0),
    ):
        self.mass = mass
        self.radius = radius
        self.initial_pos = initial_pos

        self.moment = pymunk.moment_for_circle(
            mass=self.mass, inner_radius=0, outer_radius=self.radius
        )
        self.body = pymunk.Body(mass=self.mass, moment=self.moment)
        self.body.position = initial_pos

        self.shape = pymunk.Circle(body=self.body, radius=self.radius)

        space.add(self.body, self.shape)


class Cart:
    """Cart that carries the Pendulum."""

    #: Cart Acceleration
    CART_ACCEL = 5000  # mm/s²

    def __init__(
        self,
        space: pymunk.Space,
        mass: float,
        size: tuple[float, float],
        initial_pos: tuple[float, float] = (0, 0),
    ):
        self.mass = mass
        self.size = size
        self.initial_pos = initial_pos

        self.moment = pymunk.moment_for_box(mass=self.mass, size=self.size)
        self.body = pymunk.Body(mass=self.mass, moment=self.moment)
        self.body.position = initial_pos

        self.shape = pymunk.Poly.create_box(body=self.body, size=self.size)

        space.add(self.body, self.shape)

    def accelerate_left(self) -> None:
        """Apply lateral acceleration to the left."""
        force = self.mass * self.CART_ACCEL * -1
        self.body.apply_force_at_local_point(force=(force, 0))

    def accelerate_right(self) -> None:
        """Apply lateral acceleration to the right."""
        force = self.mass * self.CART_ACCEL
        self.body.apply_force_at_local_point(force=(force, 0))


class CartPendulum(window.Window):

    CAPTION = "Inverted Pendulum Simulation"

    #: Distance between the rail endings and the screen width
    RAIL_OFFSET = 50  # mm

    def __init__(
        self,
        width: int = settings.WIDTH,
        height: int = settings.HEIGHT,
        caption: str = CAPTION,
    ):
        super().__init__(width=width, height=height, caption=caption)

        self.space = pymunk.Space()
        self.space.gravity = settings.GRAVITY

        self._create_entities()
        self._create_constraints()

        self.draw_options = DrawOptions()
        self.fps_display = FPSDisplay(window=self)

        clock.schedule_interval(self.update, interval=self.INTERVAL)

        self.keyboard = key.KeyStateHandler()
        self.push_handlers(self.keyboard)

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
        rail_x_2 = self.width - self.RAIL_OFFSET
        rail_joint = pymunk.constraints.GrooveJoint(
            a=self.space.static_body,
            b=self.cart.body,
            groove_a=(rail_x_1, self.cart.initial_pos[1]),
            groove_b=(rail_x_2, self.cart.initial_pos[1]),
            anchor_b=(0, 0),
        )

        self.space.add(rod_joint, rail_joint)

    def on_draw(self) -> None:
        """Screen Draw Event."""
        self.clear()
        self.space.debug_draw(options=self.draw_options)
        self.fps_display.draw()

    def update(self, dt: float) -> None:
        """Update PyMunk's Space state.

        :param float dt: Time between calls of `update`.
        """
        if self.keyboard[key.LEFT]:
            self.cart.accelerate_left()
        elif self.keyboard[key.RIGHT]:
            self.cart.accelerate_right()

        self.space.step(self.INTERVAL)
