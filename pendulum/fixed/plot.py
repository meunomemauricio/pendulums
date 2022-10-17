"""Plot Fixed Pendulum Simulation data."""
from pathlib import Path

import pandas as pd


def load_recording(path: Path) -> pd.DataFrame:
    """Load Recording data as a DataFrame."""
    return pd.read_csv(filepath_or_buffer=path)


def plot_recording(path: Path) -> None:
    """Plot Recording data."""
    df = load_recording(path)
    # TODO: Plot data.
    print(df.head())
