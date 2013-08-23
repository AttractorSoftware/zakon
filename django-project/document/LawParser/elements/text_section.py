from lxml import etree
from section import Section

class TextSection(Section):
    def __init__(self, level, number, name=None, text=None):
        super(TextSection, self).__init__(level, name, number)
        self._text = text
        self._subsections = []

    @property
    def subsections(self):
        return self._subsections

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    def to_xml(self):
        if self._level == "article":
            root = etree.Element(self._level, name=self._name, id=self._build_id())
        elif self._level == "item":
            root = etree.Element(self._level, id=self._build_id())

        root.text = self._text

        for element in self._subsections:
            root.append(etree.XML(element.to_xml()))
        return etree.tostring(root)