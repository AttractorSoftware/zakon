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
        self._name_pattern = u'^[ а-яА-Я]+?КЫРГЫЗСКОЙ РЕСПУБЛИКИ.*?(?=\n[ \t]*?\n\()'
        self._revisions_pattern = u'^\(В редакции Законов КР от .+?\)'
        self._taking_place_pattern = u'^г\.[а-яА-Я]+\n*?от.+?$'
        self._article_pattern = u'(?P<name>^ *Статья (?P<number>\d+)\..+?(?=\n[ \t]*?\n))'
        self._item_of_an_article_pattern_without_checking_end = u'^(?P<number>\d+)\.(?P<text>.+'
        self._not_last_items_end_pattern = u'?)(?=^\d+\.)'
        self._last_items_end_pattern = u')'
        self._article_text_pattern = u'.+'
        self._chapter_pattern = u'(?P<name>^ *?Глава (?P<number>\d+) *?\s*.*?$)'
        self._division_pattern = u'(?P<name>^ *?РАЗДЕЛ (?P<number>[IVXLCDM]+) *?\s*.*?$)'
        self._sub_division_pattern = u'(?P<name>^ *?Подраздел (?P<number>\d+)\.? *?\s*.*?$)'
        self._part_of_the_document_pattern = u'(?P<name>^[\w ]*? *ЧАСТЬ.*?)(?P<number> )?\n\n'
        self._paragraph_pattern = u'(?P<name>^ *?Параграф (?P<number>\d+).+?(?=\n[ \t]*?\n))'
        self._part_number = 1 #part usually does't contain number. We have to do number manually

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
        if result:
            result = re.sub('\n', ' ', result.group())
            result = result.strip()
        else:
            result=u'Без имени.'
        return result

    def build_revisions(self):
        result = re.search(self._revisions_pattern, self._text, self._search_flags)
        return result.group() if result else u''

    def build_taking_place(self):
        result = re.search(self._taking_place_pattern, self._text, self._search_flags)
        return result.group() if result else u''

    def build_parts(self):
        parts = self._build_empty_sections_and_save_its_start_and_end_of_content_positions(
            u'part', self._part_of_the_document_pattern, 0,  len(self._text), self.create_Section)

        self._add_content_to_built_sections(parts, self.build_divisions)

        return parts

    def build_divisions(self, start_of_section, end_of_section, parent_level_parent_number=None):
        divisions = self._build_empty_sections_and_save_its_start_and_end_of_content_positions(
            u'division', self._division_pattern, start_of_section,  end_of_section, self.create_Section)

        self._add_content_to_built_divisions(divisions)

        return divisions

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

    def _build_sub_divisions(self, level_name, start_of_section, end_of_section, parent_level_parent_number=None):
        sub_divisions = self._build_empty_sections_and_save_its_start_and_end_of_content_positions(
            level_name, self._sub_division_pattern, start_of_section, end_of_section, self.create_Section)

        self._add_content_to_built_sections(sub_divisions, self.build_chapters)

        return sub_divisions

    def build_chapters(self, start_of_section, end_of_section, parent_level_parent_number=None):
        chapters = self._build_empty_chapters_and_save_its_start_and_end_of_content_positions(
            u'chapter', self._chapter_pattern, start_of_section,  end_of_section)

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
        if not temp == []:
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

    def build_paragraphs(self, level_name,  start_of_section, end_of_section, parent_level_parent_number=None):
        paragraphs = self._build_empty_sections_and_save_its_start_and_end_of_content_positions(
            level_name, self._paragraph_pattern, start_of_section, end_of_section, self.create_Section)

        self._add_content_to_built_sections(paragraphs, self.build_articles)

        return paragraphs

    def build_articles(self, start_of_sections, end_of_sections, parent_id=None):
        articles = self._build_empty_sections_and_save_its_start_and_end_of_content_positions(
            u'article',self._article_pattern, start_of_sections,  end_of_sections, subsection_create_function=self.create_TextSection)

        self._add_content_to_built_sections(articles, self._build_items, template_method=self.article_template_method)

        return articles

    def _build_items(self, start, end, parent_level_parent_number):
        items = []
        matches = self._get_matches_iterator(self._item_of_an_article_pattern_without_checking_end+self._not_last_items_end_pattern, start, end)
        last_item_start = start
        for m in matches:
            item = TextSection(level=parent_level_parent_number+'_item', name='', number=m.group('number'))
            item.text = m.group('text').strip()
            last_item_start += len(item.text)
            items.append(item)
        matches = self._get_matches_iterator(self._item_of_an_article_pattern_without_checking_end + self._last_items_end_pattern, last_item_start, end)
        for m in matches:
            item = TextSection(level=parent_level_parent_number+'_item', name='', number=m.group('number'))
            item.text = m.group('text').strip()
            items.append(item)
        return items

    def article_template_method(self, article, content_start, content_end):
        text = self._build_article_text(content_start,  content_end)
        article.text = text

    def _build_article_text(self, start, end):
        text = re.search(self._article_text_pattern, self._text[start:end], self.search_flags).group().strip()
        return text

    def _get_matches_iterator(self, pattern, start, end):
        return re.finditer(pattern, self._text[start:end], self.search_flags)

    #refactor functions
    def _build_empty_sections_and_save_its_start_and_end_of_content_positions(
            self, level_name, search_pattern, start_of_sections, end_of_sections, subsection_create_function):
        matches = self._get_matches_iterator(search_pattern, start_of_sections, end_of_sections)
        sections = []
        self._start_of_content_of_a_building_sections = []
        self._end_of_content_of_a_building_sections = []
        temp = []
        for m in matches:
            sections.append(subsection_create_function(level_name, m))
            temp.append(m.start()+start_of_sections)
            self._start_of_content_of_a_building_sections.append(m.start() + start_of_sections+len(m.group()))
        if not temp == []:
            temp.remove(temp[0])
        i, length = 0, len(temp)
        while i < length:
            self._end_of_content_of_a_building_sections.append(temp[i])
            i += 1
        self._end_of_content_of_a_building_sections.append(end_of_sections)
        return sections

    def _add_content_to_built_sections(self, sections, build_children_method, template_method = None):
        i = 0
        start_content_of_a_building_sections = copy.deepcopy(self._start_of_content_of_a_building_sections)
        end_content_of_a_building_sections = copy.deepcopy(self._end_of_content_of_a_building_sections)
        for j in sections:
            parent_level_parent_number = j.level+(j.number)
            sub_sections = build_children_method(start_content_of_a_building_sections[i], end_content_of_a_building_sections[i], parent_level_parent_number)
            if template_method and sub_sections == []:
                template_method(j, start_content_of_a_building_sections[i], end_content_of_a_building_sections[i])
            else:
                for sub_section in sub_sections:
                    j.add_section(sub_section)
            i += 1

    def create_Section(self, level, match):
        number = match.group('number')
        if not number:
            number = self._part_number
            self._part_number += 1
        return Section(level=level, name=match.group('name').replace('\n', ' ').strip(), number=str(number))

    def create_TextSection(self, level, match):
        return TextSection(level=level, name=match.group('name').replace('\n', ' ').strip(), number=match.group('number'))