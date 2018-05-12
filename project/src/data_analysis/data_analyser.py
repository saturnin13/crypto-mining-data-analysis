import datetime

from src.data_analysis.graph_management.graph_manager import GraphManager
from src.data_analysis.preprocessor.info_pre_processor import InfoPreProcessor
from src.variables.variables import Variables


class DataAnalyser:

    def __init__(self, currencies, graphic_cards, starting_datetime=datetime.datetime(2009, 1, 1), end_datetime=datetime.datetime.now(),
                 fees=0.0, time_unit=datetime.timedelta(days=1), price_in_kwh=Variables.ELECTRICITY_COST, only_currency_present_at_start_time=False,
                 only_graphic_cards_present_at_start_time=False):
        self.__check_inputs(starting_datetime, end_datetime)
        self.currencies = self.__convert_to_list(currencies)
        self.graphic_cards = self.__convert_to_list(graphic_cards)

        self.starting_datetime = starting_datetime
        self.end_datetime = end_datetime
        self.fees = fees
        self.time_unit = time_unit
        self.only_currency_present_at_start_time = only_currency_present_at_start_time

        preprocessor = InfoPreProcessor(self.currencies, self.graphic_cards, starting_datetime, end_datetime, fees, time_unit, price_in_kwh, only_currency_present_at_start_time,
                                        only_graphic_cards_present_at_start_time)
        all_currencies_graphic_cards_info = preprocessor.currencies_graphic_cards_pre_process()
        self.currencies_graphic_cards_info = all_currencies_graphic_cards_info[1] if only_currency_present_at_start_time else all_currencies_graphic_cards_info[0]
        self.graphic_cards_info = preprocessor.graphic_cards_pre_process(all_currencies_graphic_cards_info)
        self.general_info = preprocessor.general_pre_process(self.currencies_graphic_cards_info, self.graphic_cards_info)

    def load_histogram_percentage_increase_profit_graphic_cards(self):
        sorted_graphic_cards_info = sorted(self.graphic_cards_info, key=lambda x: x["percentage_increase_profit"], reverse=True)

        GraphManager.plot_histogram([item["graphic_card"] for item in sorted_graphic_cards_info], [[item["percentage_increase_profit"] for item in sorted_graphic_cards_info]],
                                    x_label="Graphic card", y_label="percentage increase profit",
                                    title="Percentage increase profit in dollar for max profit for time interval (" + str(self.starting_datetime) + " to " + str(
                                        self.end_datetime) + ")",
                                    color_per_bar=False)

    def load_histogram_total_max_profit_graphic_cards(self):
        sorted_graphic_cards_info = sorted(self.graphic_cards_info, key=lambda x: x["total_max_profit"], reverse=True)
        Y = [[item["total_max_profit"] for item in sorted_graphic_cards_info]]
        total_profits_extrapolated = self.__get_graphic_cards_total_profits_extrapolated(self.general_info["present_currencies"], [item["graphic_card"] for item in sorted_graphic_cards_info])
        Y += [item["total_profits"] for item in total_profits_extrapolated]
        labels = ["total_max_profit"] + [item["currency"] for item in total_profits_extrapolated]

        GraphManager.plot_histogram([item["graphic_card"]for item in sorted_graphic_cards_info], Y, labels=labels,
                                    x_label="Graphic card", y_label="profit in dollar",
                                    title="Total profit in dollar for max profit for time interval (" + str(self.starting_datetime) + " to " + str(self.end_datetime) + ")",
                                    color_per_bar=False)

    def __get_graphic_cards_total_profits_extrapolated(self, currencies_ordered, graphic_cards_ordered):
        total_profits_extrapolated = []
        for currency in currencies_ordered:
            current_total_profit_extrapolated = []
            for graphic_card in graphic_cards_ordered:
                sorted_currency_graphic_card_info = list(filter(lambda x: x["currency"] == currency and x["graphic_card"] == graphic_card, self.currencies_graphic_cards_info))
                if(sorted_currency_graphic_card_info):
                    current_total_profit_extrapolated.append(sorted_currency_graphic_card_info[0]["total_profit_extrapolated"])
                else:
                    current_total_profit_extrapolated.append(0)
            total_profits_extrapolated.append({"currency":currency, "total_profits":current_total_profit_extrapolated})

        return sorted(total_profits_extrapolated, key=lambda x: sum(x["total_profits"]), reverse=True)


    def load_histograms_max_profit_graphic_cards(self, graphs=False):
        for graphic_card in self.general_info["present_graphic_cards"]:
            current_card_info = [item for item in self.graphic_cards_info if item["graphic_card"] == graphic_card][0]
            labels = [str(item) for item in current_card_info["max_profits_datetime"]["currencies"]]
            title = "Max profit for " + str(graphic_card) + " with currencies " + str(set(labels)) + " for time interval (" + str(self.time_unit) + ") (legend is ordered)"
            profits = current_card_info["max_profits_datetime"]["profits"]
            datetimes = current_card_info["max_profits_datetime"]["datetimes"]
            if(graphs):
                GraphManager.plot_graph(datetimes, profits, x_label="Time", y_label="Max profit per (" + str(self.time_unit) + ") in USD",
                                        title=title, labels=labels)
            else:
                GraphManager.plot_histogram(datetimes, profits, x_label="Time", y_label="Max profit per (" + str(self.time_unit) + ") in USD",
                                            title=title, bar_ids=labels, color_per_bar=True)

    def load_3dhistogram_average_profit(self):
        self.__display_3dhistogram_value("average_profit")

    def load_3dhistogram_instant_profit(self):
        self.__display_3dhistogram_value("instant_profit")

    def load_profit_graphs_graphic_cards(self):
        for graphic_card in self.general_info["present_graphic_cards"]:
            filtered_list = list(filter(lambda x: x["graphic_card"] == graphic_card, self.currencies_graphic_cards_info))
            labels = [str(item["currency"]) for item in filtered_list]
            title = str(graphic_card)
            profits = [item["profits_datetime"]["profits"] for item in filtered_list]
            datetimes = [item["profits_datetime"]["datetimes"] for item in filtered_list]
            GraphManager.plot_graph(datetimes, profits, x_label="Time", y_label="Profit per (" + str(self.time_unit) + ") per hashrate in USD",
                                    title=title, labels=labels)

    def display_loaded_graph(self):
        GraphManager.show()

    def __display_3dhistogram_value(self, value_string):
        title = value_string.title() + " per (" + str(self.time_unit) +") extrapolated from past data for currency and graphic card pairs for the time interval " + str(self.starting_datetime) + " to " + str(self.end_datetime)
        GraphManager.plot_3d_histogram([row["currency"] for row in self.currencies_graphic_cards_info],
                                       [row["graphic_card"] for row in self.currencies_graphic_cards_info],
                                       [row[value_string] for row in self.currencies_graphic_cards_info], title=title)

    def __convert_to_list(self, item):
        if (type(item) != list):
            return [item]
        else:
            return item

    def __check_inputs(self, starting_datetime, end_datetime):
        if(starting_datetime >= end_datetime):
            raise Exception("The starting time should be smaller than the end time")
