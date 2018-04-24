from src.currencies.currencies import Currencies
from src.data_scrapper.exchange_rate.coinmarketcap.BCN_exchange_rate_data_scrapper import BCNExchangeRateDataScrapper
from src.data_scrapper.exchange_rate.coinmarketcap.BTG_exchange_rate_data_scrapper import BTGExchangeRateDataScrapper
from src.data_scrapper.exchange_rate.coinmarketcap.ETC_exchange_rate_data_scrapper import ETCExchangeRateDataScrapper
from src.data_scrapper.exchange_rate.coinmarketcap.ETH_exchange_rate_data_scrapper import ETHExchangeRateDataScrapper
from src.data_scrapper.exchange_rate.coinmarketcap.FCN_exchange_rate_data_scrapper import FCNExchangeRateDataScrapper
from src.data_scrapper.exchange_rate.coinmarketcap.GRS_exchange_rate_data_scrapper import GRSExchangeRateDataScrapper
from src.data_scrapper.exchange_rate.coinmarketcap.QCN_exchange_rate_data_scrapper import QCNExchangeRateDataScrapper
from src.data_scrapper.exchange_rate.coinmarketcap.XMR_exchange_rate_data_scrapper import XMRExchangeRateDataScrapper


class ExchangeRateDataScrapperFactory:
    def getDataScrapper(currency):
        if(currency == Currencies.GRS):
            return GRSExchangeRateDataScrapper()
        elif(currency == Currencies.BCN):
            return BCNExchangeRateDataScrapper()
        elif (currency == Currencies.ETC):
            return ETCExchangeRateDataScrapper()
        elif (currency == Currencies.ETH):
            return ETHExchangeRateDataScrapper()
        elif (currency == Currencies.FCN):
            return FCNExchangeRateDataScrapper()
        elif (currency == Currencies.QCN):
            return QCNExchangeRateDataScrapper()
        elif (currency == Currencies.XMR):
            return XMRExchangeRateDataScrapper()
        elif (currency == Currencies.BTG):
            return BTGExchangeRateDataScrapper()