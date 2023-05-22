"""Cart Pendulum Simulator CLI."""
import click
import pyglet

from pendulum.cart.initial_conditions import InitialConditions
from pendulum.cart.plot import plot_recording
from pendulum.cart.simulator import CartPendulumSim
from pendulum.recorder import prompt_recording


@click.group()
def cart():
    """Pendulum on a Cart simulator."""


@cart.command()
@click.option("-r", "--record", is_flag=True, help="Record simulation data.")
@click.option(
    "-i", "--initial", default="rest_bottom", help="Initial Conditions File."
)
def run(record: bool, initial: str):
    """Run the simulation."""
    try:
        initial_conditions = InitialConditions.load_from_file(filename=initial)
    except FileNotFoundError:
        click.secho(
            f"Initial Conditions file '{initial}' not found.", fg="bright_red"
        )
        return

    CartPendulumSim(record=record, initial=initial_conditions)
    pyglet.app.run()


@cart.command()
@click.option("-H", "--height", type=int, default=1080, help="Plot Height.")
@click.option("-W", "--width", type=int, default=1920, help="Plot Width.")
def plot(height: int, width: int):
    """Plot Recording data."""
    rec_path = prompt_recording(prefix="cart")
    plot_recording(path=rec_path, height=height, width=width)
