from lxml import etree


class Description(object):
    def __init__(self, documentName, taking_place, revisions=None):
        self._revisions = revisions
        self._name = documentName
        self._taking_place = taking_place

    @property
    def revisions(self):
        return self._revisions

    @property
    def name(self):
        return self._name

    @property
    def place(self):
        return self._taking_place

    def to_xml(self):
        root = etree.Element("description")
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
        return etree.tostring(root)