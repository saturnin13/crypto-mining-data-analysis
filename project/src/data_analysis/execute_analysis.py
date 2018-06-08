import datetime


from src.currencies.currencies import Currencies
from src.data_analysis.data_analyser import DataAnalyser
from src.graphic_cards.graphic_cards import GraphicCards

data_analyser2 = DataAnalyser([item for item in Currencies], [item for item in GraphicCards], starting_datetime=datetime.datetime(2017, 1, 1), end_datetime=datetime.datetime.now(),
                              fees=0.02, time_unit=datetime.timedelta(days=1), comparison_time_unit=datetime.timedelta(days=20),
                              all_time_unit=[datetime.timedelta(days=item) for item in list(range(1, 1))],
                              electricity_cost=0.13, comparison_electricity_cost=0.26,
                              all_electricity_costs=[item / 20 for item in range(1, 1)], only_currency_present_at_start_time=True, only_graphic_cards_present_at_start_time=True)

# data_analyser2.calculate_pearson_correlation_max_profits(mean=True, median=True)
# data_analyser2.calculate_pearson_correlation_between_graphic_card_per_currency(mean=True, median=True)
#
# data_analyser2.load_standard_deviation_profit_graph_per_graphic_card()
# data_analyser2.display_loaded_graph()
#
# data_analyser2.load_profit_graphs_graphic_cards()
# data_analyser2.display_loaded_graph()
#
# data_analyser2.load_histograms_max_profit_graphic_cards(graphs=False)
# data_analyser2.display_loaded_graph()
#
# data_analyser2.load_3dhistogram_average_profit()
# data_analyser2.load_3dhistogram_instant_profit()
# data_analyser2.display_loaded_graph()
#
# data_analyser2.load_histogram_total_max_profit_graphic_cards()
# data_analyser2.display_loaded_graph()
#
# data_analyser2.load_histogram_percentage_increase_profit_graphic_cards()
# data_analyser2.display_loaded_graph()
#
data_analyser2.load_histogram_percentage_increase_profit_electricity_cost_graphic_cards()
data_analyser2.display_loaded_graph()
#
# data_analyser2.load_graph_average_profit_per_electricity_cost(graphs=True)
# data_analyser2.display_loaded_graph()
#
# data_analyser2.load_graph_average_profit_per_time_unit(graphs=True)
# data_analyser2.display_loaded_graph()