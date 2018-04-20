import datetime

from src.data_scrapper.exchange_rate.coinmarketcap.coinmarketcap_site_data_scrapper import CoinmarketcapDataScrapper


class GRSExchangeRateDataScrapper(CoinmarketcapDataScrapper):
    earliest_start_date = datetime.datetime(2013, 4, 28)
    currency_full_name = "groestlcoin"

