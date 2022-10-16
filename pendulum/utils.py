"""Utility Functions and Classes."""
from pyglet import text, window


class FPSDisplay(window.FPSDisplay):
    """Custom FPS Display."""

    FONT_SIZE = 12
    FONT_COLOR = 255, 0, 0, 200

    def __init__(self, window: window.Window):
        super().__init__(window=window)

        self.label = text.Label(
            font_size=self.FONT_SIZE,
            x=self.window.width - self.FONT_SIZE * 8,
            y=self.window.height - self.FONT_SIZE - 1,
            color=self.FONT_COLOR,
            bold=True,
        )

    def set_fps(self, fps):
        """Override FPS text."""
        self.label.text = f"FPS: {fps:0.2f}"
