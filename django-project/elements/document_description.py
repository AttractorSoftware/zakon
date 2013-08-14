__author__ = 'esdp'


class DocumentDescription(object):
    def __init__(self, documentName, revision):
        self._revision = revision
        self._revisions = []
        self._name = documentName

    @property
    def revision(self):
        return self._revision

    @revision.setter
    def revision(self, value):
        self._revision = value

    @property
    def revisions(self):
        return self._revisions

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value