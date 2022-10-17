"""Application Settings and constants."""

#: PyMunk Gravity value
from pathlib import Path

import click

GRAVITY = 0, -9807  # mm/s²

#: Screen Size in px
# NOTE: Currently it's also being considered a real size in mm
WIDTH = 1280
HEIGHT = 720

#: Tick Interval
INTERVAL = 1.0 / 60


#: Base Project directory
BASE_DIR = Path(__file__).parent.parent

#: Data Path
DATA_PATH = BASE_DIR / "data"
if not DATA_PATH.exists():
    click.secho("Data path doesn't exist. Creating it.", fg="yellow")
    DATA_PATH.mkdir()

#: Recordings Path
REC_PATH = DATA_PATH / "recordings"
