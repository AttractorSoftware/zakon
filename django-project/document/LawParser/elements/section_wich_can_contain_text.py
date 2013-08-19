from sections import Section


class SectionWichCanContainText(Section):
    def __init__(self, level, name, number):
        super(SectionWichCanContainText, self).__init__(level, name, number)
        self._text = ''

    @property
    def number(self):
        return self.number

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value