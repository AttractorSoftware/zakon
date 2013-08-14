class Item(object):
    def __init__(self, text, id):
        self._items = []
        self._id = id

    @property
    def items(self):
        return self._items

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
