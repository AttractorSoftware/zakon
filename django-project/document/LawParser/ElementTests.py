from unittest import TestCase
from elements.document import *
from elements.description import *
from elements.item import Item


class ElementTests(TestCase):
    def testDocumenttoXml(self):
        document = Document(1)
        self.assertEqual('<document id="1"/>', document.to_xml())

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
        document = Document(1, description)
        xml = '<document id="1"><description><name>name</name><place>place</place></description></document>'
        self.assertEqual(xml, document.to_xml())

    def test_empty_section(self):
        section = Section("part", "name", "1")
        xml = '<section id="part:1" level="part" name="name" number="1"/>'
        self.assertEqual(xml, section.to_xml())

    def test_section_with_subsections(self):
        part = Section("part", "name", "1")
        part.sections.append(Section("chapter", "name", "1"))
        part.sections.append(Section("chapter", "name", "2"))
        xml = '<section id="part:1" level="part" name="name" number="1">' \
              '<section id="chapter:1" level="chapter" name="name" number="1"/>' \
              '<section id="chapter:2" level="chapter" name="name" number="2"/>' \
              '</section>'
        self.assertEqual(xml, part.to_xml())

    def test_section_with_article(self):
        part = Section("part", "name", "1")
        chapter = Section("chapter", "name", "1")
        chapter.sections.append(Section("article", "name", "1"))
        part.sections.append(chapter)
        part.sections.append(Section("chapter", "name", "2"))
        xml = '<section id="part:1" level="part" name="name" number="1">' \
              '<section id="chapter:1" level="chapter" name="name" number="1">' \
              '<section id="article:1" level="article" name="name" number="1"/>' \
              '</section>' \
              '<section id="chapter:2" level="chapter" name="name" number="2"/>' \
              '</section>'
        self.assertEqual(xml, part.to_xml())

    def test_section_with_item(self):
        part = Section("part", "name", "1")
        chapter = Section("chapter", "name", "1")
        article = Section("article", "name", "1")
        article.sections.append(Item("1"))
        chapter.sections.append(article)
        # part.sections.append(Item("item", "name", "1"))
        part.sections.append(chapter)
        part.sections.append(Section("chapter", "name", "2"))
        xml = '<section id="part:1" level="part" name="name" number="1">' \
              '<section id="chapter:1" level="chapter" name="name" number="1">' \
              '<section id="article:1" level="article" name="name" number="1">' \
              '<item number="1"/>' \
              '</section>' \
              '</section>' \
              '<section id="chapter:2" level="chapter" name="name" number="2"/>' \
              '</section>'
        self.assertEqual(xml, part.to_xml())

    def test_section_with_item_with_text(self):
        part = Section("part", "name", "1")
        chapter = Section("chapter", "name", "1")
        article = Section("article", "name", "1")
        item = Item("1")
        item.text = "djkshkaskjdsaj"
        article.sections.append(item)
        chapter.sections.append(article)
        # part.sections.append(Item("item", "name", "1"))
        part.sections.append(chapter)
        part.sections.append(Section("chapter", "name", "2"))
        item_text = Item
        item_text.text = "test test test"
        xml = '<section id="part:1" level="part" name="name" number="1">' \
              '<section id="chapter:1" level="chapter" name="name" number="1">' \
              '<section id="article:1" level="article" name="name" number="1">' \
              '<item number="1">djkshkaskjdsaj</item>' \
              '</section>' \
              '</section>' \
              '<section id="chapter:2" level="chapter" name="name" number="2"/>' \
              '</section>'
        self.assertEqual(xml, part.to_xml())


    def test_document_with_sections(self):
        description = Description("name", "place")
        document = Document(1, description)
        section = Section("part", "name", "1")
        document.sections.append(section)
        xml = '<document id="1"><description><name>name</name><place>place</place></description></document>'
        self.assertEqual(xml, document.to_xml())
