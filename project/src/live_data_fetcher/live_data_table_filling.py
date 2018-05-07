from src.database_accessor.database_accessor import DatabaseAccessor
from src.graphic_cards.graphic_cards import GraphicCards
from src.live_data_fetcher.live_data_fetcher import LiveDataFetcher


class LiveDataTableFilling():

    def __init__(self):
        self.db = DatabaseAccessor()
        self.live_data_fetcher = LiveDataFetcher()

    def create_all_table(self):
        graphic_cards = [item for item in GraphicCards]
        for graphic_card in graphic_cards:
            self.db.create_graphic_card_table(graphic_card)

    def fill_all_tables(self):
        graphic_cards = [item for item in GraphicCards]
        for graphic_card in graphic_cards:
            ordered_profits = self.live_data_fetcher.compute_live_profit(graphic_card)
            self.__fill_live_data_table(graphic_card, ordered_profits)

    def __fill_live_data_table(self, graphic_card, ordered_profits):
        self.db.truncate_table(str(graphic_card) + "_live_data")
        for i in range(len(ordered_profits)):
            currency = ordered_profits[i][0]
            profit_per_second = ordered_profits[i][1]
            self.db.update_live_data(currency, graphic_card, profit_per_second, profit_per_second * 3600 * 24, i + 1)
