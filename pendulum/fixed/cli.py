"""Fixed Pendulum Simulator CLI Commands."""
import click
import pyglet

from pendulum.fixed.plot import plot_recording
from pendulum.fixed.simulator import FixedPendulumSim
from pendulum.recorder import prompt_recording


@click.group()
def fixed():
    """Fixed Pendulum Simulator."""


@fixed.command()
def run():
    """Run the simulation."""
    FixedPendulumSim()
    pyglet.app.run()


@fixed.command()
@click.option("-H", "--height", type=int, default=1080, help="Plot Height.")
@click.option("-W", "--width", type=int, default=1920, help="Plot Width.")
def plot(height: int, width: int):
    """Plot Recording data."""
    rec_path = prompt_recording(prefix="fixed")
    plot_recording(path=rec_path, height=height, width=width)
