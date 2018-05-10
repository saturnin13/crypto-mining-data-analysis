import datetime

from src.currencies.currencies import Currencies
from src.database_accessor.database_accessor import DatabaseAccessor
from src.profit_logic.profit_calculation import ProfitCalculation
from src.utils.utils import Utils
from src.variables.variables import Variables


class CurrenciesGraphicCardsInfoPreProcessor:
    def __init__(self, currencies, graphic_cards, starting_datetime=datetime.datetime(2009, 1, 1), end_datetime=datetime.datetime.now(), fees=0.0,
                 time_unit=datetime.timedelta(days=1), price_in_kwh=Variables.ELECTRICITY_COST):
        self.cache = {}

        self.currencies = currencies
        self.graphic_cards = graphic_cards
        self.starting_datetime = starting_datetime
        self.end_datetime = end_datetime
        self.fees = fees
        self.time_unit = time_unit

        self.price_in_kwh = price_in_kwh

    def preprocess(self):
        print("Preprocessing information per graphic cards and currencies")

        info = []

        for graphic_card in self.graphic_cards:
            for currency in self.currencies:
                current = {}
                current["profits_datetime"] = self.__calculate_profits_datetime(currency, graphic_card)
                if(current["profits_datetime"]):
                    current["average_profit"] = self.__calculate_average_profit(current["profits_datetime"]["profits"])
                    current["instant_profit"] = self.__calculate_instant_profit(current["profits_datetime"])
                    current["currency"]       = currency
                    current["graphic_card"]   = graphic_card
                    info.append(current)

        return info

    def __calculate_instant_profit(self, profits_datetime):
        date_time = profits_datetime["datetimes"]
        index = date_time.index(min(date_time, key=lambda d: abs(d - datetime.datetime.now())))
        return profits_datetime["profits"][index]

    def __calculate_average_profit(self, profits):
        return sum(profits) / len(profits)

    def __calculate_profits_datetime(self, currency, graphic_card):
        currency_historical_data = self.__get_currency_historical_data(currency)
        currency_historical_data = list(filter(lambda x: x["datetime"] and x["datetime"] >= self.starting_datetime and x["datetime"] <= self.end_datetime, currency_historical_data))
        currency_historical_data = sorted(currency_historical_data, key=lambda x: x["datetime"])

        cost_per_hashrate_per_second_in_dollar, hashrate = self.__get_cost_and_hashrate(currency.get_algorithm().value, graphic_card.value)
        if(not cost_per_hashrate_per_second_in_dollar or not hashrate):
            return None

        profits = []
        date_time_values = []
        last_date_time = datetime.datetime(500, 1, 1)
        for row in currency_historical_data:
            revenue_per_hashrate_per_second_in_dollar = row["revenue_per_second_per_hashrate_in_dollar"]
            new_date_time = row["datetime"]
            if(revenue_per_hashrate_per_second_in_dollar is None or last_date_time is None or new_date_time < last_date_time + self.time_unit):
                continue
            last_date_time = Utils.truncate_datetime_limit(self.time_unit, new_date_time)
            profit = ProfitCalculation.calculate_profit(revenue_per_hashrate_per_second_in_dollar, cost_per_hashrate_per_second_in_dollar, hashrate, self.time_unit, self.fees)
            profits.append(profit)
            date_time_values.append(last_date_time)
        profits_datetime = {"profits": profits, "datetimes": date_time_values}

        return profits_datetime

    def __get_cost_and_hashrate(self, algorithm_string, graphic_card_string):
        graphic_card_data = self.__get_graphic_card_data(algorithm_string, graphic_card_string)
        if (not graphic_card_data):
            return (None, None)
        cost_per_hashrate_per_second_in_dollar = graphic_card_data[0]["cost_per_second_per_hashrate_per_pricekwh_in_dollar"] * self.price_in_kwh
        hashrate = graphic_card_data[0]["hashrate"]
        return (cost_per_hashrate_per_second_in_dollar, hashrate)

    def __get_graphic_card_data(self, algorithm_string, graphic_card_string):
        if("graphic_card_data" not in self.cache):
            self.cache["graphic_card_data"] = DatabaseAccessor.get_graphic_card_data()
        graphic_card_data = self.cache["graphic_card_data"]

        return list(filter(lambda item: item["algorithm"] == algorithm_string and item["graphic_card"] == graphic_card_string, graphic_card_data))

    def __get_currency_historical_data(self, currency):
        if ((currency) not in self.cache):
            self.cache[(currency)] = DatabaseAccessor.get_currency_historical_data(currency)
        return self.cache[(currency)]
