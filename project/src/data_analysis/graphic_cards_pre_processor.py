import datetime
from operator import itemgetter

from src.currencies.currencies import Currencies
from src.graphic_cards.graphic_cards import GraphicCards


class GraphicCardsInfoPreProcessor:
    def __init__(self, currencies, graphic_cards, starting_datetime=datetime.datetime(2009, 1, 1), end_datetime=datetime.datetime.now(), fees=0.0,
                 time_unit=datetime.timedelta(days=1)):
        self.currencies = currencies
        self.graphic_cards = graphic_cards
        self.starting_datetime = starting_datetime
        self.end_datetime = end_datetime
        self.fees = fees
        self.time_unit = time_unit

    def preprocess(self, currency_graphic_card_info):
        print("Preprocessing information per graphic cards")
        info = []

        for graphic_card in self.graphic_cards:
            current = {}
            filtered_list = list(filter(lambda x: x["graphic_card"] == graphic_card, currency_graphic_card_info))
            current["max_profits_datetime"] = self.__calculate_max_profits_datetime(filtered_list)
            current["total_max_profit"] = self.__calculate_total_max_profit(current["max_profits_datetime"])
            current["graphic_card"] = graphic_card
            info.append(current)

        return info

    def __calculate_max_profits_datetime(self, filtered_list):
        profits = []
        datetimes = []
        currencies = []
        for item in filtered_list:
            profits += item["profits_datetime"]["profits"]
            datetimes += item["profits_datetime"]["datetimes"]
            currencies += [item["currency"]] * len(item["profits_datetime"]["profits"])

        distinct_datetimes = set(datetimes)
        result = {}
        result["profits"] = []
        result["datetimes"] = []
        result["currencies"] = []
        for date_time in distinct_datetimes:
            indices = [i for i, x in enumerate(datetimes) if x == date_time]
            max_index = None
            max_value = None
            for i in indices:
                if not max_value or profits[i] >= max_value:
                    max_index = i
                    max_value = profits[i]
            result["profits"].append(profits[max_index])
            result["datetimes"].append(datetimes[max_index])
            result["currencies"].append(currencies[max_index])

        result["datetimes"], result["profits"], result["currencies"] = zip(*sorted(zip(result["datetimes"], result["profits"],result["currencies"]), key=lambda x: x[0]))

        return result

    def __calculate_total_max_profit(self, max_profits_datetime):
        return sum(max_profits_datetime["profits"])


