class Description(object):
    def __init__(self, documentName, revisions, taking_place):
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