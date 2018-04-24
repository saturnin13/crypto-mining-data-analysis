class ConstantRegex:
    DECIMAL_NUMBER = "(\d*,?\d+)*(\\.\d*)?"
    EXPONENTIAL_NUMBER = DECIMAL_NUMBER + "e(\\+|-)?\d+"
    NUMBER = "(" + DECIMAL_NUMBER + "|" + EXPONENTIAL_NUMBER + ")"