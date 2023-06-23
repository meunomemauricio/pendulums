"""Cart Pendulum Simulator CLI."""
import click
import pyglet

from pendulum.cart.parameters import Parameters
from pendulum.cart.plot import plot_recording
from pendulum.cart.simulator import CartPendulumSim
from pendulum.recorder import prompt_recording


@click.group()
def cart():
    """Pendulum on a Cart simulator."""


@cart.command()
@click.option("-C", "--controller", is_flag=True, help="Engage Controller.")
@click.option("-e", "--export", is_flag=True, help="Export Animation.")
@click.option("-g", "--grid", is_flag=True, help="Display Grid.")
@click.option("-p", "--params", default="rest_bottom", help="Parameters File.")
@click.option("-r", "--record", is_flag=True, help="Record simulation data.")
def run(controller: bool, export: bool, grid: bool, params: str, record: bool):
    """Run the simulation."""
    try:
        sim_params = Parameters.load_from_file(filename=params)
    except FileNotFoundError:
        click.secho(f"Parameters '{params}' not found.", fg="bright_red")
        click.echo("\n".join((f" - {p}" for p in Parameters.available())))
        return

    CartPendulumSim(
        record=record,
        export=export,
        grid=grid,
        controller=controller,
        params=sim_params,
    )
    pyglet.app.run()


@cart.command()
@click.option("-H", "--height", type=int, default=1080, help="Plot Height.")
@click.option("-W", "--width", type=int, default=1920, help="Plot Width.")
def plot(height: int, width: int):
    """Plot Recording data."""
    rec_path = prompt_recording(prefix="cart")
    plot_recording(path=rec_path, height=height, width=width)
