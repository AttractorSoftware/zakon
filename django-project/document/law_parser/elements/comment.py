

class Comment(object):
    def __init__(self, content, level):
        self._content = content

    @property
    def content(self):
        return self._content
