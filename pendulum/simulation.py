import pymunk
from pyglet import clock, window
from pyglet.window import key
from pymunk.pyglet_util import DrawOptions

from pendulum import settings as sett
from pendulum.munk.utils import FPSDisplay
from pendulum.recorder import Recorder


class BaseSimulation(window.Window):

    CAPTION = "Base Simulation"
    REC_FIELDS: tuple[str, ...] = ()

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
            Recorder(fields=self.REC_FIELDS, prefix="fixed")
            if record
            else None
        )

        self.space = pymunk.Space()
        self.space.gravity = sett.GRAVITY

        self.draw_options = DrawOptions()

        self.fps_display = FPSDisplay(window=self)

        self.keyboard = key.KeyStateHandler()
        self.push_handlers(self.keyboard)

        clock.schedule_interval(self.update, interval=sett.INTERVAL)

    def on_draw(self) -> None:
        """Screen Draw Event."""
        self.clear()
        self.space.debug_draw(options=self.draw_options)
        self.fps_display.draw()

    def on_close(self) -> None:
        """Handle Window close event."""
        if self.recorder:
            self.recorder.close()
        super().on_close()

    def update(self, dt: float) -> None:
        raise NotImplementedError
