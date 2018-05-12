from src.currencies.algorithms import Algorithms
from src.data_scrapper.gpu_release_date.techpowerup.techpowerup_data_scrapper import TechpowerupDataScrapper
from src.data_scrapper.gpu_statistics.whattomine.whattomine_site_data_scrapper import WhattomineDataScrapper
from src.database_accessor.database_accessor import DatabaseAccessor
from src.graphic_cards.graphic_cards import GraphicCards
from src.historical_data_fetcher.gpu_statistics.gpu_statistics_cost_calculator import GpuStatisticsCostCalculator


class GpuStatisticsDatabaseFilling:

    def fill_in_database(self):
        self.__fill_in_whattomine_data()
        self.__fill_in_cost_data()
        self.__fill_in_release_date_data()

    def __fill_in_whattomine_data(self):
        data_scrapper = WhattomineDataScrapper()
        data = data_scrapper.get_data({"algorithm":[algoritm for algoritm in Algorithms], "graphic_card":[graphic_card for graphic_card in GraphicCards]})

        for row in data:
            DatabaseAccessor.upsert_data_gpu_statistics(row)

    def __fill_in_cost_data(self):
        cost_calculator = GpuStatisticsCostCalculator()
        cost_algorithm_and_graphic_card = cost_calculator.get_currency_graphic_card_costs()

        for row in cost_algorithm_and_graphic_card:
            DatabaseAccessor.update_cost_gpu_statistics_data(row["algorithm"], row["graphic_card"], row["cost"])

    def __fill_in_release_date_data(self):
        release_date = TechpowerupDataScrapper()
        data = release_date.get_data({"graphic_card":[graphic_card for graphic_card in GraphicCards]})

        for row in data:
            DatabaseAccessor.update_release_date_gpu_statistics_data(row["graphic_card"].value, row["release_date"])

