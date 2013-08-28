#coding=utf-8
import codecs
import re
from unittest import TestCase
from Builder import Builder
from elements.text_section import TextSection
from elements.section import Section

DOCUMENT_NAME_WITH_ONE_LINE_EXPECTED_TEXT = u'НАЛОГОВЫЙ КОДЕКС КЫРГЫЗСКОЙ РЕСПУБЛИКИ'

DOCUMENT_NAME_WITH_ONE_LINE_TEST_TEXT = u"""
г.Бишкек
от 17 октября 2008 года N 230

НАЛОГОВЫЙ КОДЕКС КЫРГЫЗСКОЙ РЕСПУБЛИКИ

(Вводится в действие Законом Кыргызской Республики
от 17 октября 2008 года N 231)

(В редакции Законов КР от 10 января 2009 года N 5,
28 марта 2009 года N 89, 30 апреля 2009 года N 143,
29 мая 2009 года N 175, 16 июля 2009 года N 222,
24 июля 2009 года N 245, 27 июля 2009 года N 255,"""

DOCUMENT_NAME_BUILD_WITH_ONE_LINE_TEST_TEXT = u'ЗАКОН КЫРГЫЗСКОЙ РЕСПУБЛИКИ  О государственной регистрации юридических лиц, филиалов (представительств)'

DOCUMENT_NAME_BUILD_WITH_MULTI_LINE_TEST_TEXT = u"""
г.Бишкек
от 20 февраля 2009 года N 57

ЗАКОН КЫРГЫЗСКОЙ РЕСПУБЛИКИ

О государственной регистрации юридических
лиц, филиалов (представительств)

(В редакции Законов КР от 15 июля 2009 года N 207,
18 декабря 2009 года N 313, 21 декабря 2011 года N 241,"""

DOCUMENT_NAME_BUILD_WITH_LINE_FOLDING = u"""
ЗАКОН КЫРГЫЗСКОЙ РЕСПУБЛИКИ

О государственной регистрации юридических
лиц, филиалов (представительств)

(В"""

REVISIONS_BUILD_TEST_TEXT = u"""
г.Бишкек
от 17 октября 2008 года N 230

НАЛОГОВЫЙ КОДЕКС КЫРГЫЗСКОЙ РЕСПУБЛИКИ

(Вводится в действие Законом Кыргызской Республики
от 17 октября 2008 года N 231)

(В редакции Законов КР от 10 января 2009 года N 5,
28 марта 2009 года N 89, 30 апреля 2009 года N 143,
29 мая 2009 года N 175, 16 июля 2009 года N 222,
24 июля 2009 года N 245, 27 июля 2009 года N 255,
18 января 2010 года N 3, 29 января 2010 года N 22,
10 февраля 2010 года N 25, 12 марта 2010 года N 48,
16 марта 2010 года N 51,
Декретов Временного Правительства КР от
21 апреля 2010 года ВП N 17, 21 апреля 2010 года ВП N 21,
17 сентября 2010 года ВП N 128,
Законов КР от 11 марта 2011 года N 5, 30 мая 2011 года N 33,
16 июня 2011 года N 47, 24 июня 2011 года N 56,
30 июня 2011 года N 64, 8 июля 2011 года N 87,
22 июля 2011 года N 123, 22 декабря 2011 года N 248,
27 февраля 2012 года N 8, 11 апреля 2012 года N 29,
13 апреля 2012 года N 38, 18 мая 2012 года N 55,
28 мая 2012 года N 68, 29 мая 2012 года N 69,
25 июля 2012 года N 123, 25 июля 2012 года N 124,
25 июля 2012 года N 125, 25 июля 2012 года N 138,
8 августа 2012 года N 154, 9 августа 2012 года N 158,
6 октября 2012 года N 169, 3 декабря 2012 года N 191,
5 декабря 2012 года N 194, 26 декабря 2012 года N 204,
26 декабря 2012 года N 205, 10 января 2013 года N 1,
20 февраля 2013 года N 25, 22 февраля 2013 года N 28,
16 марта 2013 года N 41)

ОБЩАЯ ЧАСТЬ
        """

