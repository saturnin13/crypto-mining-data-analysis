from src.currencies.currencies import Currencies
from src.data_scrapper.exchange_rate.coinmarketcap.GRS_exchange_rate_data_scrapper import \
    GRSExchangeRateDataScrapper


class ExchangeRateDataScrapperFactory:
    def __init__(self):
        pass

    def getDataScrapper(currency):
        if(currency == Currencies.GRS):
            return GRSExchangeRateDataScrapper()