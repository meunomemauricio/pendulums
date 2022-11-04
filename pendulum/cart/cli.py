"""Cart Pendulum Simulator CLI."""
import click
import pyglet

from pendulum.cart.plot import plot_recording
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
@click.option("-H", "--height", type=int, default=1080, help="Plot Height.")
@click.option("-W", "--width", type=int, default=1920, help="Plot Width.")
def plot(height: int, width: int):
    """Plot Recording data."""
    rec_path = prompt_recording(prefix="cart")
    plot_recording(path=rec_path, height=height, width=width)
