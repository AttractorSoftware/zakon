from lxml import etree


class Document(object):
    def __init__(self, description=None, sections=[]):
        self._sections = sections
        self._description = description

    @property
    def sections(self):
        return self._sections

    @property
    def description(self):
        return self._description

    @property
    def name(self):
        return self.description.name

    def add_section(self, section):
        self._sections.append(section)

    def to_xml(self):
        root = etree.Element("document")
        if self._description != None:
            root.append(etree.XML(self._description.to_xml()))
        for section in self._sections:
            root.append(etree.XML(section.to_xml()))

        return etree.tostring(root, xml_declaration=True, encoding='utf-8')

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)