#coding=utf-8
import re
from StructureElement import StructureElement

DEPTH_LEVEL_5 = 5
DEPTH_LEVEL_4 = 4
DEPTH_LEVEL_3 = 3
DEPTH_LEVEL_2 = 2
DEPTH_LEVEL_1 = 1


class Parser(object):

    def __init__(self, law_text):
        self._law_text = law_text
        self._content = ''
        self._structure_elements = [StructureElement(
                                'part', DEPTH_LEVEL_1, '(?P<content>^.*? *ЧАСТЬ *\d*$(?=(\s+?^ *?РАЗДЕЛ (?P<end_id>[IVXLCDM]+).*?$)))')
                              ,StructureElement(
                                'section', DEPTH_LEVEL_2, '(?P<content>^ *?РАЗДЕЛ (?P<end_id>[IVXLCDM]+) *?\s*.*?$)')
                              ,StructureElement(
                                'subsection', DEPTH_LEVEL_3, '(?P<content>^ *?Подраздел (?P<end_id>\d+) *?\s*.*?$)')
                              ,StructureElement(
                                'chapter', DEPTH_LEVEL_4, '(?P<content>^ *?Глава (?P<end_id>\d+) *?\s*.*?$)')
                              ,StructureElement(
                                'article', DEPTH_LEVEL_5, '(?P<content>^ *Статья (?P<end_id>\d+)\..+?$)')
        ]
        self._past_tags = "<article id='{0}_\g<end_id>'> <h{1}>\g<content></h{1}> </article>"
        self._parsed = False

    def get_parsed_text(self):
        if self._is_not_parsed():
            self._make_html_for_law()
            self._make_html_content()
            self._parsed = True
        return self._gather_piecemeal()


    def _make_html_for_law(self):
        for element in self._structure_elements:
            self._law_text = element.get_compiled_regex().sub(self._past_tags.format(element.get_name(),
                                                                        element.get_depth()), self._law_text)
        self._law_text = re.sub('\n', r'<br/>', self._law_text)

    def _make_html_content(self):
        pattern = re.compile("<article id='(?P<id>.+?)'> <h(?P<depth>[1-6])>(?P<text>.+?)</h[1-6]> </article>",
                                 re.MULTILINE | re.U | re.I)
        result = pattern.finditer(self._law_text)
        for match in result:
            class_name = re.findall('[a-z]+', match.groups()[0])
            self._content += "<a href=\"#{0}\" class='{2}'>{1}</a><br/>".format(
                match.groups()[0], match.groups()[2], class_name[0])

    def _gather_piecemeal(self):
        return self._content+self._law_text

    def _is_not_parsed(self):
        return self._parsed == False