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
    def _divide_reward_value(self):
        return 1

    def _get_regex_patterns(self, id):
        datetime_regex_pattern     = ",\"timestamp\":\"?(?P<datetime>"    + ConstantRegex.DECIMAL_NUMBER + ")\"?,.*\"transactions\""
        difficulty_regex_pattern   = ",\"difficulty\":\"?(?P<difficulty>" + ConstantRegex.DECIMAL_NUMBER + ")\"?,.*\"transactions\""
        reward_regex_pattern = ",\"reward\":\"?(?P<reward>"   + ConstantRegex.DECIMAL_NUMBER + ")\"?,.*\"transactions\""
        return [datetime_regex_pattern, difficulty_regex_pattern, reward_regex_pattern]

    def _get_primary_url(self, id):
        return "https://minergate.com/ccapi/1.0/" + str(self._get_minergate_url_identifier) + "/blocks/" + str(id["block_number"]) + "/full"

    def _post_processing_single_result(self, id, result):
        result = super()._post_processing_single_result(id, result)
        result["datetime"] = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(result["datetime"]))
        result["reward"] = float(result["reward"]) / self._divide_reward_value
        return result