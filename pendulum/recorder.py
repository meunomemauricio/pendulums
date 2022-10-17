"""Record data from simulation."""
import csv
from datetime import datetime
from pathlib import Path
from typing import Collection

import click

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


class Recorder:
    """Record data from simulation into CSV file."""

    def __init__(self, fields: Collection[str], prefix: str):
        if not sett.REC_PATH.exists():
            click.secho("Creating Recordings path.", fg="yellow")
            sett.REC_PATH.mkdir()

        file_path = sett.REC_PATH / generate_filename(prefix=prefix)
        self.csv_file = file_path.open("w")

        self.writer = csv.DictWriter(self.csv_file, fieldnames=fields)
        self.writer.writeheader()

    def insert(self, **kwargs):
        """Insert data entry."""
        self.writer.writerow(kwargs)

    def close(self):
        """Close file."""
        self.csv_file.close()
