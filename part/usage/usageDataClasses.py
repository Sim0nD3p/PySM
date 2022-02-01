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
    date: Date
    quantity: int



