from pyglet import graphics, shapes
from pymunk import Space, Vec2d

from pendulum.munk.entities import Circle


class Projectile:
    """Draw an estimation of the path of a projectile."""

    MASS = 1
    RADIUS = 5

    AIM_LINE_WIDTH = 2
    PROJECTILE_SPEED = 20

    def __init__(self, space: Space):
        self.space = space

        self.click_vector: Vec2d | None = None
        self.click_line: shapes.Line | None = None
        self.click_circle: Circle | None = None

        self._batch = graphics.Batch()

        self._click_line = None

    def start(self, x: int, y: int) -> None:
        self.click_vector = Vec2d(x=x, y=y)
        self.click_line = shapes.Line(
            x, y, x, y, width=self.AIM_LINE_WIDTH, batch=self._batch
        )

    def update_aim(self, x: int, y: int) -> None:
        if not self.click_line:
            return

        # FIXME: Line is a little janky
        self.click_line.anchor_position = (0, 0)
        self.click_line.position = (x, y)

    def fire(self, x: int, y: int) -> None:
        if not self.click_vector:
            return

        diff_vector = self.click_vector - Vec2d(x=x, y=y)
        impulse = diff_vector * self.PROJECTILE_SPEED
        self.click_circle = Circle(
            space=self.space,
            mass=self.MASS,
            radius=self.RADIUS,
            initial_pos=self.click_vector,
        )
        self.click_circle.body.apply_impulse_at_local_point(impulse)
        self.click_line = None

    def draw(self):
        if self.click_line is not None:
            self._batch.draw()
