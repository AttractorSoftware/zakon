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

    def test_rtf_with_hyperlink(self):
        str = r'{\rtf1{\field{\*\fldinst{HYPERLINK "http://www.test.com/"}}{\fldrslt{test}}}}'
        expected = u"test"
        self.assertEqual(expected, self.rtf_parser.parse(str))

    def test_rtf_wint_hyperlink_from_toktom(self):
        str = r'{\field\fldedit{\*\fldinst{\rtlch\fcs1\af1\ltrch\fcs0\insrsid1716831\hich\af1\dbch\af31505\loch\f1\hich\af1\dbch\af31505\loch\f1 HYPERLINK "toktom://db/1837"\hich\af1\dbch\af31505\loch\f1}}{\fldrslt{\rtlch\fcs1\af1\ltrch\fcs0\cs15\cf1\insrsid1716831\hich\af1\dbch\af31505\loch\f1 \hich\f1 19 \'e4\'e5\'ea\'e0\'e1\'f0\'ff\loch\f1\hich\f1  1996 \'e3\'ee\'e4\'e0\loch\f1  N 65}}}'
        self.assertEquals(u"19 декабря 1996 года N 65", self.rtf_parser.parse(str))

    def test_rtf_with_bold_text(self):
        str = r'{\rtf1\adeflang1025\ansi\ansicpg1251{\b test} test2'
        self.assertEqual(u"test test2", self.rtf_parser.parse(str))

    def test_rtf_with_article(self):
        str = r"{\rtf1\adeflang1025\ansi\ansicpg1251 {\b \'d1\'f2\'e0\'f2\'fc\'ff} test"
        self.assertEqual(u"Статья\n test", self.rtf_parser.parse(str))

    def test_rtf_with_bold_style_words_to_insert_new_line(self):
        str = r"{\rtf1\adeflang1025\ansi\ansicpg1251 {\b \'d1\'f2\'e0\'f2\'fc\'ff \pard\plain text} test2"
        self.assertEqual(u"Статья \ntext test2", self.rtf_parser.parse(str))