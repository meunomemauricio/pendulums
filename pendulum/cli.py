"""Command Line Interface for the Pendulum application."""

import click


@click.group()
def cli():
    """Pendulum CLI."""


@cli.command()
def simulation():
    """Run the PyMunk/Pyglet simulation."""
    from pendulum.simulation import pyglet

    pyglet.app.run()
