from dataclasses import dataclass

@dataclass
class Specifications:
    """
    All units SI:
        - mm for length
        - kg for mass
    """
    length: float
    width: float
    height: float
    weight: float

@dataclass
class GeneralInformation:
    """
    Class used to hold general information except code
    **elements might be added with time
    """
    description: str
    type: str   # type (3 digits after SEP)
