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