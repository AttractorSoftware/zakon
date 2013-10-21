from unittest import TestCase
from document.LawParser.elements.description import Description
from document.LawParser.elements.document import *
from document.LawParser.elements.section import Section
from document.LawParser.elements.text_section import TextSection


class ElementTests(TestCase):
    def test_document_to_xml(self):
        document = Document()
        self.assertEqual('<document/>', document.to_xml())

    def test_description_to_xml(self):
        description = Description("name", "place")
        self.assertEqual('<description><name>name</name><place>place</place></description>', description.to_xml())

    def test_description_with_revisions_to_xml(self):
        description = Description("name", "place", "(from 1995 year);(from 1997 year)")
        xml = '<description>' \
              '<name>name</name>' \
              '<place>place</place>' \
              '<revisions>(from 1995 year);(from 1997 year)</revisions>' \
              '</description>'
        self.assertEqual(xml, description.to_xml())

    def test_document_with_description(self):
        description = Description("name", "place")
        document = Document(description)
        xml = '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<document>' \
              '<description><name>name</name><place>place</place></description>' \
              '</document>'
        self.assertEqual(xml, document.to_xml())

    def test_empty_section(self):
        section = Section("part", "name", "1")
        xml = '<section id="part_1" level="part" name="name" number="1"/>'
        self.assertEqual(xml, section.to_xml())

    def test_section_with_subsections(self):
        part = Section("part", "name", "1")
        part.sections.append(Section("chapter", "name", "1"))
        part.sections.append(Section("chapter", "name", "2"))
        xml = '<section id="part_1" level="part" name="name" number="1">' \
              '<section id="chapter_1" level="chapter" name="name" number="1"/>' \
              '<section id="chapter_2" level="chapter" name="name" number="2"/>' \
              '</section>'
        self.assertEqual(xml, part.to_xml())

    def test_section_with_article(self):
        part = Section("part", "name", "1")
        chapter = Section("chapter", "name", "1")
        chapter.sections.append(TextSection("article", "1", "name"))
        part.sections.append(chapter)
        part.sections.append(Section("chapter", "name", "2"))
        xml = '<section id="part_1" level="part" name="name" number="1">' \
              '<section id="chapter_1" level="chapter" name="name" number="1">' \
              '<article id="article_1" level="article" name="name" number="1"/>' \
              '</section>' \
              '<section id="chapter_2" level="chapter" name="name" number="2"/>' \
              '</section>'
        self.assertEqual(xml, part.to_xml())

    def test_section_with_article_with_text(self):
        part = Section("part", "name", "1")
        chapter = Section("chapter", "name", "1")
        article_with_text = TextSection("article", "1", "name")
        article_with_text.text = "Hello world!"
        chapter.sections.append(article_with_text)
        part.sections.append(chapter)
        part.sections.append(Section("chapter", "name", "2"))
        xml = '<section id="part_1" level="part" name="name" number="1">' \
              '<section id="chapter_1" level="chapter" name="name" number="1">' \
              '<article id="article_1" level="article" name="name" number="1">' \
              'Hello world!' \
              '</article>' \
              '</section>' \
              '<section id="chapter_2" level="chapter" name="name" number="2"/>' \
              '</section>'
        self.assertEqual(xml, part.to_xml())

    def test_section_with_item(self):
        part = Section("part", "name", "1")
        chapter = Section("chapter", "name", "1")
        article = TextSection("article", "1", "name")
        item = TextSection("item", "1")
        article.sections.append(item)
        chapter.sections.append(article)
        # part.sections.append(Item("item", "name", "1"))
        part.sections.append(chapter)
        part.sections.append(Section("chapter", "name", "2"))
        xml = '<section id="part_1" level="part" name="name" number="1">' \
              '<section id="chapter_1" level="chapter" name="name" number="1">' \
              '<article id="article_1" level="article" name="name" number="1">' \
              '<item id="item_1" level="item" number="1"/>' \
              '</article>' \
              '</section>' \
              '<section id="chapter_2" level="chapter" name="name" number="2"/>' \
              '</section>'
        self.assertEqual(xml, part.to_xml())

    def test_section_with_item_with_text(self):
        part = Section("part", "name", "1")
        chapter = Section("chapter", "name", "1")
        article = TextSection("article", "1", "name")
        item = TextSection("item", "1")
        item.text = "djkshkaskjdsaj"
        article.sections.append(item)
        chapter.sections.append(article)
        part.sections.append(chapter)
        part.sections.append(Section("chapter", "name", "2"))
        item_text = TextSection
        item_text.text = "test test test"
        xml = '<section id="part_1" level="part" name="name" number="1">' \
              '<section id="chapter_1" level="chapter" name="name" number="1">' \
              '<article id="article_1" level="article" name="name" number="1">' \
              '<item id="item_1" level="item" number="1">djkshkaskjdsaj</item>' \
              '</article></section><section id="chapter_2" level="chapter" name="name" number="2"/>' \
              '</section>'
        self.assertEqual(xml, part.to_xml())


    def test_document_with_sections(self):
        description = Description("name", "place")
        document = Document(description)
        section = Section("part", "name", "1")
        document.add_section(section)
        xml = '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<document>' \
              '<description><name>name</name><place>place</place></description>' \
              '<section id="part_1" level="part" name="name" number="1"/>' \
              '</document>'
        self.assertEqual(xml, document.to_xml())

    def test_article_with_item(self):
        article = TextSection("article", "1", "Article")
        item = TextSection("item", "1")
        item.text = "dslkdsaldsads"

        article.sections.append(item)
        xml = '<article id="article_1" level="article" ' \
              'name="Article" number="1"><item id="item_1" level="item"' \
              ' number="1">dslkdsaldsads</item></article>'
        self.assertEqual(xml, article.to_xml())