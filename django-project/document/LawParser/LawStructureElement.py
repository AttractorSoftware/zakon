import re
class LawStructureElement(object):
    def __init__(self, name, depth, regular_expression):
        self._name = name
        self._compiled_regular_expression = re.compile(regular_expression, re.MULTILINE | re.U | re.I)
        self._depth = depth

    def get_name(self):
        return self._name

    def get_compiled_regex(self):
        return self._compiled_regular_expression

    def get_depth(self):
        return self._depth
