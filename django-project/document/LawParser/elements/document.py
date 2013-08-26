from lxml import etree


class Document(object):
    def __init__(self, description=None, sections=[]):
        self._sections = sections
        self._id = id
        self._description = description

    @property
    def id(self):
        return self._id

    @property
    def sections(self):
        return self._sections

    @property
    def description(self):
        return self._description

    @property
    def name(self):
        return self.description.name

    def to_xml(self):
        root = etree.Element("document")
        if self._description != None:
            root.append(etree.XML(self._description.to_xml()))
        for section in self._sections:
            root.append(etree.XML(section.to_xml()))

        return etree.tostring(root, xml_declaration=True, encoding='utf-8')