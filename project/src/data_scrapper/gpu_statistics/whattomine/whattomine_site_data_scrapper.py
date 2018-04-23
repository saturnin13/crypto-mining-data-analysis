from src.currencies.algorithms import Algorithms
from src.data_scrapper.gpu_statistics.generic_gpu_statistics_data_scrapper import GenericGpuStatisticsDataScrapper
from src.graphic_cards.graphic_cards import GraphicCards
from src.regex.constant_regex import ConstantRegex
from src.variables.variables import Variables


class WhattomineDataScrapper(GenericGpuStatisticsDataScrapper):

    def _get_regex_patterns(self, id):
        graphic_card = id["graphic_card"]
        return  ["(?P<" + str(graphic_card) + ">" + str(self.__convert_to_graphic_card_identifier(graphic_card)) + ")={" \
                "\"#factor_bk2b_hr\":"      + ConstantRegex.NUMBER            + "," \
                "\"#factor_x11g_hr\":(?P<"  + str(Algorithms.X11GOST)        + "_hashrate>" + ConstantRegex.NUMBER + ")," \
                "\"#factor_gro_hr\":(?P<"   + str(Algorithms.GROESTL)        + "_hashrate>" + ConstantRegex.NUMBER + ")," \
                "\"#factor_cn_hr\":(?P<"    + str(Algorithms.CRYPTONIGHT)    + "_hashrate>" + ConstantRegex.NUMBER + ")," \
                "\"#factor_ns_hr\":(?P<"    + str(Algorithms.NEOSCRYPT)      + "_hashrate>" + ConstantRegex.NUMBER + ")," \
                "\"#factor_lrev2_hr\":(?P<" + str(Algorithms.LYRA2REV2)      + "_hashrate>" + ConstantRegex.NUMBER + ")," \
                "\"#factor_n5_hr\":(?P<"    + str(Algorithms.NIST5)          + "_hashrate>" + ConstantRegex.NUMBER + ")," \
                "\"#factor_tt10_hr\":(?P<"  + str(Algorithms.TIMETRAVEL10)   + "_hashrate>" + ConstantRegex.NUMBER + ")," \
                "\"#factor_eq_hr\":(?P<"    + str(Algorithms.EQUIHASH)       + "_hashrate>" + ConstantRegex.NUMBER + ")," \
                "\"#factor_eth_hr\":(?P<"   + str(Algorithms.ETHASH)         + "_hashrate>" + ConstantRegex.NUMBER + ")," \
                "\"#factor_cn7_hr\":(?P<"   + str(Algorithms.CRYPTONIGHTV7)  + "_hashrate>" + ConstantRegex.NUMBER + ")," \
                "\"#factor_bk2b_p\":"       + ConstantRegex.NUMBER            + "," \
                "\"#factor_x11g_p\":(?P<"   + str(Algorithms.X11GOST)        + "_watt>"     + ConstantRegex.NUMBER + ")," \
                "\"#factor_gro_p\":(?P<"    + str(Algorithms.GROESTL)        + "_watt>"     + ConstantRegex.NUMBER + ")," \
                "\"#factor_cn_p\":(?P<"     + str(Algorithms.CRYPTONIGHT)    + "_watt>"     + ConstantRegex.NUMBER + ")," \
                "\"#factor_ns_p\":(?P<"     + str(Algorithms.NEOSCRYPT)      + "_watt>"     + ConstantRegex.NUMBER + ")," \
                "\"#factor_lrev2_p\":(?P<"  + str(Algorithms.LYRA2REV2)      + "_watt>"     + ConstantRegex.NUMBER + ")," \
                "\"#factor_n5_p\":(?P<"     + str(Algorithms.NIST5)          + "_watt>"     + ConstantRegex.NUMBER + ")," \
                "\"#factor_tt10_p\":(?P<"   + str(Algorithms.TIMETRAVEL10)   + "_watt>"     + ConstantRegex.NUMBER + ")," \
                "\"#factor_eq_p\":(?P<"     + str(Algorithms.EQUIHASH)       + "_watt>"     + ConstantRegex.NUMBER + ")," \
                "\"#factor_eth_p\":(?P<"    + str(Algorithms.ETHASH)         + "_watt>"     + ConstantRegex.NUMBER + ")," \
                "\"#factor_cn7_p\":(?P<"    + str(Algorithms.CRYPTONIGHTV7)  + "_watt>"     + ConstantRegex.NUMBER + ")," \
                "\"#factor_x16r_hr\":(?P<"  + str(Algorithms.X16R)           + "_hashrate>" + ConstantRegex.NUMBER + ")," \
                "\"#factor_x16r_p\":(?P<"   + str(Algorithms.X16R)           + "_watt>"     + ConstantRegex.NUMBER + ")," \
                "\"#factor_skh_hr\":(?P<"   + str(Algorithms.SKUNKHASH)      + "_hashrate>" + ConstantRegex.NUMBER + ")," \
                "\"#factor_skh_p\":(?P<"    + str(Algorithms.SKUNKHASH)      + "_watt>"     + ConstantRegex.NUMBER + ")," \
                "\"#factor_xn_hr\":(?P<"    + str(Algorithms.XEVAN)          + "_hashrate>" + ConstantRegex.NUMBER + ")," \
                "\"#factor_xn_p\":(?P<"     + str(Algorithms.XEVAN)          + "_watt>"     + ConstantRegex.NUMBER + ")" \
                "}"]

    def _get_extra_group_names(self, id):
        graphic_card_group_name = str(id["graphic_card"])
        return graphic_card_group_name

    def _relevant_id_keys_for_group_names(self, id):
        return ["algorithm"]

    def _post_processing_single_result(self, id, result):
        algorithm = id["algorithm"]
        graphic_card = id["graphic_card"]

        result["watt"] = result.pop(str(algorithm) + "_watt")
        result["hashrate"] = float(result.pop(str(algorithm) + "_hashrate")) * self.__scaling_hashrate(algorithm)

        if(float(result["watt"]) == 0 or float(result["hashrate"]) == 0):
            return None

        result[graphic_card.value.replace(" ", "_")] = graphic_card.value
        result["graphic_card"] = result.pop(graphic_card.value.replace(" ", "_"))

        result["algorithm"] = algorithm.value
        result["source"] = "http://whattomine.com/coins"

        self.__add_experiment_details(graphic_card, result)
        return result

    def _get_primary_url(self, id):
        return "http://whattomine.com/assets/application-27ffa286a83500f0c94d483f3ed80536b84425d124bf172ad94297fa176bee4c.js"

    def _extract_cache_hash(self, id):
        return 1

    def _post_processing_page_loading(self, url_content, id):
        return url_content

    def __convert_to_graphic_card_identifier(self, graphic_card):
        if(graphic_card == GraphicCards.AMD_280X):
            return "u"
        elif(graphic_card == GraphicCards.AMD_380):
            return "h"
        elif (graphic_card == GraphicCards.AMD_FURY):
            return "m"
        elif (graphic_card == GraphicCards.AMD_470):
            return "f"
        elif (graphic_card == GraphicCards.AMD_480):
            return "d"
        elif (graphic_card == GraphicCards.AMD_570):
            return "p"
        elif (graphic_card == GraphicCards.AMD_580):
            return "_"
        elif (graphic_card == GraphicCards.AMD_VEGA_56):
            return "v"
        elif (graphic_card == GraphicCards.AMD_VEGA_64):
            return "y"
        elif (graphic_card == GraphicCards.GTX_750_TI):
            return "g"
        elif (graphic_card == GraphicCards.GTX_1050_TI):
            return "r"
        elif (graphic_card == GraphicCards.GTX_1060):
            return "o"
        elif (graphic_card == GraphicCards.GTX_1070):
            return "s"
        elif (graphic_card == GraphicCards.GTX_1070_TI):
            return "a"
        elif (graphic_card == GraphicCards.GTX_1080):
            return "l"
        elif (graphic_card == GraphicCards.GTX_1080_TI):
            return "c"

    def __convert_from_graphic_card_identifier(self, graphic_card_identifier):
        for graphic_card in GraphicCards:
            if(self.__convert_to_graphic_card_identifier(graphic_card) == graphic_card_identifier):
                return graphic_card

    def __add_experiment_details(self, graphic_card, graphic_card_hashrate_watt):
        if (graphic_card == GraphicCards.AMD_280X):
            graphic_card_hashrate_watt["core"] = 1100
            graphic_card_hashrate_watt["memory"] = 1500
            graphic_card_hashrate_watt["voltage_millivolt"] = -100
        elif (graphic_card == GraphicCards.AMD_380):
            graphic_card_hashrate_watt["core"] = 1000
            graphic_card_hashrate_watt["memory"] = 1500
            graphic_card_hashrate_watt["voltage_millivolt"] = -100
        elif (graphic_card == GraphicCards.AMD_FURY):
            graphic_card_hashrate_watt["core"] = 1020
            graphic_card_hashrate_watt["memory"] = 500
            graphic_card_hashrate_watt["voltage_millivolt"] = -100
        elif (graphic_card == GraphicCards.AMD_470):
            graphic_card_hashrate_watt["core"] = 1050
            graphic_card_hashrate_watt["memory"] = 1870
            graphic_card_hashrate_watt["voltage_millivolt"] = -200
            graphic_card_hashrate_watt["gpu_memory"] = 4
        elif (graphic_card == GraphicCards.AMD_480):
            graphic_card_hashrate_watt["core"] = 1150
            graphic_card_hashrate_watt["memory"] = 2150
            graphic_card_hashrate_watt["voltage_millivolt"] = -200
            graphic_card_hashrate_watt["gpu_memory"] = 8
        elif (graphic_card == GraphicCards.AMD_570):
            graphic_card_hashrate_watt["core"] = 1100
            graphic_card_hashrate_watt["memory"] = 2000
            graphic_card_hashrate_watt["voltage_millivolt"] = -200
            graphic_card_hashrate_watt["gpu_memory"] = 4
        elif (graphic_card == GraphicCards.AMD_580):
            graphic_card_hashrate_watt["core"] = 1500
            graphic_card_hashrate_watt["memory"] = 2150
            graphic_card_hashrate_watt["voltage_millivolt"] = -200
            graphic_card_hashrate_watt["gpu_memory"] = 8
        elif (graphic_card == GraphicCards.AMD_VEGA_56):
            graphic_card_hashrate_watt["core"] = 950
            graphic_card_hashrate_watt["memory"] = 900
            graphic_card_hashrate_watt["voltage_millivolt"] = 95
        elif (graphic_card == GraphicCards.AMD_VEGA_64):
            graphic_card_hashrate_watt["core"] = 950
            graphic_card_hashrate_watt["memory"] = 1020
            graphic_card_hashrate_watt["voltage_millivolt"] = 975
        elif (graphic_card == GraphicCards.GTX_750_TI):
            graphic_card_hashrate_watt["core"] = 1350
            graphic_card_hashrate_watt["memory"] = 1500
            graphic_card_hashrate_watt["power_percentage"] = 100
        elif (graphic_card == GraphicCards.GTX_1050_TI):
            graphic_card_hashrate_watt["core"] = 150
            graphic_card_hashrate_watt["memory"] = 500
            graphic_card_hashrate_watt["power_percentage"] = 75
        elif (graphic_card == GraphicCards.GTX_1060):
            graphic_card_hashrate_watt["core"] = 150
            graphic_card_hashrate_watt["memory"] = 500
            graphic_card_hashrate_watt["power_percentage"] = 65
            graphic_card_hashrate_watt["gpu_memory"] = 6
        elif (graphic_card == GraphicCards.GTX_1070):
            graphic_card_hashrate_watt["core"] = 150
            graphic_card_hashrate_watt["memory"] = 500
            graphic_card_hashrate_watt["power_percentage"] = 65
        elif (graphic_card == GraphicCards.GTX_1070_TI):
            graphic_card_hashrate_watt["core"] = 150
            graphic_card_hashrate_watt["memory"] = 500
            graphic_card_hashrate_watt["power_percentage"] = 65
        elif (graphic_card == GraphicCards.GTX_1080):
            graphic_card_hashrate_watt["core"] = 150
            graphic_card_hashrate_watt["memory"] = 500
            graphic_card_hashrate_watt["power_percentage"] = 65
        elif (graphic_card == GraphicCards.GTX_1080_TI):
            graphic_card_hashrate_watt["core"] = 150
            graphic_card_hashrate_watt["memory"] = 500
            graphic_card_hashrate_watt["power_percentage"] = 65

    def __scaling_hashrate(self, algorithm):
        if(algorithm == Algorithms.ETHASH or algorithm == Algorithms.GROESTL or algorithm == Algorithms.X11GOST or algorithm == Algorithms.TIMETRAVEL10
                or algorithm == Algorithms.X16R or algorithm == Algorithms.SKUNKHASH or algorithm == Algorithms.NIST5 or algorithm == Algorithms.XEVAN):
            return Variables.MEGA
        elif(algorithm == Algorithms.LYRA2REV2 or algorithm == Algorithms.NEOSCRYPT):
            return Variables.KILO
        elif(algorithm == Algorithms.CRYPTONIGHT or algorithm == Algorithms.CRYPTONIGHTV7 or algorithm == Algorithms.EQUIHASH):
            return 1
