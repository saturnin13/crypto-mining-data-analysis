from abc import ABC, abstractmethod

from src.data_scrapper.blockchain_explorer.blockchain_scrapped_data import BlockchainScrappedData
from src.http_request.http_request_handling import HttpRequestHandling
from src.regex.regex_pattern_matching import RegexPatternMatching
from datetime import datetime


class GenericBlockchainDataScrapper(ABC):

    @property
    @abstractmethod
    def block_reward_regex_pattern(self):
        pass

    @property
    @abstractmethod
    def block_difficulty_regex_pattern(self):
        pass

    @property
    @abstractmethod
    def block_date_regex_pattern(self):
       pass

    def __init__(self):
        super().__init__()
        self.block_number = -1
        self.current_content = ""
        self.regex = RegexPatternMatching()

    def get_block_reward(self, block_number):
        content = self.__load_page(block_number, BlockchainScrappedData.block_reward)
        reward = self.regex.find_pattern_match(self.block_reward_regex_pattern, content, str(BlockchainScrappedData.block_reward.value))
        if(reward == None):
            print("Block reward not found in " + str(self._get_url(block_number)) + " with content:\n" + content)
            return None
        return reward

    def get_block_difficulty(self, block_number):
        content = self.__load_page(block_number, BlockchainScrappedData.block_difficulty)
        difficulty = self.regex.find_pattern_match(self.block_difficulty_regex_pattern, content, str(BlockchainScrappedData.block_difficulty.value))
        if (difficulty == None):
            print("Block difficulty not found in " + str(self._get_url(block_number)) + " with content:\n" + content)
            return None
        return difficulty

    def get_block_date(self, block_number):
        content = self.__load_page(block_number, BlockchainScrappedData.block_date)
        date_string = self.regex.find_pattern_match(self.block_date_regex_pattern, content, str(BlockchainScrappedData.block_date.value))
        if (date_string == None):
            print("Block date not found in " + str(self._get_url(block_number)) + " with content:\n" + content)
            return None
        block_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return block_date

    def __load_page(self, block_number, page_required):
        http = HttpRequestHandling()

        if(block_number != self.block_number):
            self.block_number = block_number
            self.current_content = http.get_request(self._get_url(block_number))

        secondary_url = self._get_secondary_url(block_number, self.current_content, page_required)
        if(secondary_url is not None):
            secondary_content = http.get_request(secondary_url)
            return secondary_content
        return self.current_content

    @abstractmethod
    def _get_url(self, block_number):
        pass

    def _get_secondary_url(self, block_number, primary_content, data_required):
        return None