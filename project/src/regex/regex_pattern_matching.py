import regex

from src.regex.constant_regex import ConstantRegex


class RegexPatternMatching:

    def __init__(self):
        pass

    def find_all_pattern_match(self, pattern, text, groups_name):
        return self.find_pattern_match(pattern, text, groups_name, -1)

    def find_pattern_match(self, pattern, text, group_names, match_number=0):
        iterator = regex.finditer(pattern, text)
        result = []
        for index, match in enumerate(iterator):
            if(index == match_number):
                result = self.__get_all_group_name(match, group_names)
                break
            elif(match_number == -1):
                result.append(self.__get_all_group_name(match, group_names))
        if(not result):
            return None
        return result

    def __get_all_group_name(self, match, group_names):
        if(not isinstance(group_names, (list,))):
            return match.group(group_names)
        result = {}
        for group_name in group_names:
            try:
                result[group_name] = match.group(group_name)
            except(IndexError) as error:
                pass
        return result
