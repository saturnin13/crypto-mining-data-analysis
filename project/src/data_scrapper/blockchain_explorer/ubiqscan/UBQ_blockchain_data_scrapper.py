import datetime

from src.data_scrapper.blockchain_explorer.generic_blockchain_data_scrapper import GenericBlockchainDataScrapper
from src.regex.constant_regex import ConstantRegex

# TODO: look at uncles and fee for all currency and effect on reward (currently mostly taking only base reward)
class UBQBlockchainDataScrapper(GenericBlockchainDataScrapper):

    def _get_regex_patterns(self, id):
        datetime_regex_pattern     = "\",\"timestamp\":(?P<datetime>"    + ConstantRegex.NUMBER + "),\".*\"transactions\""
        difficulty_regex_pattern = "\"difficulty\":\"(?P<difficulty>" + ConstantRegex.NUMBER + ")\",\".*\"transactions\""
        return [datetime_regex_pattern, difficulty_regex_pattern]

    def _get_primary_url(self, id):
        return "https://api1.ubiqscan.io/v2/getblock/" + str(id["block_number"]) + "/true"

    def _post_processing_single_result(self, id, result):
        result = super()._post_processing_single_result(id, result)
        result["datetime"] = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(result["datetime"]))
        result["reward"] = self.__calculate_block_reward(id["block_number"])
        return result
    
    def __calculate_block_reward(self, block_number):
        if (block_number > 2508545):
            return 1
        elif (block_number > 2150181):
            return 2
        elif (block_number > 1791818):
            return 3
        elif (block_number > 1433454):
            return 4
        elif (block_number > 1075090):
            return 5
        elif (block_number > 716727):
            return 6
        elif (block_number > 358363):
            return 7
        elif (block_number > 0):
            return 8
        else:
            return 0
