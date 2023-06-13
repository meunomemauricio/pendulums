import pymunk
from pyglet import clock, shapes, window
from pyglet.window import key, mouse
from pymunk import Vec2d
from pymunk.pyglet_util import DrawOptions

from pendulum import settings as sett
from pendulum.munk.entities import Circle
from pendulum.munk.utils import FPSDisplay, GridDisplay
from pendulum.recorder import Recorder


class BaseSimulation(window.Window):

    CAPTION = "Base Simulation"
    REC_FIELDS: tuple[str, ...]
    REC_PREFIX: str

    AIM_LINE_WIDTH = 2
    PROJECTILE_SPEED = 20

    def __init__(
        self,
        record: bool,
        width: int = sett.WIDTH,
        height: int = sett.HEIGHT,
        caption: str = CAPTION,
    ):
        assert self.CAPTION is not None, "CAPTION needs to be set."
        assert self.REC_FIELDS, "REC_FIELDS needs to be set."

        super().__init__(width=width, height=height, caption=caption)

        self.recorder = (
            Recorder(fields=self.REC_FIELDS, prefix=self.REC_PREFIX)
            if record
            else None
        )

        self.space = pymunk.Space()
        self.space.gravity = sett.GRAVITY

        self.draw_options = DrawOptions()

        self.fps_display = FPSDisplay(window=self)
        self.grid = GridDisplay(window=self)

        self.keyboard = key.KeyStateHandler()
        self.push_handlers(self.keyboard)

        clock.schedule_interval(self.update, interval=sett.INTERVAL)

        self.click_vector: Vec2d | None = None
        self.click_line: shapes.Line | None = None
        self.click_circle = None

    def on_draw(self) -> None:
        """Screen Draw Event."""
        self.clear()
        self.space.debug_draw(options=self.draw_options)
        self.fps_display.draw()
        self.grid.draw()
        if self.click_line is not None:
            self.click_line.draw()

    def on_close(self) -> None:
        """Handle Window close event."""
        if self.recorder:
            self.recorder.close()
        super().on_close()

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button != mouse.LEFT:
            return

        self.click_vector = Vec2d(x=x, y=y)
        self.click_line = shapes.Line(x, y, x, y, width=self.AIM_LINE_WIDTH)

    def on_mouse_release(self, x, y, button, modifiers):
        if button != mouse.LEFT:
            return

        diff_vector = self.click_vector - Vec2d(x=x, y=y)
        impulse = diff_vector * self.PROJECTILE_SPEED
        self.click_circle = Circle(
            space=self.space, mass=1, radius=5, initial_pos=self.click_vector
        )
        self.click_circle.body.apply_impulse_at_local_point(impulse)
        self.click_line = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not (buttons & mouse.LEFT):
            return

        # FIXME: Line is a little janky
        self.click_line.anchor_position = (0, 0)
        self.click_line.position = (x, y)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.G:
            self.grid.toggle()

    def update(self, dt: float) -> None:
        raise NotImplementedError
