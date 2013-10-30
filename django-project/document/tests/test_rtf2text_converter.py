# -*- coding: UTF-8 -*-
import os
import unittest
from document.rtf import rtf_text
from zakon.settings import PROJECT_ROOT


class Rtf2TextConverterTest(unittest.TestCase):

    def test_rtf_to_text(self):
        str = r"{\rtf1\adeflang1025\ansi\ansicpg1251\'c2\'cd\'c8\'cc\'c0\'cd\'c8\'c5\loch\f2"
        self.assertEqual(u"ВНИМАНИЕ", rtf_text(str))

    def test_rtf_text_with_unicode(self):
        str = r"{\rtf1\adeflang1025\ansi\ansicpg1251\'c2\'cd\'c8\'cc\'c0\'cd\'c8\u65\loch\f2"
        self.assertEqual(u"ВНИМАНИA", rtf_text(str))

    def test_rtf_with_unicode_skipping(self):
        str = r"{\rtf1\adeflang1025\ansi\ansicpg1251\u0065\uc1\u0066\loch\f2"
        self.assertEqual(u"A", rtf_text(str))

    def test_rtf_text_in_braces(self):
        str = r"{\rtf1\adeflang1025\ansi\ansicpg1251\f10 {\u0065\u0066}\loch\f2"
        self.assertEqual(u"AB", rtf_text(str))

    def test_rtf_text_load_from_file(self):
        str = open(os.path.join(PROJECT_ROOT, '..', 'document', 'tests', 'resources', 'sample.rtf')).read()
        expected = u"Тест\n\n" \
                   u"вылдфлвдыфлвдыфвфывоыф\n" \
                   u"kdaskdjaksdjskajdjadkasldsa\n"
        self.assertEqual(expected, rtf_text(str))


