import datetime


class ProfitCalculation():

    @staticmethod
    def calculate_profit(revenue, cost, hashrate, time_unit=datetime.timedelta(days=1), fees=0.0):
        return ((1 - fees) * revenue - cost) * hashrate * time_unit.total_seconds()