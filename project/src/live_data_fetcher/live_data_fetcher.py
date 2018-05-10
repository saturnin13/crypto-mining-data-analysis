import datetime
import multiprocessing
from functools import partial

from src.currencies.currencies import Currencies
from src.data_scrapper.blockchain_explorer.blockchain_data_scrapper_factory import BlockChainDataScrapperFactory
from src.data_scrapper.live_price.coinmarketcap.coinmarketcap_data_scrapper import CoinmarketcapDataScrapper
from src.database_accessor.database_accessor import DatabaseAccessor
from src.profit_logic.profit_calculation import ProfitCalculation
from src.profit_logic.revenue_calculation import RevenueCalculation
from src.variables.variables import Variables


class LiveDataFetcher():

    def __init__(self):
        self.graphic_card_data = DatabaseAccessor.get_graphic_card_data()
        self.revenue_info_cache = {}

    def clear_revenue_cache(self):
        for item in self.revenue_info_cache.values():
            item.pop('revenue', None)

    def compute_live_profit(self, graphic_card):
        print("Computing live profit for " + str(graphic_card))
        currencies = [item for item in Currencies]

        if(not self.revenue_info_cache or "revenue" not in list(self.revenue_info_cache.values())[0]):
            print("Gathering live revenue data")
            pool = multiprocessing.Pool()
            func = partial(self.calculate_live_revenue, self.revenue_info_cache)
            list_result = pool.map(func, [item for item in currencies])
            list_result = filter(lambda x: x, list_result)
            self.revenue_info_cache = {k: v for d in list_result for k, v in d.items()}

        profits_per_second = []
        for currency in currencies:
            if(currency in self.revenue_info_cache):
                revenue_per_second_per_hashrate = self.revenue_info_cache[currency]["revenue"]
                profits_per_second.append(self.caculate_profit_per_second(revenue_per_second_per_hashrate, currency, graphic_card))

        profits_per_second = sorted(filter(lambda x: x, profits_per_second), key=lambda x: x[1], reverse=True)
        return profits_per_second



    def caculate_profit_per_second(self, revenue_per_second_per_hashrate, currency, graphic_card):
        cost_per_second_per_hashrate = self.__calculate_live_cost(currency, graphic_card)
        if (not revenue_per_second_per_hashrate or not cost_per_second_per_hashrate):
            return None
        profit_per_second = ProfitCalculation.calculate_profit(revenue_per_second_per_hashrate, cost_per_second_per_hashrate,
                                                                            self.__get_graphic_card_info(currency, graphic_card)["hashrate"],
                                                                            time_unit=datetime.timedelta(seconds=1), fees=0.0)
        return (currency, profit_per_second)

    def __calculate_live_cost(self, currency, graphic_card):
        graphic_card_info = self.__get_graphic_card_info(currency, graphic_card)
        if(graphic_card_info):
            return graphic_card_info["cost_per_second_per_hashrate_per_pricekwh_in_dollar"] * Variables.ELECTRICITY_COST

    def __get_graphic_card_info(self, currency, graphic_card):
        for row in self.graphic_card_data:
            if(row["graphic_card"] == graphic_card.value and row["algorithm"] == currency.get_algorithm().value):
                return row


    # All after here are thread run function
    def calculate_live_revenue(self, revenue_info_cache, currency):
        live_price = self.__get_price(currency)

        reward_difficulty_block_number = self.__get_reward_difficulty_block_number(revenue_info_cache, currency)
        live_reward, live_difficulty, block_number = None, None, None
        if(reward_difficulty_block_number):
            live_reward, live_difficulty, block_number = reward_difficulty_block_number

        if(live_reward and live_price and live_difficulty and block_number):
            revenue = RevenueCalculation.calculate_revenue(currency, live_reward, live_difficulty, live_price)
            return {currency:{"revenue":revenue, "highest_block":block_number}}

    def __get_price(self, currency):
        data = CoinmarketcapDataScrapper().get_data({"currency": [currency]})
        if (not data):
            return None
        return float(data[0]["price"])

    def __get_reward_difficulty_block_number(self, revenue_info_cache, currency):
        if (revenue_info_cache and currency in revenue_info_cache and "highest_block" in revenue_info_cache[currency]):
            highest_block = revenue_info_cache[currency]["highest_block"]
        else:
            highest_block = self.__get_most_recent_valid_block_from_db(currency)
        most_recent_block = self.__find_most_recent_block_from_scrapping(currency, highest_block)
        if (not most_recent_block):
            print("ERROR: most_recent_block could not be find for " + str(currency))
            return None
        return float(most_recent_block["reward"]), float(most_recent_block["difficulty"]), most_recent_block["block_number"]

    def __get_most_recent_valid_block_from_db(self, currency):
        return DatabaseAccessor.get_most_recent_valid_row_currency_database(currency)["block_number"]

    def __find_most_recent_block_from_scrapping(self, currency, block_number):
        data_scrapper = BlockChainDataScrapperFactory.getDataScrapper(currency)
        lower_bound = block_number - 1
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

        data = data_scrapper.get_data({"block_number": [max_block_number]})
        if(data):
            return data[0]

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

