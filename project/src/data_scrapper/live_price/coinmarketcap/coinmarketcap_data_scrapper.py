from src.currencies.currencies import Currencies
from src.data_scrapper.live_price.generic_live_price_data_scrapper import GenericLiveDataScrapper
from src.regex.constant_regex import ConstantRegex


class CoinmarketcapDataScrapper(GenericLiveDataScrapper):

    def _get_regex_patterns(self, id):
        return ["            \"USD\": {\\n                \"price\": (?P<price>" + ConstantRegex.NUMBER + "), \\n"]

    def _get_primary_url(self, id):
        currency_id = self.__convert_currency_to_id(id["currency"])
        return "https://api.coinmarketcap.com/v2/ticker/" + str(currency_id) + "/?convert=EUR"

    def _post_processing_single_result(self, id, result):
        result["price"] = float(result["price"])
        return result

    def __convert_currency_to_id(self, currency):
        if(currency == Currencies.BTG):
            return 2083
        elif(currency == Currencies.GRS):
            return 258
        elif(currency == Currencies.ETH):
            return 1027
        elif(currency == Currencies.XMR):
            return 328
        elif(currency == Currencies.QCN):
            return 338
        elif(currency == Currencies.FCN):
            return 370
        elif(currency == Currencies.ETC):
            return 1321
        elif(currency == Currencies.BCN):
            return 372
        elif (currency == Currencies.EXP):
            return 1070
        elif (currency == Currencies.UBQ):
            return 588
        elif(currency == Currencies.ZEC):
            return 1437
        elif(currency == Currencies.ZCL):
            return 1447
        else:
            raise Exception("No id for coinmarketcap for currency: " + str(currency))
