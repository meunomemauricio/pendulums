"""Application Settings and constants."""

#: PyMunk Gravity value
from pathlib import Path

import click

GRAVITY = 0, -9807  # mm/s²

#: Screen Size in px
# NOTE: Currently it's also being considered a real size in mm
WIDTH = 1280
HEIGHT = 720

#: How frequently the simulation is updated. If values are higher than
# simulation steps, the simulation appears in slow motion.
SIMULATION_INTERVAL = 1.0 / 60

#: The amount of (real) time between each update in the simulation space
SIMULATION_STEP = 1.0 / 480

#: The relation between simulated time and real time (i.e. how long it takes to
# simulate 1 second)
SIMULATION_RATE = SIMULATION_INTERVAL / SIMULATION_STEP

#: How many (real) secconds to wait before clearing the aim
CLEAR_AIM_TIME = 0.5

#: Base Project directory
BASE_DIR = Path(__file__).parent.parent

#: Data Path
DATA_PATH = BASE_DIR / "data"
if not DATA_PATH.exists():
    click.secho("Data path doesn't exist. Creating it.", fg="yellow")
    DATA_PATH.mkdir()

#: Recordings Path
REC_PATH = DATA_PATH / "recordings"

#: Plots Path
PLOT_PATH = DATA_PATH / "plot"
if not PLOT_PATH.exists():
    click.secho("Plot path doesn't exist. Creating it.", fg="yellow")
    PLOT_PATH.mkdir()
