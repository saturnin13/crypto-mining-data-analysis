from datetime import datetime

from src.data_scrapper.blockchain_explorer.generic_blockchain_data_scrapper import GenericBlockchainDataScrapper
from src.regex.constant_regex import ConstantRegex


class ETHBlockchainDataScrapper(GenericBlockchainDataScrapper):

    def _get_regex_patterns(self, id):
        datetime_regex_pattern     = "( )*<tr>\\r?\\n" \
                                     "( )*<td width=\"190\">&nbsp;&nbsp;TimeStamp:\\r?\\n" \
                                     "( )*</td>\\r?\\n" \
                                     "( )*<td>\\r?\\n" \
                                     "( )*.+\\((?P<datetime>\w{3}-\d{2}-\d{4} \d{2}:\d{2}:\d{2} \w{2}) \\+UTC\\)\\r?\\n" \
                                     "( )*</td>\\r?\\n" \
                                     "( )*</tr>"
        difficulty_regex_pattern   = "( )*<tr>\\r?\\n" \
                                     "( )*<td width=\"190\">&nbsp;&nbsp;Difficulty:\\r?\\n" \
                                     "( )*</td>\\r?\\n" \
                                     "( )*<td>\\r?\\n(?P<difficulty>" + ConstantRegex.DECIMAL_NUMBER + ")\\r?\\n" \
                                     "( )*</td>\\r?\\n" \
                                     "( )*</tr>"
        block_reward_regex_pattern = "( )*<tr>\\r?\\n" \
                                     "( )*<td width=\"190\">&nbsp;&nbsp;Block Reward:\\r?\\n" \
                                     "( )*</td>\\r?\\n" \
                                     "( )*<td>\\r?\\n(?P<block_reward>" + ConstantRegex.DECIMAL_NUMBER + ")" \
                                     "(<b>.</b>(?P<block_reward_decimal>" + ConstantRegex.DECIMAL_NUMBER + "))? Ether( \\(.*\\))?( )?</td>\\r?\\n" \
                                     "( )*</tr>\\r?\\n" \
                                     "( )*<tr>"
        return [datetime_regex_pattern, difficulty_regex_pattern, block_reward_regex_pattern]

    def _get_extra_group_names(self, id):
        return "block_reward_decimal"

    def _get_primary_url(self, id):
        return "https://etherscan.io/block/" + str(id["block_number"])

    def _post_processing_single_result(self, id, result):
        result["datetime"] = datetime.strptime(result["datetime"], "%b-%d-%Y %H:%M:%S %p")
        result["block_number"] = id["block_number"]
        if(result["block_reward_decimal"]):
            result["block_reward"] = float(result["block_reward"]) + float(result["block_reward_decimal"]) / 10**len(result["block_reward_decimal"])
        result.pop("block_reward_decimal")
        result["difficulty"] = float(result["difficulty"].replace(',',''))
        return result