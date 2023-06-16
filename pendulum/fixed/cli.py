"""Fixed Pendulum Simulator CLI Commands."""
import click
import pyglet

from pendulum import settings as sett
from pendulum.fixed.plot import plot_recording
from pendulum.fixed.simulator import FixedPendulumSim
from pendulum.recorder import prompt_recording


@click.group()
def fixed():
    """Fixed Pendulum Simulator."""


@fixed.command()
@click.option("-r", "--record", is_flag=True, help="Record simulation data.")
def run(record: bool):
    """Run the simulation."""
    window = FixedPendulumSim(record=record)
    window.set_vsync(False)  # Allow Higher FPS than monitor refresh rate.
    pyglet.app.run(interval=sett.GRAPHICS_INTERVAL)


@fixed.command()
@click.option("-H", "--height", type=int, default=1080, help="Plot Height.")
@click.option("-W", "--width", type=int, default=1920, help="Plot Width.")
def plot(height: int, width: int):
    """Plot Recording data."""
    rec_path = prompt_recording(prefix="fixed")
    plot_recording(path=rec_path, height=height, width=width)
