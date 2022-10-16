"""Command Line Interface for the Pendulum application."""

import click
import pyglet

from pendulum.models.cart_pendulum import CartPendulum


@click.group()
def cli():
    """Pendulum CLI."""


@cli.command()
def cart():
    """Run PyMunk Cart Pendulum simulation."""
    CartPendulum()
    pyglet.app.run()


@cli.command()
def fixed():
    """Run the PyMunk Fixed Pendulum simulation."""
    print("TODO: Fixed pendulum.")
