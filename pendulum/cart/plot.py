"""Plot Cart Pendulum Simulation data."""
from pathlib import Path

import click
from plotly import graph_objects as go
from plotly.subplots import make_subplots

from pendulum import settings
from pendulum.plot import load_recording


def plot_recording(path: Path, height: int, width: int) -> None:
    """Plot Recording data."""
    df = load_recording(path)

    fig = make_subplots(rows=4, cols=1)

    fig.add_trace(
        go.Scatter(x=df.index, y=df["cart_x"], name="Cart Position (mm)"),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df["cart_velocity"], name="Cart Velocity (mm/s)"
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df["angle"], name="Angle (deg)"),
        row=3,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["angular_velocity"],
            name="Angular Velocity (deg/s)",
        ),
        row=4,
        col=1,
    )

    plot_path = settings.PLOT_PATH / f"{path.stem}.png"
    fig.update_layout(
        title="Cart Pendulum Simulation.",
        autosize=False,
        width=width,
        height=height,
    )

    fig.write_image(plot_path)
    click.secho(f'Plot generated: "{plot_path.name}"', fg="green")
