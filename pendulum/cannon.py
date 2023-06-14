from pyglet import graphics, shapes
from pymunk import Space, Vec2d

from pendulum.munk.entities import Circle


class Aim:

    AIM_LINE_WIDTH = 2

    def __init__(self, initial_pos: Vec2d) -> None:
        self._initial_pos = initial_pos
        self._batch = graphics.Batch()

        self._line = shapes.Line(
            initial_pos.x,
            initial_pos.y,
            initial_pos.x,
            initial_pos.y,
            width=self.AIM_LINE_WIDTH,
            batch=self._batch,
        )

    def draw(self) -> None:
        self._batch.draw()

    def update(self, x: int, y: int) -> None:
        # FIXME: Line is a little janky
        self._line.anchor_position = (0, 0)
        self._line.position = (x, y)


class Cannon:
    """Draw an estimation of the path of a projectile."""

    SPEED_FACTOR = 20

    MASS = 1
    RADIUS = 5

    def __init__(self, space: Space) -> None:
        self._space = space

        self._initial_pos: Vec2d | None = None
        self._line: shapes.Line | None = None

        # TODO: Expire the circles after a certain amount of time
        self._projectiles: list[Circle] = []

        self._aim: Aim | None = None

    def start(self, x: int, y: int) -> None:
        self._initial_pos = Vec2d(x=x, y=y)
        self._aim = Aim(initial_pos=self._initial_pos)

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

        self._aim = None
        self._line = None
        self._initial_pos = None

    def aim(self, x: int, y: int) -> None:
        if not self._aim:
            return

        self._aim.update(x=x, y=y)

    def draw(self):
        if self._aim is not None:
            self._aim.draw()
