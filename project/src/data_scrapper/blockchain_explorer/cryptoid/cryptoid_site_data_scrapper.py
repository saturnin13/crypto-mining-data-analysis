from abc import abstractmethod
from datetime import datetime

from src.data_scrapper.blockchain_explorer.generic_blockchain_data_scrapper import GenericBlockchainDataScrapper
from src.regex.constant_regex import ConstantRegex
from src.regex.regex_pattern_matching import RegexPatternMatching
from src.variables.variables import Variables


class CryptoidDataScrapper(GenericBlockchainDataScrapper):

    @property
    @abstractmethod
    def currency_short_name(self):
        pass

    def _get_regex_patterns(self, id):
        datetime_regex_pattern = "<tr><td>Date/Time<td>\\r?\\n            (?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
        difficulty_regex_pattern = "<tr><td>Difficulty<td>(?P<difficulty>" + ConstantRegex.DECIMAL_NUMBER + ")"
        reward_regex_pattern = ",\"v\":(?P<block_reward>" + ConstantRegex.DECIMAL_NUMBER + "),\"inputs\":\\[\"Generation"
        return [reward_regex_pattern, difficulty_regex_pattern, datetime_regex_pattern]

    def _get_primary_url(self, id):
        return Variables.CRYPTOID_URL_FIRST_PART + self.currency_short_name + Variables.CRYPTOID_URL_SECOND_PART + str(id["block_number"])

    def _get_auxiliary_urls(self, primary_content, id):
        hash = self.__find_hash(primary_content)
        if (hash == None):
            return None
        return ["https://chainz.cryptoid.info/explorer/block.txs.dws?coin=" + str(self.currency_short_name).lower() + "&h=" + hash + ".js"]

    def _post_processing_single_result(self, id, result):
        result["datetime"] = datetime.strptime(result["datetime"], "%Y-%m-%d %H:%M:%S")
        result["block_number"] = id["block_number"]
        return result

    def __find_hash(self, content):
        matcher = RegexPatternMatching()
        return matcher.find_pattern_match("<code class=\"hash\">(?P<hash>[a-zA-Z0-9]*)</code>", str(content), "hash")