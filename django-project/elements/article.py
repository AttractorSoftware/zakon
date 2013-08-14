class Articles(object):
    def __init__(self):
        self._items = []
        self._id = ""

    @property
    def items(self):
        return self._items

    @property
    def id(self):
        return self._id