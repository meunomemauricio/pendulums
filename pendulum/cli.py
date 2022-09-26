"""Command Line Interface for the Pendulum application."""

import click


@click.group()
def cli():
    """Pendulum CLI."""


@cli.command()
def example():
    """Example PyMunk/Pyglet application."""
    from pendulum.example import pyglet

    pyglet.app.run()
