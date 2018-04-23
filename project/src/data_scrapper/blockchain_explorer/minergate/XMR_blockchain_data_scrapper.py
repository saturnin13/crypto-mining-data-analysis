from src.data_scrapper.blockchain_explorer.minergate.minergate_blockchain_data_scrapper import MinergateBlockchainDataScrapper


class XMRBlockchainDataScrapper(MinergateBlockchainDataScrapper):

    _get_minergate_url_identifier = "mro"
    _divide_reward = True
