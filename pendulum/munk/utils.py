"""Utility Functions and Classes."""
from pyglet import graphics, shapes, text, window


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


class GridDisplay:
    """Draw a grid on the screen."""

    def __init__(self, window: window.Window):
        self.window = window

        self.enabled = True

        self._lines: list[shapes.ShapeBase] = []
        self._batch = graphics.Batch()
        self._create_grid()

    def _create_grid(self) -> None:
        """Define the Grid Lines."""
        x = self.window.width / 2
        y1 = 0
        y2 = self.window.height
        y_axis_line = shapes.Line(
            x, y1, x, y2, width=1, color=(255, 255, 255, 50), batch=self._batch
        )

        self._lines.append(y_axis_line)

    def draw(self) -> None:
        if self.enabled:
            self._batch.draw()
