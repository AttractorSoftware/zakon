from lxml import etree
from comment import Comment

class Section(object):
    def __init__(self, level, name, number, comment=None):
        self._sections = []
        self._level = level
        self._number = number if number else ''
        self._name = name
        self._comment = comment

    @property
    def comment(self):
        return self._comment

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

    def _build_id(self):
        return self._level + "_" + self._number

    def to_xml(self):
        root = etree.Element("section", id=self._build_id(), level=self._level,
                             name=self._name, number=self._number)
        if self._comment:
            root.append(etree.XML(self._comment.to_xml()))
        for item in self._sections:
            root.append(etree.XML(item.to_xml()))
        return etree.tostring(root)