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

    GRID_STEP_SIZE = 50

    def __init__(self, window: window.Window):
        self.window = window

        self.enabled = True

        self._lines: list[shapes.ShapeBase] = []
        self._batch = graphics.Batch()
        self._create_grid()

    def _create_grid(self) -> None:
        """Define the Grid Lines."""
        self._create_horizontal_grids()
        self._create_vertical_grids()

    def _create_horizontal_grids(self) -> None:
        """Create Horizontal Grid Lines.

        Start from the middle line and go up and down.
        """
        total_steps = self.window.height // (self.GRID_STEP_SIZE * 2)
        middle_y = self.window.height / 2
        self._create_horizontal_line(middle_y, color=(255, 255, 255, 100))
        for step in range(1, total_steps + 1):
            self._create_horizontal_line(middle_y - step * self.GRID_STEP_SIZE)
            self._create_horizontal_line(middle_y + step * self.GRID_STEP_SIZE)

    def _create_horizontal_line(self, y, color=(255, 255, 255, 50)) -> None:
        line = shapes.Line(
            0,
            y,
            self.window.width,
            y,
            width=1,
            color=color,
            batch=self._batch,
        )
        self._lines.append(line)

    def _create_vertical_grids(self) -> None:
        """Create Vertical Grid Lines.

        Start from the middle line and go left and right.
        """
        total_steps = self.window.width // (self.GRID_STEP_SIZE * 2)
        middle_x = self.window.width / 2
        self._create_vertical_line(middle_x, color=(255, 255, 255, 100))
        for step in range(1, total_steps + 1):
            self._create_vertical_line(middle_x - step * self.GRID_STEP_SIZE)
            self._create_vertical_line(middle_x + step * self.GRID_STEP_SIZE)

    def _create_vertical_line(self, x, color=(255, 255, 255, 50)) -> None:
        line = shapes.Line(
            x,
            0,
            x,
            self.window.height,
            width=1,
            color=color,
            batch=self._batch,
        )
        self._lines.append(line)

    def draw(self) -> None:
        if self.enabled:
            self._batch.draw()

    def toggle(self) -> None:
        self.enabled = not self.enabled
