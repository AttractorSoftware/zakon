from lxml import etree
from common.dom.elements.section import Section

class TextSection(Section):
    def __init__(self, level, number, name=None, text=None, comment=None):
        super(TextSection, self).__init__(level, name, number)
        self._text = text
        self._comment = comment

    @property
    def text(self):
        return self._text

    @property
    def comment(self):
        return self._comment

    @text.setter
    def text(self, value):
        self._text = value

    def to_xml(self):
        root = None
        if self._level == "article":
            root = etree.Element(self._level, level=self._level, number=self._number, name=self._name, id=self._build_id())
            if self._comment:
                root.append(etree.XML(self._comment.to_xml()))
        else:
            root = etree.Element('item', level=self._level, number=self._number,  id=self._build_id())

        root.text = self._text

        for element in self._sections:
            root.append(etree.XML(element.to_xml()))
        return etree.tostring(root)