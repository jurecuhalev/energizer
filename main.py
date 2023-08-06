import logging
from copy import deepcopy

from core import Component, ConnectionConfiguration, ConnectionDirection
from dataclasses import dataclass
from enum import Enum

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class BateryCell(Enum):
    LION = "Lithium-ion"
    FUEL = "Fuel Cell"


@dataclass
class BatteryAttributes:
    cell: BateryCell
    power: int
    year: int


@dataclass
class SolarPVAttributes:
    power: int
    year_installed: int
    average_hours_in_year: int = 5000


class GenericComponent(Component):
    def connect(
        self, target: Component, config: ConnectionConfiguration, is_reverse=False
    ):
        if is_reverse:
            logger.info(f"accepting connection from {target} to {self}")
            new_config = deepcopy(config)
            match config.direction:
                case ConnectionDirection.SOURCE_TO_TARGET:
                    new_config.direction = ConnectionDirection.TARGET_TO_SOURCE
                case ConnectionDirection.TARGET_TO_SOURCE:
                    new_config.direction = ConnectionDirection.SOURCE_TO_TARGET
                case ConnectionDirection.BOTH_WAYS:
                    pass

            config = new_config
        else:
            logger.info(f"connecting {self} to {target}")
            target.connect(target=self, config=config, is_reverse=True)

        self.connections.append((target, config))

    def to_ascii_art(self):
        print(f"\n---- {self.name} ----")
        for entity, config in self.connections:
            entity: Component
            config: ConnectionConfiguration
            match config.direction:
                case ConnectionDirection.SOURCE_TO_TARGET:
                    ascii_art = f"|-- {config.power}W -->"
                case ConnectionDirection.TARGET_TO_SOURCE:
                    ascii_art = f"<-- {config.power}W --|"
                case ConnectionDirection.BOTH_WAYS:
                    ascii_art = f"<-- {config.power}W -->"
                case _:
                    ascii_art = "<-- unknown -->"

            print(f"{self.name} {ascii_art} {entity.name}")
        else:
            if not self.connections:
                print(f"{self.name} |-- no connection --|")


class ElectricCarBattery(GenericComponent):
    def __init__(self, name: str, attributes: BatteryAttributes):
        super().__init__()
        self.name = name
        self.attributes = attributes
        self.connections = []


class SolarPV(GenericComponent):
    def __init__(self, name: str, attributes: SolarPVAttributes):
        super().__init__()
        self.name = name
        self.attributes = attributes
        self.connections = []


if __name__ == "__main__":
    tesla = ElectricCarBattery(
        name="Blue Tesla",
        attributes=BatteryAttributes(cell=BateryCell.LION, power=300, year=2023),
    )

    golf = ElectricCarBattery(
        name="Red Golf",
        attributes=BatteryAttributes(cell=BateryCell.FUEL, power=210, year=2021),
    )

    volvo = ElectricCarBattery(
        name="Green Volvo",
        attributes=BatteryAttributes(cell=BateryCell.FUEL, power=210, year=2021),
    )

    roof = SolarPV(
        name="Barn Roof",
        attributes=SolarPVAttributes(
            power=150, year_installed=2020, average_hours_in_year=1500
        ),
    )

    garden = SolarPV(
        name="Garden Solar Grid",
        attributes=SolarPVAttributes(
            power=1200, year_installed=2015, average_hours_in_year=1350
        ),
    )

    tesla.connect(
        roof,
        config=ConnectionConfiguration(
            direction=ConnectionDirection.SOURCE_TO_TARGET, power=200
        ),
    )
    golf.connect(
        roof,
        config=ConnectionConfiguration(
            direction=ConnectionDirection.TARGET_TO_SOURCE, power=150
        ),
    )
    roof.connect(
        garden,
        config=ConnectionConfiguration(
            direction=ConnectionDirection.BOTH_WAYS, power=1000
        ),
    )

    # components = [tesla, golf, roof, garden]
    components = [tesla, golf, roof, garden, volvo]
    for component in components:
        component.to_ascii_art()
