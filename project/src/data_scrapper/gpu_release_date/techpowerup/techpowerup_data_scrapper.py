from datetime import datetime

from src.data_scrapper.gpu_release_date.generic_gpu_release_date_data_scrapper import GenericGpuReleaseDateDataScrapper
from src.graphic_cards.graphic_cards import GraphicCards


class TechpowerupDataScrapper(GenericGpuReleaseDateDataScrapper):

    def _get_regex_patterns(self, id):
        graphic_card = id["graphic_card"]
        graphic_card_regex = self.__get_graphic_card_regex(graphic_card)
        return  ["<tr>\\r?\\n"
                 "	<td class=\".*\">\\r?\\n"
                 "		<a href=\".*\">" + graphic_card_regex + "</a>\\r?\\n"
                 "\\r?\\n"
                 "			</td>\\r?\\n"
                 "	<td>.*</td>\\r?\\n"
                 "	<td>(?P<release_date>\w{3} \d{4})</td>\\r?\\n"
                 "	<td>.*</td>\\r?\\n"
                 "	<td>.*</td>\\r?\\n"
                 "	<td>.*</td>\\r?\\n"
                 "	<td>.*</td>\\r?\\n"
                 "	<td>.*</td>\\r?\\n"
                 "</tr>"]

    def _post_processing_single_result(self, id, result):
        result["release_date"] = datetime.strptime(result["release_date"], "%b %Y")
        result["graphic_card"] = id["graphic_card"]
        return result

    def _get_primary_url(self, id):
        return "https://www.techpowerup.com/gpudb/?mfgr%5B%5D=amd&mfgr%5B%5D=nvidia&mobile=0&released%5B%5D=y14_c&released%5B%5D=y11_14&generation=&" \
               "chipname=&interface=&ushaders=&tmus=&rops=&memsize=&memtype=&buswidth=&slots=&powerplugs=&sort=released&q="

    def _extract_cache_hash(self, id):
        return 1

    def __get_graphic_card_regex(self, graphic_card):
        if("GTX" in str(graphic_card)):
            if(graphic_card == GraphicCards.GTX_1060):
                return "GeForce GTX 1060 6 GB 9Gbps"
            return "GeForce " + graphic_card.value.replace("TI", "Ti") + "( \d GB)?"
        else:
            return "Radeon( (R(5|7|9|X)|HD))? " + graphic_card.value.replace("AMD ", "").replace("VEGA", "Vega")
