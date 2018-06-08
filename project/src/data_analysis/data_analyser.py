import datetime

from src.data_analysis.graph_management.graph_manager import GraphManager
from src.data_analysis.preprocessor.info_pre_processor import InfoPreProcessor
from src.variables.variables import Variables
import pandas
import statistics


class DataAnalyser:

    def __init__(self, currencies, graphic_cards, starting_datetime=datetime.datetime(2009, 1, 1), end_datetime=datetime.datetime.now(),
                 fees=0.0, time_unit=datetime.timedelta(days=1), comparison_time_unit=datetime.timedelta(days=30), all_time_unit=[], electricity_cost=Variables.ELECTRICITY_COST, comparison_electricity_cost=Variables.ELECTRICITY_COST,
                 all_electricity_costs=[], only_currency_present_at_start_time=False, only_graphic_cards_present_at_start_time=False):
        self.__check_inputs(starting_datetime, end_datetime, time_unit, comparison_time_unit)
        self.currencies = self.__convert_to_list(currencies)
        self.graphic_cards = self.__convert_to_list(graphic_cards)

        self.starting_datetime = starting_datetime
        self.end_datetime = end_datetime
        self.fees = fees
        self.time_unit = time_unit
        self.comparison_time_unit = comparison_time_unit
        self.all_time_unit = all_time_unit
        self.electricity_cost = electricity_cost
        self.all_electricity_costs = all_electricity_costs
        self.only_currency_present_at_start_time = only_currency_present_at_start_time

        preprocessor = InfoPreProcessor(self.currencies, self.graphic_cards, starting_datetime, end_datetime, fees, time_unit, comparison_time_unit, all_time_unit, electricity_cost,
                                        comparison_electricity_cost, all_electricity_costs, only_currency_present_at_start_time, only_graphic_cards_present_at_start_time)
        all_currencies_graphic_cards_info = preprocessor.currencies_graphic_cards_pre_process()
        self.currencies_graphic_cards_info = all_currencies_graphic_cards_info[1]
        self.graphic_cards_info = preprocessor.graphic_cards_pre_process(all_currencies_graphic_cards_info[0])
        self.general_info = preprocessor.general_pre_process(all_currencies_graphic_cards_info, self.graphic_cards_info)

    def load_histogram_percentage_increase_profit_graphic_cards(self):
        self.__load_histogram_percentage_graphic_cards("percentage_increase_profit")

    def load_histogram_percentage_increase_profit_electricity_cost_graphic_cards(self):
        self.__load_histogram_percentage_graphic_cards("percentage_increase_profit_electricity_cost")

    def __load_histogram_percentage_graphic_cards(self, name_percentage):
        sorted_graphic_cards_info = sorted(self.graphic_cards_info, key=lambda x: x[name_percentage], reverse=True)

        GraphManager.plot_histogram([item["graphic_card"] for item in sorted_graphic_cards_info], [[item[name_percentage] for item in sorted_graphic_cards_info]],
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

    def load_graph_average_profit_per_electricity_cost(self, graphs=True):
        for graphic_card in self.general_info["present_graphic_cards"]:
            current_card_info = [item for item in self.graphic_cards_info if item["graphic_card"] == graphic_card][0]
            labels = "Average profit for each electricity cost"
            title = "Average profit for " + str(graphic_card) + " for each electricity cost for time interval (" + str(self.time_unit) + ") from " + str(self.starting_datetime) + " to " + str(self.end_datetime)
            profits = current_card_info["all_electricity_cost_daily_average_max_profit"]
            if(graphs):
                GraphManager.plot_graph(self.all_electricity_costs, profits, x_label="Electricity cost (in dollar/kwh)", y_label="Average profit per (" + str(self.time_unit) + ") in USD",
                                        title=title, labels=labels)
            else:
                GraphManager.plot_histogram(self.all_electricity_costs, profits, x_label="Electricity cost (in dollar/kwh)", y_label="Average profit per (" + str(self.time_unit) + ") in USD",
                                            title=title, bar_ids=labels, color_per_bar=True)

    def load_graph_average_profit_per_time_unit(self, graphs=True):
        for graphic_card in self.general_info["present_graphic_cards"]:
            current_card_info = [item for item in self.graphic_cards_info if item["graphic_card"] == graphic_card][0]
            labels = "Average profit for each time unit"
            title = "Average profit for " + str(graphic_card) + " for each time unit for electricity cost (" + str(self.electricity_cost) + ") from " + str(self.starting_datetime) + " to " + str(self.end_datetime)
            profits = current_card_info["all_time_unit_daily_average_max_profit"]
            if(graphs):
                GraphManager.plot_graph([item.days for item in self.all_time_unit], profits, x_label="Time unit", y_label="Average profit per (" + str(self.time_unit) + ") in USD",
                                        title=title, labels=labels)
            else:
                GraphManager.plot_histogram([item.days for item in self.all_time_unit], profits, x_label="Time unit", y_label="Average profit per (" + str(self.time_unit) + ") in USD",
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

    def load_standard_deviation_profit_graph_per_graphic_card(self):
        labels = []
        std =[]
        datetimes = []
        for graphic_card in self.general_info["present_graphic_cards"]:
            current_card_info = [item for item in self.graphic_cards_info if item["graphic_card"] == graphic_card][0]
            labels.append(graphic_card)
            title = "Standard deviation for each graphic cards"
            std.append(current_card_info["standard_deviation_profits_datetime"]["standard_deviations"])
            datetimes.append(current_card_info["standard_deviation_profits_datetime"]["datetimes"])
        GraphManager.plot_graph(datetimes, std, x_label="Time", y_label="Profit Standard deviation", title=title, labels=labels)

    def display_loaded_graph(self):
        GraphManager.show()

    def calculate_pearson_correlation_max_profits(self, mean=True, median=True):
        profits = [item["max_profits_datetime"]["profits"] for item in self.graphic_cards_info]
        columns = [item["graphic_card"] for item in self.graphic_cards_info]
        inverted_profits = list(zip(*profits))

        self.__pearson_correlation(inverted_profits, "max profit\\max_profit", columns=columns, mean=mean, median=median)

    def calculate_pearson_correlation_between_currencies_per_graphic_card(self, mean=True, median=True):
        for graphic_card in self.general_info["present_graphic_cards"]:
            filtered_list = list(filter(lambda x: x["graphic_card"] == graphic_card, self.currencies_graphic_cards_info))
            labels = [str(item["currency"]) for item in filtered_list]
            profits = [item["profits_datetime"]["profits"] for item in filtered_list]
            inverted_profits = list(zip(*profits))

            self.__pearson_correlation(inverted_profits, "currencies per graphic card\\" + str(graphic_card), columns=labels, mean=mean, median=median)

    def calculate_pearson_correlation_between_graphic_card_per_currency(self, mean=True, median=True):
        for currency in self.general_info["present_currencies"]:
            filtered_list = list(filter(lambda x: x["currency"] == currency, self.currencies_graphic_cards_info))
            labels = [str(item["graphic_card"]) for item in filtered_list]
            profits = [item["profits_datetime"]["profits"] for item in filtered_list]
            inverted_profits = list(zip(*profits))

            self.__pearson_correlation(inverted_profits, "graphic cards per currency\\" + str(currency), columns=labels, mean=mean, median=median)


    def __pearson_correlation(self, data, file_name, columns=None, mean=True, median=True):
        data = pandas.DataFrame(data, columns=columns)
        corr = data.corr()
        print(file_name)
        print(corr)
        if(mean):
            print("Mean")
            print(corr.mean())
        if(median):
            print("Median")
            print(corr.median())
        print()
        data.corr().to_csv("..\\..\\..\\graphs\\pearson correlation coefficent\\" + file_name + ".csv")

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

    def __check_inputs(self, starting_datetime, end_datetime, time_unit, comparison_time_unit):
        if(starting_datetime >= end_datetime):
            raise Exception("The starting time should be smaller than the end time")
        if(time_unit >= comparison_time_unit):
            raise Exception("The base time unit time should be smaller than the comparison time unit")





