#coding=utf-8
from unittest import TestCase
from document.LawParser.LawHtmlParser import LawHtmlParser


class LawParserTests(TestCase):
    def test_expected_and_current_text_equal_1(self):
        text_after_parsing = LawHtmlParser(open("text_law.txt").read()).get_parsed_text()
        #print text_after_parsing
        self.assertEqual(open("1_law_source_text.txt", 'r').read(), text_after_parsing)

    def test_empty_file(self):
        text_after_parsing = LawHtmlParser(open("2_law_source_text.txt").read()).get_parsed_text()
        #print text_after_parsing
        self.assertTrue(text_after_parsing == '')

    def test_only_title(self):
        text_after_parsing = LawHtmlParser(open("3_law_source_text.txt").read()).get_parsed_text()
        print text_after_parsing
        self.assertTrue(text_after_parsing ==
                         'Закон Кыргызской Республики<br/>о некоммерческих организациях<br/>г. Бишкек, 15 октября 1999 года N 111')

    def test_article_dot_after_number(self):
        self.assertFalse(LawHtmlParser("Статья 3.").get_parsed_text() ==
                         LawHtmlParser("Статья 3").get_parsed_text())
        self.assertFalse(LawHtmlParser("Статья 3. текст").get_parsed_text() ==
                         LawHtmlParser("Статья 3 текст").get_parsed_text())

    def test_article_dot_after_number(self):
        self.assertFalse(LawHtmlParser("Глава I.").get_parsed_text() ==
                         LawHtmlParser("Глава 1.").get_parsed_text())
        self.assertFalse(LawHtmlParser("Глава I.").get_parsed_text() ==
                         LawHtmlParser("Глава I").get_parsed_text())