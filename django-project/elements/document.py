class Document(object):
    def __init__(self, id, description):
        self._sections = []
        self._id = id
        self._articles = []
        self._description = description

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = id

    @property
    def sections(self):
        return self._sections

    @property
    def articles(self):
        return self._articles

    @property
    def description(self):
        return self._description

