
class Date(object):
    def __init__(self, year, month, day):
        self._month = month
        self._year = year
        self._day = day

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day