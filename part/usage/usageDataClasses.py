from dataclasses import dataclass
from datetime import date


@dataclass
class Date:
    year: int
    month: int
    day: int

    def get_date(self):
        """
        :return: date object
        """
        return date(self.year, self.month, self.day)



@dataclass
class Order:
    part_code: str
    date: Date
    quantity: int
    supplier_name: str



