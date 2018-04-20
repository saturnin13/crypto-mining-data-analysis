import re


class RegexPatternMatching:

    def __init__(self):
        pass

    def find_all_pattern_match(self, pattern, text, groups_name):
        return self.find_pattern_match(pattern, text, groups_name, -1)

    def find_pattern_match(self, pattern, text, groups_name, match_number=0):
        iterator = re.finditer(pattern, text)
        result = []
        for index, match in enumerate(iterator):
            if(index == match_number):
                 result = self.__get_all_group_name(match, groups_name)
                 break
            elif(match_number == -1):
                result.append(self.__get_all_group_name(match, groups_name))
        if(match_number != -1 and not result):
            return None
        return result

    def __get_all_group_name(self, match, groups_name):
        if(not isinstance(groups_name,(list,))):
            return match.group(groups_name)
        result = []
        for group_name in groups_name:
            result.append(match.group(group_name))
        return result