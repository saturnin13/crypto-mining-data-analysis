import datetime
from abc import abstractmethod

from src.data_scrapper.blockchain_explorer.generic_blockchain_data_scrapper import GenericBlockchainDataScrapper
from src.regex.constant_regex import ConstantRegex


class MinergateBlockchainDataScrapper(GenericBlockchainDataScrapper):

    @property
    @abstractmethod
    def _get_minergate_url_identifier(self):
        pass

    @property
    def _divide_reward(self):
        return False

    def _get_regex_patterns(self, id):
        datetime_regex_pattern     = ",\"timestamp\":\"?(?P<datetime>"    + ConstantRegex.DECIMAL_NUMBER + ")\"?,.*\"transactions\""
        difficulty_regex_pattern   = ",\"difficulty\":\"?(?P<difficulty>" + ConstantRegex.DECIMAL_NUMBER + ")\"?,.*\"transactions\""
        block_reward_regex_pattern = ",\"reward\":\"?(?P<block_reward>"   + ConstantRegex.DECIMAL_NUMBER + ")\"?,.*\"transactions\""
        return [datetime_regex_pattern, difficulty_regex_pattern, block_reward_regex_pattern]

    def _get_primary_url(self, id):
        return "https://minergate.com/ccapi/1.0/" + str(self._get_minergate_url_identifier) + "/blocks/" + str(id["block_number"]) + "/full"

    def _post_processing_single_result(self, id, result):
        result["block_number"] = id["block_number"]
        result["datetime"] =  datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(result["datetime"]))
        if(self._divide_reward):
            result["block_reward"] = float(result["block_reward"]) / 1000000000000
        return result