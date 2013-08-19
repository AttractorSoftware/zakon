class Revision(object):
    def __init__(self, date, number):
        self._date = date
        self._number = number

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value