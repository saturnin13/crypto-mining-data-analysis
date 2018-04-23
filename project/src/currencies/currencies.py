from enum import Enum

from src.currencies.algorithms import Algorithms


class Currencies(Enum):
    GRS = "GRS"
    ETH = "ETH"

    @staticmethod
    def get_algorithm(currency):
        if(currency == Currencies.GRS):
            return Algorithms.GROESTL
        elif(currency == Currencies.ETH):
            return Algorithms.ETHASH

    def __str__(self):
        return self.name