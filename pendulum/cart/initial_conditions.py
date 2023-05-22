import json
from dataclasses import dataclass

from pendulum import settings as sett

DIRECTORY = sett.BASE_DIR / "pendulum/cart/initial_conditions"


@dataclass
class InitialConditions:
    """Initial Condition parameters for the Cart Pendulum"""

    angle: float
    cart_x: float
    cart_v: float

    @classmethod
    def load_from_file(cls, filename: str) -> "InitialConditions":
        filepath = DIRECTORY / f"{filename}.json"
        with filepath.open() as fd:
            parameters = json.load(fd)

        return cls(
            angle=parameters["angle"],
            cart_x=parameters["cart_x"],
            cart_v=parameters["cart_v"],
        )
