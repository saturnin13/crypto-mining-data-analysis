from src.data_scrapper.blockchain_explorer.minergate.minergate_blockchain_data_scrapper import MinergateBlockchainDataScrapper


class QCNBlockchainDataScrapper(MinergateBlockchainDataScrapper):

    _get_minergate_url_identifier = "qcn"
    _divide_reward_value = 1000000000000

