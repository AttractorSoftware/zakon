# -*- coding: UTF-8 -*-
import codecs
import locale
import os
import unittest
from document.rtf import striprtf
from zakon.settings import PROJECT_ROOT


class Rtf2TextConverterTest(unittest.TestCase):
    def test_conversion(self):
        tmp = codecs.open(os.path.join(PROJECT_ROOT, '..', 'document/selenium_tests/features/Nalogovij_Kodeks.rtf'),
                   'r', 'cp1251').read()
        temp = striprtf(tmp)
        self.assertEqual("", temp)
        #f = open("w.txt", 'w')
        #f.write(temp)
