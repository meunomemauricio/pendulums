import pymunk
from pyglet import clock, window
from pyglet.window import key, mouse
from pymunk.pyglet_util import DrawOptions

from pendulum import settings as sett
from pendulum.cannon import Cannon
from pendulum.recorder import Recorder
from pendulum.utils import AnimationExporter, FPSDisplay, GridDisplay


class BaseSimulation(window.Window):

    CAPTION = "Base Simulation"
    REC_FIELDS: tuple[str, ...]
    REC_PREFIX: str

    def __init__(
        self,
        record: bool,
        export: bool = False,
        grid: bool = False,
        width: int = sett.WIDTH,
        height: int = sett.HEIGHT,
    ):
        assert self.CAPTION is not None, "CAPTION needs to be set."
        assert self.REC_FIELDS, "REC_FIELDS needs to be set."

        super().__init__(width=width, height=height, caption=self.CAPTION)

        self.recorder = (
            Recorder(fields=self.REC_FIELDS, prefix=self.REC_PREFIX)
            if record
            else None
        )

        self.space = pymunk.Space()
        self.space.gravity = sett.GRAVITY

        self.draw_options = DrawOptions()

        self.fps_display = FPSDisplay(window=self)
        self.exporter = AnimationExporter(enabled=export)
        self.grid = GridDisplay(window=self, enabled=grid)

        self.cannon = Cannon(space=self.space)

        self.keyboard = key.KeyStateHandler()
        self.push_handlers(self.keyboard)

        clock.schedule_interval(self.update, interval=sett.UPDATE_INTERVAL)

    def on_draw(self) -> None:
        """Screen Draw Event."""
        self.clear()
        self.fps_display.draw()
        self.grid.draw()
        self.cannon.draw()
        self.space.debug_draw(options=self.draw_options)
        self.draw_extra()
        self.exporter.save_frame()

    def draw_extra(self) -> None:
        """Draw simulation specific graphics.

        Use this method, instead of overriding `on_draw`. This will make sure
        that the extra stuff is drawn before exporting the frame.
        """
        pass

    def on_close(self) -> None:
        """Handle Window close event."""
        if self.recorder:
            self.recorder.close()

        super().on_close()

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button != mouse.LEFT:
            return

        self.cannon.start(x=x, y=y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button != mouse.LEFT:
            return

        self.cannon.fire(x=x, y=y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not (buttons & mouse.LEFT):
            return

        self.cannon.aim(x=x, y=y)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.G:
            self.grid.toggle()

    def update(self, dt: float) -> None:
        """Update the Simulation."""
        raise NotImplementedError
