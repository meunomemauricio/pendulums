"""Main Entities used by PyMunk simulations.

Entities are an abstraction comprised of a PyMunk body and shape.
"""
import pymunk


class Circle:
    """Circle that sits on the end of the pendulum rod."""

    def __init__(
        self,
        space: pymunk.Space,
        mass: float,
        radius: float,
        initial_pos: pymunk.Vec2d = pymunk.Vec2d(0, 0),
        color: tuple[int, int, int, int] | None = None,
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
        if color:
            self.shape.color = color

        space.add(self.body, self.shape)


class Cart:
    """Cart that carries the Pendulum."""

    def __init__(
        self,
        space: pymunk.Space,
        mass: float,
        size: tuple[float, float],
        initial_pos: pymunk.Vec2d = pymunk.Vec2d(0, 0),
    ):
        self.mass = mass
        self.size = size
        self.initial_pos = initial_pos

        self.moment = pymunk.moment_for_box(mass=self.mass, size=self.size)
        self.body = pymunk.Body(mass=self.mass, moment=self.moment)
        self.body.position = initial_pos

        self.shape = pymunk.Poly.create_box(body=self.body, size=self.size)

        space.add(self.body, self.shape)


class Fixed:
    """Fixed point in the space."""

    def __init__(
        self,
        space: pymunk.Space,
        pos: tuple[float, float] = (0, 0),
    ):
        self.pos = pos

        self.body: pymunk.Body = space.static_body
        self.body.position = pos
