from dataclasses import dataclass
from enum import Enum
from typing import Any, Tuple, List


class ConnectionDirection(Enum):
    SOURCE_TO_TARGET = "Source To Target"
    TARGET_TO_SOURCE = "Target To Source"
    BOTH_WAYS = "Both Directions"


@dataclass
class ConnectionConfiguration:
    direction: ConnectionDirection
    power: int


class Component:
    connections: List[Tuple["Component", ConnectionConfiguration]]
    name: str
    attributes: Any

    def __init__(self):
        pass

    def connect(
        self, target: "Component", config: ConnectionConfiguration, is_reverse=False
    ):
        pass

    def __str__(self):
        return self.name
