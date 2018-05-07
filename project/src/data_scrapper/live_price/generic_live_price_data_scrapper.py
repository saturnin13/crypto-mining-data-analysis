from src.data_scrapper.generic_data_scrapper import GenericDataScrapper


class GenericLiveDataScrapper(GenericDataScrapper):

    _optional_input_default_value = {}
    _expected_inputs = ["currency"]
    _get_outputs_as_string = ["price"]

    def _get_auxiliary_urls(self, primary_content, id):
        return super()._get_auxiliary_urls(primary_content, id)

    def _get_extra_group_names(self, id):
        return super()._get_extra_group_names(id)

    def _relevant_id_keys_for_group_names(self, id):
        return super()._relevant_id_keys_for_group_names(id)

    def _extract_cache_hash(self, id):
        return super()._extract_cache_hash(id)

    def _pre_processing_page_loading(self, id):
        super()._pre_processing_page_loading(id)

    def _post_processing_page_loading(self, url_content, id):
        return super()._post_processing_page_loading(url_content, id)

    def _post_processing_all_result(self, result):
        return super()._post_processing_all_result(result)