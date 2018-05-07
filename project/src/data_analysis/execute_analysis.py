import datetime

from src.currencies.currencies import Currencies
from src.data_analysis.data_analyser import DataAnalyser
from src.graphic_cards.graphic_cards import GraphicCards

data_analyser = DataAnalyser([item for item in Currencies], [item for item in GraphicCards], starting_datetime=datetime.datetime(2017, 1, 1), end_datetime=datetime.datetime(2018, 1, 1),
                             time_unit=datetime.timedelta(days=1), price_in_kwh=0.13)

data_analyser.load_profit_graphs_graphic_cards()
data_analyser.display_loaded_graph()

data_analyser.load_histograms_max_profit_graphic_cards(graphs=False)
data_analyser.display_loaded_graph()

data_analyser.load_histogram_total_max_profit_graphic_cards()
data_analyser.load_3dhistogram_average_profit()
data_analyser.load_3dhistogram_instant_profit()
data_analyser.display_loaded_graph()
