from abc import abstractmethod

from src.data_scrapper.exchange_rate.coinmarkercap_scrapped_data import CoinmarketcapScrappedData
from src.data_scrapper.exchange_rate.generic_exchange_rate_data_scrapper import GenericExchangeRateDataScrapper
from src.regex.constant_regex import ConstantRegex


class CoinmarketcapDataScrapper(GenericExchangeRateDataScrapper):
    closes_regex_pattern = "( )*<tr class=\"text-right\">\\r?\\n" \
                           "( )*<td class=\"text-left\">(?P<" + str(CoinmarketcapScrappedData.date.value) + ">\w+ \d+, \d+)</td>\\r?\\n" \
                           "( )*<td data-format-fiat data-format-value=\"" + ConstantRegex.DECIMAL_NUMBER + "\">" + ConstantRegex.DECIMAL_NUMBER + "</td>\\r?\\n" \
                           "( )*<td data-format-fiat data-format-value=\"" + ConstantRegex.DECIMAL_NUMBER + "\">" + ConstantRegex.DECIMAL_NUMBER + "</td>\\r?\\n" \
                           "( )*<td data-format-fiat data-format-value=\"" + ConstantRegex.DECIMAL_NUMBER + "\">" + ConstantRegex.DECIMAL_NUMBER + "</td>\\r?\\n" \
                           "( )*<td data-format-fiat data-format-value=\"(?P<" + str(CoinmarketcapScrappedData.close.value) + ">" + ConstantRegex.DECIMAL_NUMBER + ")\">" + ConstantRegex.DECIMAL_NUMBER + "</td>\\r?\\n" \
                           "( )*<td data-format-market-cap data-format-value=\"" + ConstantRegex.DECIMAL_NUMBER + "\">" + ConstantRegex.DECIMAL_NUMBER + "</td>\\r?\\n" \
                           "( )*<td data-format-market-cap data-format-value=\"" + ConstantRegex.DECIMAL_NUMBER + "\">" + ConstantRegex.DECIMAL_NUMBER + "</td>\\r?\\n" \
                           "( )*</tr>"

    @property
    @abstractmethod
    def currency_full_name(self):
        pass

    def _get_url(self, start_date, end_date):
        start = start_date.strftime('%Y%m%d')
        end = end_date.strftime('%Y%m%d')
        return "https://coinmarketcap.com/currencies/" + str(self.currency_full_name) + "/historical-data/?start=" + start + "&end=" + end