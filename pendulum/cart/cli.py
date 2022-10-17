"""Cart Pendulum Simulator CLI."""
import click
import pyglet

from pendulum.cart.simulator import CartPendulum


@click.group()
def cart():
    """Pendulum on a Cart simulator."""


@cart.command()
def run():
    """Run the simulation."""
    CartPendulum()
    pyglet.app.run()
