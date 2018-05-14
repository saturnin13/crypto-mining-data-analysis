import datetime

from src.currencies.currencies import Currencies
from src.database_accessor.database_accessor import DatabaseAccessor
from src.profit_logic.profit_calculation import ProfitCalculation
from src.utils.utils import Utils
from src.variables.variables import Variables


class CurrenciesGraphicCardsInfoPreProcessor:
    def __init__(self, currencies, graphic_cards, starting_datetime=datetime.datetime(2009, 1, 1), end_datetime=datetime.datetime.now(), fees=0.0,
                 time_unit=datetime.timedelta(days=1), comparison_time_unit=datetime.timedelta(days=30), price_in_kwh=Variables.ELECTRICITY_COST, only_currency_present_at_start_time=False,
                 only_graphic_cards_present_at_start_time=False):
        self.cache = {}

        self.currencies = currencies
        self.graphic_cards = graphic_cards
        self.starting_datetime = starting_datetime
        self.end_datetime = end_datetime
        self.fees = fees
        self.time_unit = time_unit
        self.comparison_time_unit = comparison_time_unit
        self.only_currency_present_at_start_time = only_currency_present_at_start_time
        self.only_graphic_cards_present_at_start_time = only_graphic_cards_present_at_start_time

        self.price_in_kwh = price_in_kwh

    def preprocess(self):
        print("Preprocessing information per graphic cards and currencies")

        info_all = []

        for graphic_card in self.graphic_cards:
            for currency in self.currencies:
                current = {}
                current["profits_datetime"] = self.__calculate_profits_datetime(currency, graphic_card, self.time_unit)
                current["profits_datetime_comparison_time_unit"] = self.__calculate_profits_datetime(currency, graphic_card, self.comparison_time_unit)
                if(current["profits_datetime"] and current["profits_datetime"]["profits"]):
                    current["average_profit"] = self.__calculate_average_profit(current["profits_datetime"]["profits"])
                    current["total_profit_extrapolated"] = self.__calculate_total_profit_extrapolated(current["average_profit"], self.time_unit)
                    current["instant_profit"] = self.__calculate_instant_profit(current["profits_datetime"])

                    current["currency"]       = currency
                    current["graphic_card"]   = graphic_card

                    info_all.append(current)
        info_all_currency_present_at_start_time = list(filter(lambda x: not self.only_currency_present_at_start_time or self.__currency_present_at_start_time(x["currency"]), info_all))
        return info_all, info_all_currency_present_at_start_time

    def __calculate_total_profit_extrapolated(self, average_profit, time_unit):
        number_of_time_unit = int((self.end_datetime.timestamp() - self.starting_datetime.timestamp()) / time_unit.total_seconds())
        return average_profit * number_of_time_unit

    def __calculate_instant_profit(self, profits_datetime):
        date_time = profits_datetime["datetimes"]
        index = date_time.index(min(date_time, key=lambda d: abs(d - datetime.datetime.now())))
        return profits_datetime["profits"][index]

    def __calculate_average_profit(self, profits):
        return sum(profits) / len(profits)

    def __calculate_profits_datetime(self, currency, graphic_card, time_unit):
        currency_historical_data = self.__get_currency_historical_data(currency)
        currency_historical_data = list(filter(lambda x: x["datetime"] and x["datetime"] >= self.starting_datetime and x["datetime"] <= self.end_datetime
                                                         and x["revenue_per_second_per_hashrate_in_dollar"], currency_historical_data))
        currency_historical_data = sorted(currency_historical_data, key=lambda x: x["datetime"])

        cost_per_hashrate_per_second_in_dollar, hashrate = self.__get_cost_and_hashrate(currency.get_algorithm().value, graphic_card.value)
        if(not cost_per_hashrate_per_second_in_dollar or not hashrate):
            return None

        profits, date_time_values = self.__calculate_profits_datetime_helper(currency_historical_data, cost_per_hashrate_per_second_in_dollar, hashrate, time_unit)
        profits_datetime = {"profits": profits, "datetimes": date_time_values}

        return profits_datetime

    def __calculate_profits_datetime_helper(self, currency_historical_data, cost_per_hashrate_per_second_in_dollar, hashrate, time_unit):
        profits = []
        date_time_values = []
        current_sum_revenue, revenue_count = 0, 0
        datetime_lower_limit = self.starting_datetime
        while(datetime_lower_limit < currency_historical_data[0]["datetime"]):
            datetime_lower_limit += time_unit
        for i in range(len(currency_historical_data)):
            revenue_per_hashrate_per_second_in_dollar = currency_historical_data[i]["revenue_per_second_per_hashrate_in_dollar"]
            new_date_time = currency_historical_data[i]["datetime"]
            if (revenue_per_hashrate_per_second_in_dollar is None or new_date_time is None or new_date_time < datetime_lower_limit):
                continue
            if (new_date_time >= datetime_lower_limit + time_unit):
                if(revenue_count != 0):
                    profit = ProfitCalculation.calculate_profit(current_sum_revenue / revenue_count, cost_per_hashrate_per_second_in_dollar, hashrate,
                                                                time_unit, self.fees)
                    profits.append(profit)
                    date_time_values.append(datetime_lower_limit)
                datetime_lower_limit += time_unit
                current_sum_revenue, revenue_count = 0, 0
            current_sum_revenue += revenue_per_hashrate_per_second_in_dollar
            revenue_count += 1
        return profits, date_time_values

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

        for row in graphic_card_data:
            if(self.only_graphic_cards_present_at_start_time and not self.__graphic_card_present_at_start_time(row)):
                graphic_card_data.remove(row)

        return list(filter(lambda item: item["algorithm"] == algorithm_string and item["graphic_card"] == graphic_card_string, graphic_card_data))

    def __get_currency_historical_data(self, currency):
        if ((currency) not in self.cache):
            self.cache[(currency)] = DatabaseAccessor.get_currency_historical_data(currency)
        return self.cache[(currency)]

    def __currency_present_at_start_time(self, currency):
        currency_historical_data = [item["datetime"] for item in self.__get_currency_historical_data(currency)]
        return min(currency_historical_data) <= self.starting_datetime

    def __graphic_card_present_at_start_time(self, graphic_card_data):
        return graphic_card_data["release_date"] <= self.starting_datetime
