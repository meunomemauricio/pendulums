"""Fixed Pendulum Simulator CLI Commands."""
from pathlib import Path

import click
import pyglet

from pendulum.fixed.simulator import FixedPendulum
from pendulum.recorder import list_recordings, parse_filename


@click.group()
def fixed():
    """Fixed Pendulum Simulator."""


@fixed.command()
def run():
    """Run the simulation."""
    FixedPendulum()
    pyglet.app.run()


@fixed.command()
def plot():
    """Plot Recording data."""
    click.echo("Available Fixed Pendulum recordings:")
    click.echo(80 * "-")
    recordings = list_recordings(prefix="fixed")
    for idx, rec_path in enumerate(recordings):
        click.echo(f"{idx} - {parse_filename(path=rec_path)}")

    click.echo(80 * "-")

    def value_proc(value: str) -> Path:
        try:
            return recordings[int(value)]
        except (IndexError, ValueError):
            raise click.UsageError(f"Invalid recording index: {value}.")

    selection = click.prompt("Recording", value_proc=value_proc)

    # TODO: Plot selection
    print(selection)
