class Document(object):
    def __init__(self, id, description, sections):
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