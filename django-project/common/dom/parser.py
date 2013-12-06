#coding=utf-8
from common.dom.builder import Builder
from common.dom.elements.document import Document
from common.dom.elements.header import Header


class Parser(object):
    def parse(self, content_of_the_document):
        self.builder = Builder(content_of_the_document)
        description = self._build_header(self.builder)
        sections = self.builder.build_sections()
        return Document(description, sections)

    def _build_header(self, builder):
        name_of_the_document = builder.build_name()
        revisions_of_the_document = builder.build_revisions()
        taking_place = builder.build_place_and_date()
        description = builder.build_description()
        return Header(name_of_the_document, taking_place, revisions_of_the_document, description)

    def has_errors(self):
        return len(self.builder.errors) > 0

    def get_errors(self):
        return self.builder.errors