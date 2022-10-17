"""Fixed Pendulum Simulator CLI Commands."""
import click
import pyglet

from pendulum.fixed.simulator import FixedPendulum


@click.group()
def fixed():
    """Fixed Pendulum Simulator."""


@fixed.command()
def run():
    """Run the simulation."""
    FixedPendulum()
    pyglet.app.run()
