"""PyMunk simulation of a Pendulum attached to a fixed point."""
import pymunk
from pyglet import clock, window
from pyglet.window import key
from pymunk import Vec2d
from pymunk.pyglet_util import DrawOptions

from pendulum import settings as sett
from pendulum.munk.entities import Circle, Fixed
from pendulum.munk.utils import FPSDisplay
from pendulum.recorder import Recorder


class FixedPendulumModel:
    """Fixed Pendulum PyMunk Model."""

    FORCE = 10  # mN

    def __init__(self, space: pymunk.Space, window: window.Window):
        self.space = space
        self.window = window

        self._create_entities()
        self._create_constraints()

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
    def angle(self) -> float:
        """Angle (deg) between the Pendulum and the resting location."""
        return self.vector.get_angle_degrees_between(Vec2d(0, -1))

    @property
    def vector(self) -> Vec2d:
        """Pendulum Vector, from Fixed point to the center of the Circle."""
        return self.circle.body.position - self.fixed.body.position

    def accelerate(self, direction: Vec2d):
        """Apply acceleration in the direction `dir`."""
        impulse = self.FORCE * direction.normalized()
        self.circle.body.apply_impulse_at_local_point(impulse=impulse)


class FixedPendulumSim(window.Window):

    CAPTION = "PyMunk Fixed Pendulum Simulation"

    #: Recorder fields
    REC_FIELDS = (
        "angle",
        "input_left",
        "input_right",
    )

    def __init__(
        self,
        width: int = sett.WIDTH,
        height: int = sett.HEIGHT,
        caption: str = CAPTION,
    ):
        super().__init__(width=width, height=height, caption=caption)

        self.space = pymunk.Space()
        self.space.gravity = sett.GRAVITY

        self.draw_options = DrawOptions()
        self.fps_display = FPSDisplay(window=self)
        self.keyboard = key.KeyStateHandler()
        self.model = FixedPendulumModel(space=self.space, window=self)
        self.recorder = Recorder(fields=self.REC_FIELDS, prefix="fixed")

        self.push_handlers(self.keyboard)

        clock.schedule_interval(self.update, interval=sett.INTERVAL)

    def on_draw(self) -> None:
        """Screen Draw Event."""
        self.clear()
        self.space.debug_draw(options=self.draw_options)
        self.fps_display.draw()

    def on_close(self) -> None:
        """Window close event handler."""
        self.recorder.close()
        super().on_close()

    def update(self, dt: float) -> None:
        """Update PyMunk's Space state.

        :param float dt: Time between calls of `update`.
        """
        self._handle_input(keyboard=self.keyboard)

        self.space.step(sett.INTERVAL)

        self.recorder.insert(
            angle=self.model.angle,
            input_left=self.keyboard[key.LEFT],
            input_right=self.keyboard[key.RIGHT],
        )

    def _handle_input(self, keyboard: key.KeyStateHandler) -> None:
        """Handle User Input."""
        if keyboard[key.LEFT]:
            self._accelerate_cw()
        elif keyboard[key.RIGHT]:
            self._accelerate_ccw()

    def _accelerate_cw(self) -> None:
        """Apply a Clockwise force to the pendulum."""
        self.model.accelerate(direction=self.model.vector.rotated_degrees(-90))

    def _accelerate_ccw(self) -> None:
        """Apply a Counter Clockwise force to the pendulum."""
        self.model.accelerate(direction=self.model.vector.rotated_degrees(90))
