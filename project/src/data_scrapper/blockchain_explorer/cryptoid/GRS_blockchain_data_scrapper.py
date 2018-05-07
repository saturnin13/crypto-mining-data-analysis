from src.currencies.currencies import Currencies
from src.data_scrapper.blockchain_explorer.cryptoid.cryptoid_site_data_scrapper import CryptoidDataScrapper


class GRSBlockchainDataScrapper(CryptoidDataScrapper):
    currency_short_name = "grs"

    def _get_sleep_time(self):
        return 3
