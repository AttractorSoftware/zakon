from lxml import etree


class Comment(object):
    def __init__(self, content):
        self._content = content

    @property
    def content(self):
        return self._content

    def to_xml(self):
        root = etree.Element('comment')
        root.text=self._content
        return etree.tostring(root)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

