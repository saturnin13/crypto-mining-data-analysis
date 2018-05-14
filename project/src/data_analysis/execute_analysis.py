import datetime

from src.currencies.currencies import Currencies
from src.data_analysis.data_analyser import DataAnalyser
from src.graphic_cards.graphic_cards import GraphicCards

data_analyser2 = DataAnalyser([item for item in Currencies],[item for item in GraphicCards], starting_datetime=datetime.datetime(2016, 1, 1), end_datetime=datetime.datetime.now(),
                              time_unit=datetime.timedelta(days=1), comparison_time_unit=datetime.timedelta(days=20), price_in_kwh=0.13, only_currency_present_at_start_time=True,
                              only_graphic_cards_present_at_start_time=True)


data_analyser2.load_profit_graphs_graphic_cards()
data_analyser2.display_loaded_graph()

data_analyser2.load_histograms_max_profit_graphic_cards(graphs=False)
data_analyser2.display_loaded_graph()

data_analyser2.load_3dhistogram_average_profit()
data_analyser2.load_3dhistogram_instant_profit()
data_analyser2.display_loaded_graph()

data_analyser2.load_histogram_total_max_profit_graphic_cards()
data_analyser2.display_loaded_graph()

data_analyser2.load_histogram_percentage_increase_profit_graphic_cards()
data_analyser2.display_loaded_graph()