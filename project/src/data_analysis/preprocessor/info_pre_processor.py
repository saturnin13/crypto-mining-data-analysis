import datetime

from src.data_analysis.preprocessor.currencies_graphic_cards_info_pre_processor import CurrenciesGraphicCardsInfoPreProcessor
from src.data_analysis.preprocessor.graphic_cards_pre_processor import GraphicCardsInfoPreProcessor
from src.variables.variables import Variables


class InfoPreProcessor:
    def __init__(self, currencies, graphic_cards, starting_datetime=datetime.datetime(2009, 1, 1), end_datetime=datetime.datetime.now(), fees=0.0,
                 time_unit=datetime.timedelta(days=1), price_in_kwh=Variables.ELECTRICITY_COST):
        self.currencies = currencies
        self.graphic_cards = graphic_cards
        self.starting_datetime = starting_datetime
        self.end_datetime = end_datetime
        self.fees = fees
        self.time_unit = time_unit

        self.currencies_graphic_cars_preprocessor = CurrenciesGraphicCardsInfoPreProcessor(currencies, graphic_cards, starting_datetime, end_datetime, fees, time_unit, price_in_kwh)
        self.currencies_preprocessor = GraphicCardsInfoPreProcessor(currencies, graphic_cards, starting_datetime, end_datetime, fees, time_unit)

    def currencies_graphic_cards_pre_process(self):
        return self.currencies_graphic_cars_preprocessor.preprocess()

    def graphic_cards_pre_process(self, currency_graphic_card_info):
        return self.currencies_preprocessor.preprocess(currency_graphic_card_info)

