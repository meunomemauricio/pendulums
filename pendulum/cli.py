"""Command Line Interface for the Pendulum application."""

import click

from pendulum.cart.cli import cart
from pendulum.fixed.cli import fixed
from pendulum.utils import render_animation


@click.group()
def cli():
    """Pendulum Simulator CLI."""


cli.add_command(cart)
cli.add_command(fixed)


@cli.command()
@click.option("-n", "--name", help="Custom name to the animation file.")
def render(name: str):
    render_animation(name=name)
