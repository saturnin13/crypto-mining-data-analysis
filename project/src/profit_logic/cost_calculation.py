import datetime


class CostCalculation():

    @staticmethod
    def cost_calculation(watt, hash_per_second, cost_unit=datetime.timedelta(seconds=1)):
        return 1 / (1000 * 3600) * (watt / hash_per_second) * cost_unit.total_seconds()