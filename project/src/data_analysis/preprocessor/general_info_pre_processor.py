import datetime


class GeneralInfoPreProcessor:
    def __init__(self, currencies, graphic_cards, starting_datetime=datetime.datetime(2009, 1, 1), end_datetime=datetime.datetime.now(), fees=0.0,
                 time_unit=datetime.timedelta(days=1)):
        self.currencies = currencies
        self.graphic_cards = graphic_cards
        self.starting_datetime = starting_datetime
        self.end_datetime = end_datetime
        self.fees = fees
        self.time_unit = time_unit

    def preprocess(self, currency_graphic_card_info, graphic_card_info):
        print("Preprocessing general information")

        info = {}
        info["present_currencies"] = self.__calculate_present_currencies(currency_graphic_card_info)
        info["present_graphic_cards"] = self.__calculate_present_graphic_cards(currency_graphic_card_info)

        if(not info["present_currencies"]):
            raise Exception("No currencies present")

        if (not info["present_graphic_cards"]):
            raise Exception("No graphic cards present")

        return info

    def __calculate_present_currencies(self, currency_graphic_card_info):
        return list(set([item["currency"] for item in currency_graphic_card_info]))

    def __calculate_present_graphic_cards(self, currency_graphic_card_info):
        return list(set([item["graphic_card"] for item in currency_graphic_card_info]))