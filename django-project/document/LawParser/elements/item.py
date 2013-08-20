from lxml import etree
from section import Section
class Item(Section):
    def __init__(self, number, text=None):
        self._number = number
        self._text = text

    @property
    def number(self):
        return self.number

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    def to_xml(self):
        root = etree.Element("item", number=self._number)
        root.text = self._text
        return etree.tostring(root)