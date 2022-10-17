"""Plot Fixed Pendulum Simulation data."""
from pathlib import Path

import pandas as pd


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
    # TODO: Plot data.
    print(df.head())
