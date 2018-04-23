from enum import Enum

from src.currencies.algorithms import Algorithms


class Currencies(Enum):
    GRS = "GRS"

    @staticmethod
    def get_algorithm(currency):
        if(currency == Currencies.GRS):
            return Algorithms.GROESTL

    def __str__(self):
        return self.name