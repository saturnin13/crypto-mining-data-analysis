import datetime

from src.database_accessor.database_accessor import DatabaseAccessor
from src.variables.variables import Variables


class GpuStatisticsCostCalculator:
    def __init__(self):
        self.db = DatabaseAccessor()

    def get_currency_graphic_card_costs(self, price_kwh=Variables.ELECTRICITY_COST, cost_unit=datetime.timedelta(days=1), hashrate=1):
        currency_graphic_card_historical_data = self.db.get_graphic_card_data()

        cost_algorithm_and_graphic_card = []
        for row in currency_graphic_card_historical_data:
            current_cost = {}
            watt = row["watt"]
            hash_per_second = row["hashrate"]
            if(watt is None or hash_per_second is None):
                continue
            cost = price_kwh / (1000 * 3600) * (watt / hash_per_second) * hashrate * cost_unit.total_seconds()
            current_cost["cost"] = cost
            current_cost["algorithm"] = row["algorithm"]
            current_cost["graphic_card"] = row["graphic_card"]
            cost_algorithm_and_graphic_card.append(current_cost)

        return cost_algorithm_and_graphic_card
