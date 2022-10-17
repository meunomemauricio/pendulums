"""Command Line Interface for the Pendulum application."""

import click

from pendulum.cart.cli import cart
from pendulum.fixed.cli import fixed


@click.group()
def cli():
    """Pendulum Simulator CLI."""


cli.add_command(cart)
cli.add_command(fixed)
