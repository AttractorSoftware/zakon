# coding=utf-8
from StringIO import StringIO
from lxml import etree


def update_xml_of_reference_document(reference_content, reference_element, linked_doc_id, linked_element):
    """
     Контент документа,
     Элемент документа с которого ссылаемся,
     ID документа на кототорый ссылаемся,
     Элемент на который ссылаемся
     """

    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    tree = etree.parse(StringIO(reference_content), parser)
    root = tree.getroot()
    selected_reference_element = root.xpath("//article[@id='" + remove_sharp(reference_element) + "']")[0]

    if selected_reference_element.find("references") is None:
        references_tag = etree.SubElement(selected_reference_element, "references")
        add_sub_refs(linked_doc_id, remove_sharp(linked_element), references_tag)
    else:
        references_tag = selected_reference_element.xpath("//references")[0]
        add_sub_refs(linked_doc_id, remove_sharp(linked_element), references_tag)
    return etree.tostring(root, pretty_print=True)


def update_xml_of_linked_document(linked_content, linked_element, reference_doc_id, reference_element):
    """
     Контент документа,
     Элемент документа на который ссылаемся,
     ID документа с кототорого ссылаемся,
     Элемент с которого ссылаемся
     """

    try:
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        tree = etree.parse(StringIO(linked_content), parser)
        root = tree.getroot()
    except Exception as ex:
        return ex

    try:
        selected_reference_element = root.xpath("//article[@id='" + remove_sharp(linked_element) + "']")[0]
    except Exception as e:
        return e

    if selected_reference_element.find("links") is None:
        links_tag = etree.SubElement(selected_reference_element, "links")
        add_sub_links(reference_doc_id, remove_sharp(reference_element), links_tag)
    else:
        links_tag = selected_reference_element.xpath("//links")[0]
        add_sub_links(reference_doc_id, remove_sharp(reference_element), links_tag)
    return etree.tostring(root, pretty_print=True)


def remove_sharp(element):
    return element.replace("#", "")


def add_sub_refs(linked_doc_id, linked_element, references_tag):
    reference_tag = etree.SubElement(references_tag, "reference")
    reference_tag.set("linked_doc_id", "" + linked_doc_id.__str__() + "")
    reference_tag.set("linked_element", "" + linked_element.__str__() + "")


def add_sub_links(reference_doc_id, reference_element, links_tag):
    link_tag = etree.SubElement(links_tag, "link")
    link_tag.set("reference_doc_id", "" + reference_doc_id.__str__() + "")
    link_tag.set("reference_element", "" + reference_element.__str__() + "")