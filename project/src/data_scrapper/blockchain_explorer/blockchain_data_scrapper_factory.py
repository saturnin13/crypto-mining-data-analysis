from src.currencies.currencies import Currencies
from src.data_scrapper.blockchain_explorer.btgblocks.BTG_blockchain_data_scrapper import BTGBlockchainDataScrapper
from src.data_scrapper.blockchain_explorer.cryptoid.GRS_blockchain_data_scrapper import GRSBlockchainDataScrapper
from src.data_scrapper.blockchain_explorer.etherscan.ETH_blockchain_data_scrapper import ETHBlockchainDataScrapper
from src.data_scrapper.blockchain_explorer.minergate.BCN_blockchain_data_scrapper import BCNBlockchainDataScrapper
from src.data_scrapper.blockchain_explorer.minergate.ETC_blockchain_data_scrapper import ETCBlockchainDataScrapper
from src.data_scrapper.blockchain_explorer.minergate.FCN_blockchain_data_scrapper import FCNBlockchainDataScrapper
from src.data_scrapper.blockchain_explorer.minergate.QCN_blockchain_data_scrapper import QCNBlockchainDataScrapper
from src.data_scrapper.blockchain_explorer.minergate.XMR_blockchain_data_scrapper import XMRBlockchainDataScrapper


class BlockChainDataScrapperFactory:
    def __init__(self):
        pass

    def getDataScrapper(currency):
        if(currency == Currencies.GRS):
            return GRSBlockchainDataScrapper()
        elif(currency == Currencies.ETH):
            return ETHBlockchainDataScrapper()
        elif (currency == Currencies.XMR):
            return XMRBlockchainDataScrapper()
        elif (currency == Currencies.ETC):
            return ETCBlockchainDataScrapper()
        elif (currency == Currencies.BCN):
            return BCNBlockchainDataScrapper()
        elif (currency == Currencies.FCN):
            return FCNBlockchainDataScrapper()
        elif (currency == Currencies.QCN):
            return QCNBlockchainDataScrapper()
        elif (currency == Currencies.BTG):
            return BTGBlockchainDataScrapper()
