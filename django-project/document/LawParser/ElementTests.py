from unittest import TestCase
from elements.document import *
from elements.description import *
from elements.section import *
from elements.text_section import TextSection


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
        chapter.sections.append(TextSection("article", "1", "name"))
        part.sections.append(chapter)
        part.sections.append(Section("chapter", "name", "2"))
        xml = '<section id="part:1" level="part" name="name" number="1">' \
              '<section id="chapter:1" level="chapter" name="name" number="1">' \
              '<article id="article:1" name="name"/>' \
              '</section>' \
              '<section id="chapter:2" level="chapter" name="name" number="2"/>' \
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
        xml = '<section id="part:1" level="part" name="name" number="1">' \
              '<section id="chapter:1" level="chapter" name="name" number="1">' \
              '<article id="article:1" name="name">' \
              'Hello world!'\
              '</article>' \
              '</section>' \
              '<section id="chapter:2" level="chapter" name="name" number="2"/>' \
              '</section>'
        self.assertEqual(xml, part.to_xml())

    def test_section_with_item(self):
        part = Section("part", "name", "1")
        chapter = Section("chapter", "name", "1")
        article = TextSection("article", "1", "name")
        item = TextSection("item", "1")
        article.subsections.append(item)
        chapter.sections.append(article)
        # part.sections.append(Item("item", "name", "1"))
        part.sections.append(chapter)
        part.sections.append(Section("chapter", "name", "2"))
        xml = '<section id="part:1" level="part" name="name" number="1">' \
              '<section id="chapter:1" level="chapter" name="name" number="1">' \
              '<article id="article:1" name="name">' \
              '<item id="item:1"/>' \
              '</article>' \
              '</section>' \
              '<section id="chapter:2" level="chapter" name="name" number="2"/>' \
              '</section>'
        self.assertEqual(xml, part.to_xml())

    def test_section_with_item_with_text(self):
        part = Section("part", "name", "1")
        chapter = Section("chapter", "name", "1")
        article = TextSection("article", "1", "name")
        item = TextSection("item", "1")
        item.text = "djkshkaskjdsaj"
        article.subsections.append(item)
        chapter.sections.append(article)
        part.sections.append(chapter)
        part.sections.append(Section("chapter", "name", "2"))
        item_text = TextSection
        item_text.text = "test test test"
        xml = '<section id="part:1" level="part" name="name" number="1">' \
              '<section id="chapter:1" level="chapter" name="name" number="1">' \
              '<article id="article:1" name="name">' \
              '<item id="item:1">djkshkaskjdsaj</item>' \
              '</article>' \
              '</section>' \
              '<section id="chapter:2" level="chapter" name="name" number="2"/>' \
              '</section>'
        self.assertEqual(xml, part.to_xml())


    def test_section_with_two_articles_with_items_with_text(self):
        part = Section("part", "name", "1")
        chapter = Section("chapter", "name", "1")
        article = TextSection("article", "1", "name")
        item = TextSection("item", "1")
        item.text = "djkshkaskjdsaj"
        article.subsections.append(item)
        chapter.sections.append(article)
        article = TextSection("article", "2", "name1")
        item = TextSection("item", "1")
        item.text = "I am first item of second article!!!"
        article.subsections.append(item)
        chapter.sections.append(article)
        part.sections.append(chapter)
        part.sections.append(Section("chapter", "name", "2"))
        item_text = TextSection
        item_text.text = "test test test"
        xml = '<section id="part:1" level="part" name="name" number="1">' \
              '<section id="chapter:1" level="chapter" name="name" number="1">' \
              '<article id="article:1" name="name">' \
              '<item id="item:1">djkshkaskjdsaj</item>' \
              '</article>' \
              '<article id="article:2" name="name1">' \
              '<item id="item:1">I am first item of second article!!!</item>' \
              '</article>' \
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
