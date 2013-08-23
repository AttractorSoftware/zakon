#coding=utf-8
import re
from document.LawParser.Builder import Builder
from elements.document import Document
from elements.description import Description


class Parser(object):

    def parse(self, content_of_the_document, id):
        builder = Builder(content_of_the_document)
        description = self._build_description()
        sections = self._build_sections(builder)
        return Document(id, description, sections)

    def _build_description(self, builder):
        name_of_the_document = builder.build_document_name()
        revisions_of_the_document = builder.build_revisions()
        taking_place = builder.build_taking_place()
        return Description(name_of_the_document, revisions_of_the_document, taking_place)

    def _build_sections(self, builder):
        sections = builder.build_parts()
        if sections == None:
            sections = builder.build_parts()
            if sections == None:
                sections = builder.build_chapters()
                if sections == None:
                    sections = builder.build_articles()
        return sections