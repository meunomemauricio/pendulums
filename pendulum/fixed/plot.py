"""Plot Fixed Pendulum Simulation data."""
from pathlib import Path

import click
import pandas as pd
from plotly import graph_objects as go

from pendulum import settings


def load_recording(path: Path) -> pd.DataFrame:
    """Load Recording data as a DataFrame.

    Dataframe is indexed with the elapsed time from the beginning of the
    simulation, using the defined `interval` as the step.
    """
    df = pd.read_csv(filepath_or_buffer=path)
    df.index = pd.Index(df.index * df["interval"])
    return df


def plot_recording(path: Path) -> None:
    """Plot Recording data."""
    df = load_recording(path)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["angle"], name="Angle (deg)"))
    plot_path = settings.PLOT_PATH / f"{path.stem}.png"
    fig.write_image(plot_path)
    click.secho(f'Plot generated: "{plot_path.name}"', fg="green")
