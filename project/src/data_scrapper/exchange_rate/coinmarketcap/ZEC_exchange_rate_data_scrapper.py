from src.data_scrapper.exchange_rate.coinmarketcap.coinmarketcap_site_data_scrapper import CoinmarketcapDataScrapper


# TODO: add the fees in the block reward
class ZECExchangeRateDataScrapper(CoinmarketcapDataScrapper):

    _currency_full_name = "zcash"

