import re


class ElementBuild(object):
    def __init__(self, regex, flags, level=None):
        self._template = re.compile(regex, flags)
        self._level = level

    @property
    def template(self):
        return self._template

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
