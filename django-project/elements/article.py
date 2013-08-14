class Article(object):
    def __init__(self, text, id):
        self._items = []
        self._id = id
        self._text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def items(self):
        return self._items

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value