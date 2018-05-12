import datetime

from src.data_scrapper.exchange_rate.coinmarketcap.coinmarketcap_site_data_scrapper import CoinmarketcapDataScrapper


class BTCPExchangeRateDataScrapper(CoinmarketcapDataScrapper):
    _currency_full_name = "bitcoin-private"

