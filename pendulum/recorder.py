"""Record data from simulation."""
import csv
import time
from datetime import datetime
from pathlib import Path
from typing import Collection

import click
from click import UsageError
from click.exceptions import Exit

from pendulum import settings as sett


def generate_filename(prefix: str) -> str:
    """Generate filename with Prefix and Timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    return f"{prefix}_{timestamp}.csv"


def list_recordings(prefix: str) -> list[Path]:
    """Return list of all Recording files related to `prefix`."""
    return list(sett.REC_PATH.glob(f"{prefix}_*.csv"))


def parse_filename(path: Path) -> datetime:
    """Parse filename into a timestamp."""
    ts = path.stem.split("_", maxsplit=1)[1]
    return datetime.strptime(ts, "%Y-%m-%d_%H:%M:%S")


def prompt_recording(prefix: str) -> Path:
    """Print a list of recordings and prompt user for selection."""
    recordings = sorted(list_recordings(prefix=prefix), reverse=True)
    if not recordings:
        msg = f'There are no "{prefix}" recordings available.'
        click.secho(msg, fg="bright_red")
        raise Exit(0)

    if len(recordings) == 1:
        click.secho("Selecting only recording available.", fg="yellow")
        return recordings[0]

    click.echo()
    click.secho(f'Available "{prefix}" recordings:', underline=True)
    for idx, rec_path in enumerate(recordings):
        idx_str = click.style(idx, bold=True)
        ts_str = click.style(parse_filename(path=rec_path), fg="green")
        click.echo(f"[{idx_str}] - {ts_str}")

    def value_proc(value: str) -> Path:
        try:
            return recordings[int(value)]
        except (IndexError, ValueError):
            raise UsageError(f"Invalid recording index: {value}.")

    click.echo()
    return click.prompt("Select", value_proc=value_proc, default=0)


class Recorder:
    """Record data from simulation into CSV file."""

    def __init__(self, fields: Collection[str], prefix: str):
        if not sett.REC_PATH.exists():
            click.secho("Creating Recordings path.", fg="yellow")
            sett.REC_PATH.mkdir()

        file_path = sett.REC_PATH / generate_filename(prefix=prefix)
        self.csv_file = file_path.open("w")

        fieldnames = ["ts", "interval"]
        fieldnames.extend(fields)
        self.writer = csv.DictWriter(self.csv_file, fieldnames=fieldnames)
        self.writer.writeheader()

    def insert(self, **kwargs):
        """Insert data entry.

        Timestamp is inserted automatically.
        """
        row = dict(ts=time.time(), interval=sett.SIMULATION_STEP, **kwargs)
        self.writer.writerow(row)

    def close(self):
        """Close file."""
        self.csv_file.close()