REVISIONS_BUILD_ECPECTED_TEXT = u"""(В редакции Законов КР от 10 января 2009 года N 5,
28 марта 2009 года N 89, 30 апреля 2009 года N 143,
29 мая 2009 года N 175, 16 июля 2009 года N 222,
24 июля 2009 года N 245, 27 июля 2009 года N 255,
18 января 2010 года N 3, 29 января 2010 года N 22,
10 февраля 2010 года N 25, 12 марта 2010 года N 48,
16 марта 2010 года N 51,
Декретов Временного Правительства КР от
21 апреля 2010 года ВП N 17, 21 апреля 2010 года ВП N 21,
17 сентября 2010 года ВП N 128,
Законов КР от 11 марта 2011 года N 5, 30 мая 2011 года N 33,
16 июня 2011 года N 47, 24 июня 2011 года N 56,
30 июня 2011 года N 64, 8 июля 2011 года N 87,
22 июля 2011 года N 123, 22 декабря 2011 года N 248,
27 февраля 2012 года N 8, 11 апреля 2012 года N 29,
13 апреля 2012 года N 38, 18 мая 2012 года N 55,
28 мая 2012 года N 68, 29 мая 2012 года N 69,
25 июля 2012 года N 123, 25 июля 2012 года N 124,
25 июля 2012 года N 125, 25 июля 2012 года N 138,
8 августа 2012 года N 154, 9 августа 2012 года N 158,
6 октября 2012 года N 169, 3 декабря 2012 года N 191,
5 декабря 2012 года N 194, 26 декабря 2012 года N 204,
26 декабря 2012 года N 205, 10 января 2013 года N 1,
20 февраля 2013 года N 25, 22 февраля 2013 года N 28,
16 марта 2013 года N 41)"""

ARTICLE_WITH_MULTI_LINE_REGEX_EXPECTED_TEXT = u"""Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской
Республики"""

ARTICLE_WITH_MULTI_LINE_REGEX_TEST_TEXT = u"""
Общие положения

Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской
Республики

1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения:"""

ITEM_OF_AN_ARTICLE_EXPECTED_TEXT_2 = u"""2. Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано
Жогорку Кенешем Кыргызской Республики
либо заключено по поручению Жогорку Кенеша Кыргызской Республики во исполнение соглашения, ратифицированного Жогорку Кенешем
Кыргызской Республики, устанавливает иные нормы, чем предусмотренные налоговым законодательством Кыргызской Республики, то к
урегулированным таким соглашением налоговым отношениям применяются нормы этого соглашения.
(В редакции Законов КР от 30 апреля 2009 года N 143, 29 мая 2009 года N 175)

См.:
постановление Правительства КР от 15 мая 2012 года N 298 "Об утверждении Положения о порядке применения соглашений (конвенций)
об избежании двойного налогообложения и предотвращении уклонения от уплаты налогов на доход и капитал (имущество), заключенных
Кыргызской Республикой с иностранными государствами\""""

ITEM_OF_AN_ARTICLE_EXPECTED_TEXT_1 = u"""1. Если вступившим в установленном законом порядке международным договором, участником которого является Кыргызская Республика,
установлены иные нормы, чем предусмотренные налоговым законодательством Кыргызской Республики, то применяются нормы такого
международного договора."""

ITEM_OF_AN_ARTICLE_TEST_TEXT = u"""
Статья 3. Действие международных договоров и иных соглашений

1. Если вступившим в установленном законом порядке международным договором, участником которого является Кыргызская Республика,
установлены иные нормы, чем предусмотренные налоговым законодательством Кыргызской Республики, то применяются нормы такого
международного договора.
2. Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано
Жогорку Кенешем Кыргызской Республики
либо заключено по поручению Жогорку Кенеша Кыргызской Республики во исполнение соглашения, ратифицированного Жогорку Кенешем
Кыргызской Республики, устанавливает иные нормы, чем предусмотренные налоговым законодательством Кыргызской Республики, то к
урегулированным таким соглашением налоговым отношениям применяются нормы этого соглашения.
(В редакции Законов КР от 30 апреля 2009 года N 143, 29 мая 2009 года N 175)

См.:
постановление Правительства КР от 15 мая 2012 года N 298 "Об утверждении Положения о порядке применения соглашений (конвенций)
об избежании двойного налогообложения и предотвращении уклонения от уплаты налогов на доход и капитал (имущество), заключенных
Кыргызской Республикой с иностранными государствами\""""

