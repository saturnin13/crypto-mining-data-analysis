from src.data_scrapper.blockchain_explorer.minergate.minergate_blockchain_data_scrapper import MinergateBlockchainDataScrapper


class ETCBlockchainDataScrapper(MinergateBlockchainDataScrapper):

    _get_minergate_url_identifier = "etc"
