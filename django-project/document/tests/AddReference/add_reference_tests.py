import unittest
from document.add_reference import AddReference


class AddReferenceTests(unittest.TestCase):
    def test_add_one_reference(self):
        before = '<document><article id="article_12" >I want to close this ticket</article></document>'
        after = '<document><article id="article_12">I want to close this <reference>ticket</reference></article></document>'

        add_reference = AddReference()
        result = add_reference.add_node_reference(before, 'article_12', 21, 27, 0)

        self.assertEqual(after, result)

    def test_add_reference_to_one_reference(self):
        before = '<document><article id="article_12">I want <reference>to</reference> close this ticket</article></document>'
        after = '<document><article id="article_12">I want <reference>to</reference> close this <reference>ticket</reference></article></document>'

        add_reference = AddReference()
        result = add_reference.add_node_reference(before, 'article_12', 21, 27, 0)

        self.assertEqual(after, result)

    def test_add_reference_to_two_references(self):

        before = '<document><article id="article_12">I want <reference>to</reference> <reference>close</reference> this ticket</article></document>'
        after = '<document><article id="article_12">I want <reference>to</reference> <reference>close</reference> this <reference>ticket</reference></article></document>'

        add_reference = AddReference()
        result = add_reference.add_node_reference(before, 'article_12', 21, 27, 0)

        self.assertEqual(after, result)

    def test_add_reference_to_two_references_some_text(self):

        before = '<document><article id="article_12">I want <reference>to</reference> <reference>close</reference> this ticket</article></document>'
        after = '<document><article id="article_12">I want <reference>to</reference> <reference>close</reference> this <reference>tic</reference>ket</article></document>'

        add_reference = AddReference()
        result = add_reference.add_node_reference(before, 'article_12', 21, 24, 0)

        self.assertEqual(after, result)

    def test_add_reference_to_reference(self):

        before = '<document><article id="article_12">I want to close this <reference>ticket</reference></article></document>'
        after = '<document><article id="article_12">I want to close this <reference>ticket</reference></article></document>'

        add_reference = AddReference()
        result = add_reference.add_node_reference(before, 'article_12', 21, 27, 0)

        self.assertEqual(after, result)