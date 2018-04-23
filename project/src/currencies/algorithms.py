from enum import Enum


class Algorithms(Enum):
    ETHASH        = "ethash"
    GROESTL       = "groestl"
    X11GOST       = "x11gost"
    CRYPTONIGHT   = "cryptonight"
    CRYPTONIGHTV7 = "cryptonightv7"
    EQUIHASH      = "equihash"
    LYRA2REV2     = "lyra2rev2"
    NEOSCRYPT     = "neoscrypt"
    TIMETRAVEL10  = "timetravel10"
    X16R          = "x16r"
    SKUNKHASH     = "skunkhash"
    NIST5         = "nist5"
    XEVAN         = "xevan"

    def __str__(self):
        return self.name

