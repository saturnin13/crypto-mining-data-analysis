import datetime

from src.data_scrapper.blockchain_explorer.generic_blockchain_data_scrapper import GenericBlockchainDataScrapper
from src.regex.constant_regex import ConstantRegex
from src.regex.regex_pattern_matching import RegexPatternMatching


class BTXBlockchainDataScrapper(GenericBlockchainDataScrapper):

    __block_hash_value = ""

    def _get_regex_patterns(self, id):
        datetime_regex_pattern = "\\],\"time\":(?P<datetime>" + ConstantRegex.NUMBER + "),\""
        difficulty_regex_pattern = "\",\"difficulty\":(?P<difficulty>" + ConstantRegex.NUMBER + "),\""
        reward_regex_pattern = ",\"valueOut\":(?P<reward>" + ConstantRegex.NUMBER + ")\\}"
        return [reward_regex_pattern, difficulty_regex_pattern, datetime_regex_pattern]

    def _get_primary_url(self, id):
        return "https://insight.bitcore.cc/api/block/" + str(self.__block_hash_value)

    def _get_auxiliary_urls(self, primary_content, id):
        return ["https://insight.bitcore.cc/api/txs?block=" + str(self.__block_hash_value) + "&pageNum=0"]

    def _pre_processing_page_loading(self, id):
        self.__block_hash_value = self.__find_hash(self.http.get_request("https://insight.bitcore.cc/api/block-index/" + str(id["block_number"]), verify=False)) # Check into this (security issue)

    def _post_processing_single_result(self, id, result):
        result = super()._post_processing_single_result(id, result)
        result["datetime"] = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(result["datetime"]))
        return result

    def __find_hash(self, content):
        matcher = RegexPatternMatching()
        return matcher.find_pattern_match("{\"blockHash\":\"(?P<hash>[a-zA-Z0-9]*)\"}", str(content), "hash")