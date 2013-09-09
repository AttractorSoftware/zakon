#coding=utf-8
import re
import copy
from nose import result
from elements.section import Section
from elements.text_section import TextSection
from StructureElement import ElementBuild


class ParserError(Exception):
    pass

class Builder(object):
    def __init__(self, text):
        # self._start_of_content_of_a_building_sections = []
        # self._end_of_content_of_a_building_sections = []
        self._text = text
        self._search_flags = re.M | re.DOTALL | re.U

        self._name_build_info = ElementBuild(u'^[ а-яА-Я]+?КЫРГЫЗСКОЙ РЕСПУБЛИКИ.*?(?=^\()', self._search_flags)
        self._place_and_date_build_info = ElementBuild(u'^г\.[а-яА-Я]+\n*?от.+?$', self._search_flags)
        self._revisions_build_info = ElementBuild(u'^\(В редакции Законов КР от .+?\)', self._search_flags)

        #part usually does't contain number. We have to do number manually
        self._part_number = 1

        self._part_build_info = ElementBuild(u'(?P<name>^[\w ]*? *ЧАСТЬ.*?)(?P<number> )?$', self._search_flags, 'part')

        self._division_build_info =  ElementBuild(u'(?P<name>^ *?РАЗДЕЛ (?P<number>[IVXLCDM]+) *?\s*.*?$)', self._search_flags, 'division')

        self._sub_division_build_info = ElementBuild(u'(?P<name>^ *?Подраздел (?P<number>\d+)\.? *?\s*.*?$)', self._search_flags)

        self._chapter_build_info = ElementBuild(u'(?P<name>^ *?Глава (?P<number>\d+) *?\s*.*?$)', self._search_flags, 'chapter')

        self._paragraphs_build_info = ElementBuild(u'(?P<name>^ *?Параграф (?P<number>\d+).+?(?=\n[ \t]*?\n))', self._search_flags)

        self._article_build_info = ElementBuild(u'(?P<name>^ *Статья (?P<number>\d+)\..+?(?=\n[ \t]*?\n))', self._search_flags, 'article')
        self._article_text_build_info = ElementBuild(u'.+', self._search_flags)

        self._last_item_build_info = ElementBuild(u'^(?P<number>\d+)\.(?P<text>.+)', self._search_flags)
        self._not_last_item_build_info = ElementBuild(u'^(?P<number>\d+)\.(?P<text>.+?)(?=^\d+\.)', self._search_flags)

        self._start_of_sections = self._find_start_of_sections()

    def _get_match_text(self, template):
        match = template.search(self._text)
        if match:
            return match.group()

    def _get_first_highest_section_text(self):
        text = self._get_match_text(self._part_build_info.template)
        if text is None:
            text = self._get_match_text(self._division_build_info.template)
        if text is None:
            text = self._get_match_text(self._chapter_build_info.template)
        if text is None:
            text = self._get_match_text(self._article_build_info.template)
        return text

    def _find_start_of_sections(self):
        highest_section_text = self._get_first_highest_section_text()
        last_match_of_first_highest_section = None
        if highest_section_text:
            template = re.compile(highest_section_text, self._search_flags)
            iterator = self._get_iterator(template, 0, len(self._text))
            for match in iterator:
                last_match_of_first_highest_section = match
        return last_match_of_first_highest_section.start() if last_match_of_first_highest_section else len(self._text)

    def build_sections(self):
        sections = self.build_parts(self._start_of_sections)
        if sections == []:
            sections = self.build_divisions(self._start_of_sections, len(self._text))
            if sections == []:
                sections = self.build_chapters(self._start_of_sections, len(self._text))
                if sections == []:
                    sections = self.build_articles(self._start_of_sections, len(self._text))
        return sections

    def _find_match_text_or_raise_error_with_msg(self, template, error_msg):
        match = template.search(self._text)
        if match:
            result = match.group().strip()
        else:
            raise ParserError(error_msg)
        return result

    def build_name(self):
        return self._find_match_text_or_raise_error_with_msg(self._name_build_info.template, u'Не найдено наименование закона')

    def build_revisions(self):
        return self._find_match_text_or_raise_error_with_msg(self._revisions_build_info.template, u'Не найдены ревизии закона')

    def build_place_and_date(self):
        return self._find_match_text_or_raise_error_with_msg(self._place_and_date_build_info.template, u'Не найдены место и дата принятия')

    def _get_iterator(self, template, start, end):
        return template.finditer(self._text[start:end])

    def build_parts(self, section_start):
        parts = self._build_empty_sections_and_save_its_start_and_end_of_content_positions(
            self._part_build_info.level, self._part_build_info.template, section_start, len(self._text), self.create_Section
        )
        build_childer_methods = [self.build_divisions]
        self._add_content_to_built_sections(parts, build_childer_methods, self._add_sub_sections)

        return parts

    def build_divisions(self, section_start, section_end, parent_level_and_number=None):
        divisions = self._build_empty_sections_and_save_its_start_and_end_of_content_positions(
            self._division_build_info.level, self._division_build_info.template, section_start, section_end, self.create_Section
        )
        build_children_methods = [self.build_sub_divisions, self.build_chapters]
        self._add_content_to_built_sections(divisions, build_children_methods, self._add_sub_sections)

        return divisions

    def build_sub_divisions(self, section_start, section_end, parent_level_and_number=None):
        self._sub_division_build_info.level = parent_level_and_number + '_''sub_division'
        sub_divisions = self._build_empty_sections_and_save_its_start_and_end_of_content_positions(
            self._sub_division_build_info.level, self._sub_division_build_info.template, section_start, section_end, self.create_Section
        )
        build_children_methods = [self.build_chapters]
        self._add_content_to_built_sections(sub_divisions, build_children_methods, self._add_sub_sections)

        return sub_divisions

    def build_chapters(self, section_start, section_end, parent_level_and_number=None):
        chapters = self._build_empty_sections_and_save_its_start_and_end_of_content_positions(
            self._chapter_build_info.level, self._chapter_build_info.template, section_start, section_end, self.create_Section)

        build_children_methods = [self.build_paragraphs, self.build_articles]
        self._add_content_to_built_sections(chapters, build_children_methods, self._add_sub_sections)
        return chapters

    def build_paragraphs(self, section_start, section_end, parent_level_and_number=None):
        self._paragraphs_build_info.level = parent_level_and_number + '_''paragraph'
        paragraphs = self._build_empty_sections_and_save_its_start_and_end_of_content_positions(
            self._paragraphs_build_info.level, self._paragraphs_build_info.template, section_start, section_end, self.create_Section)
        build_childer_methods = [self.build_articles]
        self._add_content_to_built_sections(paragraphs, build_childer_methods, self._add_sub_sections)

        return paragraphs

    def build_articles(self, start_of_sections, end_of_sections, parent_level_and_number=None):
        articles = self._build_empty_sections_and_save_its_start_and_end_of_content_positions(
            self._article_build_info.level, self._article_build_info.template, start_of_sections,  end_of_sections, self.create_TextSection)

        build_childer_methods = [self._build_items, self._build_article_text]

        self._add_content_to_built_sections(articles, build_childer_methods, self._add_text_or_sub_sections)

        return articles

    def _add_sub_sections(self, section, sub_sections):
        for sec in sub_sections:
            section.add_section(sec)

    def _add_text_or_sub_sections(self, article, sub_sections):
        if type(sub_sections) is list:
            self._add_sub_sections(article, sub_sections)
        else:
            article.text = sub_sections

    def _build_items(self, content_start, content_end, parent_level_and_number):
        self._not_last_item_build_info.level = parent_level_and_number + '_item'
        items = []

        matches = self._get_iterator(self._not_last_item_build_info.template, content_start, content_end)
        last_item_start = content_start
        for m in matches:
            item = TextSection(self._not_last_item_build_info.level, name='', number=m.group('number'))
            item.text = m.group('text').strip()
            last_item_start += len(item.text)
            items.append(item)

        self._last_item_build_info.level = parent_level_and_number + '_item'
        matches = self._get_iterator(self._last_item_build_info.template, last_item_start, content_end)
        for m in matches:
            item = TextSection(parent_level_and_number+'_item', name='', number=m.group('number'))
            item.text = m.group('text').strip()
            items.append(item)
        return items

    def _build_article_text(self, start, end, parent_level_and_number=None):
        match = self._article_text_build_info.template.search(self._text[start:end])
        result = match.group().strip()
        return result

    def _build_empty_sections_and_save_its_start_and_end_of_content_positions(self, level, template, section_start, section_end, create_section):
        match_iterator = self._get_iterator(template, section_start, section_end)
        sections = []
        self._start_of_sections_content = []
        self._end_of_sections_content= []
        to_find_end_of_sections_content_list = []
        for m in match_iterator:
            sections.append(create_section(level, m))
            to_find_end_of_sections_content_list.append(m.start()+section_start)
            self._start_of_sections_content.append(m.start() + section_start+len(m.group()))
        if not to_find_end_of_sections_content_list == []:
            to_find_end_of_sections_content_list.remove(to_find_end_of_sections_content_list[0])
        for i in to_find_end_of_sections_content_list:
            self._end_of_sections_content.append(i)
        self._end_of_sections_content.append(section_end)
        return sections

    def _add_content_to_built_sections(self, sections, build_children_methods, add_sub_sections_method):
        i = 0
        start_of_sections_content = copy.copy(self._start_of_sections_content)
        end_of_sections_content= copy.copy(self._end_of_sections_content)
        for section in sections:
            parent_level_and_number = section.level+(section.number)

            j = 0
            sub_sections = []
            while sub_sections == [] and j < len(build_children_methods):
                sub_sections = build_children_methods[j](start_of_sections_content[i], end_of_sections_content[i], parent_level_and_number)
                j += 1
            if sub_sections:
                add_sub_sections_method(section, sub_sections)
            else:
                raise ParserError(u'Ошиибка! "{0}" пустая!'.format(section.name))
            i += 1

    def create_Section(self, level, match):
        number = match.group('number')
        if number is None:
            number = self._part_number
            self._part_number += 1
        return Section(level, match.group('name').replace('\n', ' ').strip(), number=str(number))

    def create_TextSection(self, level, match):
        return TextSection(level=level, name=match.group('name').replace('\n', ' ').strip(), number=match.group('number'))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, a_text):
        self._text = a_text