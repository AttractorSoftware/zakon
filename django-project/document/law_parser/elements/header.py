from lxml import etree


class Header(object):
    def __init__(self, documentName, taking_place, revisions=None, description=None):
        self._revisions = revisions
        self._name = documentName
        self._taking_place = taking_place
        self._description = description

    @property
    def revisions(self):
        return self._revisions

    @property
    def name(self):
        return self._name

    @property
    def place(self):
        return self._taking_place

    @property
    def description(self):
        return self._description

    def to_xml(self):
        root = etree.Element("header")
        name_tag = etree.Element("name")
        name_tag.text = self._name
        root.append(name_tag)
        place_tag = etree.Element("place")
        place_tag.text = self._taking_place
        root.append(place_tag)
        if self._revisions != None:
            revisions_tag = etree.Element("revisions")
            revisions_tag.text = self._revisions
            root.append(revisions_tag)
        if self._description != None:
            description_tag = etree.Element("description")
            description_tag.text = self._description
            root.append(description_tag)
        return etree.tostring(root)