from unittest import TestCase
from django.http import HttpRequest
from mock import Mock
from References.views import TARGET_ELEMENT, SOURCE_ELEMENT, SOURCE_DOCUMENT_ID, TARGET_DOCUMENT_ID, ReferenceAdder
from document.models import Document

class TestReferenceAdder(TestCase):
    def test_add_reference(self):
        request = HttpRequest()
        request.POST = {SOURCE_DOCUMENT_ID: 1, SOURCE_ELEMENT: 'article_1', TARGET_DOCUMENT_ID: 2, TARGET_ELEMENT: 'article_2'}

        adder = ReferenceAdder(request)
        adder.manager.get = Mock()
        source = Document()
        source.id = 1
        source.content = '<document>' \
              '<header><name>name</name><place>place</place></header>' \
              '<section id="chapter_1" level="chapter" name="name" number="1">' \
              '<article id="article_1" level="article" name="name" number="1">test</article>' \
              '<article id="article_2" level="article" name="name" number="2">test</article>' \
              '</section>' \
              '</document>'

        target = Document()
        target.id = 2
        target.content = '<document>' \
              '<header><name>name</name><place>place</place></header>' \
              '<section id="chapter_1" level="chapter" name="name" number="1">' \
              '<article id="article_1" level="article" name="name" number="1">test</article>' \
              '<article id="article_2" level="article" name="name" number="2">test</article>' \
              '</section>' \
              '</document>'
        adder.manager.get.return_value = source
        adder.add_reference()
        adder.save_reference = Mock()
        adder.add_reference()

        expected_doc = source
        expected_doc.content = '<document>' \
              '<header><name>name</name><place>place</place></header>' \
              '<section id="chapter_1" level="chapter" name="name" number="1">' \
              '<article id="article_1" level="article" name="name" number="1">test' \
              '<references>' \
              '<reference doc_id="" element="article_2">' \
              '</references>' \
              '</article>' \
              '<article id="article_2" level="article" name="name" number="2">test</article>' \
              '</section>' \
              '</document>'

        self.assertEqual(expected_doc.content, adder.source_document.content)
