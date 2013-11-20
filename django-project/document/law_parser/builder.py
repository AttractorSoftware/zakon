# -*- coding: utf-8 -*-
import re
import copy
from document.law_parser.elements.comment import Comment
from document.law_parser.structure_element import ElementBuild
from elements.section import Section
from elements.text_section import TextSection
from document.rtfparser import RTFParser


class ParserError(Exception):
    pass


class Builder(object):
    def __init__(self, text):
        self._text = text
        self._search_flags = re.M | re.DOTALL | re.U | re.I

        self._name_build_info = ElementBuild(u'(^[ а-яА-Я]+? РЕСПУБЛИКИ.*?)(?=\()', self._search_flags)
        self._place_and_date_build_info = ElementBuild(u'^г\.[а-яА-Я,]*\s*?от.+?$', self._search_flags)
        self._revisions_build_info = ElementBuild(u'^\s*\(В редакции Закон.*? КР от .*?\)', self._search_flags)

        self._part_number = 1

        self._part_build_info = ElementBuild(u'(?P<name>^[\w ]*? *ЧАСТЬ[\sIVXLCDM]*?)(?P<number> )?$',
                                             self._search_flags, 'part')

        self._division_build_info = ElementBuild(u'(?P<name>^ *?РАЗДЕЛ (?P<number>[IVXLCDM]+) *?\s*.*?$)',
                                                 self._search_flags, 'division')

        self._sub_division_build_info = ElementBuild(u'(?P<name>^ *?Подраздел (?P<number>\d+)\.? *?\s*.*?$)',
                                                     self._search_flags)

        self._chapter_build_info = ElementBuild(u'(?P<name>^ *?Глава (?P<number>[\w\d-]*)\s*.*?)(?=\()',
                                                self._search_flags, 'chapter')

        self._chapter_with_comment_build_info = ElementBuild(
            u'(?P<name>^ *?Глава (?P<number>[\w\d]+(-\d+)?)\s*.*?)(?=Параграф|Статья|См|Глава \d+)',
            self._search_flags, 'chapter')
        self._comment_build_info = ElementBuild(u'(?P<name>^\(.*?\))$', self._search_flags)

        self._paragraphs_build_info = ElementBuild(u'(?P<name>^ *?Параграф (?P<number>\d+(-\d+)?).+?(?=\n[ \t]*?\n))',
                                                   self._search_flags)

        self._article_with_comment_build_info = ElementBuild(u'(?P<name>^ *Статья (?P<number>\d+(-\d+)?) *?\s*.*?)$',
                                                             self._search_flags, 'article')
        self._article_build_info = ElementBuild(u'(?P<name>^ *Статья (?P<number>\d+(-\d+)?) *?\s*.*?)(?=\(|$)',
                                                self._search_flags, 'article')
        self._article_text_build_info = ElementBuild(u'.+', self._search_flags)

        self._last_item_build_info = ElementBuild(u'^(?P<number>\d+)\.(?P<text>.+)', self._search_flags)
        self._not_last_item_build_info = ElementBuild(u'^(?P<number>\d+)\.(?P<text>.+?)(?=^\d+\.)', self._search_flags)

        self._sections_start = self._find_start_of_sections()
        self._sections_end = len(self._text)
        self.errors = []

    def escape_braces(self, highest_section_text):
        return highest_section_text.replace("(", "\(").replace(")", "\)")

    def _find_start_of_sections(self):
        highest_section_text = self._get_first_highest_section_text()
        if highest_section_text is None:
            return 0
        last_match_of_first_highest_section = None
        if highest_section_text:

            template = re.compile(self.escape_braces(highest_section_text), self._search_flags)
            iterator = self._get_iterator(template, 0, len(self._text))
            for match in iterator:
                last_match_of_first_highest_section = match
        return last_match_of_first_highest_section.start() if last_match_of_first_highest_section else len(self._text)

    def _get_first_highest_section_text(self):
        section_text_and_start_positions = {}
        part_match = self._part_build_info.template.search(self._text)
        # print part_match
        if part_match:
            section_text_and_start_positions[part_match.start()] = part_match.group()
        division_match = self._division_build_info.template.search(self._text)
        if division_match:
            section_text_and_start_positions[division_match.start()] = division_match.group()
        chapter_match = self._chapter_with_comment_build_info.template.search(self._text)
        if chapter_match:
            section_text_and_start_positions[chapter_match.start()] = chapter_match.group()
        article_match = self._article_build_info.template.search(self._text)
        if article_match:
            section_text_and_start_positions[article_match.start()] = article_match.group()
        keys = section_text_and_start_positions.keys()
        keys.sort()
        return section_text_and_start_positions[keys[0]] if keys else None

    def _find_match_text_or_raise_error_with_msg(self, match, error_msg):
        if match:
            result = match.strip()
        else:
            self.errors.append(ParserError(error_msg))
            return ''
        return result

    def build_name(self):
        template = self._place_and_date_build_info.template.search(self._text)
        if template:
            place_and_date = template.group()
        else: place_and_date = ''

        template = self._revisions_build_info.template.search(self._text)
        if template:
            revision = template.group()
            revision = revision.replace('(','\(')
            revision = revision.replace(')','\)')
        else: revision = ''

        name_build_info = ElementBuild(u'(^[ а-яА-Я]+? РЕСПУБЛИКИ.*?)(?='+revision+u')', self._search_flags)
        name = name_build_info.template.search(self._text)
        if name:
            name = name.group()
            name = name.replace(place_and_date, '')
        else: name = ''

        comment  = self._comment_build_info.template.search(name)
        if comment:
            comment = comment.group()
            name = name.replace(comment, '')

        return self._find_match_text_or_raise_error_with_msg(name,
                                                             u'Не найдено наименование закона')

    def build_revisions(self):
        revision = ''
        template = self._revisions_build_info.template.search(self._text)
        if template:
            revision = template.group()
        return self._find_match_text_or_raise_error_with_msg(revision,
                                                             u'Не найдены ревизии закона')

    def build_place_and_date(self):
        place_and_data = ''
        template = self._place_and_date_build_info.template.search(self._text)
        if template:
            place_and_data = template.group()
        return self._find_match_text_or_raise_error_with_msg(place_and_data,
                                                             u'Не найдены место и дата принятия')

    def _get_iterator(self, template, start, end):
        return template.finditer(self._text[start:end])

    def build_sections(self):
        sections = self.build_parts(self._sections_start, self._sections_end)
        if sections == []:
            sections = self.build_divisions(self._sections_start, self._sections_end)
            if sections == []:
                sections = self.build_chapters(self._sections_start, self._sections_end)
                if sections == []:
                    sections = self.build_articles(self._sections_start, self._sections_end)
        return sections

    def _build_sections(self, level, template, build_childer_methods, section_start, section_end, create_section_method,
                        add_sub_element_method):
        parts = self._build_empty_sections_and_save_its_start_and_end_of_content_positions(
            level, template, section_start, section_end, create_section_method
        )
        self._add_content_to_built_sections(parts, build_childer_methods, add_sub_element_method)
        return parts

    def build_parts(self, section_start, section_end):
        build_childer_methods = [self.build_divisions, self.build_chapters, self.build_articles]
        parts = self._build_sections(self._part_build_info.level, self._part_build_info.template, build_childer_methods,
                                     section_start, section_end, self.create_Section, self._add_sub_sections)
        return parts

    def build_divisions(self, section_start, section_end, parent_level_and_number=None):
        sections = self.build_smaller_sections_in_this_level(section_start, section_end,
                                                             self._division_build_info.template)
        build_childer_methods = [self.build_sub_divisions, self.build_chapters, self.build_articles]
        divisions = self._build_sections(self._division_build_info.level, self._division_build_info.template,
                                         build_childer_methods,
                                         section_start, section_end, self.create_Section, self._add_sub_sections)
        for i in divisions:
            sections.append(i)
        return sections

    def build_sub_divisions(self, section_start, section_end, parent_level_and_number=None):
        level = parent_level_and_number + '_''sub_division'
        build_childer_methods = [self.build_chapters, self.build_articles]
        divisions = self._build_sections(level, self._sub_division_build_info.template, build_childer_methods,
                                         section_start, section_end, self.create_Section, self._add_sub_sections)
        return divisions

    def build_chapters(self, section_start, section_end, parent_level_and_number=None):
        sections = self.build_smaller_sections_in_this_level(section_start, section_end,
                                                             self._chapter_with_comment_build_info.template)
        build_childer_methods = [self.build_paragraphs, self.build_articles]
        chapters = self._build_sections(self._chapter_with_comment_build_info.level,
                                        self._chapter_with_comment_build_info.template,
                                        build_childer_methods,
                                        section_start, section_end, self.create_Section, self._add_sub_sections)
        for i in chapters:
            sections.append(i)
        return sections

    def build_smaller_sections_in_this_level(self, section_start, section_end, template):
        match = template.search(self._text[section_start:section_end])
        sections = []
        if match:
            buffer_for_start = self._sections_start
            self._sections_start = section_start
            buffer_for_end = self._sections_end
            self._sections_end = match.start() + section_start
            sections = self.build_sections()
            self._sections_start = buffer_for_start
            self._sections_end = buffer_for_end
        return sections

    def build_paragraphs(self, section_start, section_end, parent_level_and_number=None):
        level = parent_level_and_number + '_''paragraph'
        build_childer_methods = [self.build_articles]
        paragraphs = self._build_sections(level, self._paragraphs_build_info.template, build_childer_methods,
                                          section_start, section_end, self.create_Section, self._add_sub_sections)
        return paragraphs

    def build_articles(self, section_start, section_end, parent_level_and_number=None):
        build_childer_methods = [self._build_items, self._build_article_text]
        articles = self._build_sections(self._article_with_comment_build_info.level,
                                        self._article_with_comment_build_info.template,
                                        build_childer_methods,
                                        section_start, section_end, self.create_TextSection,
                                        self._add_text_or_sub_sections)
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
            item = TextSection(parent_level_and_number + '_item', name='', number=m.group('number'))
            item.text = m.group('text').strip()
            items.append(item)
        return items

    def _build_article_text(self, start, end, parent_level_and_number=None):
        match = self._article_text_build_info.template.search(self._text[start:end])
        result = match.group().strip()
        return result

    def _build_empty_sections_and_save_its_start_and_end_of_content_positions(self, level, template, section_start,
                                                                              section_end, create_section):
        match_iterator = self._get_iterator(template, section_start, section_end)
        sections = []
        self._start_of_sections_content = []
        self._end_of_sections_content = []
        to_find_end_of_sections_content_list = []
        for m in match_iterator:
            sections.append(create_section(level, m))
            to_find_end_of_sections_content_list.append(m.start() + section_start)
            self._start_of_sections_content.append(m.start() + section_start + len(m.group()))
        if not to_find_end_of_sections_content_list == []:
            to_find_end_of_sections_content_list.remove(to_find_end_of_sections_content_list[0])
        for i in to_find_end_of_sections_content_list:
            self._end_of_sections_content.append(i)
        self._end_of_sections_content.append(section_end)
        return sections

    def _add_content_to_built_sections(self, sections, build_children_methods, add_sub_sections_method):
        i = 0
        start_of_sections_content = copy.copy(self._start_of_sections_content)
        end_of_sections_content = copy.copy(self._end_of_sections_content)
        for section in sections:
            parent_level_and_number = section.level + (section.number)
            j = 0
            sub_sections = []
            while sub_sections == [] and j < len(build_children_methods):
                sub_sections = build_children_methods[j](start_of_sections_content[i], end_of_sections_content[i],
                                                         parent_level_and_number)
                j += 1
            if sub_sections:
                add_sub_sections_method(section, sub_sections)
            i += 1

    def create_Section(self, level, match):
        text = match.group()
        result = self._chapter_build_info.template.search(text)
        if result:
            name = result.group()
        else:
            name = match.group()

        number = match.group('number')
        if number:
            number = number.encode('utf-8')
        if number is None:
            number = self._part_number
            self._part_number += 1
        comment = self.create_Comment(match)
        return Section(level, name=name.replace('\n', ' ').strip(), number=str(number), comment=comment)

    def create_TextSection(self, level, match):
        text = match.group()
        result = self._article_build_info.template.search(text)
        if result:
            name = result.group()
        else:
            name = match.group()
        comment = self.create_Comment(match)
        return TextSection(level=level, name=name.replace('\n', ' ').strip(),
                           number=match.group('number'), comment=comment)

    def create_Comment(self, match):
        section_name = match.group()
        result = self._comment_build_info.template.search(section_name)
        if result:
            comment = result.group()
            return Comment(content=comment)
        else:
            return None

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, a_text):
        self._sections_start = self._find_start_of_sections()
        self._text = a_text
        self._sections_end = len(self._text)

    def filter_invalid_strings(k, v):
        return (k, filter(lambda x: x != u'\x0b', v)
        if isinstance(v, basestring) else v)

        # def Tprint(self):
        #     template = self._place_and_date_build_info.template.search(self._text)
        #     place_and_date = template.group()
        #     print place_and_date+'\n'
        #     template = self._revisions_build_info.template.search(self._text)
        #     revision = template.group()
        #     revision = revision.replace('(', '\(')
        #     revision = revision.replace(')', '\)')
        #     print revision
        #     name_build = ElementBuild(u'(^[ а-яА-Я]+? РЕСПУБЛИКИ.*?)(?='+revision+u')', self._search_flags)
        #     name = name_build.template.search(self._text)
        #     name = name.group()
        #     name = name.replace(place_and_date,'')
        #     print name

# a=open('/home/bolushbekov/projects/zakon/django-project/document/selenium_tests/features/zakon.rtf')
# temp = a.read()
# parser=RTFParser()
# text_content = parser.parse(temp)
#
# b=Builder(text_content)
# b.Tprint()
