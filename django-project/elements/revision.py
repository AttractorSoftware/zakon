__author__ = 'esdp'


class Revision(object):
    def __init__(self, date, place, id):
        self._date = date
        self._place = place
        self._id = id

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        self._place = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value