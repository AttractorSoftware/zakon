#coding=utf-8
from Builder import Builder
from elements.document import Document
from elements.description import Description


class Parser(object):

    def parse(self, content_of_the_document):
        builder = Builder(content_of_the_document)
        description = self._build_description(builder)
        sections = builder.build_sections()
        return Document(description, sections)

    def _build_description(self, builder):
        name_of_the_document = builder.build_name()
        revisions_of_the_document = builder.build_revisions()
        taking_place = builder.build_place_and_date()
        return Description(name_of_the_document, taking_place, revisions_of_the_document)
