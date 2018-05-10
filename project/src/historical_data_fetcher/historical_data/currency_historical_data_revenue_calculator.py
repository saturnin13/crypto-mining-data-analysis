import datetime

from src.database_accessor.database_accessor import DatabaseAccessor
from src.profit_logic.revenue_calculation import RevenueCalculation


class HistoricalDataRevenueCalculator:

    def get_currency_historic_revenue(self, currency, revenue_unit=datetime.timedelta(seconds=1), hashrate=1):
        currency_historical_data = DatabaseAccessor.get_currency_historical_data(currency)
        currency_historical_data.sort(key=lambda x: x["datetime"])

        revenues_and_datetime = []
        for row in currency_historical_data:
            reward = row["reward"]
            difficulty = row["difficulty"]
            usd_per_currency = row["usd_per_" + str(currency).lower()]
            if(reward is None or difficulty is None or usd_per_currency is None):
                continue
            revenue = RevenueCalculation.calculate_revenue(currency, reward, difficulty, usd_per_currency, revenue_unit=revenue_unit, hashrate=hashrate)
            revenues_and_datetime.append((revenue, row["datetime"]))

        return revenues_and_datetime

