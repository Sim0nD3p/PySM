from dataclasses import dataclass

@dataclass
class ElementConstructorData:
    name: str
    type: str
    x_position: float
    y_position: float
    length: float
    width: float
    height: float
    angle: float

@dataclass
# useless
class RackingID:
    name: str
    id: int


