import pymunk
from pyglet import clock, window
from pyglet.window import key, mouse
from pymunk.pyglet_util import DrawOptions

from pendulum import settings as sett
from pendulum.projectile import Projectile
from pendulum.recorder import Recorder
from pendulum.utils import FPSDisplay, GridDisplay


class BaseSimulation(window.Window):

    CAPTION = "Base Simulation"
    REC_FIELDS: tuple[str, ...]
    REC_PREFIX: str

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

        self.projectile = Projectile(space=self.space)

        self.keyboard = key.KeyStateHandler()
        self.push_handlers(self.keyboard)

        clock.schedule_interval(self.update, interval=sett.INTERVAL)

    def on_draw(self) -> None:
        """Screen Draw Event."""
        self.clear()
        self.space.debug_draw(options=self.draw_options)
        self.fps_display.draw()
        self.grid.draw()
        self.projectile.draw()

    def on_close(self) -> None:
        """Handle Window close event."""
        if self.recorder:
            self.recorder.close()
        super().on_close()

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button != mouse.LEFT:
            return

        self.projectile.start(x=x, y=y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button != mouse.LEFT:
            return

        self.projectile.fire(x=x, y=y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not (buttons & mouse.LEFT):
            return

        self.projectile.update_aim(x=x, y=y)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.G:
            self.grid.toggle()

    def update(self, dt: float) -> None:
        """Update the Simulation."""
        raise NotImplementedError
