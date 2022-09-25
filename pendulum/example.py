"""Simple Example Pymunk + Pyglet Application."""

import pyglet
import pymunk
from pymunk.pyglet_util import DrawOptions

space = pymunk.Space()
space.gravity = 0, -1000

body = pymunk.Body(mass=1, moment=1666)
body.position = 640, 700  # x, y

poly = pymunk.Poly.create_box(body=body, size=(50, 50))

space.add(body, poly)

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
