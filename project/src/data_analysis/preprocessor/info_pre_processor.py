import datetime

from src.data_analysis.preprocessor.currencies_graphic_cards_info_pre_processor import CurrenciesGraphicCardsInfoPreProcessor
from src.data_analysis.preprocessor.general_info_pre_processor import GeneralInfoPreProcessor
from src.data_analysis.preprocessor.graphic_cards_pre_processor import GraphicCardsInfoPreProcessor
from src.variables.variables import Variables


class InfoPreProcessor:
    def __init__(self, currencies, graphic_cards, starting_datetime=datetime.datetime(2009, 1, 1), end_datetime=datetime.datetime.now(), fees=0.0,
                 time_unit=datetime.timedelta(days=1), comparison_time_unit=datetime.timedelta(days=30), all_time_unit=[], electricity_cost=Variables.ELECTRICITY_COST, comparison_electricity_cost=Variables.ELECTRICITY_COST,
                 all_electricity_costs=[], only_currency_present_at_start_time=False, only_graphic_cards_present_at_start_time=False):
        self.currencies = currencies
        self.graphic_cards = graphic_cards
        self.starting_datetime = starting_datetime
        self.end_datetime = end_datetime
        self.fees = fees
        self.time_unit = time_unit
        self.comparison_time_unit = comparison_time_unit
        self.only_currency_present_at_start_time = only_currency_present_at_start_time
        self.only_graphic_cards_present_at_start_time = only_graphic_cards_present_at_start_time

        self.currencies_graphic_cars_preprocessor = CurrenciesGraphicCardsInfoPreProcessor(currencies, graphic_cards, starting_datetime, end_datetime,
                                                                                           fees, time_unit, comparison_time_unit, all_time_unit, electricity_cost, comparison_electricity_cost,
                                                                                           all_electricity_costs, only_currency_present_at_start_time, only_graphic_cards_present_at_start_time)
        self.currencies_preprocessor = GraphicCardsInfoPreProcessor(currencies, graphic_cards, starting_datetime, end_datetime, fees, time_unit, comparison_time_unit, all_time_unit)
        self.general_preprocessor = GeneralInfoPreProcessor(currencies, graphic_cards, starting_datetime, end_datetime, fees, time_unit)

    def currencies_graphic_cards_pre_process(self):
        return self.currencies_graphic_cars_preprocessor.preprocess()

    def graphic_cards_pre_process(self, currency_graphic_card_info):
        return self.currencies_preprocessor.preprocess(currency_graphic_card_info)

    def general_pre_process(self, currency_graphic_card_info, graphic_card_info):
        return self.general_preprocessor.preprocess(currency_graphic_card_info, graphic_card_info)

