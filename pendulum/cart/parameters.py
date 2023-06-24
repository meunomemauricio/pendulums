import json
from dataclasses import dataclass

from pendulum import settings as sett

DIRECTORY = sett.BASE_DIR / "pendulum/cart/parameters"


@dataclass
class Parameters:
    """Simulation Parameters for the Cart Pendulum"""

    # Initial Conditions
    angle: float
    cart_x: float
    cart_v: float

    # Entity Properties
    cart_friction: float | None  # mN
    cart_mass: float
    cart_size: tuple[float, float]

    circle_length: float
    circle_mass: float
    circle_radius: float

    @classmethod
    def load_from_file(cls, filename: str) -> "Parameters":
        filepath = DIRECTORY / f"{filename}.json"
        with filepath.open() as fd:
            parameters = json.load(fd)

        return cls(
            angle=parameters["angle"],
            cart_x=parameters["cart_x"],
            cart_v=parameters["cart_v"],
            cart_friction=parameters["cart_friction"],
            cart_mass=parameters["cart_mass"],
            cart_size=parameters["cart_size"],
            circle_length=parameters["circle_length"],
            circle_mass=parameters["circle_mass"],
            circle_radius=parameters["circle_radius"],
        )

    @classmethod
    def available(cls) -> list[str]:
        """List all the available parameters."""
        return [
            path.stem for path in DIRECTORY.iterdir() if path.suffix == ".json"
        ]
