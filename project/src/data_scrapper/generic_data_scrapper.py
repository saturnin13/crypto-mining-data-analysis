from abc import ABC, abstractmethod

from src.http_request.http_request_handling import HttpRequestHandling
from src.regex.regex_pattern_matching import RegexPatternMatching


class GenericDataScrapper(ABC):


    def __init__(self):
        super().__init__()
        self.regex = RegexPatternMatching()
        self.http = HttpRequestHandling()
        self.cache = {}

    def get_data(self, ids={}):

        ids = self.__initialise_input(ids)
        self.__check_input(ids)

        result = self.__find_all_patterns(ids)

        result = self._post_processing_all_result(result)

        return result

    def __initialise_input(self, ids):
        return {**self._optional_input_default_value, **ids}

    def __check_input(self, ids):
        for input in self._expected_inputs:
            if(input not in ids.keys()):
                raise Exception("The input " + input + " is missing from the function call")

    def __find_all_patterns(self, ids, id_buffer={}):
        if(not ids):
            pattern_result = self.__execute_pattern(id_buffer)
            is_valid_pattern_result = self.__verify_result(pattern_result, id_buffer)
            return (pattern_result if is_valid_pattern_result else None)

        ids_copy = dict(ids)
        result = []
        key = list(ids_copy.keys())[0]
        current_id = ids_copy.pop(key)
        for elem in current_id:
            id_buffer[key] = elem
            result += self.__find_all_patterns(ids_copy, id_buffer=id_buffer)

        return result

    def __execute_pattern(self, id):
        contents = self.__get_pages(id)
        patterns = self._get_regex_patterns(id)
        group_names = self.__get_group_names(id)

        # for now this is brute force
        all_matched_data = []
        for content in contents:
            for pattern in patterns:
                matched_data = self.regex.find_all_pattern_match(pattern, content, group_names)
                if(matched_data):
                    if len(all_matched_data) != 0:
                        for i in range(len(matched_data)):
                            if(len(matched_data) != len(all_matched_data)):
                                raise Exception("The list of data found in each pair of pattern and content must be of the same size")
                            all_matched_data[i] = {**all_matched_data[i], **matched_data[i]}
                    else:
                        all_matched_data += (matched_data)
        result = []
        for i in range(len(all_matched_data)):
            processed_data = self._post_processing_single_result(id, all_matched_data[i])
            if(processed_data):
                result.append(processed_data)
        return result

    def __get_group_names(self, id):
        group_names = []
        outputs = self._get_outputs_as_string
        id_keys = sorted(self._relevant_id_keys_for_group_names(id)) if self._relevant_id_keys_for_group_names(id) else []
        id_values_string = ""
        for key in id_keys:
            id_values_string += str(id[key]) + "_"
        for output in outputs:
            group_names.append(id_values_string + str(output))

        if self._get_extra_group_names(id):
            group_names.append(self._get_extra_group_names(id))
        return group_names

    def __verify_result(self, result, id):
        if(result is None):
            print("No result found for id: " + str(id) + " and url: " + str(self._get_primary_url(id)[0]) + ", with content: " + self.__get_pages(id)[0][:50])
            return False
        return True

    def __get_pages(self, id):
        cache_id = self._extract_cache_hash(id)
        if(cache_id in self.cache):
            return self.cache[cache_id]
        contents = self.__load_pages(id)
        self.cache[cache_id] = contents
        return contents

    def __load_pages(self, id):
        self._pre_processing_page_loading(id)

        url = self._get_primary_url(id)
        print("Fetching page for scrapping with url: " + str(url))

        url_contents = [self.http.get_request(url)]

        other_urls = self._get_auxiliary_urls(url_contents, id) if self._get_auxiliary_urls(url_contents, id) else []
        for other_url in other_urls:
            url_contents.append(self.http.get_request(other_url))

        url_contents = self._post_processing_page_loading(url_contents, id)

        return url_contents

    @property
    @abstractmethod
    def _optional_input_default_value(self):
        pass

    @property
    @abstractmethod
    def _expected_inputs(self):
        pass

    @property
    @abstractmethod
    def _get_outputs_as_string(self):
        pass

    @abstractmethod
    def _get_regex_patterns(self, id):
        pass

    @abstractmethod
    def _get_primary_url(self, id):
        pass

    @abstractmethod
    def _get_auxiliary_urls(self, primary_content, id):
        pass

    @abstractmethod
    def _get_extra_group_names(self, id):
        return None

    @abstractmethod
    def _post_processing_single_result(self, id, result):
        return result

    @abstractmethod
    def _relevant_id_keys_for_group_names(self, id):
        return None

    @abstractmethod
    def _extract_cache_hash(self, id):
        return hash(tuple(id.items()))

    @abstractmethod
    def _pre_processing_page_loading(self, id):
        pass

    @abstractmethod
    def _post_processing_page_loading(self, url_content, id):
        return url_content

    @abstractmethod
    def _post_processing_all_result(self, result):
        return result
