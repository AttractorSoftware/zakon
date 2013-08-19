class Section(object):
    def __init__(self, level, name, number):
        self._sections = []
        self._level = level
        self._number = number
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number

    @property
    def level(self):
        return self._level

    @property
    def sections(self):
        return self._sections

    def add_section(self, section):
        self._sections.append(section)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)