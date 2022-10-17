"""Cart Pendulum Simulator CLI."""
import click
import pyglet

from pendulum.cart.simulator import CartPendulumSim
from pendulum.recorder import prompt_recording


@click.group()
def cart():
    """Pendulum on a Cart simulator."""


@cart.command()
def run():
    """Run the simulation."""
    CartPendulumSim()
    pyglet.app.run()


@cart.command()
def plot():
    """Plot Recording data."""
    rec_path = prompt_recording(prefix="cart")
    print(rec_path)  # TODO: Plot selection
