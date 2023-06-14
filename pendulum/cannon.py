from pyglet import graphics, shapes
from pymunk import Space, Vec2d

from pendulum.munk.entities import Circle


class Cannon:
    """Draw an estimation of the path of a projectile."""

    AIM_LINE_WIDTH = 2
    SPEED_FACTOR = 20

    MASS = 1
    RADIUS = 5

    def __init__(self, space: Space) -> None:
        self._space = space

        self._initial_pos: Vec2d | None = None
        self._line: shapes.Line | None = None

        # TODO: Expire the circles after a certain amount of time
        self._projectiles: list[Circle] = []

        self._batch = graphics.Batch()

    def start(self, x: int, y: int) -> None:
        self._initial_pos = Vec2d(x=x, y=y)
        self._line = shapes.Line(
            x, y, x, y, width=self.AIM_LINE_WIDTH, batch=self._batch
        )

    def fire(self, x: int, y: int) -> None:
        if not self._initial_pos:
            raise Exception("Cannon not started.")

        velocity = (self._initial_pos - Vec2d(x=x, y=y)) * self.SPEED_FACTOR

        projectile = Circle(
            space=self._space,
            mass=self.MASS,
            radius=self.RADIUS,
            initial_pos=self._initial_pos,
        )
        projectile.body.apply_impulse_at_local_point(velocity * self.MASS)
        self._projectiles.append(projectile)

        self._line = None
        self._initial_pos = None

    def aim(self, x: int, y: int) -> None:
        if not self._line:
            return

        # FIXME: Line is a little janky
        self._line.anchor_position = (0, 0)
        self._line.position = (x, y)

    def draw(self):
        if self._line is not None:
            self._batch.draw()
