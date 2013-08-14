class Section(object):
    def __init__(self, level, name, id):
        self._articles = []
        self._sections = []
        self._level = level
        self._id = id
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def articles(self):
        return self._articles

    @property
    def sections(self):
        return self._sections
