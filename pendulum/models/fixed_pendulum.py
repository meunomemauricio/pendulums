"""PyMunk simulation of a Pendulum attached to a fixed point."""
import pymunk
from pyglet import clock, window
from pyglet.window import key
from pymunk import Vec2d
from pymunk.pyglet_util import DrawOptions

from pendulum import settings as sett
from pendulum.models.entities import Circle, Fixed
from pendulum.models.utils import FPSDisplay


class FixedPendulum(window.Window):

    CAPTION = "PyMunk Fixed Pendulum Simulation"

    #: Distance between the rail endings and the screen width
    RAIL_OFFSET = 50  # mm

    def __init__(
        self,
        width: int = sett.WIDTH,
        height: int = sett.HEIGHT,
        caption: str = CAPTION,
    ):
        super().__init__(width=width, height=height, caption=caption)

        self.space = pymunk.Space()
        self.space.gravity = sett.GRAVITY

        self._create_entities()
        self._create_constraints()

        self.draw_options = DrawOptions()
        self.fps_display = FPSDisplay(window=self)

        clock.schedule_interval(self.update, interval=sett.INTERVAL)

        self.keyboard = key.KeyStateHandler()
        self.push_handlers(self.keyboard)

    def _create_entities(self) -> None:
        """Create the entities that form the Pendulum."""
        self.circle = Circle(
            space=self.space, mass=0.100, radius=10.0, initial_pos=(640, 50)
        )

        self.fixed = Fixed(space=self.space, pos=(640, 360))

    def _create_constraints(self) -> None:
        """Create the constraints between the Entities."""
        rod_joint = pymunk.constraints.PinJoint(
            a=self.fixed.body,
            b=self.circle.body,
        )

        self.space.add(rod_joint)

    @property
    def _rod_vector(self) -> Vec2d:
        """Vector from the Fixed point to the center of the Circle."""
        return self.fixed.body.position - self.circle.body.position

    def _accelerate_cw(self):
        """Apply a Clockwise force to the pendulum."""
        self.circle.accelerate(dir=self._rod_vector.rotated_degrees(90))

    def _accelerate_ccw(self):
        """Apply a Counter Clockwise force to the pendulum."""
        self.circle.accelerate(dir=self._rod_vector.rotated_degrees(-90))

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
            self._accelerate_cw()
        elif self.keyboard[key.RIGHT]:
            self._accelerate_ccw()

        self.space.step(sett.INTERVAL)
