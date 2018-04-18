from abc import ABC, abstractmethod

from src.data_scrapper.blockchain_explorer.scrapped_data import ScrappedData
from src.http_request.http_request_handling import HttpRequestHandling
from src.regex.regex_pattern_matching import RegexPatternMatching
from datetime import datetime


class GenericDataScrapper(ABC):

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

    def get_block_reward(self, block_number):
        content = self.__load_page(block_number, ScrappedData.block_reward)
        regex = RegexPatternMatching()
        reward = regex.find_pattern_match(self.block_reward_regex_pattern, content, str(ScrappedData.block_reward.value))
        if(reward == None):
            raise Exception("Block reward not found in " + str(self._get_initial_url(block_number)) + " with content:\n" + content)
        return reward

    def get_block_difficulty(self, block_number):
        content = self.__load_page(block_number, ScrappedData.block_difficulty)
        regex = RegexPatternMatching()
        difficulty = regex.find_pattern_match(self.block_difficulty_regex_pattern, content, str(ScrappedData.block_difficulty.value))
        if (difficulty == None):
            raise Exception("Block difficulty not found in " + str(self._get_initial_url(block_number)) + " with content:\n" + content)
        return difficulty

    def get_block_date(self, block_number):
        content = self.__load_page(block_number, ScrappedData.block_date)
        regex = RegexPatternMatching()
        date_string = regex.find_pattern_match(self.block_date_regex_pattern, content, str(ScrappedData.block_date.value))
        block_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        if (block_date == None):
            raise Exception("Block date not found in " + str(self._get_initial_url(block_number)) + " with content:\n" + content)
        return block_date

    def __load_page(self, block_number, page_required):
        http = HttpRequestHandling()

        if(block_number != self.block_number):
            self.block_number = block_number
            self.current_content = http.get_request(self._get_initial_url(block_number))

        secondary_url = self._get_secondary_url(block_number, self.current_content, page_required)
        if(secondary_url is not None):
            secondary_content = http.get_request(secondary_url)
            return secondary_content
        return self.current_content

    @abstractmethod
    def _get_initial_url(self, block_number):
        pass

    def _get_secondary_url(self, block_number, primary_content, data_required):
        return None