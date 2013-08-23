#coding=utf-8
import re
import copy
from elements.section import Section
from elements.text_section import TextSection


class Builder(object):
    def __init__(self, text):
        self._start_of_content_of_a_building_sections = []
        self._end_of_content_of_a_building_sections = []
        self._text = text
        self._search_flags = re.M | re.I | re.DOTALL | re.U
        self._name_pattern = u'^[ а-яА-Я]+?КЫРГЫЗСКОЙ РЕСПУБЛИКИ.*?(?=(^\(.+?Закон))'
        self._revisions_pattern = u'^\(В редакции Законов КР от .+?\)'
        self._taking_place_pattern = u'г\.[а-яА-Я]+\nот.+?$'
        self._article_pattern = u'^ *Статья (?P<number>\d+)\.(?P<name>.+?(?=\n[ \t]*?\n))'
        self._item_of_an_article_pattern_without_checking_end = u'^(?P<number>\d+)\.(?P<text>.+'
        self._not_last_items_end_pattern = u'?)(?=^\d+\.)'
        self._last_items_end_pattern = u')'
        self._article_text_pattern = u'.+'
        self._chapter_pattern = u'^ *?Глава (?P<number>\d+)(?P<name> *?\s*.*?$)'
        self._division_pattern = u'^ *?РАЗДЕЛ (?P<number>[IVXLCDM]+)(?P<name> *?\s*.*?$)'
        self._sub_division_pattern = u'^ *?Подраздел (?P<number>\d+)\.?(?P<name> *?\s*.*?$)'
        self._part_of_the_document_pattern = u'(?P<name>^[\w ]*? *ЧАСТЬ.*?)(?P<number> )?\n\n'
        self._paragraph_pattern = u'^ *?Параграф (?P<number>\d+)(?P<name>.+?(?=\n[ \t]*?\n))'

    @property
    def text(self):
        return self._text

    @property
    def name_pattern(self):
        return self._name_pattern

    @property
    def revisions_pattern (self):
        return self._revisions_pattern

    @property
    def taking_place_pattern(self):
        return self._taking_place_pattern

    @property
    def part_pattern(self):
        return self._part_of_the_document_pattern

    @property
    def division_pattern(self):
        return self._division_pattern

    @property
    def chapter_pattern(self):
        return self._chapter_pattern

    @property
    def paragraph_pattern(self):
        return self._paragraph_pattern

    @property
    def article_pattern(self):
        return self._article_pattern

    @property
    def item_of_an_article_pattern_without_checking_end(self):
        return self._item_of_an_article_pattern_without_checking_end

    @property
    def not_last_items_end_pattern(self):
        return self._not_last_items_end_pattern

    @property
    def last_items_end_pattern(self):
        return self._last_items_end_pattern

    @property
    def search_flags(self):
        return self._search_flags

    @property
    def article_text_pattern(self):
        return self._article_text_pattern

    def build_document_name(self):
        result = re.search(self._name_pattern, self._text, self._search_flags)
        result = re.sub('\n', ' ', result.group())
        result = result.strip()
        return result

    def build_revisions(self):
        result = re.search(self._revisions_pattern, self._text, self._search_flags)
        return result.group()

    def build_taking_place(self):
        result = re.search(self._taking_place_pattern, self._text, self._search_flags)
        return result.group()

    def build_parts(self):
        parts = self._build_empty_parts_and_save_its_start_and_end_of_content_positions(
            u'part', self.part_pattern, 0,  len(self.text))

        self._add_content_to_built_parts(parts)

        return parts

    def _build_empty_parts_and_save_its_start_and_end_of_content_positions(
         self, level_of_section, search_pattern, start_of_section, end_of_section):
        matches = self._get_matches_iterator(search_pattern, start_of_section, end_of_section)
        sections = []
        self._start_of_content_of_a_building_sections = []
        self._end_of_content_of_a_building_sections = []
        temp = []
        for m in matches:
            sections.append(Section(level=level_of_section, name=m.group('name').replace('\n', ' ').strip(), number=m.group('number')))
            temp.append(m.start())
            self._start_of_content_of_a_building_sections.append(m.start() + len(m.group()))
        temp.remove(temp[0])
        i, length = 0, len(temp)
        while i < length:
            self._end_of_content_of_a_building_sections.append(temp[i])
            i += 1
        self._end_of_content_of_a_building_sections.append(end_of_section)
        return sections

    def _add_content_to_built_parts(self, parts):
        i = 0
        section_start_of_content_of_abuilding_sections = copy.deepcopy(self._start_of_content_of_a_building_sections)
        section_end_of_content_of_abuilding_sections = copy.deepcopy(self._end_of_content_of_a_building_sections)
        for j in parts:
            sub_sections = self.build_divisions(section_start_of_content_of_abuilding_sections[i], section_end_of_content_of_abuilding_sections[i])
            for sub_section in sub_sections:
                j.add_section(sub_section)
            i += 1

    def build_divisions(self, start_of_section, end_of_section):
        divisions = self._build_empty_divisions_and_save_its_start_and_end_of_content_positions(
            u'division', self.division_pattern, start_of_section,  end_of_section)

        self._add_content_to_built_divisions(divisions)

        return divisions

    def _build_empty_divisions_and_save_its_start_and_end_of_content_positions(
         self, level_of_section, search_pattern, start_of_section, end_of_section):
        matches = self._get_matches_iterator(search_pattern, start_of_section, end_of_section)
        sections = []
        self._start_of_content_of_a_building_sections = []
        self._end_of_content_of_a_building_sections = []
        temp = []
        for m in matches:
            sections.append(Section(level=level_of_section, name=m.group('name').replace('\n', ' ').strip(), number=m.group('number')))
            temp.append(m.start()+start_of_section)
            self._start_of_content_of_a_building_sections.append(m.start() + start_of_section + len(m.group()))
        temp.remove(temp[0])
        i, length = 0, len(temp)
        while i < length:
            self._end_of_content_of_a_building_sections.append(temp[i])
            i += 1
        self._end_of_content_of_a_building_sections.append(end_of_section)
        return sections

    def _add_content_to_built_divisions(self, chapters):
        i = 0
        section_start_of_content_of_abuilding_sections = copy.deepcopy(self._start_of_content_of_a_building_sections)
        section_end_of_content_of_abuilding_sections = copy.deepcopy(self._end_of_content_of_a_building_sections)
        for j in chapters:
            sub_sections = self._build_sub_divisions(
                j.level+j.number+u'_sub_division', section_start_of_content_of_abuilding_sections[i], section_end_of_content_of_abuilding_sections[i])
            if sub_sections == []:
                sub_sections = self.build_chapters(section_start_of_content_of_abuilding_sections[i], section_end_of_content_of_abuilding_sections[i])
            for sub_section in sub_sections:
                j.add_section(sub_section)
            i += 1

    def _build_sub_divisions(self, level_name, start_of_section, end_of_section):
        sub_divisions = self._build_empty_sub_divisions_and_save_its_start_and_end_of_content_positions(
            level_name, self._sub_division_pattern, start_of_section,  end_of_section)

        self._add_content_to_build_sub_divisions(sub_divisions)

        return sub_divisions

    def _build_empty_sub_divisions_and_save_its_start_and_end_of_content_positions(
         self, level_name, search_pattern, start_of_section, end_of_section):
        matches = self._get_matches_iterator(search_pattern, start_of_section, end_of_section)
        sections = []
        self._start_of_content_of_a_building_sections = []
        self._end_of_content_of_a_building_sections = []
        temp = []
        for m in matches:
            sections.append(Section(level=level_name, name=m.group('name').replace('\n', ' ').strip(), number=m.group('number')))
            temp.append(m.start()+start_of_section)
            self._start_of_content_of_a_building_sections.append(m.start() + start_of_section + len(m.group()))
        if not temp == []:
            temp.remove(temp[0])
        i, length = 0, len(temp)
        while i < length:
            self._end_of_content_of_a_building_sections.append(temp[i])
            i += 1
        self._end_of_content_of_a_building_sections.append(end_of_section)
        return sections

    def _add_content_to_build_sub_divisions(self, chapters):
        i = 0
        section_start_of_content_of_abuilding_sections = copy.deepcopy(self._start_of_content_of_a_building_sections)
        section_end_of_content_of_abuilding_sections = copy.deepcopy(self._end_of_content_of_a_building_sections)
        for j in chapters:
            sub_sections = self.build_chapters(section_start_of_content_of_abuilding_sections[i], section_end_of_content_of_abuilding_sections[i])
            for sub_section in sub_sections:
                j.add_section(sub_section)
            i += 1

    def build_chapters(self, start_of_section, end_of_section):
        chapters = self._build_empty_chapters_and_save_its_start_and_end_of_content_positions(
            u'chapter', self.chapter_pattern, start_of_section,  end_of_section)

        self._add_content_to_built_chapters(chapters)

        return chapters

    def _build_empty_chapters_and_save_its_start_and_end_of_content_positions(
         self, level, search_pattern, start_of_section, end_of_section):
        matches = self._get_matches_iterator(search_pattern, start_of_section, end_of_section)
        sections = []
        self._start_of_content_of_a_building_sections = []
        self._end_of_content_of_a_building_sections = []
        temp = []
        for m in matches:
            sections.append(Section(level=level, name=m.group('name').replace('\n', ' ').strip(), number=m.group('number')))
            temp.append(m.start()+start_of_section)
            self._start_of_content_of_a_building_sections.append(m.start() + start_of_section + len(m.group()))
        temp.remove(temp[0])
        i, length = 0, len(temp)
        while i < length:
            self._end_of_content_of_a_building_sections.append(temp[i])
            i += 1
        self._end_of_content_of_a_building_sections.append(end_of_section)
        return sections

    def _add_content_to_built_chapters(self, chapters):
        i = 0
        section_start_of_content_of_abuilding_sections = copy.deepcopy(self._start_of_content_of_a_building_sections)
        section_end_of_content_of_abuilding_sections = copy.deepcopy(self._end_of_content_of_a_building_sections)
        for j in chapters:
            sub_sections = self.build_paragraphs(j.level+j.number+u'_paragraph',
                                                 section_start_of_content_of_abuilding_sections[i], section_end_of_content_of_abuilding_sections[i])
            if sub_sections == []:
                sub_sections = self.build_articles(section_start_of_content_of_abuilding_sections[i], section_end_of_content_of_abuilding_sections[i])
            for sub_section in sub_sections:
                j.add_section(sub_section)
            i += 1

    def build_paragraphs(self, level_name,  start_of_section, end_of_section):
        paragraphs = self._build_empty_paragraphs__and_save_its_start_and_end_of_content_positions(
            level_name, self.paragraph_pattern, start_of_section, end_of_section)

        self._add_content_to_built_paragraphs(paragraphs)

        return paragraphs

    def _build_empty_paragraphs__and_save_its_start_and_end_of_content_positions(self, level, search_pattern, start_of_section, end_of_section):
        matches = self._get_matches_iterator(search_pattern, start_of_section, end_of_section)
        sections = []
        self._start_of_content_of_a_building_sections = []
        self._end_of_content_of_a_building_sections = []
        temp = []
        for m in matches:
            sections.append(Section(level=level, name=m.group('name').replace('\n', ' ').strip(), number=m.group('number')))
            temp.append(m.start()+start_of_section)
            self._start_of_content_of_a_building_sections.append(m.start() + start_of_section + len(m.group()))
        if not temp == []:
            temp.remove(temp[0])
        i, length = 0, len(temp)
        while i < length:
            self._end_of_content_of_a_building_sections.append(temp[i])
            i += 1
        self._end_of_content_of_a_building_sections.append(end_of_section)
        return sections

    def _add_content_to_built_paragraphs(self, paragraphs):
        i = 0
        section_start_of_content_of_abuilding_sections = copy.deepcopy(self._start_of_content_of_a_building_sections)
        section_end_of_content_of_abuilding_sections = copy.deepcopy(self._end_of_content_of_a_building_sections)
        for j in paragraphs:
            sub_sections = self.build_articles(section_start_of_content_of_abuilding_sections[i], section_end_of_content_of_abuilding_sections[i])
            for sub_section in sub_sections:
                j.add_section(sub_section)
            i += 1

    def build_articles(self, start_of_section, end_of_section):
        articles = self._build_empty_articles_and_save_its_start_and_end_of_content_positions(
            u'article',self.article_pattern, start_of_section,  end_of_section)

        self._add_content_to_built_articles(articles)

        return articles

    def _build_empty_articles_and_save_its_start_and_end_of_content_positions(self, level, search_pattern, start_of_section, end_of_section):
        matches = self._get_matches_iterator(search_pattern, start_of_section, end_of_section)
        articles = []
        self._start_of_content_of_a_building_sections = []
        self._end_of_content_of_a_building_sections = []
        temp = []
        for m in matches:
            articles.append(TextSection(
                level=level, name=m.group('name').replace('\n', ' ').strip(), number=m.group('number')))
            temp.append(m.start()+start_of_section)
            self._start_of_content_of_a_building_sections.append(m.start() + start_of_section + len(m.group()))
        temp.remove(temp[0])
        i, length = 0, len(temp)
        while i < length:
            self._end_of_content_of_a_building_sections.append(temp[i])
            i += 1
        self._end_of_content_of_a_building_sections.append(end_of_section)
        return articles

    def _add_content_to_built_articles(self, articles):
        i = 0
        for article in articles:
            items = self._build_items(self._start_of_content_of_a_building_sections[i], self._end_of_content_of_a_building_sections[i])
            if items == []:
                text = self._build_article_text(self._start_of_content_of_a_building_sections[i],  self._end_of_content_of_a_building_sections[i])
                article.text = text
            else:
                for item in items:
                    article.add_section(item)
            i += 1

    def _build_items(self, start, end):
        items = []
        matches = self._get_matches_iterator(self.item_of_an_article_pattern_without_checking_end+self.not_last_items_end_pattern, start, end)
        last_item_start = start
        for m in matches:
            item = TextSection(level='item', name='', number=m.group('number'))
            item.text = m.group('text').strip()
            last_item_start += len(item.text)
            items.append(item)
        matches = self._get_matches_iterator(self.item_of_an_article_pattern_without_checking_end + self.last_items_end_pattern, last_item_start, end)
        for m in matches:
            item = TextSection(level='item', name='', number=m.group('number'))
            item.text = m.group('text').strip()
            items.append(item)
        return items

    def _build_article_text(self, start, end):
        text = re.search(self.article_text_pattern, self.text[start:end], self.search_flags).group().strip()
        return text

    def _get_matches_iterator(self, pattern, start, end):
        return re.finditer(pattern, self.text[start:end], self.search_flags)