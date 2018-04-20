from enum import Enum


class Currencies(Enum):
    GRS = "GRS"

    @staticmethod
    def get_algorithm(currency):
        if(currency == Currencies.GRS):
            return "groestl"