"""Simple Example Pymunk + Pyglet Application."""

import pyglet
import pymunk
from pymunk.pyglet_util import DrawOptions


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


class Rod:
    """Main body of the Pendulum, connecting the Circle to the Cart."""

    def __init__(
        self,
        space: pymunk.Space,
        mass: float,
        a: tuple[float, float],
        b: tuple[float, float],
        radius: float,
    ):
        self.mass = mass
        self.a = a
        self.b = b
        self.radius = radius

        self.moment = pymunk.moment_for_segment(
            mass=mass, a=a, b=b, radius=radius
        )
        self.body = pymunk.Body(mass=mass, moment=self.moment)

        self.shape = pymunk.Segment(body=self.body, a=a, b=b, radius=radius)

        space.add(self.body, self.shape)


class FPSDisplay(pyglet.window.FPSDisplay):
    """Custom FPS Display."""

    FONT_SIZE = 12
    FONT_COLOR = 255, 0, 0, 200

    def __init__(self, window: pyglet.window.Window):
        super().__init__(window=window)

        self.label = pyglet.text.Label(
            font_size=self.FONT_SIZE,
            x=self.window.width - self.FONT_SIZE * 8,
            y=self.window.height - self.FONT_SIZE - 1,
            color=self.FONT_COLOR,
            bold=True,
        )

    def set_fps(self, fps):
        """Override FPS text."""
        self.label.text = f"FPS: {fps:0.2f}"


class SimulationWindow(pyglet.window.Window):

    WIDTH = 1280
    HEIGHT = 720
    CAPTION = "Inverted Pendulum Simulation"

    FPS_FONT_SIZE = 12
    FPS_FONT_COLOR = 255, 0, 0, 200

    #: Distance between the rail endings and the screen width
    RAIL_OFFSET = 50

    def __init__(
        self, width: int = WIDTH, height: int = HEIGHT, caption: str = CAPTION
    ):
        super().__init__(width=width, height=height, caption=caption)

        self.space = pymunk.Space()
        self.space.gravity = 0, 0

        self._create_entities()
        self._create_constraints()

        self.draw_options = DrawOptions()
        self.fps_display = FPSDisplay(window=self)

        pyglet.clock.schedule_interval(self.update, interval=1.0 / 60)

    def _create_entities(self) -> None:
        """Create the entities that form the Pendulum."""
        self.circle = Circle(
            space=self.space, mass=0.1, radius=15.0, initial_pos=(640, 400)
        )
        self.cart = Cart(
            space=self.space, mass=0.5, size=(100, 50), initial_pos=(640, 200)
        )
        self.rod = Rod(
            space=self.space,
            mass=0.05,
            a=self.cart.initial_pos,
            b=self.circle.initial_pos,
            radius=2.0,
        )

    def _create_constraints(self) -> None:
        """Create the constraints between the Entities."""
        joint_1 = pymunk.constraints.PivotJoint(
            self.circle.body, self.rod.body, self.circle.initial_pos
        )
        joint_1.collide_bodies = False

        joint_2 = pymunk.constraints.PivotJoint(
            self.rod.body, self.cart.body, self.cart.initial_pos
        )
        joint_2.collide_bodies = False

        rail_x_1 = self.RAIL_OFFSET
        rail_x_2 = self.width - self.RAIL_OFFSET
        rail_joint = pymunk.constraints.GrooveJoint(
            a=self.space.static_body,
            b=self.cart.body,
            groove_a=(rail_x_1, self.cart.initial_pos[1]),
            groove_b=(rail_x_2, self.cart.initial_pos[1]),
            anchor_b=(0, 0),
        )

        self.space.add(joint_1, joint_2, rail_joint)

    def on_draw(self) -> None:
        """Screen Draw Event."""
        self.clear()
        self.space.debug_draw(options=self.draw_options)
        self.fps_display.draw()

    def update(self, dt: float) -> None:
        """Update PyMunk's Space state.

        :param float dt: Time between calls of `update`.
        """
        self.space.step(dt)
