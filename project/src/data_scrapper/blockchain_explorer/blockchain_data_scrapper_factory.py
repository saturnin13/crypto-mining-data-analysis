from src.currencies.currencies import Currencies
from src.data_scrapper.blockchain_explorer.cryptoid.GRS_blockchain_data_scrapper import GRSBlockchainDataScrapper
from src.data_scrapper.blockchain_explorer.etherscan.ETH_blockchain_data_scrapper import ETHBlockchainDataScrapper


class BlockChainDataScrapperFactory:
    def __init__(self):
        pass

    def getDataScrapper(currency):
        if(currency == Currencies.GRS):
            return GRSBlockchainDataScrapper()
        elif(currency == Currencies.ETH):
            return ETHBlockchainDataScrapper()