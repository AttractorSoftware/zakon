from lxml import etree


class Document(object):
    def __init__(self, id, description=None):
        self._sections = []
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

    def to_xml(self):
        root = etree.Element("document", id=str(self._id))
        if self._description != None:
            root.append(etree.XML(self._description.to_xml()))
        for section in self._sections:
            root.append(etree.XML(section.to_xml()))
        return etree.tostring(root)