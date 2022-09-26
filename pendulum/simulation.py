"""Simple Example Pymunk + Pyglet Application."""

import pyglet
import pymunk
from pymunk.pyglet_util import DrawOptions


class Circle:
    """Circle that sits on the end of the pendulum rod."""

    def __init__(
        self,
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


class Cart:
    """Cart that carries the Pendulum."""

    def __init__(
        self,
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


class Rod:
    """Main body of the Pendulum, connecting the Circle to the Cart."""

    def __init__(
        self,
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


space = pymunk.Space()
space.gravity = 0, 0

circle = Circle(mass=0.1, radius=15.0, initial_pos=(640, 400))
space.add(circle.body, circle.shape)

cart = Cart(mass=0.5, size=(100, 50), initial_pos=(640, 200))
space.add(cart.body, cart.shape)

rod = Rod(mass=0.05, a=cart.initial_pos, b=circle.initial_pos, radius=2.0)
space.add(rod.body, rod.shape)

joint_1 = pymunk.constraints.PivotJoint(
    circle.body, rod.body, circle.initial_pos
)
joint_1.collide_bodies = False

joint_2 = pymunk.constraints.PivotJoint(rod.body, cart.body, cart.initial_pos)
joint_2.collide_bodies = False

space.add(joint_1, joint_2)

window = pyglet.window.Window(1280, 720, "Inverted Pendulum.", resizable=False)
options = DrawOptions()


@window.event
def on_draw() -> None:
    """Screen Draw Event."""
    window.clear()
    space.debug_draw(options=options)


def update(dt: float) -> None:
    """Update PyMunk's Space state.

    :param float dt: Time between calls of `update`.
    """
    space.step(dt)


pyglet.clock.schedule_interval(update, interval=1.0 / 60)
