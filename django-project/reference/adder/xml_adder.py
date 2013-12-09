# coding=utf-8
from StringIO import StringIO
from lxml import etree

DOCUMENT_ID_ATTRIBUTE_NAME = "doc_id"
LINKED_ELEMENT_ATTRIBUTE_NAME = "element"


class XMLReferenceAdder(object):
    def __init__(self, reference_object):
        self.source_document = reference_object.source_document
        self.source_element = self.remove_sharp(reference_object.source_element)
        self.target_document = reference_object.target_document
        self.target_element = self.remove_sharp(reference_object.target_element)

    def go(self):
        self.update_source_document_content()
        if self.is_inner_reference():
            self.target_document.content = self.source_document.content
        self.update_target_document_content()

    def update_source_document_content(self):
        root = self.get_document_root(self.source_document.content)
        selected_element = self.get_selected_element(root, self.source_element)
        self.add_reference(selected_element)
        self.source_document.content = etree.tostring(root, pretty_print=True)
        self.source_document.save()

    def update_target_document_content(self):
        root = self.get_document_root(self.target_document.content)
        selected_element = self.get_selected_element(root, self.target_element)
        self.add_link(selected_element)
        self.target_document.content = etree.tostring(root, pretty_print=True)
        self.target_document.save()

    def add_reference(self, selected_element):
        parent_element = self.find_or_create_subelement_in_element("references", selected_element)
        self.add_sub_node(self.target_document, self.target_element, parent_element)

    def add_link(self, selected_element):
        parent_element = self.find_or_create_subelement_in_element("links", selected_element)
        self.add_sub_node(self.source_document, self.source_element, parent_element)

    def find_or_create_subelement_in_element(self, element_name, selected_element):
        XPATH_EXPRESSION = "//" + element_name
        if selected_element.find(element_name) is None:
            parent_node = etree.SubElement(selected_element, element_name)
        else:
            parent_node = selected_element.xpath(XPATH_EXPRESSION)[0]
        return parent_node

    def add_sub_node(self, document, element, parent_node):
        if parent_node.tag == "references":
            childnode_name = "reference"
        else:
            childnode_name = "link"

        child_element = etree.SubElement(parent_node, childnode_name)
        child_element.set(DOCUMENT_ID_ATTRIBUTE_NAME, document.id.__str__())
        child_element.set(LINKED_ELEMENT_ATTRIBUTE_NAME, element.__str__())

    def get_document_root(self, document_content):
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        tree = etree.parse(StringIO(document_content), parser)
        root = tree.getroot()
        return root

    def get_selected_element(self, root, element):
        return root.xpath("//article[@id='" + element + "']")[0]

    def remove_sharp(self, element):
        return element.replace("#", "")

    def is_inner_reference(self):
        return self.source_document == self.target_document