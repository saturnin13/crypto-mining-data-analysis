import datetime

from src.currencies.currencies import Currencies
from src.data_analysis.data_analyser import DataAnalyser
from src.graphic_cards.graphic_cards import GraphicCards

data_analyser = DataAnalyser([currency for currency in Currencies], [GraphicCards.GTX_750_TI, GraphicCards.GTX_1070_TI], starting_datetime=datetime.datetime(2015, 4, 18), time_unit=datetime.timedelta(days=1))

data_analyser.load_histograms_max_profit_graphic_cards(graphs=False)
data_analyser.display_loaded_graph()

data_analyser.load_histogram_total_max_profit_graphic_cards()
data_analyser.load_3dhistogram_average_profit()
data_analyser.load_3dhistogram_instant_profit()
data_analyser.display_loaded_graph()

data_analyser.load_profit_graphs_graphic_cards()
data_analyser.display_loaded_graph()