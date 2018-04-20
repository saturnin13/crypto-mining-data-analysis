import datetime

from src.database_accessor.database_accessor import DatabaseAccessor


class GpuStatisticsCostCalculator:
    def __init__(self):
        self.db = DatabaseAccessor()

    def get_currency_graphic_card_costs(self, price_kwh=0.13, cost_unit=datetime.timedelta(days=1), hashrate=1):
        currency_graphic_card_historical_data = self.db.get_graphic_card_data()

        cost_algorithm_and_graphic_card = []
        for row in currency_graphic_card_historical_data:
            watt = row["total_watt"]
            hash_per_second = row["hash_per_second"]
            if(watt is None or hash_per_second is None):
                continue
            cost = price_kwh / (1000 * 3600) * (watt / hash_per_second) * hashrate * cost_unit.total_seconds()
            cost_algorithm_and_graphic_card.append((cost, row["algorithm"], row["graphic_card"]))

        return cost_algorithm_and_graphic_card
