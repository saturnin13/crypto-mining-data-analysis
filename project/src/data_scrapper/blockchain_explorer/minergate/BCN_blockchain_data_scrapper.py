from src.data_scrapper.blockchain_explorer.minergate.minergate_blockchain_data_scrapper import MinergateBlockchainDataScrapper


class BCNBlockchainDataScrapper(MinergateBlockchainDataScrapper):

    _get_minergate_url_identifier = "bcn"
    _divide_reward_value = 100000000

