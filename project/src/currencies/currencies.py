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
    BTG = "BTG"

    @staticmethod
    def get_algorithm(currency):
        if(currency == Currencies.GRS):
            return Algorithms.GROESTL
        elif(currency == Currencies.ETH or currency == Currencies.ETC):
            return Algorithms.ETHASH
        elif (currency == Currencies.XMR):
            return Algorithms.CRYPTONIGHTV7
        elif (currency == Currencies.BTG):
            return Algorithms.EQUIHASH
        elif(currency == Currencies.BCN or currency == Currencies.FCN or currency == Currencies.QCN):
            return Algorithms.CRYPTONIGHT

    def starting_block(self):
        if(self == Currencies.GRS or self == Currencies.ETH or self == Currencies.XMR or self == Currencies.BCN or self == Currencies.FCN
                or self == Currencies.QCN):
            return 1
        elif(self == Currencies.ETC):
            return 1920000
        elif(self == Currencies.BTG):
            return 491407

    def difficulty_one_target(self):
        if(self == Currencies.GRS or self == Currencies.BTG):
            return 2**32
        elif(self == Currencies.ETH or self == Currencies.ETC or self == Currencies.XMR or self == Currencies.BCN or self == Currencies.FCN
             or self == Currencies.QCN):
            return 1

    def __str__(self):
        return self.name