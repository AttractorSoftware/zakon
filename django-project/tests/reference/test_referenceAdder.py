from datetime import datetime
from django.test import TestCase
from django.test.client import RequestFactory
from document.models import Document
from reference.adder import SOURCE_DOCUMENT_ID, SOURCE_ELEMENT, TARGET_DOCUMENT_ID, TARGET_ELEMENT, ReferenceAdder


class TestReferenceAdder(TestCase):
    def setUp(self):
        self.source = self.create_source_document()
        self.target = self.create_target_document()

    def test_add_reference(self):
        factory = RequestFactory()
        request = factory.post("/wrap_text",
                               data={SOURCE_DOCUMENT_ID: 1, SOURCE_ELEMENT: 'article_1', TARGET_DOCUMENT_ID: 2,
                                     TARGET_ELEMENT: 'article_2'})
        adder = ReferenceAdder(request)
        adder.add_reference()

        expected_doc = self.source
        expected_doc.content = """<document>
  <header>
    <name>name</name>
    <place>place</place>
  </header>
  <section id="chapter_1" level="chapter" name="name" number="1">
    <article id="article_1" level="article" name="name" number="1">test<references><reference doc_id="2" element="article_2"/></references></article>
    <article id="article_2" level="article" name="name" number="2">test</article>
  </section>
</document>
"""

        self.assertEqual(expected_doc.content, adder.source_document.content)


    def create_source_document(self):
        source = Document()
        source.id = 1
        source.content = '<document>' \
                         '<header><name>name</name><place>place</place></header>' \
                         '<section id="chapter_1" level="chapter" name="name" number="1">' \
                         '<article id="article_1" level="article" name="name" number="1">test</article>' \
                         '<article id="article_2" level="article" name="name" number="2">test</article>' \
                         '</section>' \
                         '</document>'

        source.uploaded_date = datetime.now()
        source.save()
        return source


    def create_target_document(self):
        target = Document()
        target.id = 2
        target.content = '<document>' \
                         '<header><name>name</name><place>place</place></header>' \
                         '<section id="chapter_1" level="chapter" name="name" number="1">' \
                         '<article id="article_1" level="article" name="name" number="1">test</article>' \
                         '<article id="article_2" level="article" name="name" number="2">test</article>' \
                         '</section>' \
                         '</document>'
        target.uploaded_date = datetime.now()
        target.save()
        return target
