from enum import Enum


class GraphicCards(Enum):
    AMD_280X    = "AMD 280X"
    AMD_380     = "AMD 380"
    AMD_FURY    = "AMD FURY"
    AMD_470     = "AMD 470"
    AMD_480     = "AMD 480"
    AMD_570     = "AMD 570"
    AMD_580     = "AMD 580"
    AMD_VEGA_56 = "AMD VEGA 56"
    AMD_VEGA_64 = "AMD VEGA 64"


    GTX_750_TI  = "GTX 750 TI"
    GTX_1050_TI = "GTX 1050 TI"
    GTX_1060    = "GTX 1060"
    GTX_1070    = "GTX 1070"
    GTX_1070_TI = "GTX 1070 TI"
    GTX_1080    = "GTX 1080"
    GTX_1080_TI = "GTX 1080 TI"

    def __str__(self):
        return self.name


