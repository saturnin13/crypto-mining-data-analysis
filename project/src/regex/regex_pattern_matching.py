import re

class RegexPatternMatching:
    def __init__(self):
        pass
    def find_pattern_match(self, pattern, text, group_name, match_number=0):
        iterator = re.finditer(pattern, text)
        for index, match in enumerate(iterator):
            if(index == match_number):
                return match.group(group_name)


