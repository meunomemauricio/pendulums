"""Main Entities used by PyMunk simulations.

Entities are an abstraction comprised of a PyMunk body and shape.
"""
import pymunk


class Circle:
    """Circle that sits on the end of the pendulum rod."""

    ACCELERATION = 3000  # mm/s²

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

    def accelerate_left(self) -> None:
        """Apply lateral acceleration to the left."""
        force = self.mass * self.ACCELERATION * -1
        self.body.apply_force_at_local_point(force=(force, 0))

    def accelerate_right(self) -> None:
        """Apply lateral acceleration to the right."""
        force = self.mass * self.ACCELERATION
        self.body.apply_force_at_local_point(force=(force, 0))


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
