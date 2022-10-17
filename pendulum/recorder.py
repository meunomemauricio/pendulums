"""Record data from simulation."""
import csv
from datetime import datetime
from typing import Collection

import click

from pendulum import settings as sett


class Recorder:
    """Record data from simulation into CSV file."""

    def __init__(self, fields: Collection[str], prefix: str):
        if not sett.REC_PATH.exists():
            click.secho("Creating Recordings path.", fg="yellow")
            sett.REC_PATH.mkdir()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        filename = f"{prefix}_{timestamp}.csv"
        file_path = sett.REC_PATH / filename
        self.csv_file = file_path.open("w")

        self.writer = csv.DictWriter(self.csv_file, fieldnames=fields)
        self.writer.writeheader()

    def insert(self, **kwargs):
        """Insert data entry."""
        self.writer.writerow(kwargs)

    def close(self):
        """Close file."""
        self.csv_file.close()
