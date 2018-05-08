import datetime

from src.database_accessor.database_accessor import DatabaseAccessor
from src.profit_logic.cost_calculation import CostCalculation
from src.variables.variables import Variables


class GpuStatisticsCostCalculator:
    def __init__(self):
        self.db = DatabaseAccessor()

    def get_currency_graphic_card_costs(self, cost_unit=datetime.timedelta(seconds=1)):
        currency_graphic_card_historical_data = self.db.get_graphic_card_data()

        cost_algorithm_and_graphic_card = []
        for row in currency_graphic_card_historical_data:
            current_cost = {}
            watt = row["watt"]
            hash_per_second = row["hashrate"]
            if(watt is None or hash_per_second is None):
                continue
            cost =  CostCalculation.cost_calculation(watt, hash_per_second, cost_unit=cost_unit)
            current_cost["cost"] = cost
            current_cost["algorithm"] = row["algorithm"]
            current_cost["graphic_card"] = row["graphic_card"]
            cost_algorithm_and_graphic_card.append(current_cost)

        return cost_algorithm_and_graphic_card
