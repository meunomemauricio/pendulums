"""Fixed Pendulum Simulator CLI Commands."""
import click
import pyglet

from pendulum.fixed.plot import plot_recording
from pendulum.fixed.simulator import FixedPendulum
from pendulum.recorder import prompt_recording


@click.group()
def fixed():
    """Fixed Pendulum Simulator."""


@fixed.command()
def run():
    """Run the simulation."""
    FixedPendulum()
    pyglet.app.run()


@fixed.command()
def plot():
    """Plot Recording data."""
    rec_path = prompt_recording(prefix="fixed")
    plot_recording(path=rec_path)
