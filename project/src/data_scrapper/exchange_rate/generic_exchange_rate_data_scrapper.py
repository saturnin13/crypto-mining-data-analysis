from abc import abstractmethod, ABC
from datetime import datetime

from src.data_scrapper.exchange_rate.coinmarkercap_scrapped_data import CoinmarketcapScrappedData
from src.http_request.http_request_handling import HttpRequestHandling
from src.regex.regex_pattern_matching import RegexPatternMatching


class GenericExchangeRateDataScrapper(ABC):
    @property
    @abstractmethod
    def earliest_start_date(self):
        pass

    @property
    @abstractmethod
    def closes_regex_pattern(self):
        pass

    def __init__(self):
        self.regex = RegexPatternMatching()

    def get_all_closes_and_dates(self, start_date=None, end_date=datetime.now().date()):
        if(start_date is None or start_date < self.earliest_start_date):
            start_date = self.earliest_start_date
        content = self.__load_page(start_date, end_date)
        closes = self.regex.find_all_pattern_match(self.closes_regex_pattern, content, [str(CoinmarketcapScrappedData.close.value), str(CoinmarketcapScrappedData.date.value)])
        if(not closes):
            print("Closes were not found in " + str(self._get_url(start_date, end_date)) + " with content:\n" + content)
            return None
        for close in closes:
            close[0] = float(close[0])
            close[1] = datetime.strptime(close[1], "%b %d, %Y")
        closes.reverse()
        return closes

    def __load_page(self, start_date, end_date):
        http = HttpRequestHandling()
        url = self._get_url(start_date, end_date)
        return http.get_request(url)

    @abstractmethod
    def _get_url(self, start_date, end_date):
        pass

