from abc import abstractmethod
from datetime import datetime

from src.data_scrapper.exchange_rate.generic_exchange_rate_data_scrapper import GenericExchangeRateDataScrapper
from src.regex.constant_regex import ConstantRegex


class CoinmarketcapDataScrapper(GenericExchangeRateDataScrapper):

    @property
    @abstractmethod
    def _currency_full_name(self):
        pass

    _earliest_start_date = datetime(2013, 4, 28)

    def _get_regex_patterns(self, id):
        return  ["( )*<tr class=\"text-right\">\\r?\\n" \
                "( )*<td class=\"text-left\">(?P<datetime>\w+ \d+, \d+)</td>\\r?\\n" \
                "( )*<td data-format-fiat data-format-value=\"" + ConstantRegex.NUMBER + "\">" + ConstantRegex.NUMBER + "</td>\\r?\\n" \
                "( )*<td data-format-fiat data-format-value=\"" + ConstantRegex.NUMBER + "\">" + ConstantRegex.NUMBER + "</td>\\r?\\n" \
                "( )*<td data-format-fiat data-format-value=\"" + ConstantRegex.NUMBER + "\">" + ConstantRegex.NUMBER + "</td>\\r?\\n" \
                "( )*<td data-format-fiat data-format-value=\"(?P<close>" + ConstantRegex.NUMBER + ")\">" + ConstantRegex.NUMBER + "</td>\\r?\\n" \
                "( )*<td data-format-market-cap data-format-value=\"" + ConstantRegex.NUMBER + "\">" + ConstantRegex.NUMBER + "</td>\\r?\\n" \
                "( )*<td data-format-market-cap data-format-value=\"" + ConstantRegex.NUMBER + "\">" + ConstantRegex.NUMBER + "</td>\\r?\\n" \
                "( )*</tr>"]

    def _get_primary_url(self, id):
        start = id["start_date"].strftime('%Y%m%d') if self._earliest_start_date >= id["start_date"] else self._earliest_start_date
        end = id["end_date"].strftime('%Y%m%d')
        return "https://coinmarketcap.com/currencies/" + str(self._currency_full_name) + "/historical-data/?start=" + start + "&end=" + end

    def _post_processing_single_result(self, id, result):
        result["datetime"] = datetime.strptime(result["datetime"], "%b %d, %Y")
        return result

    def _post_processing_all_result(self, result):
        return list(reversed(result))