ARTICLES_BUILD_TEXT = u"""
Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской
Республики

1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...
2. Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.
3. К отношениям по взиманию налогов с перемещаемых через таможенную границу...

Статья 2. Налоговое законодательство Кыргызской Республики

1. Налоговое законодательство Кыргызской Республики - это система нормативных правовых...
2. Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...
3. Настоящий Кодекс устанавливает:...

Статья 3. Действие международных договоров и иных соглашений

1. Если вступившим в установленном законом порядке международным договором, участником...
2. Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...
"""

BUILD_CHAPTERS_WITHOUT_PARAGRAPHS_TEXT = u"""Глава 1
Общие положения\n""" + ARTICLES_BUILD_TEXT + u"""Глава 2
Налоговая система Кыргызской Республики\n""" + ARTICLES_BUILD_TEXT

DIVISIONS_BUILD_TEXT_WITHOUT_SUB_DIVISIONS = u'РАЗДЕЛ I\nОБЩИЕ ПОЛОЖЕНИЯ\n\n' + BUILD_CHAPTERS_WITHOUT_PARAGRAPHS_TEXT \
                                             + u'\nРАЗДЕЛ II\nНАЛОГОВОЕ ОБЯЗАТЕЛЬСТВО И НАЛОГОВАЯ ЗАДОЛЖЕННОСТЬ\n\n'\
                                             + BUILD_CHAPTERS_WITHOUT_PARAGRAPHS_TEXT

PARTS_BUILD_TEXT = u'ОБЩАЯ ЧАСТЬ\n\n'+ DIVISIONS_BUILD_TEXT_WITHOUT_SUB_DIVISIONS\
                   + u'ОСОБЕННАЯ ЧАСТЬ\n\n' + DIVISIONS_BUILD_TEXT_WITHOUT_SUB_DIVISIONS

BUILD_CHAPTERS_WITH_PARAGRAPH_TEXT = u"""
Глава 23
Купля-продажа

Параграф 1
Общие положения о купле-продаже\n\n""" + ARTICLES_BUILD_TEXT + u"""

Параграф 2
Розничная купля-продажа\n\n""" + ARTICLES_BUILD_TEXT

DIVISIONS_WITH_SUB_DIVISIONS_BUILD_TEXT = u'РАЗДЕЛ I\nОБЩИЕ ПОЛОЖЕНИЯ\n\nПодраздел 1. я подраздел 1\n\n'\
    + BUILD_CHAPTERS_WITHOUT_PARAGRAPHS_TEXT + u'\n\nПодраздел 2. я подраздел 2\n\n' + BUILD_CHAPTERS_WITHOUT_PARAGRAPHS_TEXT



