from pyglet import graphics, shapes
from pymunk import Space, Vec2d

from pendulum import settings as sett
from pendulum.munk.entities import Circle


class Aim:
    """Estimate the trajectory of a projectile and draw a path."""

    SPEED_FACTOR = 5  # Factor relating length traveled by mouse to speed.

    PATH_DOTS = 50  # How many dots to draw for the trajectory.

    DOT_COLOR = (255, 255, 0, 200)
    DOT_RADIUS = 5

    def __init__(self, x: int, y: int) -> None:
        self.initial_pos = Vec2d(x=x, y=y)

        self.velocity = Vec2d(0, 0)

        self._batch = graphics.Batch()
        self._dots = self._create_dots()

    def _create_dots(self) -> list[shapes.Circle]:
        dots = []
        for _ in range(self.PATH_DOTS):
            dot = shapes.Circle(
                x=self.initial_pos.x,
                y=self.initial_pos.y,
                radius=self.DOT_RADIUS,
                color=self.DOT_COLOR,
                batch=self._batch,
            )
            dots.append(dot)

        return dots

    def draw(self) -> None:
        self._batch.draw()

    def update(self, x: int, y: int) -> None:
        cur_pos = Vec2d(x=x, y=y)
        self.velocity = (self.initial_pos - cur_pos) * self.SPEED_FACTOR
        self._estimate_trajectory()

    def _estimate_trajectory(self) -> None:
        """Estimate the trajectory of the projectile."""
        x_o, y_o = self.initial_pos.x, self.initial_pos.y
        v_xo, v_yo = self.velocity.x, self.velocity.y
        half_g = 0.5 * sett.GRAVITY[1]  # g already negative

        for n in range(self.PATH_DOTS):
            t_step = n * sett.INTERVAL
            x = x_o + v_xo * t_step
            y = y_o + v_yo * t_step + half_g * (t_step**2)

            self._dots[n].position = Vec2d(x=x, y=y)


class Cannon:
    """Draw an estimation of the path of a projectile."""

    PROJECTILE_MASS = 0.05
    PROJECTILE_RADIUS = 5

    def __init__(self, space: Space) -> None:
        self._space = space

        # TODO: Expire the circles after a certain amount of time
        self._projectiles: list[Circle] = []

        self._aim: Aim | None = None

    def start(self, x: int, y: int) -> None:
        self._aim = Aim(x=x, y=y)

    def aim(self, x: int, y: int) -> None:
        if not self._aim:
            raise Exception("Cannon not started.")

        self._aim.update(x=x, y=y)

    def fire(self, x: int, y: int) -> None:
        if not self._aim:
            raise Exception("Cannon not started.")

        projectile = Circle(
            space=self._space,
            mass=self.PROJECTILE_MASS,
            radius=self.PROJECTILE_RADIUS,
            initial_pos=self._aim.initial_pos,
            color=(255, 0, 0, 255),
        )
        projectile.body.velocity = self._aim.velocity
        self._projectiles.append(projectile)

        self._aim = None

    def draw(self):
        if self._aim is not None:
            self._aim.draw()
