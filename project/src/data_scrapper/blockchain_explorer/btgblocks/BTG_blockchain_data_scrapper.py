import datetime

from src.data_scrapper.blockchain_explorer.generic_blockchain_data_scrapper import GenericBlockchainDataScrapper
from src.regex.constant_regex import ConstantRegex


class BTGBlockchainDataScrapper(GenericBlockchainDataScrapper):

    __block_hash_value = ""

    def _get_regex_patterns(self, id):
        datetime_regex_pattern   = ",\"time\":(?P<datetime>"           + ConstantRegex.DECIMAL_NUMBER + "),\""
        difficulty_regex_pattern = "\",\"difficulty\":(?P<difficulty>" + ConstantRegex.DECIMAL_NUMBER + "),\""
        reward_regex_pattern     = "\",\"reward\":(?P<reward>"         + ConstantRegex.DECIMAL_NUMBER + "),\""
        return [reward_regex_pattern, difficulty_regex_pattern, datetime_regex_pattern]

    def _get_primary_url(self, id):
        return "https://explorer.bitcoingold.org/insight-api/block/" + str(self.__block_hash_value)

    def _pre_processing_page_loading(self, id):
        self.__block_hash_value = self.http.get_request("https://www.btgblocks.com/api/getblockhash?index=" + str(id["block_number"]))

    def _post_processing_single_result(self, id, result):
        result = super()._post_processing_single_result(id, result)
        result["datetime"] = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(result["datetime"]))
        return result