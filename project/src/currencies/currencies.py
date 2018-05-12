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
    EXP = "EXP"
    UBQ = "UBQ"
    ZEC = "ZEC"
    ZCL = "ZCL"

    def get_algorithm(self):
        if(self == Currencies.GRS):
            return Algorithms.GROESTL
        elif(self == Currencies.ETH or self == Currencies.ETC or self == Currencies.EXP or self == Currencies.UBQ):
            return Algorithms.ETHASH
        elif (self == Currencies.XMR):
            return Algorithms.CRYPTONIGHTV7
        elif (self == Currencies.BTG or self == Currencies.ZEC or self == Currencies.ZCL):
            return Algorithms.EQUIHASH
        elif(self == Currencies.BCN or self == Currencies.FCN or self == Currencies.QCN):
            return Algorithms.CRYPTONIGHT
        else:
            raise Exception("Unknown algorithm")

    def starting_block(self):
        if(self == Currencies.GRS or self == Currencies.ETH or self == Currencies.XMR or self == Currencies.BCN or self == Currencies.FCN
                or self == Currencies.QCN or self == Currencies.EXP or self == Currencies.UBQ or self == Currencies.ZEC or self == Currencies.ZCL):
            return 1
        elif(self == Currencies.ETC):
            return 1920000
        elif(self == Currencies.BTG):
            return 491407
        else:
            raise Exception("Unknown starting block")

    def difficulty_one_target(self):
        if(self == Currencies.GRS or self == Currencies.BTG):
            return 2**32
        elif(self == Currencies.ETH or self == Currencies.ETC or self == Currencies.XMR or self == Currencies.BCN or self == Currencies.FCN
             or self == Currencies.QCN or self == Currencies.EXP or self == Currencies.UBQ):
            return 1
        elif(self == Currencies.ZEC or self == Currencies.ZCL):
            return 2**13
        else:
            raise Exception("Unknown difficulty one target")

    def __str__(self):
        return self.name