import datetime

from src.database_accessor.database_accessor import DatabaseAccessor


class HistoricalDataRevenueCalculator:
    def __init__(self):
        self.db = DatabaseAccessor()

    def get_currency_historic_revenue(self, currency, revenue_unit=datetime.timedelta(days=1), hashrate=1):
        currency_historical_data = self.db.get_currency_historical_data(currency)
        currency_historical_data.sort(key=lambda x: x["datetime"])

        revenues_and_datetime = []
        for row in currency_historical_data:
            reward = row["reward"]
            difficulty = row["difficulty"]
            usd_per_currency = row["usd_per_" + str(currency).lower()]
            if(reward is None or difficulty is None or usd_per_currency is None):
                continue
            revenue = reward * hashrate / (difficulty * 2**32) * revenue_unit.total_seconds() * usd_per_currency
            revenues_and_datetime.append((revenue, row["datetime"]))

        return revenues_and_datetime