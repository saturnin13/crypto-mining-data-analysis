import datetime

from src.data_scrapper.blockchain_explorer.blockchain_data_scrapper_factory import BlockChainDataScrapperFactory
from src.data_scrapper.live_price.coinmarketcap.coinmarketcap_data_scrapper import CoinmarketcapDataScrapper
from src.database_accessor.database_accessor import DatabaseAccessor
from src.graphic_cards.graphic_cards import GraphicCards
from src.historical_data_fetcher.historical_data.currency_historical_data_revenue_calculator import HistoricalDataRevenueCalculator
from src.currencies.currencies import Currencies
from src.profit_logic.profit_calculation import ProfitCalculation
from src.variables.variables import Variables


class LiveDataFetcher():

    def __init__(self):
        self.db = DatabaseAccessor()
        self.graphic_card_data = self.db.get_graphic_card_data()
        self.revenue_cache = {}
        self.highest_block_cache = {}

    def compute_live_profit(self, graphic_card):
        currencies = [item for item in Currencies]
        profits_per_second = []
        print(graphic_card)
        for currency in currencies:
            revenue_per_second_per_hashrate = self.__calculate_live_revenue(currency)
            cost_per_second_per_hashrate = self.__calculate_live_cost(currency, graphic_card)
            if(not revenue_per_second_per_hashrate or not cost_per_second_per_hashrate):
                continue
            profit_per_second_per_hashrate = ProfitCalculation.calculate_profit(revenue_per_second_per_hashrate, cost_per_second_per_hashrate,
                                               self.__get_graphic_card_info(currency, graphic_card)["hashrate"], time_unit=datetime.timedelta(seconds=1), fees=0.0)
            profits_per_second.append((currency, profit_per_second_per_hashrate))
        profits_per_second = sorted(profits_per_second, key=lambda x: x[1], reverse=True)
        return profits_per_second


    def __calculate_live_revenue(self, currency):
        if(currency in self.revenue_cache and self.revenue_cache[currency][1] + datetime.timedelta(seconds=Variables.CURRENCY_LIVE_DATABASE_UPDATE_RATE / 1000) >  datetime.datetime.now()):
            return self.revenue_cache[currency][0]

        live_price = float(CoinmarketcapDataScrapper().get_data({"currency": [currency]})[0]["price"])

        most_recent_valid_block = self.__get_most_recent_block(currency)
        most_recent_block = self.__find_most_recent_block(currency, most_recent_valid_block)
        self.highest_block_cache[currency] = most_recent_block["block_number"]

        live_reward = float(most_recent_block["reward"])
        live_difficulty = float(most_recent_block["difficulty"])

        revenue_calculator = HistoricalDataRevenueCalculator()
        revenue = revenue_calculator.get_currency_revenue(currency, live_reward, live_difficulty, live_price)

        self.revenue_cache[currency] = (revenue, datetime.datetime.now())
        return revenue

    def __get_most_recent_block(self, currency):
        if (currency not in self.highest_block_cache):
            self.highest_block_cache[currency] = self.db.get_most_recent_valid_row_currency_database(currency)["block_number"]

        return self.highest_block_cache[currency]

    def __find_most_recent_block(self, currency, block_number):
        data_scrapper = BlockChainDataScrapperFactory.getDataScrapper(currency)
        lower_bound = -1
        speed = 1
        while(True):
            current_data = data_scrapper.get_data_with_sleep({"block_number": [block_number]})
            if(not current_data):
                upper_bound = block_number
                break
            else:
                lower_bound = block_number
                speed = int(speed * 2)
            block_number += speed
        max_block_number = self.__find_max_block_number(lower_bound, upper_bound, currency)
        return data_scrapper.get_data({"block_number": [max_block_number]})[0]

    def __find_max_block_number(self, lower_bound, upper_bound, currency):
        if(upper_bound == lower_bound + 1):
            return lower_bound

        middle_block_number = int((upper_bound - lower_bound) / 2 + lower_bound)
        data_scrapper = BlockChainDataScrapperFactory.getDataScrapper(currency)
        data = data_scrapper.get_data_with_sleep({"block_number": [middle_block_number]})

        if(data):
            return self.__find_max_block_number(middle_block_number, upper_bound, currency)
        else:
            return self.__find_max_block_number(lower_bound, middle_block_number, currency)

    def __calculate_live_cost(self, currency, graphic_card):
        graphic_card_info = self.__get_graphic_card_info(currency, graphic_card)
        if(graphic_card_info):
            return graphic_card_info["cost_per_second_per_hashrate_per_pricekwh_in_dollar"] * Variables.ELECTRICITY_COST

    def __get_graphic_card_info(self, currency, graphic_card):
        for row in self.graphic_card_data:
            if(row["graphic_card"] == graphic_card.value and row["algorithm"] == Currencies.get_algorithm(currency).value):
                return row