from src.currencies.currencies import Currencies
from src.data_scrapper.blockchain_explorer.cryptoid.GRS_data_scrapper import GRSDataScrapper


class DataScrapperFactory:
    def __init__(self):
        pass

    def getDataScrapper(currency):
        if(currency == Currencies.GRS):
            return GRSDataScrapper()