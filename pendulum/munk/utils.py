"""Utility Functions and Classes."""
from pyglet import text, window


class FPSDisplay(window.FPSDisplay):
    """Custom FPS Display."""

    FONT_SIZE = 16
    FONT_COLOR = 255, 0, 0, 200

    def __init__(self, window: window.Window):
        super().__init__(window=window)

        self.label = text.Label(
            font_size=self.FONT_SIZE,
            x=window.width - self.FONT_SIZE * 4,
            y=window.height - self.FONT_SIZE - 1,
            color=self.FONT_COLOR,
            bold=True,
        )
