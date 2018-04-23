from enum import Enum

from src.currencies.algorithms import Algorithms


class Currencies(Enum):
    GRS = "GRS"
    ETH = "ETH"
    XMR = "XMR"
    ETC = "ETC"
    BCN = "BCN"
    FCN = "FCN"
    QCN = "QCN"

    @staticmethod
    def get_algorithm(currency):
        if(currency == Currencies.GRS):
            return Algorithms.GROESTL
        elif(currency == Currencies.ETH or currency == Currencies.ETC):
            return Algorithms.ETHASH
        elif (currency == Currencies.XMR or currency == Currencies.FCN or currency == Currencies.QCN):
            return Algorithms.CRYPTONIGHTV7
        elif (currency == Currencies.BCN):
            return Algorithms.EQUIHASH

    def __str__(self):
        return self.name