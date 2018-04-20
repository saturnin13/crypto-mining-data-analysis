from abc import abstractmethod

from src.data_scrapper.blockchain_explorer.generic_blockchain_data_scrapper import GenericBlockchainDataScrapper
from src.data_scrapper.blockchain_explorer.blockchain_scrapped_data import BlockchainScrappedData
from src.regex.constant_regex import ConstantRegex
from src.regex.regex_pattern_matching import RegexPatternMatching
from src.variables.variables import Variables


class CryptoidDataScrapper(GenericBlockchainDataScrapper):

    block_reward_regex_pattern = ",\"v\":(?P<" + str(BlockchainScrappedData.block_reward.value) + ">" + ConstantRegex.DECIMAL_NUMBER + ")"
    block_difficulty_regex_pattern = "<tr><td>Difficulty<td>(?P<" + str(BlockchainScrappedData.block_difficulty.value) + ">" + ConstantRegex.DECIMAL_NUMBER + ")"
    block_date_regex_pattern = "<tr><td>Date/Time<td>\\r?\\n            (?P<" + str(BlockchainScrappedData.block_date.value) + ">\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"

    @property
    @abstractmethod
    def currency_short_name(self):
        pass

    def _get_url(self, block_number):
        return Variables.CRYPTOID_URL_FIRST_PART + self.currency_short_name + Variables.CRYPTOID_URL_SECOND_PART + str(self.block_number)

    def _get_secondary_url(self, block_number, primary_content, data_required):
        if(data_required == BlockchainScrappedData.block_reward):
            hash = self.__find_hash(primary_content)
            if(hash == None):
                return None
            return "https://chainz.cryptoid.info/explorer/block.txs.dws?coin=" + str(self.currency_short_name).lower() + "&h=" + hash + ".js"

    def __find_hash(self, content):
        matcher = RegexPatternMatching()
        return matcher.find_pattern_match("<code class=\"hash\">(?P<hash>[a-zA-Z0-9]*)</code>", content, "hash")