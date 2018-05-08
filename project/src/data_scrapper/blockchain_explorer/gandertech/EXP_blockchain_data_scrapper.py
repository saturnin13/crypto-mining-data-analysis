import datetime

from src.data_scrapper.blockchain_explorer.generic_blockchain_data_scrapper import GenericBlockchainDataScrapper
from src.regex.constant_regex import ConstantRegex


class EXPBlockchainDataScrapper(GenericBlockchainDataScrapper):

    def _get_regex_patterns(self, id):
        datetime_regex_pattern   = "\",\"timestamp\":\"(?P<datetime>"    + ConstantRegex.NUMBER + ")\",\".*\"transactions\""
        difficulty_regex_pattern = "\",\"difficulty\":\"(?P<difficulty>" + ConstantRegex.NUMBER + ")\",\".*\"transactions\""
        reward_regex_pattern     = ",\"blockReward\":(?P<reward>"        + ConstantRegex.NUMBER + "),\""
        return [reward_regex_pattern, difficulty_regex_pattern, datetime_regex_pattern]

    def _get_primary_url(self, id):
        return "https://api.gander.tech/block/" + str(id["block_number"])

    def _post_processing_single_result(self, id, result):
        result = super()._post_processing_single_result(id, result)
        result["datetime"] = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(result["datetime"]))
        return result
