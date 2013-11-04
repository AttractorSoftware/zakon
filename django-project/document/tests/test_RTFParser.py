# -*- coding: UTF-8 -*-
import os
import unittest
from document.rtfparser import RTFParser
from zakon.settings import PROJECT_ROOT


class RTFParserTests(unittest.TestCase):

    def setUp(self):
        self.rtf_parser = RTFParser()

    def test_rtf_to_text(self):
        str = r"{\rtf1\adeflang1025\ansi\ansicpg1251\'c2\'cd\'c8\'cc\'c0\'cd\'c8\'c5\loch\f2"
        self.assertEqual(u"ВНИМАНИЕ", self.rtf_parser.parse(str))

    def test_rtf_parsed_text_is_unicode(self):
        str = r"{\rtf1\adeflang1025\ansi\ansicpg1251\'c2\'cd\'c8\'cc\'c0\'cd\'c8\'c5\loch\f2"
        self.assertEqual(True, isinstance(self.rtf_parser.parse(str), unicode))


    def test_rtf_text_with_unicode(self):
        str = r"{\rtf1\adeflang1025\ansi\ansicpg1251\'c2\'cd\'c8\'cc\'c0\'cd\'c8\u65\loch\f2"
        self.assertEqual(u"ВНИМАНИA", self.rtf_parser.parse(str))

    def test_rtf_with_unicode_skipping(self):
        str = r"{\rtf1\adeflang1025\ansi\ansicpg1251\u0065\uc1\u0066\loch\f2"
        self.assertEqual(u"A", self.rtf_parser.parse(str))

    def test_rtf_text_in_braces(self):
        str = r"{\rtf1\adeflang1025\ansi\ansicpg1251\f10 {\u0065\u0066}\loch\f2"
        self.assertEqual(u"AB", self.rtf_parser.parse(str))

    def test_rtf_text_load_from_file(self):
        str = open(os.path.join(PROJECT_ROOT, 'document', 'tests', 'resources', 'sample.rtf')).read()
        expected = u"Тест\n\n" \
                   u"вылдфлвдыфлвдыфвфывоыф\n" \
                   u"kdaskdjaksdjskajdjadkasldsa\n"
        self.assertEqual(expected, self.rtf_parser.parse(str))


