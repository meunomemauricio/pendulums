"""Command Line Interface for the Pendulum application."""

import click
import pyglet

from pendulum.simulation import SimulationWindow


@click.group()
def cli():
    """Pendulum CLI."""


@cli.command()
def simulation():
    """Run the PyMunk/Pyglet simulation."""
    SimulationWindow()
    pyglet.app.run()
