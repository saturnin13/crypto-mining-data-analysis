from src.database_accessor.database_accessor import DatabaseAccessor
from src.historical_data_fetcher.gpu_statistics.gpu_statistics_cost_calculator import GpuStatisticsCostCalculator


class GpuStatisticsDatabaseFilling:
    def __init__(self):
        self.db = DatabaseAccessor()

    def fill_in_database(self):
        self.__fill_in_cost_data()

    def __fill_in_cost_data(self):
        cost_calculator = GpuStatisticsCostCalculator()
        cost_algorithm_and_graphic_card = cost_calculator.get_currency_graphic_card_costs(price_kwh=0.13)

        for row in cost_algorithm_and_graphic_card:
            cost = row[0]
            algorithm = row[1]
            graphic_card = row[2]
            self.db.update_cost_gpu_statistics_data(algorithm, graphic_card, cost)

test = GpuStatisticsDatabaseFilling()
test.fill_in_database()