class BuilderTest(TestCase):
    def test_build_document_name_with_one_line_document_name(self):
        builder = Builder(DOCUMENT_NAME_WITH_ONE_LINE_TEST_TEXT)
        self.assertEqual(DOCUMENT_NAME_WITH_ONE_LINE_EXPECTED_TEXT, builder.build_document_name())

    def test_build_document_name_with_multi_line_document_name(self):
        builder = Builder(DOCUMENT_NAME_BUILD_WITH_MULTI_LINE_TEST_TEXT)
        self.assertEqual(
            DOCUMENT_NAME_BUILD_WITH_ONE_LINE_TEST_TEXT,
            builder.build_document_name()
        )

    def test_build_document_name_with_line_folding(self):
        builder = Builder(DOCUMENT_NAME_BUILD_WITH_LINE_FOLDING)
        self.assertEqual(
            u'ЗАКОН КЫРГЫЗСКОЙ РЕСПУБЛИКИ  О государственной регистрации юридических лиц, филиалов (представительств)',
            builder.build_document_name()
        )

    def test_build_revisions(self):
        REVISIONS_BUILD_TEST_TEXT
        builder = Builder(REVISIONS_BUILD_TEST_TEXT)
        self.assertEqual(REVISIONS_BUILD_ECPECTED_TEXT, builder.build_revisions())

    def test_build_taking_place(self):
        test_text = u"""г.Бишкек
от 17 октября 2008 года N 230

НАЛОГОВЫЙ КОДЕКС КЫРГЫЗСКОЙ РЕСПУБЛИКИ

(Вводится в действие Законом Кыргызской Республики
от 17 октября 2008 года N 231)"""
        builder = Builder(test_text)
        self.assertEqual(
            u"""г.Бишкек\nот 17 октября 2008 года N 230""", builder.build_taking_place())

    def _test_regex(self, builder, pattern, expected, search_start_position=0):
        actual = re.search(pattern, builder.text[search_start_position:], builder.search_flags).group().strip()
        self.assertEqual(expected, actual)

    def test_regex_article_of_the_document_with_one_line_article_name(self):
        text = u"""
законодательством Кыргызской Республики.

Статья 42. Права налогоплательщика

1. Налогоплательщик имеет """
        builder = Builder(text)
        self._test_regex(builder, builder.article_pattern, expected=u'Статья 42. Права налогоплательщика')

    def test_regex_article_of_the_document_search_last_article(self):
        text = u"""Статья 41. Налогоплательщик

Налогоплательщиком является субъект, на которого возлагается обязанность уплачивать налог при наличии обстоятельств,
установленных налоговым законодательством Кыргызской Республики."""

    def test_regex_article_of_the_document_with_multi_line_article_name(self):
        builder = Builder(ARTICLE_WITH_MULTI_LINE_REGEX_TEST_TEXT)
        self._test_regex(builder, builder.article_pattern, expected=ARTICLE_WITH_MULTI_LINE_REGEX_EXPECTED_TEXT)

    def test_regex_article_with_text_and_without_items(self):
        text = u"""Статья 41. Налогоплательщик
(продолжение имени...)

Налогоплательщиком является субъект, на которого возлагается обязанность уплачивать налог
при наличии обстоятельств, установленных налоговым законодательством Кыргызской Республики."""

        expected = u"Статья 41. Налогоплательщик (продолжение имени...)"
        builder = Builder('')
        actual = re.search(builder.article_pattern, text, builder.search_flags).group().strip()
        actual = actual.replace('\n', ' ')
        self.assertEqual(expected, actual)

    def test_regex_items_of_an_article_with_2_items(self):
        builder = Builder(ITEM_OF_AN_ARTICLE_TEST_TEXT)

        pattern = builder.item_of_an_article_pattern_without_checking_end + builder.not_last_items_end_pattern
        ITEM_OF_AN_ARTICLE_EXPECTED_TEXT_1
        self._test_regex(builder, pattern,
                         expected=ITEM_OF_AN_ARTICLE_EXPECTED_TEXT_1)

        pattern = builder.item_of_an_article_pattern_without_checking_end + builder.last_items_end_pattern
        start = len(ITEM_OF_AN_ARTICLE_EXPECTED_TEXT_1)
        self._test_regex(builder, pattern, expected=ITEM_OF_AN_ARTICLE_EXPECTED_TEXT_2, search_start_position=start)

    def test_regex_items_of_an_article_with_3_items(self):
        builder = Builder(u"""Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской
Республики

1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...
2. Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.
3. К отношениям по взиманию налогов с перемещаемых через таможенную границу...
""")
        pattern = builder.item_of_an_article_pattern_without_checking_end + builder.not_last_items_end_pattern
        matches = re.finditer(pattern, builder.text, builder.search_flags)
        m = next(matches)
        self.assertEqual(u'1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...', m.group().strip())

    def test_regex_article_text_pattern(self):
        text = u"""Статья 41. Налогоплательщик

Налогоплательщиком является субъект, на которого возлагается обязанность уплачивать налог при наличии
обстоятельств, установленных налоговым законодательством Кыргызской Республики."""
        builder = Builder(text)
        start = len(u'Статья 41. Налогоплательщик')
        self._test_regex(builder, builder.article_text_pattern,
                         expected=u"""Налогоплательщиком является субъект, на которого возлагается обязанность уплачивать налог при наличии
обстоятельств, установленных налоговым законодательством Кыргызской Республики.""", search_start_position=start)

    def test_regex_paragraph_pattern(self):
        text = u"""Параграф 2
Розничная купля-продажа

Статья 455"""
        builder = Builder('')
        actual_text = re.search(builder.paragraph_pattern, text, builder.search_flags).group().replace('\n', ' ').strip()
        expected_text = u'Параграф 2 Розничная купля-продажа'
        self.assertEqual(expected_text, actual_text)

    def test_regex_chapter_of_the_document(self):
        text = u"""частия.

Глава 2
Налоговая система Кыргызской Республики

С"""
        builder = Builder('')
        actual = re.search(builder.chapter_pattern, text, builder.search_flags).group().replace('\n', ' ').strip()
        expected = u'Глава 2 Налоговая система Кыргызской Республики'
        self.assertEqual(expected, actual)

    def test_regex_division_of_the_document(self):
        text = u"""
РАЗДЕЛ III
НАЛОГОВОЕ ОБЯЗАТЕЛЬСТВО И НАЛОГОВАЯ ЗАДОЛЖЕННОСТЬ

Г"""
        builder = Builder('')
        actual = re.search(builder.division_pattern, text, builder.search_flags).group().replace('\n', ' ').strip()
        expected = u'РАЗДЕЛ III НАЛОГОВОЕ ОБЯЗАТЕЛЬСТВО И НАЛОГОВАЯ ЗАДОЛЖЕННОСТЬ'
        self.assertEqual(expected, actual)

    def test_regex_part_of_the_document(self):
        text = u"""ОСОБЕННАЯ ЧАСТЬ

Статья 153. Термины и определения, используемые в Особенной части
настоящего Кодекса"""
        builder = Builder('')
        actual = re.search(builder.part_pattern, text, builder.search_flags).group().replace('\n', ' ').strip()
        expected = u'ОСОБЕННАЯ ЧАСТЬ'
        self.assertEqual(expected, actual)

    def test_build_articles_with_items(self):
        builder = Builder(ARTICLES_BUILD_TEXT)
        start_of_chapter = 0
        end_of_chapter = len(ARTICLES_BUILD_TEXT)
        expected = self._build_expected_articles_with_items()
        actual = builder.build_articles(start_of_chapter, end_of_chapter)
        self.assertEqual(expected, actual)

    def _build_expected_articles_with_items(self):
        expected_articles = []

        article = TextSection(level='article', name=u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской Республики', number=u'1')

        item = TextSection(level='article1_item', name='', number=u'1')
        item.text = u'Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number=u'2')
        item.text = u'Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number=u'3')
        item.text = u'К отношениям по взиманию налогов с перемещаемых через таможенную границу...'
        article.add_section(item)

        expected_articles.append(article)

        article = TextSection(level='article', name=u'Статья 2. Налоговое законодательство Кыргызской Республики', number=u'2')

        item = TextSection(level='article2_item', name='', number=u'1')
        item.text = u'Налоговое законодательство Кыргызской Республики - это система нормативных правовых...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number=u'2')
        item.text = u'Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number=u'3')
        item.text = u'Настоящий Кодекс устанавливает:...'
        article.add_section(item)

        expected_articles.append(article)

        article = TextSection(level='article', name=u'Статья 3. Действие международных договоров и иных соглашений', number=u'3')

        item = TextSection(level='article3_item', name='', number=u'1')
        item.text = u'Если вступившим в установленном законом порядке международным договором, участником...'
        article.add_section(item)

        item = TextSection(level='article3_item', name='', number=u'2')
        item.text = u'Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...'
        article.add_section(item)

        expected_articles.append(article)
        return expected_articles

    def test_build_article_with_text(self):
        text = u"""Статья 41. Налогоплательщик

Налогоплательщиком является субъект, на которого возлагается обязанность
уплачивать налог при наличии обстоятельств, установленных налоговым законодательством Кыргызской Республики."""

        expected = TextSection(level=u'article', name=u'Статья 41. Налогоплательщик', number=u'41')
        expected.text = u"""Налогоплательщиком является субъект, на которого возлагается обязанность
уплачивать налог при наличии обстоятельств, установленных налоговым законодательством Кыргызской Республики."""
        builder = Builder(text)
        actual = builder.build_articles(0, len(text))[0]
        self.assertEqual(expected, actual)

    def test_build_chapters_without_paragraph(self):
        builder = Builder(BUILD_CHAPTERS_WITHOUT_PARAGRAPHS_TEXT)
        expected_chapters = self._build_expected_chapters_without_paragraphs()
        actual_chapters = builder.build_chapters(0, len(BUILD_CHAPTERS_WITHOUT_PARAGRAPHS_TEXT))
        self.assertEqual(expected_chapters, actual_chapters)

    def _build_expected_chapters_without_paragraphs(self):
        expected_chapters = []
        chapter = Section(level=u'chapter', name=u'Глава 1 Общие положения', number=u'1')
        articles = self._build_expected_articles_with_items()
        self._add_sub_sections_to_section(chapter, articles)
        expected_chapters.append(chapter)
        chapter = Section(level=u'chapter', name=u'Глава 2 Налоговая система Кыргызской Республики', number=u'2')
        self._add_sub_sections_to_section(chapter, articles)
        expected_chapters.append(chapter)
        return expected_chapters

    def test_build_chapters_with_paragraph(self):
        builder = Builder(BUILD_CHAPTERS_WITH_PARAGRAPH_TEXT)
        expected_chapters = self._build_expected_chapters_with_paragraphs()
        actual_chapters = builder.build_chapters(0, len(BUILD_CHAPTERS_WITH_PARAGRAPH_TEXT))
        self.assertEqual(expected_chapters, actual_chapters)

    def _build_expected_chapters_with_paragraphs(self):
        expected_chapters = []

        chapter = Section(level=u'chapter', name=u'Глава 23 Купля-продажа', number=u'23')

        paragraph = Section(level=u'chapter23_paragraph', name=u'Параграф 1 Общие положения о купле-продаже', number=u'1')
        articles = self._build_expected_articles_with_items()
        self._add_sub_sections_to_section(paragraph, articles)
        chapter.add_section(paragraph)

        paragraph = Section(level=u'chapter23_paragraph', name=u'Параграф 2 Розничная купля-продажа', number=u'2')
        articles = self._build_expected_articles_with_items()
        self._add_sub_sections_to_section(paragraph, articles)
        chapter.add_section(paragraph)

        expected_chapters.append(chapter)
        return expected_chapters

    def test_build_divisions_without_sub_divisions(self):
        builder = Builder(DIVISIONS_BUILD_TEXT_WITHOUT_SUB_DIVISIONS)
        expected_divisions = self._build_expected_divisions_without_sub_divisions()
        actual_divisions = builder.build_divisions(0, len(DIVISIONS_BUILD_TEXT_WITHOUT_SUB_DIVISIONS))
        self.assertEqual(expected_divisions, actual_divisions)

    def _build_expected_divisions_without_sub_divisions(self):
        expected_divisions = []
        division = Section(level=u'division', name=u'РАЗДЕЛ I ОБЩИЕ ПОЛОЖЕНИЯ', number=u'I')
        chapters = self._build_expected_chapters_without_paragraphs()
        self._add_sub_sections_to_section(division, chapters)
        expected_divisions.append(division)
        division = Section(level=u'division', name=u'РАЗДЕЛ II НАЛОГОВОЕ ОБЯЗАТЕЛЬСТВО И НАЛОГОВАЯ ЗАДОЛЖЕННОСТЬ', number=u'II')
        self._add_sub_sections_to_section(division, chapters)
        expected_divisions.append(division)
        return expected_divisions

    def test_build_division_with_sub_divisions(self):
        builder = Builder(DIVISIONS_WITH_SUB_DIVISIONS_BUILD_TEXT)
        expected_division = self._build_expected_sub_divisions_without_sub_divisions()
        actual_division = builder.build_divisions(0, len(DIVISIONS_WITH_SUB_DIVISIONS_BUILD_TEXT))
        self.assertEqual(expected_division, actual_division)

    def _build_expected_sub_divisions_without_sub_divisions(self):
        expected_divisions = []
        chapters = self._build_expected_chapters_without_paragraphs()
        division = Section(level=u'division', name=u'РАЗДЕЛ I ОБЩИЕ ПОЛОЖЕНИЯ', number=u'I')
        sub_division = Section(level=u'divisionI_sub_division', name=u'Подраздел 1. я подраздел 1', number=u'1')
        self._add_sub_sections_to_section(sub_division, chapters)
        division.add_section(sub_division)
        sub_division = Section(level=u'divisionI_sub_division', name=u'Подраздел 2. я подраздел 2', number=u'2')
        self._add_sub_sections_to_section(sub_division, chapters)
        division.add_section(sub_division)
        expected_divisions.append(division)
        return expected_divisions

    def test_build_parts(self):
        builder = Builder(PARTS_BUILD_TEXT)
        expected_parts = self._build_expected_parts()
        actual_parts = builder.build_parts()
        self.assertEqual(expected_parts, actual_parts)

    def _build_expected_parts(self):
        expected_parts = []
        part = Section(level=u'part', name=u'ОБЩАЯ ЧАСТЬ', number='1')
        divisions = self._build_expected_divisions_without_sub_divisions()
        self._add_sub_sections_to_section(part, divisions)
        expected_parts.append(part)
        part = Section(level=u'part', name=u'ОСОБЕННАЯ ЧАСТЬ', number='2')
        self._add_sub_sections_to_section(part, divisions)
        expected_parts.append(part)
        return expected_parts

    def _add_sub_sections_to_section(self, section, sections):
        for i in sections:
            section.add_section(i)